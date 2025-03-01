from __future__ import annotations
import requests
from typing_extensions import TypedDict
from typing import Union, Dict
from app.config import POKEAPI_BASE_URL, POKEAPI_POKEMON_URL, POKEAPI_SPECIES_URL, POKEAPI_TYPE_URL, HIGH_LIMIT
from fastapi import HTTPException


class PokemonListEntry(TypedDict):
    name: str
    url: str


class RawPokemonType(TypedDict):
    slot: int
    type: PokemonListEntry


class EvolutionChain(TypedDict):
    evolves_to: list['EvolutionChain']
    species: PokemonListEntry


class Varieties(TypedDict):
    is_default: bool
    pokemon: PokemonListEntry


class PokemonSpecies(TypedDict, total=False):
    evolution_chain: Dict[str, str]  # only url
    varieties: list[Varieties]


class RawPokemon(TypedDict, total=False):
    name: str
    weight: int
    height: int
    species: PokemonListEntry
    sprites: Dict[str, Union[str, Dict[str, Dict[str, str]]]]
    types: list[RawPokemonType]


class RawTypePokemon(TypedDict):
    slot: int
    pokemon: PokemonListEntry


class RawType(TypedDict, total=False):
    pokemon: list[RawTypePokemon]
    sprites: dict[str, dict[str, dict[str, str]]]


class PokemonList:
    results: list[PokemonListEntry]


def api_online() -> bool:
    response: requests.Response = requests.get(POKEAPI_BASE_URL)
    if response.status_code != 200:
        return False
    return True


def get_pokemon_species(speciesName: str) -> PokemonSpecies:
    response: requests.Response = requests.get(f'{POKEAPI_SPECIES_URL}/{speciesName}/{HIGH_LIMIT}')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'{speciesName} not found, (get_pokemon_species)')
    return response.json()


def get_pokemon(name: str) -> RawPokemon:
    response: requests.Response = requests.get(f'{POKEAPI_POKEMON_URL}/{name}')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'{name} not found, (get_pokemon)')
    return response.json()


def get_type(type: str) -> RawType:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{type}/{HIGH_LIMIT}')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'{type} not found, (get_type)')
    return response.json()


def get_evolution_chain(url: str) -> EvolutionChain:
    response: requests.Response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'evolution not found: {url}, (get_evolution_chain)')
    chain: EvolutionChain | None = response.json().get('chain')
    if not chain:
        raise HTTPException(status_code=404, detail=f'evolution chain not found: {url}, (get_evolution_chain)')
    return chain


def get_all_types() -> PokemonList:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail='pokemon species list not found, (get_all_types)')
    return response.json()


def get_all_pokemon_species() -> PokemonList:
    # TODO: maybe a optimization for a dropdown for searching
    response: requests.Response = requests.get(f'{POKEAPI_SPECIES_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail='pokemon species list not found, (get_all_pokemon_species)')

    return response.json()
