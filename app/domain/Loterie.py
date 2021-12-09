import pandas as pd
import numpy as np
import glob
import joblib
from random import seed
from random import randint
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

data_dir = "/home/eisti/Documents/ING3/DevOps/Projet/euro_data.csv"

def lecture(data_dir):
    data = pd.read_csv("euro_data.csv", sep=";")
    data = data.drop(columns=["Date","Gain","Winner"],axis=1)
    data['Result'] = 1
    return data

def generation(data):
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

def modelePrevision(data):


    ##PARTIE 2
    data = generation(data)

    ##PARTIE 3
    features = data.columns.drop('Result')
    X = data[features]
    y = data['Result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2,random_state=0)

    pipeline = Pipeline(steps=[
    ('classifieur', RandomForestClassifier(random_state=0, max_features='auto', n_estimators= 50, max_depth=8, criterion='gini'))
    ])

    RegLog = pipeline.fit(X_train,y_train)

    ##PARTIE 4

    modele_path = os.getcwd()+ "/lotterie_model.sav"
    if os.path.isfile(modele_path):
        modele = joblib.load(modele_path)
    else:
        model_saved = "lotterie_model.sav"
        joblib.dump(RegLog, model_saved)
        modele = joblib.load(modele_path)

    return modele

data = lecture(data_dir)
modele = modelePrevision(data)

def prevision(modele,new_entries):

    new_entries = np.array(new_entries).reshape(1,-1)
    proba_gain = modele.predict_proba(new_entries)

    return round(proba_gain[0][0],2), round(proba_gain[0][1],2)

def generationCombinaisons(data):

    data.drop(columns=['Result'])
    tab = []
    for i in range(len(data.columns)):
        if (i == 0 or i == 1 or i == 2 or i == 3 or i == 4):
            tab.append(randint(1,50))
        elif (i== 5 or i == 6):
            tab.append(randint(1,12))
    return tab

def validationCombi(data):

    for _ in range(10):
        entree = generationCombinaisons(data)
        if prevision(modele,entree)[1] >= .1:
            return entree

print(validationCombi(data))
entree = [45,8,15,33,29,12,12]
print(prevision(modele,entree))
