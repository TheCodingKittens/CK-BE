from typing import List

# CRUD operations for the Command model
from app import crud

# Controllers
from app.controllers.command_controller import CommandController

# Models
from app.models.command import Command, UserInput, UserInputUpdate

# Services
from app.services.executor import Executor
from app.services.jupyter_executor import ExecutorJuypter
from app.services.parser import Parser

# Fastapi Dependencies
from aredis_om.model import NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()


# User Posts a new command to /api/v1/command
@router.post("", response_model=List[Command])
async def save_command(
    user_input: UserInput,
    command_controller: CommandController = Depends(CommandController),
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
) -> List[Command]:

    try:
        return await command_controller.save(
            user_input=user_input,
            parser=parser,
            executor=executor,
            jupyter_executor=jupyter_executor,
            output=[],  # giving an empty list results in jupyter being run
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[Command])
async def list_commands(request: Request, response: Response):
    # To retrieve this command with its primary key, we use `command.get()`:

    try:
        return await crud.command.read_all()
    except NotFoundError:
        raise HTTPException(status_code=404, detail="No commands found")


@router.get("/{pk}", response_model=Command)
@cache(expire=10)
async def get_command(pk: str, request: Request, response: Response):
    # To retrieve this command with its primary key, we use `command.get()`:
    try:
        return await crud.command.read(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")


# TODO make it so that token, nodeID and commandwrapperID are sent from frontend
# 1. User changes a node and sends a request including NodeID, respective CommandWrapperID and new command (for the node)
@router.put("/{pk}", response_model=List[Command])
async def put_command(
    pk: str,
    user_input: UserInputUpdate,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    command_controller: CommandController = Depends(CommandController),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
) -> List[Command]:

    try:
        return await command_controller.update(
            pk=pk,
            user_input=user_input,
            parser=parser,
            executor=executor,
            jupyter_executor=jupyter_executor,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{pk}", response_model=Command)
async def delete_command(pk: str):
    try:
        return await crud.command.delete(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")
