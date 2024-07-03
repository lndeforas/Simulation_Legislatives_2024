from Preprocessing import PreprocessingCSV, PreprocessingJSON
import json

# Preprocessing des données brutes
path = "resultats_elections_2024_circonscriptions.csv"
path_json = "france-circonscriptions-legislatives-2012 copy.json"
PreprocessingJSON(path_json)
df = PreprocessingCSV(path).df_ready

print(df.groupby("Nuance").count())

# df2 est la df qui contient les résultats simulés
df2 = df[df["Elu(e)"] != -1][["Département", "Circonscription", "Nuance", "Liste des candidats"]]
df2[["Voix","Elu(e)"]] = 0

with open('coefficients.json', 'r') as file:
    coefficients = json.load(file)

def simul(dep, circ):
    # fonction principale qui simule les résultats pour une circonscription donnée
    df1 = df[(df["Département"]==dep) & (df["Circonscription"]==circ)]

    partis = set(df2[(df2["Département"]==dep) & (df2["Circonscription"]==circ)]["Nuance"])
    ligne = (df2["Département"]==dep) & (df2["Circonscription"]==circ)

    # Victoire au premier tour ou deux candidats du même parti au second tour
    if (df1["Elu(e)"] == 1).any() or (len(partis) == 1): 
            nom = df1[df1["Voix"] == df1["Voix"].max()]["Liste des candidats"].values[0]
            ligne = (df2["Département"]==dep) & (df2["Circonscription"]==circ) & (df2["Liste des candidats"] == nom)
            df2.loc[ligne, "Elu(e)"] = 1
            df2.loc[ligne, "Voix"] = df1["Voix"].sum()

    elif (df1[df1["Elu(e)"] == 0].shape[0] >= 2): # Duel, triangulaire ou quadrangulaire
        calcul_voix(partis, ligne, df1)
        
def calcul_voix(partis, ligne, df1):
    # Calcul du nombre de voix à partir des coefficients
    key = "_".join(sorted(partis))
    if key in coefficients:
        for parti in partis:
            coeffs = coefficients[key][parti]
            tot_voix= 0
            for k, v in coeffs.items():
                tot_voix += v * df1[df1["Nuance"] == k]["Voix"].sum()
            df2.loc[ligne & (df2["Nuance"] == parti), "Voix"] = int(tot_voix)
        df2.loc[df2.loc[ligne, "Voix"].idxmax(), "Elu(e)"] = 1
    else:
        print(partis, dep, circ)
        print("Combinaison non disponible")

# boucle sur toutes les circonscriptions
for dep in df2["Département"].unique():
      for circ in df2[df2["Département"] == dep]["Circonscription"].unique():
            simul(dep, circ)

df2.to_csv(f'simulation_elections_2024_circonscriptions.csv', index=False, encoding='utf-8')

# python3 -m http.server 8000