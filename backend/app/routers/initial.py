from fastapi import APIRouter
from typing_extensions import TypedDict
import app.pokeapi_requests as pokeapi_requests

router: APIRouter = APIRouter(prefix='/initial', responses={404: {'description': 'Not found'}})


class TypesType(TypedDict):
    name: str
    img: str


@router.get('/types', response_model=list[TypesType])
def get_all_types() -> list[TypesType]:
    type_list: list[str] | None = pokeapi_requests.get_all_types()
    if not type_list:
        return []

    result: list[TypesType] = []
    for type in type_list:
        img: str | None = pokeapi_requests.get_img_of_type(type)
        if img:
            result.append({'name': type, 'img': img})
    return result
