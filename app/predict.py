from fastapi.routing import APIRouter
from pydantic import BaseModel
from Loterie import *

TAG = "predict"
data_dir = os.getcwd() + "/euro_data.csv"
router = APIRouter()

class Tirage(BaseModel):
    """
    Classe des numéros d'un tirage.
    """
    N1: int
    N2: int
    N3: int
    N4: int
    N5: int
    E1: int
    E2: int


class Combinaison(BaseModel):
    """
    Classe du format d'une donnée.
    """
    Date : str
    N1: int
    N2: int
    N3: int
    N4: int
    N5: int
    E1: int
    E2: int
    Winner : int
    Gain : int



@router.post("/api/predict", tags=[TAG])
async def create_tirage(tirage: Tirage):
    """
    Requête permettant d'initialiser un tirage et de prédire sa probabilité de gain et de perte.

    Paramètres : 

    tirage (Liste) : Ensemble des numéros d'un tirage telle que les numéros N1 à N5 aient des valeurs de 1 à 50, et les numéros E1 et E2 aient des valeurs entre 1 et 12.

    Return :

    Probabilité de perte et de gain.
    """
    tirage = [tirage.N1, tirage.N2, tirage.N3, tirage.N4, tirage.N5, tirage.E1, tirage.E2]
    if (0 < tirage[0] and tirage[0] <= 52) and (0 < tirage[1]and tirage[1] <= 52) and (0 < tirage[2] and tirage[2] <= 52) and (0 < tirage[3] and tirage[3] <= 52) and (0 < tirage[4] and tirage[4]<= 52) and (0 < tirage[5] and tirage[5] <= 12) and (0 < tirage[6] and tirage[6] <= 12):
        data = lecture(data_dir)
        modele = modelePrevision(data)
        result = prevision(modele,tirage)

        return {"Probabilité de perte : ": result[0], "Probabilité de gain : ": result[1]}
    else:
        return{"L'un des numéros saisie ne satisfait pas les normes."}


@router.get("/api/predict", tags=[TAG])
async def generate_combinations():
    """
    Requête permettant de générer une combinaison à fort taux de gain.

    Return :

    Combinaison à fort taux de gain.
    """
    data = lecture(data_dir)
    combi = validationCombi(data)
    return {"Tirage a fort taux de gain : ": combi}


@router.put("/api/enrich/model", tags=[TAG])
async def enrich_Model(combinaison: Combinaison):
    """
    Requête permettant d'ajouter une nouvelle donnée dans le dataset initial.

    Paramètres : 

    combinaison (Liste) : Liste d'éléments au format des données initiales

    Return :

    Jeu de données auquel a été ajouté les nouvelles informations si la date correcte. Sinon message d'erreur.
    """
    combinaison = [combinaison.Date, combinaison.N1,combinaison.N2,combinaison.N3,combinaison.N4,combinaison.N5,combinaison.E1,combinaison.E2,combinaison.Winner,combinaison.Gain]
    data = lecture(data_dir)
    dataNew = lecture(ligne=combinaison,ajout = True)
    if (0 < combinaison[1] and combinaison[1] <= 52) and (0 < combinaison[2]and combinaison[2] <= 52) and (0 < combinaison[3] and combinaison[3] <= 52) and (0 < combinaison[4] and combinaison[4] <= 52) and (0 < combinaison[5] and combinaison[5]<= 52) and (0 < combinaison[6] and combinaison[6] <= 12) and (0 < combinaison[7] and combinaison[7] <= 12) and combinaison[8] >= 0 and combinaison[9] > 0:
        if dataNew is None:
            return {"Le premier élément de la saisie n'est pas une date"} 
        else:
            df = lectureRetrain(data,combinaison,True)
            df.to_csv("euro_data.csv",sep=";",index=False)
            return {"Ajout terminé. Passage de {} lignes à {} lignes !".format(data.shape[0], dataNew.shape[0])}
    else:
        return{"L'un des numéros saisie ne satisfait pas les normes."}

@router.post("/api/model/retrain", tags=[TAG])
async def retrain_Model(tirage: Tirage):
    """
    Requête permettant de réentrainer le modèle après l'ajout de nouvelles données

    Paramètres : 

    tirage (Liste) : Ensemble des numéros d'un tirage

    Return :

    Probabilité de perte et de gain selon le nouveaux modèle.
    """
    tirage = [tirage.N1, tirage.N2, tirage.N3, tirage.N4, tirage.N5, tirage.E1, tirage.E2]
    if (0 < tirage[0] and tirage[0] <= 52) and (0 < tirage[1]and tirage[1] <= 52) and (0 < tirage[2] and tirage[2] <= 52) and (0 < tirage[3] and tirage[3] <= 52) and (0 < tirage[4] and tirage[4]<= 52) and (0 < tirage[5] and tirage[5] <= 12) and (0 < tirage[6] and tirage[6] <= 12):
        data = lecture(data_dir)
        modele = modelePrevision(data,sauv=True)
        result = prevision(modele,tirage)
        return {"Probabilité de perte : ": result[0], "Probabilité de gain : ": result[1]}
    else:
        return{"L'un des numéros saisie ne satisfait pas les normes."}


@router.get("/api/model", tags=[TAG])
async def get_Model_Infos():
    """
    Requête permettant d'avoir les informations du modèle.

    Return :

    Informations du modèle.
    """
    metrique = "Accuracy_score"
    algo = "RandomForestClassifier"
    params = "RandomForestClassifier(max_depth=8, n_estimators=50, random_state=0)"
    return {"Métrique de précision : {}  algorithme : {}  paramètres : {}".format(metrique,algo,params)}
