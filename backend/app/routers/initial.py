from fastapi import APIRouter
from typing import Set
import pokeapi_requests
from pprint import pprint

router: APIRouter = APIRouter(prefix='/initial', responses={404: {'description': 'Not found'}})

@router.get('/types')
def get_all_types() -> Set[str] | None:
    a=pokeapi_requests.get_all_types()
    pprint(a)
    return a