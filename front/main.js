document.addEventListener('DOMContentLoaded', () => {
    
    let allData = [];
    let sortState = { column: 'record_count', direction: 'desc' }; 
    let isGrouped = false;

    const tableContainer = document.getElementById('table-container');
    const groupByChampionBtn = document.getElementById('group-by-champion-btn');
    const resetViewBtn = document.getElementById('reset-view-btn');
    const choicesLeague = new Choices('#league-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione ligas...' });
    const choicesPatch = new Choices('#patch-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione patches...' });
    const choicesSplit = new Choices('#split-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione splits...' });
    const choicesChampion = new Choices('#champion-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione campeões...' });

    async function main() {
        tableContainer.innerHTML = '<p>Carregando dados...</p>';
        try {

            const response = await fetch('front/data/champions.json'); 
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            allData = await response.json();
            
            populateAllFiltersOnce();
            setupEventListeners();
            renderTable();
        } catch (error) {
            console.error('Erro:', error);
            tableContainer.innerHTML = `<p style="color: red;">Falha ao carregar dados.</p>`;
        }
    }

    function populateAllFiltersOnce() {
        const unique = {
            leagues: [...new Set(allData.map(item => item.league))].sort(),
            patches: [...new Set(allData.map(item => String(item.patch)))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
            splits: [...new Set(allData.map(item => item.split))].sort(),
            champions: [...new Set(allData.map(item => item.champion))].sort()
        };
        choicesLeague.setChoices(unique.leagues.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesPatch.setChoices(unique.patches.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesSplit.setChoices(unique.splits.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesChampion.setChoices(unique.champions.map(val => ({ value: val, label: val })), 'value', 'label', true);
    }
    
    function setupEventListeners() {
        document.getElementById('league-filter').addEventListener('change', renderTable);
        document.getElementById('patch-filter').addEventListener('change', renderTable);
        document.getElementById('split-filter').addEventListener('change', renderTable);
        document.getElementById('champion-filter').addEventListener('change', renderTable);
        
        groupByChampionBtn.addEventListener('click', () => {
            isGrouped = true;
            sortState = { column: 'record_count', direction: 'desc' };
            renderTable();
        });

        resetViewBtn.addEventListener('click', () => {
            isGrouped = false;
            sortState = { column: 'banrate', direction: 'desc' };

            [choicesLeague, choicesPatch, choicesSplit, choicesChampion].forEach(c => c.clearStore());
            populateAllFiltersOnce();
            renderTable();
        });
    }

    function groupDataByChampion(data) {
        if (data.length === 0) {
            return [];
        }

        const seenCombinations = new Set();
        let trueTotalGames = 0;

        data.forEach(row => {
            const combinationKey = `${row.league}|${row.patch}|${row.split}`;
            if (!seenCombinations.has(combinationKey)) {
                trueTotalGames += row['total games'] || 0;
                seenCombinations.add(combinationKey);
            }
        });

        const grouped = {};
        const columnsToProcess = ['picked games', 'banned games', 'winrate'];

        data.forEach(row => {
            const champion = row.champion;
            if (!champion) return;

            if (!grouped[champion]) {
                grouped[champion] = { champion: champion, record_count: 0 };
                columnsToProcess.forEach(col => grouped[champion][col] = 0);
            }
            
            grouped[champion].record_count++;
            columnsToProcess.forEach(col => {
                if (row.hasOwnProperty(col) && typeof row[col] === 'number') {
                    grouped[champion][col] += row[col];
                }
            });
        });

        const finalResult = Object.values(grouped).map(group => {
            const denominator = trueTotalGames > 0 ? trueTotalGames : 1;
            const recordCount = group.record_count > 0 ? group.record_count : 1;

            return {
                'champion': group.champion,
                'record_count': group.record_count,
                'picked games': group['picked games'],
                'pickrate': (group['picked games'] / denominator), 
                'banned games': group['banned games'],
                'banrate': (group['banned games'] / denominator), 
                'winrate': (group['winrate'] / recordCount),
                'total games': trueTotalGames 
            };
        });

        return finalResult;
    }

    function renderTable() {
        const selectedLeagues = choicesLeague.getValue(true);
        const selectedPatches = choicesPatch.getValue(true);
        const selectedSplits = choicesSplit.getValue(true);
        const selectedChampions = choicesChampion.getValue(true);

        let filteredData = allData.filter(item => 
            (selectedLeagues.length === 0 || selectedLeagues.includes(item.league)) &&
            (selectedPatches.length === 0 || selectedPatches.includes(String(item.patch))) &&
            (selectedSplits.length === 0 || selectedSplits.includes(item.split)) &&
            (selectedChampions.length === 0 || selectedChampions.includes(item.champion))
        );
        
        let dataToRender = isGrouped ? groupDataByChampion(filteredData) : filteredData;

        dataToRender.sort((a, b) => {
            if (!a.hasOwnProperty(sortState.column) || !b.hasOwnProperty(sortState.column)) return 0;
            const valA = a[sortState.column];
            const valB = b[sortState.column];
            if (valA == null || valB == null) return 0;
            let comparison = typeof valA === 'string' ? valA.localeCompare(b[sortState.column], undefined, { numeric: true }) : (valA > valB ? 1 : -1);
            return sortState.direction === 'desc' ? -comparison : comparison;
        });
        
        if (dataToRender.length === 0) {
            tableContainer.innerHTML = '<p>Nenhum dado encontrado.</p>';
            return;
        }

        const headers = Object.keys(dataToRender[0]);
        const getSortIndicator = col => sortState.column === col ? (sortState.direction === 'asc' ? ' ▲' : ' ▼') : '';
        
        let tableHTML = '<table><thead><tr>';
        headers.forEach(h => tableHTML += `<th data-sort="${h}">${h.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}${getSortIndicator(h)}</th>`);
        tableHTML += '</tr></thead><tbody>';
        
        dataToRender.slice(0, 200).forEach(row => {
            tableHTML += '<tr>';
            headers.forEach(header => {
                let value = row[header];
                if (typeof value === 'number' && (header.includes('rate') || header.includes('winrate'))) {
                    value = (value * 100).toFixed(2) + '%';
                } else if (typeof value === 'number' && value % 1 !== 0) {
                     value = value.toFixed(2);
                }
                tableHTML += `<td>${value ?? 'N/A'}</td>`;
            });
            tableHTML += '</tr>';
        });
        
        tableHTML += '</tbody></table>';
        tableContainer.innerHTML = tableHTML;
        addSortListeners();
    }
    
    function addSortListeners() {
        document.querySelectorAll('#table-container th[data-sort]').forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const column = header.dataset.sort;
                if (sortState.column === column) {
                    sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
                } else {
                    sortState.column = column;
                    sortState.direction = 'desc';
                }
                renderTable();
            });
        });
    }

    main();
});