import httpx
from fastapi import HTTPException

from app.config import HIGH_LIMIT, POKEAPI_BASE_URL, POKEAPI_POKEMON_URL, POKEAPI_SPECIES_URL, POKEAPI_TYPE_URL
from app.types import EvolutionChain, PokemonList, PokemonSpecies, RawPokemon, RawType


def api_online(client: httpx.Client) -> bool:
    response: httpx.Response = client.get(POKEAPI_BASE_URL)
    if response.status_code != httpx.codes.OK:
        return False
    return True


async def get_pokemon_species(speciesName: str, client: httpx.AsyncClient) -> PokemonSpecies:
    response: httpx.Response = await client.get(f'{POKEAPI_SPECIES_URL}/{speciesName}/{HIGH_LIMIT}')
    if response.status_code != httpx.codes.OK:
        raise HTTPException(status_code=404, detail=f'{speciesName} not found, (get_pokemon_species)')
    return response.json()


async def get_pokemon(name: str, client: httpx.AsyncClient) -> RawPokemon:
    response: httpx.Response = await client.get(f'{POKEAPI_POKEMON_URL}/{name}')
    if response.status_code != httpx.codes.OK:
        raise HTTPException(status_code=404, detail=f'{name} not found, (get_pokemon)')
    return response.json()


async def get_evolution_chain(url: str, client: httpx.AsyncClient) -> EvolutionChain:
    response: httpx.Response = await client.get(url)
    if response.status_code != httpx.codes.OK:
        raise HTTPException(status_code=404, detail=f'evolution not found: {url}, (get_evolution_chain)')
    chain: EvolutionChain | None = response.json().get('chain')
    if not chain:
        raise HTTPException(status_code=404, detail=f'evolution chain not found: {url}, (get_evolution_chain)')
    return chain


async def get_type(type: str, client: httpx.AsyncClient) -> RawType:
    response: httpx.Response = await client.get(f'{POKEAPI_TYPE_URL}/{type}/{HIGH_LIMIT}')
    if response.status_code != httpx.codes.OK:
        raise HTTPException(status_code=404, detail=f'{type} not found, (get_type)')
    return response.json()


async def get_all_types(client: httpx.AsyncClient) -> PokemonList:
    response: httpx.Response = await client.get(f'{POKEAPI_TYPE_URL}/{HIGH_LIMIT}')
    if response.status_code != httpx.codes.OK:
        raise HTTPException(status_code=404, detail='pokemon types list not found, (get_all_types)')
    return response.json()


def get_all_pokemon_species(client: httpx.AsyncClient) -> PokemonList:
    # TODO: maybe a optimization for a dropdown for searching
    response: httpx.Response = client.get(f'{POKEAPI_SPECIES_URL}/{HIGH_LIMIT}')
    if response.status_code != httpx.codes.OK:
        raise HTTPException(status_code=404, detail='pokemon species list not found, (get_all_pokemon_species)')
    return response.json()
