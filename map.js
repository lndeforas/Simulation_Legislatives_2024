// Fonction pour charger le fichier CSV
function loadCSV(file) {
    return fetch(file)
        .then(response => response.text())
        .then(text => {
            const data = Papa.parse(text, { header: true }).data;
            return data;
        });
}

// Fonction pour charger le fichier GeoJSON
function loadGeoJSON(file) {
    return fetch(file)
        .then(response => response.json());
}

// Fusionner les données du CSV avec le GeoJSON
function mergeData(geoData, csvData) {
    const mergedFeatures = geoData.features.map(feature => {
        const circ = csvData.find(c => 
            c.Département.includes(feature.properties.code_dpt) &&
            c.Circonscription.includes(feature.properties.num_circ));
        
        if (circ) {
            feature.properties = { ...feature.properties, ...circ };
        }
        return feature;
    });

    return { ...geoData, features: mergedFeatures };
}

// Définir les couleurs en fonction de la nuance et de l'état élu
function getColor(feature) {
    if (feature.properties['Elu(e)'] === '1') {
        switch (feature.properties.Nuance) {
            case 'RN':
                return '#000000'; // Black pour RN
            case 'NFP':
                return '#ff0000'; // Rouge pour NFP
            case 'ENS':
                return '#ff00ff'; // Violet pour ENS
            case 'LR':
                return '#0000ff'; //Blue
            case 'DIV':
                return '#ffff00'; //Yellow
            default:
                return '#ff8c00'; // Default color if no match
        }
    } else {
        return '#ffffff'; // Default color if not elected
    }
}

// Charger et afficher les données sur la carte
function displayMap() {
    const map = L.map('map').setView([46.603354, 1.888334], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    Promise.all([loadGeoJSON('france-circonscriptions-legislatives-2012.json'), loadCSV('simulation_elections_2024_circonscriptions.csv')])
        .then(([geoData, csvData]) => {
            const mergedData = mergeData(geoData, csvData);
            const firstThreeFeatures = mergedData.features;

            L.geoJSON(firstThreeFeatures, {
                style: function (feature) {
                    return {
                        color: getColor(feature),
                        weight: 2
                    };
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup('<b>Département:</b> ' + feature.properties.nom_dpt + '<br>' +
                                    '<b>Circonscription:</b> ' + feature.properties.num_circ + '<br>' +
                                    '<b>Région:</b> ' + feature.properties.nom_reg + '<br>' +
                                    '<b>Nuance:</b> ' + feature.properties.Nuance + '<br>' +
                                    '<b>Elu:</b> ' + (feature.properties['Elu(e)'] === '1' ? 'Oui' : 'Non'));
                }
            }).addTo(map);
        })
        .catch(error => {
            console.error('Error loading the data:', error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    displayMap();
});
