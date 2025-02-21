import requests
from typing import TypedDict, List, Set
from app.config import POKEAPI_BASE_URL, POKEAPI_POKEMON_URL, POKEAPI_SPECIES_URL, POKEAPI_TYPE_URL, HIGH_LIMIT
from glom import glom, Iter


class PokemonListEntry(TypedDict):
    name: str
    url: str


class Pokemon(TypedDict):
    default: str
    other: List[str]


class SpeciesSubtypes(TypedDict):
    name: str
    weight: int
    height: int


def api_online() -> bool:
    response: requests.Response = requests.get(POKEAPI_BASE_URL)
    if response.status_code != 200:
        return False
    return True  # TODO: Test


def get_all_pokemon() -> Set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_POKEMON_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None  # TODO: maybe abstract those 2 lines

    pokemon_obj: List[PokemonListEntry] = response.json()['results']
    return {pokemon['name'] for pokemon in pokemon_obj}


def get_all_pokemon_species() -> Set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_SPECIES_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    species_obj: List[PokemonListEntry] = response.json()['results']
    return {species['name'] for species in species_obj}


def get_pokemon_of_species(species: str) -> SpeciesSubtypes | None:
    response: requests.Response = requests.get(f'{POKEAPI_SPECIES_URL}/{species}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    species_obj = response.json()
    return glom(
        species_obj,
        {
            # this assumes that there can only be one first item
            'default': ('varieties', Iter().filter(lambda p: p['is_default']).first(), 'pokemon.name'),
            'other': ('varieties', Iter().filter(lambda p: not p['is_default']).all(), ['pokemon.name']),
        },
        default=None,
    )


def get_single_pokemon(name: str) -> Pokemon | None:
    response: requests.Response = requests.get(f'{POKEAPI_POKEMON_URL}/{name}')  # TODO: get all from .env
    if response.status_code != 200:
        return None

    full_pokemon: Pokemon = response.json()
    return glom(
        full_pokemon,
        {
            'name': 'name',
            'weight': 'weight',
            'height': 'height',
        },
    )


def get_all_types() -> Set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    species_obj: List[PokemonListEntry] = response.json()['results']
    return {species['name'] for species in species_obj}


def get_pokemon_of_type(type: str) -> Set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{type}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    full_type: Pokemon = response.json()
    return glom(full_type, ('pokemon', ['pokemon.name'], set))


# pprint(get_pokemon_of_type('water'))

# 'palafin-zero'
# 'palafin-hero'

# 'ogerpon'
# 'ogerpon-wellspring-mask'
# 'ogerpon-hearthflame-mask'
# 'ogerpon-cornerstone-mask'

# 'burmy'
