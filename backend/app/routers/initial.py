from fastapi import APIRouter
from typing import Set
import app.pokeapi_requests as pokeapi_requests
from pprint import pprint

router: APIRouter = APIRouter(prefix='/initial', responses={404: {'description': 'Not found'}})


@router.get('/types', response_model=Set[str] | None)
def get_all_types() -> Set[str] | None:
    a: Set[str] | None = pokeapi_requests.get_all_types()
    pprint(a)
    return a
