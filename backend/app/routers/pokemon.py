from fastapi import APIRouter
import app.pokeapi_requests as pokeapi_requests
from app.pokeapi_requests import Pokemon, SpeciesSubtypes
from pprint import pprint

router: APIRouter = APIRouter(prefix='/pokemon', responses={404: {'description': 'Not found'}})


@router.get('/{name}', response_model=Pokemon)
def get_pokemon(name: str) -> Pokemon | None:
    pokemon: Pokemon | None = pokeapi_requests.get_single_pokemon(name)
    pprint(pokemon)
    return pokemon


@router.get('/species/{name}', response_model=list[Pokemon | None])
def get_all_types(name: str) -> list[Pokemon | None]:
    species_subtypes: SpeciesSubtypes | None = pokeapi_requests.get_pokemon_of_species(name)
    if species_subtypes is None:
        return []
    default: str | None = species_subtypes.get('default')
    result: list[Pokemon | None] = [pokeapi_requests.get_single_pokemon(default) if default else None]
    result.extend(pokeapi_requests.get_single_pokemon(name) for name in species_subtypes.get('other', {}))

    return result
