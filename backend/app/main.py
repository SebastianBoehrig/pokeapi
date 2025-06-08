from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

from app.pokeapi_requests import api_online
from app.routers.initial import router as initial_router
from app.routers.pokemon import router as pokemon_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    with httpx.Client() as client:
        async with httpx.AsyncClient() as async_client:
            app.state.client = client
            app.state.async_client = async_client
            yield


app: FastAPI = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root() -> dict[str, str]:
    pokeapi_state: str = 'Running' if api_online(app.state.client) else 'Offline'
    return {'description': f'Backend up and running, pokeapi is {pokeapi_state}'}


app.include_router(initial_router)
app.include_router(pokemon_router)
