from app.models.command import Command
from aredis_om.model import HashModel, NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()


@router.post("", response_model=Command)
async def save_command(command: Command):
    # We can save the model to Redis by calling `save()`:
    return await command.save()


@router.get("", response_model=list[str])
async def list_commands(request: Request, response: Response):
    # To retrieve this command with its primary key, we use `command.get()`:
    return {"commands": [pk async for pk in await Command.all_pks()]}


@router.get("/{pk}", response_model=Command)
@cache(expire=10)
async def get_command(pk: str, request: Request, response: Response):
    # To retrieve this command with its primary key, we use `command.get()`:
    try:
        return await Command.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")


@router.put("/{pk}", response_model=Command)
async def put_command(pk: str, command: Command, response: Response) -> Command:
    try:
        existing_command = await Command.get(pk)

        if existing_command:
            await existing_command.update(**command.dict())
            return existing_command

    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")
