from typing import List

import libcst as cst
from app import crud
from app.models.command import Command, CommandRead
from app.services.parser import Parser, TypingCollector, TypingTransformer
from app.utils.deps import create_parser, create_vistor
from aredis_om.model import HashModel, NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()


@router.post("", response_model=CommandRead)
async def save_command(command: str, parser: Parser = Depends(Parser)) -> CommandRead:
    # We can save the model to Redis by calling `save()`:

    parsed_expression = parser.parse_expression(command)
    return await crud.command.create(obj_in=parsed_expression)

    # Save the Command and return the newly saved command


@router.get("", response_model=List[CommandRead])
async def list_commands(request: Request, response: Response):
    # To retrieve this command with its primary key, we use `command.get()`:

    try:
        return await crud.command.read_all()
    except NotFoundError:
        raise HTTPException(status_code=404, detail="No commands found")


@router.get("/{pk}", response_model=CommandRead)
@cache(expire=10)
async def get_command(pk: str, request: Request, response: Response):
    # To retrieve this command with its primary key, we use `command.get()`:
    try:
        return await crud.command.read(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")


@router.put("/{pk}", response_model=CommandRead)
async def put_command(pk: str, command: Command, response: Response) -> CommandRead:
    try:
        return await crud.command.update(pk=pk, obj_in=command)

    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")
