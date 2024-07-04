// Fonction pour charger le fichier CSV qui contient les résultats
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

        const candidates = csvData.filter(c => 
            normalizeString(c.Département).includes(code_dpt) &&
            normalizeString(c.Circonscription) === num_circ);

        if (candidates.length > 0) {
            const elected = candidates.find(c => c["Elu(e)"] === '1');
            const topCandidate = candidates.reduce((prev, current) => (parseFloat(prev.Voix) > parseFloat(current.Voix)) ? prev : current);
            feature.properties.candidates = candidates.filter(c => c !== topCandidate);;

            if (elected) {
                feature.properties = { ...feature.properties, ...elected };
                feature.properties.elu = true;
            } else {
                feature.properties = { ...feature.properties, ...topCandidate };
                feature.properties.elu = false;
            }

            feature.merged = true;
        } else {
            feature.merged = false;
            feature.properties.candidates = [];
            console.log('Unmerged feature:', feature.properties); // Log unmerged features
        }
        return feature;
    });

    return { ...geoData, features: mergedFeatures };
}

// Définir les couleurs en fonction de la nuance du candidat élu ou du candidat avec le plus de voix
function getColor(feature) {
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
            return '#ff8c00'; // Orange pour default
    }
}

let geojsonLayer; // Variable pour stocker la couche GeoJSON

// Charger et afficher les données sur la carte
function displayMap() {
    const map = L.map('map').setView([46.603354, 1.888334], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    document.getElementById('simulation').addEventListener('change', function() {
        if (this.checked) {
            loadDataAndDisplay('simulation_elections_2024_circonscriptions.csv', map);
        }
    });

    document.getElementById('results1').addEventListener('change', function() {
        if (this.checked) {
            loadDataAndDisplay('resultats_1_elections_2024_circonscriptions.csv', map);
        }
    });

    loadDataAndDisplay('simulation_elections_2024_circonscriptions.csv', map);
}

// Fonction pour charger les données et les afficher sur la carte
function loadDataAndDisplay(csvFile, map) {
    Promise.all([loadGeoJSON('france-circonscriptions-legislatives-2012.json'), loadCSV(csvFile)])
        .then(([geoData, csvData]) => {
            const mergedData = mergeData(geoData, csvData);
            const features = mergedData.features;

            if (geojsonLayer) {
                map.removeLayer(geojsonLayer); // Retirer la couche GeoJSON existante
            }

            geojsonLayer = L.geoJSON(features, {
                style: function (feature) {
                    return {
                        color: '#ffffff',
                        weight: 1,
                        fillColor: getColor(feature),
                        fillOpacity: 0.7
                    };
                },
                onEachFeature: function (feature, layer) {
                    let candidatesInfo = feature.properties.candidates.map(c => `${c['Liste des candidats']} (${c['Voix']})`).join(', ');
                    let popupContent = '<b>Département:</b> ' + feature.properties.nom_dpt + '<br>' +
                                       '<b>Circonscription:</b> ' + feature.properties.num_circ + '<br>' +
                                       '<b>Région:</b> ' + feature.properties.nom_reg + '<br>' +
                                       '<b>Nuance:</b> ' + feature.properties.Nuance + '<br>';

                    if (feature.properties.elu) {
                        popupContent += '<b>Elu.e:</b> ' + feature.properties['Liste des candidats'] + ' (' + feature.properties.Voix + ')<br>';
                        popupContent += '<b>Candidats:</b> ' + candidatesInfo + '<br>';
                    } else {
                        popupContent += '<b>Candidat en tête:</b> ' + feature.properties['Liste des candidats'] + ' (' + feature.properties.Voix + ')<br>';
                        popupContent += '<b>Candidats:</b> ' + candidatesInfo + '<br>';
                    }

                    layer.bindPopup(popupContent);
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
