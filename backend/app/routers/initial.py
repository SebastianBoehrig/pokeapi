from fastapi import APIRouter
import app.logic as logic

router: APIRouter = APIRouter(prefix='/initial', responses={404: {'description': 'Not found'}})


@router.get('/types', response_model=list[logic.TypesType])
def get_types_router() -> list[logic.TypesType]:
    return logic.get_types()
