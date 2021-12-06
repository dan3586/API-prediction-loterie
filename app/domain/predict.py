from fastapi.routing import APIRouter
from pydantic import BaseModel

TAG = "predict"
router = APIRouter()

class Tirage(BaseModel):
    N1: int
    N2: int
    N3: int
    N4: int
    N5: int
    E1: int
    E2: int


@router.post("/api/predict", tags=[TAG])
async def create_tirage(tirage: Tirage):
    return {"tirage": tirage}

@router.get("/api/generate/predict", tags=[TAG])
async def generate_combinations():
    return {"tirage": "Tirage"}

@router.get("/api/model", tags=[TAG])
async def get_Model_Infos():
    return {"model": "Model"}

@router.put("/api/enrich/model", tags=[TAG])
async def enrich_Model(tirage: Tirage):
    return {"tirage": tirage}

@router.post("/api/model/retrain", tags=[TAG])
async def retrain_Model():
    return {"tirage": "tirage"}
