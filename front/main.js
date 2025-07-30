document.addEventListener('DOMContentLoaded', () => {
    
    let allData = [];
    let currentView = 'champions'; // 'champions' ou 'objectives'
    let sortState = { column: 'banrate', direction: 'desc' }; 
    let isGrouped = false;

    const tableContainer = document.getElementById('table-container');
    const viewSelector = document.getElementById('view-selector');
    const groupByBtn = document.getElementById('group-by-btn');
    const resetViewBtn = document.getElementById('reset-view-btn');

    // Inicializa todos os filtros
    const choicesLeague = new Choices('#league-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesPatch = new Choices('#patch-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesSplit = new Choices('#split-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesChampion = new Choices('#champion-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesObjective = new Choices('#objective-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });

    async function loadAndRender(jsonPath) {
        tableContainer.innerHTML = '<p>Carregando dados...</p>';
        try {
            const response = await fetch(`front/data/${jsonPath}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            allData = await response.json();
            
            populateFilters();
            renderTable();
        } catch (error) {
            console.error('Erro ao carregar ou processar dados:', error);
            tableContainer.innerHTML = `<p style="color: red;">Falha ao carregar ${jsonPath}.</p>`;
        }
    }

    function switchView(view, source) {
        currentView = view;
        isGrouped = false;

        document.querySelector('#view-selector button.active').classList.remove('active');
        document.querySelector(`button[data-view="${view}"]`).classList.add('active');

        // Mostra/esconde os filtros específicos
        document.getElementById('champion-filter-group').classList.toggle('hidden', view !== 'champions');
        document.getElementById('objective-filter-group').classList.toggle('hidden', view !== 'objectives');
        
        // Atualiza o texto do botão e a ordenação padrão
        if (view === 'champions') {
            groupByBtn.textContent = 'Agrupar por Campeão';
            sortState = { column: 'banrate', direction: 'desc' };
        } else {
            groupByBtn.textContent = 'Agrupar por Objetivo';
            sortState = { column: 'winrate', direction: 'desc' };
        }

        loadAndRender(source);
    }

    function populateFilters() {
        // Limpa todas as opções anteriores
        [choicesLeague, choicesPatch, choicesSplit, choicesChampion, choicesObjective].forEach(c => c.clearStore());
        
        const unique = {
            leagues: [...new Set(allData.map(item => item.league))].sort(),
            patches: [...new Set(allData.map(item => String(item.patch)))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
            splits: [...new Set(allData.map(item => item.split))].sort(),
            champions: [...new Set(allData.map(item => item.champion))].sort(),
            objectives: [...new Set(allData.map(item => item.objective))].sort()
        };

        choicesLeague.setChoices(unique.leagues.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesPatch.setChoices(unique.patches.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesSplit.setChoices(unique.splits.map(val => ({ value: val, label: val })), 'value', 'label', true);
        
        if (currentView === 'champions') {
            choicesChampion.setChoices(unique.champions.map(val => ({ value: val, label: val })), 'value', 'label', true);
        } else {
            choicesObjective.setChoices(unique.objectives.map(val => ({ value: val, label: val })), 'value', 'label', true);
        }
    }
    
    function setupEventListeners() {
        viewSelector.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') {
                switchView(e.target.dataset.view, e.target.dataset.source);
            }
        });

        [choicesLeague, choicesPatch, choicesSplit, choicesChampion, choicesObjective].forEach(choiceInstance => {
            choiceInstance.passedElement.element.addEventListener('change', renderTable);
        });
        
        groupByBtn.addEventListener('click', () => {
            isGrouped = true;
            renderTable();
        });

        resetViewBtn.addEventListener('click', () => {
            isGrouped = false;
            populateFilters(); // Repopula e limpa seleções
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
    
    // NOVA FUNÇÃO PARA AGRUPAR OBJETIVOS
    function groupDataByObjective(data) {
        if (data.length === 0) return [];
        const grouped = {};

        data.forEach(row => {
            const objective = row.objective;
            if (!objective) return;
            if (!grouped[objective]) {
                grouped[objective] = {
                    objective: objective,
                    record_count: 0,
                    total_games: 0,
                    weighted_winrate_sum: 0
                };
            }
            grouped[objective].record_count++;
            grouped[objective].total_games += row.games || 0;
            grouped[objective].weighted_winrate_sum += (row.winrate || 0) * (row.games || 0);
        });

        return Object.values(grouped).map(group => {
            const totalGames = group.total_games > 0 ? group.total_games : 1;
            return {
                'objective': group.objective,
                'record_count': group.record_count,
                'games': group.total_games,
                'winrate': group.weighted_winrate_sum / totalGames
            };
        });
    }

    function renderTable() {
        const selectedLeagues = choicesLeague.getValue(true);
        const selectedPatches = choicesPatch.getValue(true);
        const selectedSplits = choicesSplit.getValue(true);

        let filteredData = allData.filter(item => 
            (selectedLeagues.length === 0 || selectedLeagues.includes(item.league)) &&
            (selectedPatches.length === 0 || selectedPatches.includes(String(item.patch))) &&
            (selectedSplits.length === 0 || selectedSplits.includes(item.split))
        );
        
        if (currentView === 'champions') {
            const selectedChampions = choicesChampion.getValue(true);
            if (selectedChampions.length > 0) {
                filteredData = filteredData.filter(item => selectedChampions.includes(item.champion));
            }
        } else { // objectives view
            const selectedObjectives = choicesObjective.getValue(true);
            if (selectedObjectives.length > 0) {
                filteredData = filteredData.filter(item => selectedObjectives.includes(item.objective));
            }
        }
        
        let dataToRender;
        if (isGrouped) {
            dataToRender = currentView === 'champions' ? groupDataByChampion(filteredData) : groupDataByObjective(filteredData);
        } else {
            dataToRender = filteredData;
        }

        // ... O resto da função renderTable e addSortListeners continua exatamente igual ...
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

        const headers = Object.keys(dataToRender[0] || {});
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

    // Carga Inicial da primeira visão
    switchView('champions', 'champions.json');
    setupEventListeners();
});