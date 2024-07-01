import pandas as pd
import json

listes_gauche = ['UG', 'EXG', 'COM', 'FI', 'SOC', 'RDG', 'VEC', 'DVG', 'ECO']
listes_centre = ['REN', 'MDM', 'HOR', 'ENS', 'DVC', 'UDI']
listes_droite = ['LR', 'DSV', 'DVD']
listes_exdroite = ['RN', 'EXD', 'UXD', 'REC']
listes_autres = ['DIV', 'REG']

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

class PreprocessingCSV():
    def __init__(self, path):
        df = pd.read_csv(path).drop(columns=["% Inscrits"])
        df["% Exprimés"] = df["% Exprimés"].str.replace(',', '.').astype(float)
        df.loc[df["Elu(e)"] == "OUI", "Elu(e)"] = 1
        df.loc[df["Elu(e)"] == "QUALIF T2", "Elu(e)"] = 0
        df.loc[df["Elu(e)"] == "NON", "Elu(e)"] = -1
        df["Voix"] = df["Voix"].str.replace('\u202f', '', regex=True).astype(int)
        self.df = df
        self.df_ready = self.group_nuance()

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
    
class PreprocessingJSON():
    def __init__(self, path):
        file = open(path)
        self.data = json.load(file)
        self.data_ready = self.replace_values(self.data, replacements)
        new_file = open('france-circonscriptions-legislatives-2012.json', 'w', encoding='utf-8')
        json.dump(self.data_ready, new_file, ensure_ascii=False, indent=4)

    def replace_values(self, obj, replacements):
        if isinstance(obj, dict):
            for key in obj:
                if isinstance(obj[key], str):
                    for old, new in replacements.items():
                        obj[key] = obj[key].replace(old, new)
        elif isinstance(obj, list):
            for i in range(len(obj)):
                if isinstance(obj[i], str):
                    for old, new in replacements.items():
                        obj[i] = obj[i].replace(old, new)
        return obj