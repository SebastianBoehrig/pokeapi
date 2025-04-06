import asyncio

import httpx

from app.logic.helpers import extract_img_from_raw_pokemon_sprites
from app.pokeapi_requests import get_pokemon, get_type
from app.types import PokemonImg, PokemonPrimitive, RawPokemon, RawType


async def get_pokemon_primitive_of_type(type_name: str, client: httpx.AsyncClient) -> list[PokemonPrimitive]:
    type: RawType = await get_type(type_name, client)

    pokemon_name_list: list[str] = []
    for raw_type_pokemon in type.get('pokemon', {}):
        pokemon_name: str | None = raw_type_pokemon.get('pokemon', {}).get('name')
        if pokemon_name:
            pokemon_name_list.append(pokemon_name)

    raw_pokemon_task_list: list[asyncio.Task[RawPokemon]] = []
    result: list[PokemonPrimitive] = []

    async with asyncio.TaskGroup() as tg:
        for name in pokemon_name_list:
            task: asyncio.Task[RawPokemon] = tg.create_task(get_pokemon(name, client))
            raw_pokemon_task_list.append(task)

    for pokemon_task in raw_pokemon_task_list:
        pokemonImg: PokemonImg = extract_img_from_raw_pokemon_sprites(pokemon_task.result().get('sprites', {}))
        result.append({'name': pokemon_task.result().get('name', ''), 'img': pokemonImg.get('default')})
    return result
