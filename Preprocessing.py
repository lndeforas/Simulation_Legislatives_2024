import pandas as pd
import json

listes_gauche = ['UG', 'EXG', 'COM', 'FI', 'SOC', 'RDG', 'VEC', 'DVG', 'ECO']
listes_centre = ['REN', 'MDM', 'HOR', 'ENS', 'DVC', 'UDI']
listes_droite = ['LR', 'DSV', 'DVD']
listes_exdroite = ['RN', 'EXD', 'UXD', 'REC']
listes_autres = ['DIV', 'REG']

class PreprocessingCSV():
    def __init__(self, path):
        df = pd.read_csv(path).drop(columns=["% Inscrits"])
        df["% Exprimés"] = df["% Exprimés"].str.replace(',', '.').astype(float)
        df.loc[df["Elu(e)"] == "OUI", "Elu(e)"] = 1
        df.loc[df["Elu(e)"] == "QUALIF T2", "Elu(e)"] = 0
        df.loc[df["Elu(e)"] == "NON", "Elu(e)"] = -1
        df["Voix"] = df["Voix"].str.replace('\u202f', '', regex=True).astype(int)
        df["Circonscription"] = df["Circonscription"].apply(lambda x: x[6:]).str.replace(r'\D', '', regex=True)
        self.df = df
        self.df_nuance = self.group_nuance()
        self.df_ready = self.desistements()
        df['Circonscription'] = df['Circonscription'].apply(lambda x: "1" if "Saint-Pierre-et-Miquelon" in x else x)

    def group_nuance(self):
        df = self.df

        nb_lines = df.shape[0]

        for i in range(nb_lines):
            if df.iloc[i]["Nuance"] in listes_gauche:
                df.loc[i,"Nuance"]='NFP'
            elif df.iloc[i]["Nuance"] in listes_centre:
                df.loc[i,"Nuance"]='ENS'
            elif df.iloc[i]["Nuance"] in listes_droite:
                df.loc[i,"Nuance"]='LR'
            elif df.iloc[i]["Nuance"] in listes_exdroite:
                df.loc[i,"Nuance"]='RN'
            elif df.iloc[i]["Nuance"] in listes_autres:
                df.loc[i,"Nuance"]='DIV'

        print("Dataframe ready", df["Nuance"].unique())
        return df
    
    def desistements(self):
        df = self.df_nuance
        return df


replacements = {
    'ZS': '975',
    'ZN': '988',
    'ZW': '986',
    'ZP': '987',
    'ZD': '974',
    'ZB': '972',
    'ZC': '973',
    'ZM': '976',
    'ZA': '971'
}

class PreprocessingJSON():
    def __init__(self, path):
        # Lire le fichier JSON comme du texte brut
        with open(path, 'r', encoding='utf-8') as file:
            self.data = file.read()
        
        # Remplacer les valeurs
        self.data_ready = self.replace_values(self.data, replacements)
        
        # Enregistrer les nouvelles données dans un fichier
        with open('france-circonscriptions-legislatives-2012.json', 'w', encoding='utf-8') as new_file:
            new_file.write(self.data_ready)

    def replace_values(self, text, replacements):
        # Remplacer les chaînes de caractères spécifiées
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text