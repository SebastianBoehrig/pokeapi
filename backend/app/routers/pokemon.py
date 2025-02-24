from fastapi import APIRouter
from app.logic import (
    PokemonDetail,
    PokemonPrimitive,
    get_pokemon_primitive,
    get_pokemon_detail,
    get_pokemon_primitive_of_type,
)

router: APIRouter = APIRouter(prefix='/pokemon', responses={404: {'description': 'Not found'}})


@router.get('/primitives/{name}', response_model=PokemonPrimitive)
def get_pokemon_primitive_route(name: str) -> PokemonPrimitive:
    return get_pokemon_primitive(name)


@router.get('/detail/{name}', response_model=PokemonDetail)
def get_pokemon_detail_route(name: str) -> PokemonDetail:
    return get_pokemon_detail(name)


@router.get('/type/{type}', response_model=list[PokemonPrimitive])
def get_pokemon_primitive_of_type_route(type: str) -> list[PokemonPrimitive]:
    return get_pokemon_primitive_of_type(type)  # TODO: async calls !!!!!!!!!!!!!!
