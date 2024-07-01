document.addEventListener('DOMContentLoaded', function() {
    // Fonction pour charger le fichier CSV
    function loadCSV(file) {
        return fetch(file)
            .then(response => response.text())
            .then(text => {
                const data = Papa.parse(text, { header: true }).data;
                return data;
            });
    }

    // Créer le graphique
    function createChart(csvData) {
        const nuanceCounts = csvData.reduce((acc, row) => {
            if (row["Elu(e)"] === '1') {
                acc[row.Nuance] = (acc[row.Nuance] || 0) + 1;
            }
            return acc;
        }, {});

        const colors = {
            'RN': '#000000',  // Noir pour RN
            'NFP': '#ff0000', // Rouge pour NFP
            'ENS': '#ff00ff', // Violet pour ENS
            'LR': '#0000ff',  // Bleu pour LR
            'DIV': '#ffff00', // Jaune pour DIV
            'default': '#ff8c00'  // Orange par défaut
        };

        const labels = Object.keys(nuanceCounts);
        const data = Object.values(nuanceCounts);
        const backgroundColors = labels.map(label => colors[label] || colors['default']);

        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Proportion des Nuances Elues',
                    data: data,
                    backgroundColor: backgroundColors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });
    }

    // Charger et afficher les données CSV
    loadCSV('simulation_elections_2024_circonscriptions.csv')
        .then(createChart)
        .catch(error => {
            console.error('Error loading the CSV data:', error);
        });
});
