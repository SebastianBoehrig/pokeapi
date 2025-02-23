import requests
from typing_extensions import TypedDict
from typing import List, Set, Union, Dict
from app.config import POKEAPI_BASE_URL, POKEAPI_POKEMON_URL, POKEAPI_SPECIES_URL, POKEAPI_TYPE_URL, HIGH_LIMIT
from glom import glom, Iter, Coalesce
from pprint import pprint


class PokemonListEntry(TypedDict):
    name: str
    url: str


class SpeciesSubtypes(TypedDict):
    default: str
    other: List[str]


class RawTypePokemon(TypedDict):
    slot: int
    pokemon: PokemonListEntry


class RawPokemonType(TypedDict):
    slot: int
    type: PokemonListEntry


class RawPokemon(TypedDict, total=False):
    name: str
    weight: int
    height: int
    types: list[RawPokemonType]
    sprites: Dict[str, Union[str, Dict[str, Dict[str, str]]]]


class SpriteLinks(TypedDict):
    default: str
    shiny: str


class Pokemon(TypedDict):
    name: str
    weight: int
    height: int
    types: set[str]
    img: SpriteLinks


class SpeciesVarieties(TypedDict):
    is_default: bool
    pokemon: PokemonListEntry


def api_online() -> bool:
    response: requests.Response = requests.get(POKEAPI_BASE_URL)
    if response.status_code != 200:
        return False
    return True


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

    species_obj: list[SpeciesVarieties] = response.json()['varieties']
    return glom(
        species_obj,
        {
            # this assumes that there can only be one default pokemon
            'default': (Iter().filter(lambda p: p['is_default']).first(), 'pokemon.name'),
            'other': (Iter().filter(lambda p: not p['is_default']).all(), ['pokemon.name']),
        },
        default=None,
    )


def get_single_pokemon(name: str) -> Pokemon | None:
    response: requests.Response = requests.get(f'{POKEAPI_POKEMON_URL}/{name}')  # TODO do .gets
    if response.status_code != 200:
        return None

    raw_pokemon: RawPokemon = response.json()
    return glom(
        raw_pokemon,
        {
            'name': 'name',
            'weight': 'weight',
            'height': 'height',
            'types': ('types', ['type.name'], set),
            'img': {
                'default': Coalesce(
                    'sprites.other.official-artwork.front_default', 'sprites.front_default', default=None, skip=None
                ),
                'shiny': Coalesce(
                    'sprites.other.official-artwork.front_shiny', 'sprites.front_shiny', default=None, skip=None
                ),
            },
        },
    )


def get_all_types() -> Set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    species_obj: List[PokemonListEntry] = response.json()['results']
    return {species['name'] for species in species_obj}


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


def get_pokemon_of_type(type: str) -> Set[str] | None:
    response: requests.Response = requests.get(f'{POKEAPI_TYPE_URL}/{type}/{HIGH_LIMIT}')
    if response.status_code != 200:
        return None

    pokemon_type_list: list[RawTypePokemon] = response.json()['pokemon']
    return {entry['pokemon']['name'] for entry in pokemon_type_list}


# 'palafin-zero'
# 'palafin-hero'

# 'ogerpon'
# 'ogerpon-wellspring-mask'
# 'ogerpon-hearthflame-mask'
# 'ogerpon-cornerstone-mask'

# 'burmy'

# 'charizard'

# 2 or 9
