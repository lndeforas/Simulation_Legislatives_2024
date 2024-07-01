import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page principale
base_url = f"https://www.resultats-elections.interieur.gouv.fr/legislatives2024/ensemble_geographique/index.html"

# Fonction pour récupérer les données d'une circonscription
def get_circonscription_data(circonscription_url):
    response = requests.get(circonscription_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les résultats des tableaux (à adapter en fonction de la structure HTML)
    tables = soup.find_all('table')
    
    # La première table est celle des résultats
    results_table = tables[0]
    
    data = []
    headers = [header.text for header in results_table.find_all('th')]
    rows = results_table.find_all('tr')[1:]  # Ignorer l'en-tête

    for row in rows:
        cols = row.find_all('td')
        data.append([col.text.strip() for col in cols])
    
    return headers, data

# Fonction pour récupérer les données d'un département
def get_department_data(department_url):
    response = requests.get(department_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Récupérer les options du menu déroulant des circonscriptions
    select = soup.find('select', {'id': 'selectCir'})
    options = select.find_all('option')
    
    department_data = []
    for option in options:
        if option.get('value'):
            circ_name = option.text.strip()
            circ_url = department_url.rsplit('/', 1)[0] + '/' + option.get('value')
            print(f"  Collecting data for circonscription {circ_name}")
            headers, data = get_circonscription_data(circ_url)
            for row in data:
                row.insert(0, circ_name)  # Ajouter le nom de la circonscription dans chaque ligne
            department_data.extend(data)
    
    return headers, department_data

# Récupérer la liste des départements
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
select = soup.find('select', {'id': 'selectDep'})
options = select.find_all('option')

departments = {}
for option in options:
    if option.get('value'):
        department_name = option.text.strip()
        department_url = base_url[:-10] + option.get('value')
        departments[department_name] = department_url

# Collecter les données de chaque département et chaque circonscription
all_data = []
for department, dept_url in departments.items():
    print(f"Collecting data for {department}")
    headers, data = get_department_data(dept_url)
    for row in data:
        row.insert(0, department)  # Ajouter le nom du département dans chaque ligne
    all_data.extend(data)

# Convertir les données en DataFrame pandas
columns = ["Département", "Circonscription"] + headers
df = pd.DataFrame(all_data, columns=columns)

# Enregistrer les données dans un fichier CSV
df.to_csv(f'resultats_elections_2024_circonscriptions.csv', index=False, encoding='utf-8')

print(f"Données sauvegardées dans 'resultats_elections_2024_circonscriptions.csv'")
