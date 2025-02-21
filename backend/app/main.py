from fastapi import FastAPI
from typing import Dict
from app.routers.initial import router as initial_router
from app.pokeapi_requests import api_online

app: FastAPI = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    pokeapi_state: str = "Running" if api_online() else "Offline"
    return {"description": f"Backend up and running, pokeapi is {pokeapi_state}"}

app.include_router(initial_router)
