from fastapi import FastAPI

from src.api.routes import shifter

app: FastAPI = FastAPI()  # uvicorn main:app --reload

app.include_router(shifter.router, prefix='/api/v1')
