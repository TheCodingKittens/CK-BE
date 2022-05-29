from app import crud
from app.models.history import History
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()

# History could be just a get all with everything in a Timestamp order


@router.get("/{token}", response_model=History)
async def list_commands(token: str, request: Request, response: Response) -> History:

    return await crud.history.read_all_by_token(token=token)
