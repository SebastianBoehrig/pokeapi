from fastapi import FastAPI
from app.routers.initial import router as initial_router
from app.routers.pokemon import router as pokemon_router
from app.pokeapi_requests import api_online
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root() -> dict[str, str]:
    pokeapi_state: str = 'Running' if api_online() else 'Offline'
    return {'description': f'Backend up and running, pokeapi is {pokeapi_state}'}


app.include_router(initial_router)
app.include_router(pokemon_router)
