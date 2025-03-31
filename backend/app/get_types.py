import httpx
from typing_extensions import TypedDict
from glom import Coalesce, glom
from app.pokeapi_requests import RawType, get_all_types, get_type
import asyncio
import time


class TypesType(TypedDict):
    name: str
    img: str


async def get_types(client: httpx.AsyncClient) -> list[TypesType]:
    type_list: list[str] = [species['name'] for species in get_all_types().get('results', {})]
    raw_type_task_list: list[RawType] = []
    result: list[TypesType] = []

    mid = time.time()
    async with asyncio.TaskGroup() as tg:
        for type in type_list:
            raw_type: RawType = tg.create_task(get_type(type, client))
            raw_type_task_list.append(raw_type)
    mid2 = time.time()

    for raw_type in raw_type_task_list:
        img: str | None = glom(
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
            result.append({'name': raw_type.result()['name'], 'img': img})

    print(f'took {mid2 - mid}s for requests part')
    return result
