from typing import Any, List

# CRUD operations for the Command model
from app import crud

# Controllers
from app.controllers.command_controller import CommandController

# Models
from app.models.command import (
    Command,
    UserInput,
    UserInputDelete,
    UserInputSwap,
    UserInputUpdate,
)

# Services
from app.services.executor import Executor
from app.services.jupyter_executor import ExecutorJuypter
from app.services.parser import Parser
from app.services.variable_transformer import VariableTransformer

# Fastapi Dependencies
from fastapi import APIRouter, Depends

router = APIRouter()


# User Posts a new command
@router.post("", response_model=List[Command])
async def save_command(
    user_input: UserInput,
    command_controller: CommandController = Depends(CommandController),
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
    variable_transformer: VariableTransformer = Depends(VariableTransformer),
) -> List[Command]:

    return await command_controller.save(
        user_input=user_input,
        parser=parser,
        executor=executor,
        jupyter_executor=jupyter_executor,
        variable_transformer=variable_transformer,
        output=[],  # giving an empty list results in jupyter being run
    )


# User changes a node and sends a request including NodeID, respective CommandWrapperID and new command (for the node)
@router.put("/{pk}", response_model=List[Command])
async def put_command(
    pk: str,
    user_input: UserInputUpdate,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    command_controller: CommandController = Depends(CommandController),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
    variable_transformer: VariableTransformer = Depends(VariableTransformer),
) -> List[Command]:

    return await command_controller.update(
        pk=pk,
        user_input=user_input,
        parser=parser,
        executor=executor,
        jupyter_executor=jupyter_executor,
        variable_transformer=variable_transformer,
    )


# User swaps two commands
@router.put("/{pk}/swap", response_model=List[Command])
async def put_command(
    pk: str,
    user_input: UserInputSwap,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    command_controller: CommandController = Depends(CommandController),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
    variable_transformer: VariableTransformer = Depends(VariableTransformer),
) -> List[Command]:

    return await command_controller.swap(
        pk=pk,
        user_input=user_input,
        parser=parser,
        executor=executor,
        jupyter_executor=jupyter_executor,
        variable_transformer=variable_transformer,
    )


# User deletes a command
@router.delete("/{pk}", response_model=List[Command])
async def delete_command(
    pk: str,
    user_input: UserInputDelete,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    command_controller: CommandController = Depends(CommandController),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
    variable_transformer: VariableTransformer = Depends(VariableTransformer),
) -> List[Command]:

    return await command_controller.delete(
        pk=pk,
        user_input=user_input,
        parser=parser,
        executor=executor,
        jupyter_executor=jupyter_executor,
        variable_transformer=variable_transformer,
    )
