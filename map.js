// Fonction pour charger le fichier CSV qui contient la simulation des résultats
function loadCSV(file) {
    console.log('Loading CSV:', file);
    return fetch(file)
        .then(response => response.text())
        .then(text => {
            const data = Papa.parse(text, { header: true }).data;
            return data;
        });
}

// Fonction pour charger le fichier GeoJSON qui contient les coordonnées des circonscriptions
function loadGeoJSON(file) {
    return fetch(file)
        .then(response => response.json());
}

// Fonction pour nettoyer et normaliser les valeurs des chaînes de caractères
function normalizeString(str) {
    return str.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

// Fusionner les données du CSV avec le GeoJSON, en utilisant le département et la circonscription comme clé
function mergeData(geoData, csvData) {
    const mergedFeatures = geoData.features.map(feature => {
        const code_dpt = normalizeString(feature.properties.code_dpt);
        const num_circ = normalizeString(feature.properties.num_circ);

        const elected = csvData.find(c => 
            normalizeString(c.Département).includes(code_dpt) &&
            normalizeString(c.Circonscription) === num_circ &&
            c["Elu(e)"] === '1');

        const eliminated = csvData.filter(c => 
            normalizeString(c.Département).includes(code_dpt) &&
            normalizeString(c.Circonscription) === num_circ &&
            c["Elu(e)"] === '0');
        
        if (elected) {
            feature.properties = { ...feature.properties, ...elected };
            feature.properties.eliminatedCandidates = eliminated;
            feature.merged = true; 
        } else {
            feature.merged = false; 
            feature.properties.eliminatedCandidates = eliminated;
            console.log('Unmerged feature:', feature.properties); // Log unmerged features
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
                return '#0000ff'; // Bleu pour LR
            case 'DIV':
                return '#ffff00'; // Jaune pour DIV
            default:
                return '#ff8c00'; // Orange pour dafault
        }
    } else {
        return '#ffffff'; // Bnalc si on n'a pas de résultat
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
            const features = mergedData.features;

            L.geoJSON(features, {
                style: function (feature) {
                    return {
                        color: '#ffffff',
                        weight: 1,
                        fillColor: getColor(feature),
                        fillOpacity: 0.7
                    };
                },
                onEachFeature: function (feature, layer) {
                    let eliminatedCandidates = feature.properties.eliminatedCandidates.map(c => `${c['Liste des candidats']} (${c['Voix']})`).join(', ');
                    layer.bindPopup('<b>Département:</b> ' + feature.properties.nom_dpt + '<br>' +
                                    '<b>Circonscription:</b> ' + feature.properties.num_circ + '<br>' +
                                    '<b>Région:</b> ' + feature.properties.nom_reg + '<br>' +
                                    '<b>Nuance:</b> ' + feature.properties.Nuance + '<br>' +
                                    '<b>Elu.e:</b> ' + feature.properties['Liste des candidats'] + ' (' + feature.properties.Voix + ')' + '<br>' +
                                    '<b>Eliminé.e.s:</b> ' + eliminatedCandidates);
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
