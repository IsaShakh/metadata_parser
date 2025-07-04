
from fastapi import FastAPI
from app.api import suip_data

app = FastAPI()

app.include_router(suip_data.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "parser is running"}
