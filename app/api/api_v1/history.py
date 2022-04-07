from typing import List

from app import crud
from app.models.history import History
from aredis_om.connections import get_redis_connection
from aredis_om.model import HashModel, NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()

# History could be just a get all with everything in a Timestamp order

# GEt all commands
@router.get("", response_model=History)
async def list_commands(request: Request, response: Response) -> History:
    # To retrieve this commands with its primary key, we use `commands.get()`:

    return await crud.history.read_all()
