import asyncio

import httpx
from glom import Coalesce, glom # type: ignore

from app.pokeapi_requests import PokemonList, RawType, get_all_types, get_type
from app.types import TypesType


async def get_types(client: httpx.AsyncClient) -> list[TypesType]:
    pokemon_list: PokemonList = await get_all_types(client)
    type_list: list[str] = [species.get('name') for species in pokemon_list.get('results', {})]
    raw_type_task_list: list[asyncio.Task[RawType]] = []
    result: list[TypesType] = []

    async with asyncio.TaskGroup() as tg:
        for type in type_list:
            task: asyncio.Task[RawType] = tg.create_task(get_type(type, client))
            raw_type_task_list.append(task)

    for raw_type in raw_type_task_list:
        img: str | None = glom( # type: ignore
            raw_type.result(),
            (
                'sprites',
                Coalesce(
                    'generation-ix.scarlet-violet.name_icon',
                    'generation-iv.platinum.name_icon',
                    default=None,
                    skip=None,
                ),
            ),
        )
        if img:
            result.append({'name': raw_type.result().get('name', ''), 'img': img})
    return result
