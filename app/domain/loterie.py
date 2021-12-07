import os
import joblib
import pandas as pd
import numpy as np
from random import seed
from random import randint

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import balanced_accuracy_score

data_dir = "../datasource/EuroMillions_numbers.csv"

def makePrevision(new_entries):

    ##PARTIE 1
    data = pd.read_csv("../datasource/EuroMillions_numbers.csv", sep=";")
    data = data.drop(columns=["Date","Gain","Winner"],axis=1)
    data['Result'] = 1

    ##PARTIE 2
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

    ##PARTIE 3
    features = data.columns.drop('Result')
    X = data[features]
    y = data['Result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2,random_state=0)

    pipeline = Pipeline(steps=[
    ('classifieur', RandomForestClassifier())
    ])

    RegLog = pipeline.fit(X_train,y_train)
    predict = RegLog.predict(X_test)

    ##PARTIE 4

    modele_path = "../datasource/lotterie_model.sav"
    if os.path.isfile(modele_path):
        modele = joblib.load(modele_path)
    else:
        model_saved = "lotterie_model.sav"
        joblib.dump(RegLog, model_saved)
        modele = joblib.load(modele_path)

      ##PARTIE 5
    
    new_entries = np.array(new_entries).reshape(1,-1)
    proba = modele.predict_proba(new_entries)
    
    return proba[0], proba[1]