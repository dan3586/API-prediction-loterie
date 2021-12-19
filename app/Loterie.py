import pandas as pd
import numpy as np
import joblib
from random import seed
from random import randint
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from dateutil.parser import parse

data_dir = "/home/eisti/Documents/ING3/DevOps/Projet/euro_data.csv"
modele_path = "/home/eisti/Documents/ING3/DevOps/Projet/lotterie_model.sav"

def is_date(string, fuzzy=False):
    """
    Retourne si une chaine de caractère est une date ou non

    Paramètres : 

    string(str) : chaine de caractère à tester
    fuzzy(booléen) : ignore les caractères inconnus de la chaine si True

    Return :

    True si la chaine de caractère est une date, False sinon.
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def ajoutLigne(data,ligne):

    """
    Ajoute une donnée supplémentaire de même format que les données. 

    Paramètres : 
    
    data (Pandas DataFrame) : Jeu de données d'entrée.
    ligne (Liste) : Liste contenant les données à rajouter au format [date,N1,N2,N3,N4,N5,E1,E2,Winner,Gain] 

    Return :

    Retourne un nouveau dataframe ayant la données saisie
    """
    cles = ['Date','N1', 'N2', 'N3','N4', 'N5', 'E1', 'E2','Winner','Gain']
    if is_date(ligne[0]) == True:
        df = dict(zip(cles,ligne))
        data = data.append(df, ignore_index = True)
        return data
    else:
        print("Le premier élément de la saisie n'est pas une date")


def lecture(ligne=[], ajout = False):

    """
    Lecture du fichier de données, suppression des variables Date, Gain et Winner et création de la variable Result, définissant
    la classe d'une combinaison gagnante.

    Paramètres : 
    
    ligne (Liste) : Liste contenant les données à rajouter au format [date,N1,N2,N3,N4,N5,E1,E2,Winner,Gain]
    ajout (Booleen) : Si False lecture seule du fichier de données, si True lecture du fichier et enrichessement du fichier de données
    d'un nouveau tirage gagnant.

    Return :

    Retourne le dataframe du fichier de données (si ajout=False) ou le dataframe du fichier enrichi de la nouvelle donnée (si ajout=True)  
    """

    if ajout == False:
        data = pd.read_csv("euro_data.csv", sep=";")
        data = data.drop(columns=["Date","Gain","Winner"],axis=1)
        data['Result'] = 1
        return data
    else:
        data = pd.read_csv("euro_data.csv", sep=";")
        dataNew = ajoutLigne(data,ligne)
        if type(dataNew) == type(data):
            data = dataNew.drop(columns=["Date","Gain","Winner"],axis=1)
            data['Result'] = 1
            return data
        else:
            print("Le premier élément de la saisie n'est pas une date")

def lectureRetrain(data,ligne=[],index = False):

    """
    Création du jeu de données après ajout d'un nouveau tirage. 

    Paramètres : 

    data (pandas dataframe) : Jeu de données nouvellement crée.
    ligne (Liste) : Liste des informations du nouveau tirage.

    Return :

    Nouveau dataframe contenant la nouvelle donnée.
    """
    if index == False:
        data = pd.read_csv("euro_data.csv", sep=";")
        features = ['Date','N1','N2','N3','N4','N5','E1','E2','Winner','Gain']
        data = data[features]
        return data
    else:
        data = pd.read_csv("euro_data.csv", sep=";")
        features = ['Date','N1','N2','N3','N4','N5','E1','E2','Winner','Gain']
        data = data[features]
        data = ajoutLigne(data,ligne)
        return data


def generation(data):
    """
    Génère de faux tirages selon les conditions de choix des chiffres puis les ajoute au dataframe initial.

    Paramètres : 
    
    data (Pandas DataFrame) : Jeu de données d'entrée.

    Return :

    Retourne le dataframe auquel ont été ajouté les fausses combinaisons.
    """
    tab = []
    seed(42)
    for _ in range(8*data.shape[0]):
        for i in range(len(data.columns)):
            if (i == 0 or i == 1 or i == 2 or i == 3 or i == 4):
                tab.append(randint(1,50))
            elif (i== 5 or i == 6):
                tab.append(randint(1,12))
        tab.append(0)
        data = data.append(dict(zip(data.columns,tab)), ignore_index=True)
        tab = []
    if (data[data.duplicated() == False].shape[0] == data.shape[0]) == True:
        data = data
    return data

def modelePrevision(data:pd.DataFrame,sauv=False) -> (float,float):
    """
    Détermine la probabilité que la combinaison d'entrée soit gagnante et perdante.

    Paramètres : 
    
    data (Pandas DataFrame) : Jeu de données d'entrée.
    new_entries (tableau) : Tableau d'entiers correspondant à la combinaison à tester.

    Return :

    Retourne un tuple de réels dont la première valeur est la probabilité de gain et la seconde celle de perte.
    """

    ##PARTIE 1
    data = generation(data)

    ##PARTIE 2
    features = data.columns.drop('Result')
    X = data[features]
    y = data['Result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2,random_state=0)

    pipeline = Pipeline(steps=[
    ('classifieur', RandomForestClassifier(random_state=0, max_features='auto', n_estimators= 50, max_depth=8, criterion='gini'))
    ])

    RegLog = pipeline.fit(X_train,y_train)

    ##PARTIE 3

    if sauv==False:
        modele_path = os.getcwd()+ "/lotterie_model.sav"
        if os.path.isfile(modele_path):
            modele = joblib.load(modele_path)
        else:
            model_saved = "lotterie_model.sav"
            joblib.dump(RegLog, model_saved)
            modele = joblib.load(modele_path)

        return modele
    else:
       modele_path = os.getcwd()+ "/lotterie_model.sav"
       model_saved = "lotterie_model.sav"
       joblib.dump(RegLog, model_saved)
       modele = joblib.load(modele_path)
       return modele

data = lecture(data_dir)
modele = modelePrevision(data)

def generationCombinaisons(data):
    """
    Génération de tirages ayant une forte probabilité de gain.

    Paramètres : 
    
    data (Pandas DataFrame) : Jeu de données d'entrée.

    Return :

    Retourne un tirage ayant une forte probailité de gain.
    """
    data.drop(columns=['Result'])
    tab = []
    for i in range(len(data.columns)):
        if (i == 0 or i == 1 or i == 2 or i == 3 or i == 4):
            tab.append(randint(1,50))
        elif (i== 5 or i == 6):
            tab.append(randint(1,12))
    return tab

def prevision(modele,new_entries:np.array):

    """
    Prédiction de la probabilité qu'une combinaison soit gagnte et perdante

    Paramètres : 

    modele : sauvegarde du modèle utilisé lors de l'entrainement
    new_entries (Liste) : Liste des éléments de la nouvelle combinaison

    Return :

    Probabilité de perte et probabilité de gain
    """

    new_entries = np.array(new_entries).reshape(1,-1)
    proba_gain = modele.predict_proba(new_entries)

    return round(proba_gain[0][0],2), round(proba_gain[0][1],2)

def validationCombi(data):
    """
    Génération d'une combinaison ayant une forte probabilité de gain.

    Paramètres : 

    data (pandas dataframe) : Jeu de données d'étude

    Return :

    Tirage ayant une forte probabilité de gain.
    """

    for _ in range(10):
        entree = generationCombinaisons(data)
        if prevision(modele,entree)[1] >= .1:
            return entree