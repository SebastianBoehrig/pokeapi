from fastapi import APIRouter, Request

from app.logic.get_types import get_types
from app.types import TypesType

router: APIRouter = APIRouter(prefix='/initial', responses={404: {'description': 'Not found'}})


@router.get('/types', response_model=list[TypesType])
async def get_types_router(request: Request) -> list[TypesType]:
    return await get_types(request.app.state.client)
