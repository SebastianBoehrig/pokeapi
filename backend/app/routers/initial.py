from fastapi import APIRouter, Request

import app.get_types as get_types

router: APIRouter = APIRouter(prefix='/initial', responses={404: {'description': 'Not found'}})


@router.get('/types', response_model=list[get_types.TypesType])
async def get_types_router(request: Request) -> list[get_types.TypesType]:
    return await get_types.get_types(request.app.state.client)
