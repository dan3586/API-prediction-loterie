from fastapi import FastAPI
import predict

NAME = "Euro-Prevision"
VERSION = "1.0"

app = FastAPI(
    title = NAME,
    version = VERSION
)

app.include_router(predict.router)
