from typing import List

from app.models.command import Command
from aredis_om.connections import get_redis_connection
from aredis_om.model import HashModel, NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()

# History could be just a get all with everything in a Timestamp order

# GEt all commands
@router.get("", response_model=list[Command])
async def list_commands(request: Request, response: Response) -> list[Command]:
    # To retrieve this commands with its primary key, we use `commands.get()`:

    all_pks = [pk async for pk in await Command.all_pks()]

    all_commands = []
    for pk in all_pks:
        try:
            all_commands.append(await Command.get(pk))
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Command not found")

    return all_commands
