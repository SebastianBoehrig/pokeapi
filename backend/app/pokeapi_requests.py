from __future__ import annotations
import requests
from typing_extensions import TypedDict
from typing import Union, Dict
from app.config import POKEAPI_BASE_URL, POKEAPI_POKEMON_URL, POKEAPI_SPECIES_URL, POKEAPI_TYPE_URL, HIGH_LIMIT
from glom import glom, Coalesce
from fastapi import HTTPException


# TODO: replace NOne checks with error 500
class PokemonListEntry(TypedDict):
    name: str
    url: str


class RawPokemonType(TypedDict):
    slot: int
    type: PokemonListEntry


class SpriteLinks(TypedDict):
    default: str
    shiny: str


class Pokemon(TypedDict):
    name: str
    weight: int
    height: int
    types: set[str]
    img: SpriteLinks


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
    sprites: Dict[str, Dict[str, Dict[str, str]]]


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


def get_pokemon_of_type(type: str) -> RawType:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{type}/{HIGH_LIMIT}')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'{type} not found, (get_pokemon_of_type)')
    return response.json()


def get_evolution_chain(url: str) -> EvolutionChain:
    response: requests.Response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f'evolution not found: {url}, (get_evolution_chain)')
    chain: EvolutionChain | None = response.json().get('chain')
    if not chain:
        raise HTTPException(status_code=404, detail=f'evolution chain not found: {url}, (get_evolution_chain)')
    return chain


######


def get_all_pokemon() -> set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_POKEMON_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None  # TODO: maybe a optimization for a dropdown for searching

    pokemon_obj: list[PokemonListEntry] = response.json()['results']
    return {pokemon['name'] for pokemon in pokemon_obj}


def get_all_pokemon_species() -> set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_SPECIES_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None  # TODO: do i need this?

    species_obj: list[PokemonListEntry] = response.json()['results']
    return {species['name'] for species in species_obj}


def get_all_types() -> list[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    species_obj: list[PokemonListEntry] = response.json()['results']
    return [species['name'] for species in species_obj]


def get_img_of_type(type: str) -> str | None:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{type}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    return glom(
        response.json(),
        (
            'sprites',
            Coalesce(
                'generation-ix.scarlet-violet.name_icon', 'generation-iv.platinum.name_icon', default=None, skip=None
            ),
        ),
    )


# 'palafin-zero'
# 'palafin-hero'

# 'ogerpon'
# 'ogerpon-wellspring-mask'
# 'ogerpon-hearthflame-mask'
# 'ogerpon-cornerstone-mask'

# 'burmy'

# 'charizard'

# 'eternatus' has ??? type, but not in api
