from Preprocessing import Preprocessing
import json

path = "resultats_elections_2024_circonscriptions.csv"

df = Preprocessing(path).df_ready
print(df.groupby("Nuance").count())

df2 = df[df["Elu(e)"] != -1][["Département", "Circonscription", "Nuance", "Liste des candidats"]]
df2[["Voix","% Exprimés","Elu(e)"]] = 0

with open('coefficients.json', 'r') as file:
    coefficients = json.load(file)

def duel(dep, circ):
    df1 = df[(df["Département"]==dep) & (df["Circonscription"]==circ)]
    if (df1["Elu(e)"] == 1).any():
            nom = df1[df1["Elu(e)"] == 1]["Liste des candidats"].values[0]
            ligne = (df2["Département"]==dep) & (df2["Circonscription"]==circ) & (df2["Liste des candidats"] == nom)
            df2.loc[ligne, "Elu(e)"] = 1
            df2.loc[ligne, "% Exprimés"] = 100
            df2.loc[ligne, "Voix"] = df1["Voix"].sum()

    elif df1[df1["Elu(e)"] == 0].shape[0] == 2:
        partis = set(df2[(df2["Département"]==dep) & (df2["Circonscription"]==circ)]["Nuance"])
        ligne = (df2["Département"]==dep) & (df2["Circonscription"]==circ)
        votants = df1["Voix"].sum()

        key = "_".join(sorted(partis))
        if key in coefficients:
            for parti in partis:
                coeffs = coefficients[key][parti]
                tot_voix= 0
                for k, v in coeffs.items():
                    tot_voix += v * df1[df1["Nuance"] == k]["Voix"].sum()
                df2.loc[ligne & (df2["Nuance"] == parti), "Voix"] = int(tot_voix)
                df2.loc[ligne & (df2["Nuance"] == parti), "% Exprimés"] = (int(tot_voix) / votants).round(2)
            df2.loc[ligne & (df2["% Exprimés"] >= 0.5), "Elu(e)"] = 1

for dep in df2["Département"].unique():
      for circ in df2[df2["Département"] == dep]["Circonscription"].unique():
            duel(dep, circ)

df2.to_csv(f'simulation_elections_2024_circonscriptions.csv', index=False, encoding='utf-8')

# python3 -m http.server 8000