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
        df.loc[df["Liste des candidats"] == "M. Sébastien GUERAUD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Maxime MEYER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Christian JOLIE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Charline LIOTIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Aline JEUDI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Benoit GAUVAN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Dominique BLANC", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Pascale BOYER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Sébastien FINE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Philippe PRADAL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Christine BREYTON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Léon THEBAULT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Samuel DEGUARA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Richard BOUIGUE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jimmy BESSAIH", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Mohamed LAQHILA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Claire PITOLLAT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Allan POPELARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Lionel ROYER-PERREAUT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Alexandre BEDDOCK", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Ludivine DAOUDI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pierre MOURARET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Thomas DUPONT-FEDERICI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Noé GAUCHARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Valérie RUEDA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Carole BALLU", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Gwenhaël FRANÇOIS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anne-Laure BABAULT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Philippe ARDOUIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anne BRACHET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Hugo LEFELLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Gabriel BEHAGHEL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Amandine DEWAELE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Benoît BORDAT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Fadila KHATTABI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Valérie JACQ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jérôme FLACHE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jérémy DAUPHIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Antoine RAVARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Cyril JOBIC", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Clément TONON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Michel DELPON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Pierre CUBERTAFON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Benoît VUILLEMIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Virginie DAYET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Philippe GAUTIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Nicolas MICHEL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Lander MARCHIONNI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Christine LE BONTÉ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pierre-Yves JOURDAIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-François BRIDET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Nadia FAVERIS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pierre SMOLARZ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Gladys GRELAUD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Sébastien MIOSSEC", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Thomas LE BON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Erwan CROUAN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sylvie JOUART", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Valérie ROUVERAND", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Christian BAUME", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Aurélien COLSON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sylvie ESPAGNOLLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Dominique FAURE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Monique IBORRA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Elisabeth TOUTUT-PICARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pascal LEVIEUX", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pascal BOURGOIS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pascal LAVERGNE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Stéphane SENCE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marylène FAURE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Corinne MARTINEZ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Patricia MIRALLES", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Laurence CRISTOL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-François ELIAOU", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Patrick VIGNAL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anne PATAULT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Gilles RENAULT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Elsa LAFAYE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Nicolas GUIVARC'H", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Eloïse GONZALEZ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Clément SAPIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Christelle GOBERT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sandra BARBIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Fabienne COLBOC", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marina COCCIA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marjolaine MEYNIER-MILLEFERT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Louve CARRIÈRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Émilie CHALAS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Charles COLAS-ROY", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Dominique DICHARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Caroline ABADIE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Élodie JACQUIER-LAFORGE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Anthony BRONDEL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Evelyne TERNANT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Hervé PRAT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marie-Laure LAFARGUE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Marc LESPADE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Noé PETIT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Quentin BATAILLON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Vincent BONY", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Bernard PAEMELAERE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Celline GACON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Andre Antoine Célestin CHAPAVEIRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Véronique MAHÉ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Audrey DUFEU", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Hélène MACON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Ghislaine KOUNOWSKI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Caroline JANVIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Clément VERDE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anne-Laure BOUTET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Christophe LAVIALLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Paul VO VAN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Marie LENZI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Patrick ALEXANDRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Charlyne BOUVET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sylvie GABIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Gaëlle VEROVE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Evelyne BOURGOIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Stéphane PIROUELLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Benjamin LAMBERT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Vincent SAULNIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Grégory BOISSEAU", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Stéphanie LEFOULON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Philippe GUILLEMARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Barbara BERTOZZI-BIÉVELOT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anne GALLO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Jade BENIGUEL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marie Madeleine DORÉ-LUCAS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Michel BAUDRY", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Vincent FELIX", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Victorien NICOLAS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Charlotte LEDUC", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Brigitte VAÎSSE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Brice LARÈPE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sandra GERMAIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Leslie MORTREUX", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Ingrid BRULANT-FORTIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Damien LACROIX", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pierrick COLPIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Ophélie DELNESTE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Célia PEREIRA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Baptiste DE FRESSE DE MONVAL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Patricia CHAPELOTTE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Lori HELLOCO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Alexandre COUSIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Pierre PONT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Valérie GOLÉO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Yves LALANNE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Julien BRUNEL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Florence LASSERRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Bernard SEMPASTOUS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Benoit MOURNET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Laurence GAYTE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Raphaële KRATTINGER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Nadia EL HAJJAJI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Florence CLAUDEPIERRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Florence Janine Jacqueline PERRIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Dominique DESPRAS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Abdel YOUSFI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sarah TANZILLI", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Dominique DESPRAS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Henri SOUMIREU-LARTIGUE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Luc DELPEUCH", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Richard BENINGER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Anthony VADOT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Louis MARGUERITTE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Ghislaine BONNET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Samuel CHEVALLIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sylvie CASENAVE-PÉRÉ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Christophe ROUILLON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Christel GRANATA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Pascale MARTINOT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anaïs GOMERO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Anne-Valérie DUVAL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Guillaume TATU", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Gérard VEZ", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Dominique LACHENAL", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean-Baptiste BAUD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Alain ROUBIAN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Vincent DECORDE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Laurent BONNATERRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Jean DELALANDRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Florence MARTIN PÉRÉON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Nour BENAÏSSA WATBOT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Albane BRANLANT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Margot LAPEYRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pierre VERDIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Julien LASSALLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Eric HABOUZIT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sylvie VIALA", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Adrien MORENAS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Lucie ETONNO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Nicolas HELARY", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Pierre-Hugues FOURAGE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Gisèle JEAN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Yves TROUSSELLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marie-Eve TAYOT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Philippe VEYSSIERE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marie-Eve BELORGEY", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Sébastien MEURANT", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Sophie CHARLES", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Gilles LE GENDRE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Théa FOUDRINIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Laura VALLÉE-HANS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Mathieu GARNIER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Laurie CAENBERGS", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Régis SARAZIN", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Michèle PEYRON", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Thomas CIANO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Bruno MILLIENNE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Naïma SIFER", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Alexis IZARD", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Amadou DEME", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Hella KRIBI - ROMDHANE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Marie GUÉVENOUX", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Raquel GARRIDO", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Frédéric DESCROZAILLE", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Guillaume VUILLETET", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "Mme Cécile RILHAC", "Elu(e)"] = -1
        df.loc[df["Liste des candidats"] == "M. Dominique DA SILVA", "Elu(e)"] = -1

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