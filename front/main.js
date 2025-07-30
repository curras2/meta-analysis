document.addEventListener('DOMContentLoaded', () => {
    
    let allData = [];
    let currentView = 'champions';
    let sortState = { column: 'banrate', direction: 'desc' }; 
    let isGrouped = false;

    const tableContainer = document.getElementById('table-container');
    const viewSelector = document.getElementById('view-selector');
    const groupByBtn = document.getElementById('group-by-btn');
    const resetViewBtn = document.getElementById('reset-view-btn');

    const choicesLeague = new Choices('#league-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesPatch = new Choices('#patch-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesSplit = new Choices('#split-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesChampion = new Choices('#champion-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesObjective = new Choices('#objective-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesSoul = new Choices('#soul-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });
    const choicesSide = new Choices('#side-filter', { removeItemButton: true, placeholder: true, placeholderValue: 'Selecione...' });

    function getViewConfig(view) {
        const defaultConfig = {
            groupByKey: null,
            defaultSort: { column: 'winrate', direction: 'desc' },
            columnOrder: [],
            groupedColumnOrder: []
        };

        switch (view) {
            case 'champions':
                return {
                    groupByKey: 'champion',
                    defaultSort: { column: 'champion', direction: 'asc' },
                    columnOrder: ['league', 'split','patch', 'champion', 'pickrate', 'banrate', 'picked games', 'banned games', 'total games', 'winrate'],
                    groupedColumnOrder: ['champion', 'pickrate', 'banrate', 'picked games', 'banned games', 'total games', 'winrate']
                };
            case 'objectives':
                return {
                    groupByKey: 'objective',
                    defaultSort: { column: 'winrate', direction: 'desc' },
                    columnOrder: ['objective', 'league', 'patch', 'split', 'winrate', 'games'],
                    groupedColumnOrder: ['objective', 'record_count', 'winrate', 'games']
                };
            case 'souls':
                return {
                    groupByKey: 'soul',
                    defaultSort: { column: 'winrate', direction: 'desc' },
                    columnOrder: ['soul', 'league', 'patch', 'split', 'winrate', 'count'],
                    groupedColumnOrder: ['soul', 'record_count', 'winrate', 'count']
                };
            case 'sides':
                return {
                    groupByKey: 'side',
                    defaultSort: { column: 'winrate', direction: 'desc' },
                    columnOrder: ['side', 'league', 'patch', 'split', 'winrate'],
                    groupedColumnOrder: ['side', 'record_count', 'winrate']
                };
            case 'game_length':
                return {
                    groupByKey: 'league',
                    defaultSort: { column: 'game_length_mean', direction: 'desc' },
                    columnOrder: ['league', 'patch', 'split', 'game_length_mean'],
                    groupedColumnOrder: ['league', 'record_count', 'game_length_mean', 'game_length_mean_seconds']
                };
            default:
                return defaultConfig;
        }
    }

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
        const config = getViewConfig(view);

        document.querySelector('#view-selector button.active').classList.remove('active');
        document.querySelector(`button[data-view="${view}"]`).classList.add('active');

        document.getElementById('champion-filter-group').classList.toggle('hidden', view !== 'champions');
        document.getElementById('objective-filter-group').classList.toggle('hidden', view !== 'objectives');
        document.getElementById('soul-filter-group').classList.toggle('hidden', view !== 'souls');
        document.getElementById('side-filter-group').classList.toggle('hidden', view !== 'sides');
        
        groupByBtn.style.display = config.groupByKey ? 'inline-block' : 'none';
        if (config.groupByKey) {
            groupByBtn.textContent = `Agrupar por ${config.groupByKey.charAt(0).toUpperCase() + config.groupByKey.slice(1)}`;
        }
        
        sortState = config.defaultSort;
        loadAndRender(source);
    }

    function populateFilters() {
        [choicesLeague, choicesPatch, choicesSplit, choicesChampion, choicesObjective, choicesSoul, choicesSide].forEach(c => c.clearStore());
        
        const unique = {
            leagues: [...new Set(allData.map(item => item.league))].sort(),
            patches: [...new Set(allData.map(item => String(item.patch)))].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
            splits: [...new Set(allData.map(item => item.split))].sort(),
            champions: [...new Set(allData.map(item => item.champion))].sort(),
            objectives: [...new Set(allData.map(item => item.objective))].sort(),
            souls: [...new Set(allData.map(item => item.soul))].sort(),
            sides: [...new Set(allData.map(item => item.side))].sort()
        };

        choicesLeague.setChoices(unique.leagues.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesPatch.setChoices(unique.patches.map(val => ({ value: val, label: val })), 'value', 'label', true);
        choicesSplit.setChoices(unique.splits.map(val => ({ value: val, label: val })), 'value', 'label', true);
        
        if (currentView === 'champions') choicesChampion.setChoices(unique.champions.map(val => ({ value: val, label: val })), 'value', 'label', true);
        else if (currentView === 'objectives') choicesObjective.setChoices(unique.objectives.map(val => ({ value: val, label: val })), 'value', 'label', true);
        else if (currentView === 'souls') choicesSoul.setChoices(unique.souls.map(val => ({ value: val, label: val })), 'value', 'label', true);
        else if (currentView === 'sides') choicesSide.setChoices(unique.sides.map(val => ({ value: val, label: val })), 'value', 'label', true);
    }
    
    function setupEventListeners() {
        viewSelector.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON' && !e.target.classList.contains('active')) {
                switchView(e.target.dataset.view, e.target.dataset.source);
            }
        });

        [choicesLeague, choicesPatch, choicesSplit, choicesChampion, choicesObjective, choicesSoul, choicesSide].forEach(choiceInstance => {
            choiceInstance.passedElement.element.addEventListener('change', renderTable);
        });
        
        groupByBtn.addEventListener('click', () => { isGrouped = true; renderTable(); });
        resetViewBtn.addEventListener('click', () => { isGrouped = false; populateFilters(); renderTable(); });
    }

    function groupDataByChampion(data) {
        if (data.length === 0) return [];
        const grouped = {};
        const columnsToProcess = ['picked games', 'banned games', 'total games', 'winrate'];
        const seenCombinations = new Set();
        let trueTotalGames = 0;
        data.forEach(row => {
            const combinationKey = `${row.league}|${row.patch}|${row.split}`;
            if (!seenCombinations.has(combinationKey)) {
                trueTotalGames += row['total games'] || 0;
                seenCombinations.add(combinationKey);
            }
        });
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
        return Object.values(grouped).map(group => {
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
    }
    
    function groupDataByObjective(data) {
        if (data.length === 0) return [];
        const grouped = {};
        data.forEach(row => {
            const objective = row.objective;
            if (!objective) return;
            if (!grouped[objective]) {
                grouped[objective] = {
                    objective: objective, record_count: 0, total_games: 0, weighted_winrate_sum: 0
                };
            }
            grouped[objective].record_count++;
            grouped[objective].total_games += row.games || 0;
            grouped[objective].weighted_winrate_sum += (row.winrate || 0) * (row.games || 0);
        });
        return Object.values(grouped).map(group => {
            const totalGames = group.total_games > 0 ? group.total_games : 1;
            return {
                'objective': group.objective, 'record_count': group.record_count, 'games': group.total_games, 'winrate': group.weighted_winrate_sum / totalGames
            };
        });
    }

    function groupDataBySoul(data) {
        if (data.length === 0) return [];
        const grouped = {};
        data.forEach(row => {
            const soul = row.soul;
            if (!soul) return;
            if (!grouped[soul]) {
                grouped[soul] = {
                    soul: soul, record_count: 0, total_count: 0, weighted_winrate_sum: 0
                };
            }
            grouped[soul].record_count++;
            grouped[soul].total_count += row.count || 0;
            grouped[soul].weighted_winrate_sum += (row.winrate || 0) * (row.count || 0);
        });
        return Object.values(grouped).map(group => {
            const totalCount = group.total_count > 0 ? group.total_count : 1;
            return {
                'soul': group.soul, 'record_count': group.record_count, 'count': group.total_count, 'winrate': group.weighted_winrate_sum / totalCount
            };
        });
    }

    function groupDataBySide(data) {
        if (data.length === 0) return [];
        const grouped = {};
        data.forEach(row => {
            const side = row.side;
            if (!side) return;
            if (!grouped[side]) {
                grouped[side] = { side: side, record_count: 0, winrate_sum: 0 };
            }
            grouped[side].record_count++;
            grouped[side].winrate_sum += row.winrate || 0;
        });
        return Object.values(grouped).map(group => {
            const recordCount = group.record_count > 0 ? group.record_count : 1;
            return {
                'side': group.side, 'record_count': group.record_count, 'winrate': group.winrate_sum / recordCount
            };
        });
    }

    function groupDataByLeague(data) {
        if (data.length === 0) return [];
        const grouped = {};
        data.forEach(row => {
            const league = row.league;
            if (!league) return;
            const timeParts = String(row.game_length_mean).split(':');
            const seconds = (+timeParts[0] || 0) * 60 + (+timeParts[1] || 0);
            if (!grouped[league]) {
                grouped[league] = { league: league, record_count: 0, total_seconds: 0 };
            }
            grouped[league].record_count++;
            grouped[league].total_seconds += seconds;
        });
        return Object.values(grouped).map(group => {
            const recordCount = group.record_count > 0 ? group.record_count : 1;
            const avgSeconds = group.total_seconds / recordCount;
            const minutes = Math.floor(avgSeconds / 60);
            const seconds = Math.round(avgSeconds % 60).toString().padStart(2, '0');
            return {
                'league': group.league,
                'record_count': group.record_count,
                'game_length_mean_seconds': avgSeconds,
                'game_length_mean': `${minutes}:${seconds}`
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
        
        switch (currentView) {
            case 'champions':
                const selectedChampions = choicesChampion.getValue(true);
                if (selectedChampions.length > 0) filteredData = filteredData.filter(item => selectedChampions.includes(item.champion));
                break;
            case 'objectives':
                const selectedObjectives = choicesObjective.getValue(true);
                if (selectedObjectives.length > 0) filteredData = filteredData.filter(item => selectedObjectives.includes(item.objective));
                break;
            case 'souls':
                const selectedSouls = choicesSoul.getValue(true);
                if (selectedSouls.length > 0) filteredData = filteredData.filter(item => selectedSouls.includes(item.soul));
                break;
            case 'sides':
                const selectedSides = choicesSide.getValue(true);
                if (selectedSides.length > 0) filteredData = filteredData.filter(item => selectedSides.includes(item.side));
                break;
        }
        
        let dataToRender;
        if (isGrouped) {
            switch (currentView) {
                case 'champions': dataToRender = groupDataByChampion(filteredData); break;
                case 'objectives': dataToRender = groupDataByObjective(filteredData); break;
                case 'souls': dataToRender = groupDataBySoul(filteredData); break;
                case 'sides': dataToRender = groupDataBySide(filteredData); break;
                case 'game_length': dataToRender = groupDataByLeague(filteredData); break;
                default: dataToRender = filteredData;
            }
        } else {
            dataToRender = filteredData;
        }

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

        const config = getViewConfig(currentView);
        const headers = isGrouped ? config.groupedColumnOrder : config.columnOrder;
        const getSortIndicator = col => sortState.column === col ? (sortState.direction === 'asc' ? ' ▲' : ' ▼') : '';
        
        let tableHTML = '<table><thead><tr>';
        headers.forEach(h => {
            if (dataToRender[0].hasOwnProperty(h)) {
                tableHTML += `<th data-sort="${h}">${h.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}${getSortIndicator(h)}</th>`;
            }
        });
        tableHTML += '</tr></thead><tbody>';
        
        dataToRender.slice(0, 200).forEach(row => {
            tableHTML += '<tr>';
            headers.forEach(header => {
                if (row.hasOwnProperty(header)) {
                    let value = row[header];
                    if (typeof value === 'number' && (header.includes('rate') || header.includes('winrate'))) {
                        value = (value * 100).toFixed(2) + '%';
                    } else if (typeof value === 'number' && value % 1 !== 0) {
                         value = value.toFixed(2);
                    }
                    tableHTML += `<td>${value ?? 'N/A'}</td>`;
                }
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

    setupEventListeners();
    switchView('champions', 'champions.json');
});