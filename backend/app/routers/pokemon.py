from fastapi import APIRouter, Request

from app.logic.get_pokemon_detail import get_pokemon_detail
from app.logic.get_pokemon_primitive import get_pokemon_primitive
from app.logic.get_pokemon_primitive_of_type import get_pokemon_primitive_of_type
from app.types import PokemonDetail, PokemonPrimitive

router: APIRouter = APIRouter(prefix='/pokemon', responses={404: {'description': 'Not found'}})


@router.get('/primitives/{name}', response_model=PokemonPrimitive)
async def get_pokemon_primitive_route(name: str, request: Request) -> PokemonPrimitive:
    return await get_pokemon_primitive(name, request.app.state.client)


@router.get('/detail/{name}', response_model=PokemonDetail)
async def get_pokemon_detail_route(name: str, request: Request) -> PokemonDetail:
    return await get_pokemon_detail(name, request.app.state.client)


@router.get('/type/{type}', response_model=list[PokemonPrimitive])
async def get_pokemon_primitive_of_type_route(type: str, request: Request) -> list[PokemonPrimitive]:
    return await get_pokemon_primitive_of_type(type, request.app.state.client)
