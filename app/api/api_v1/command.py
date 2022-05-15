from platform import node
from typing import List

# CRUD operations for the Command model
from app import crud
# Models
from app.models.command import Command, CommandRead, UserInput
# Services
from app.services.edgecreator import EdgeCreator
from app.services.executor import Executor
from app.services.jupyter_executor import ExecutorJuypter
# Fastapi Dependencies
from app.services.parser import Parser
from aredis_om.model import NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()


# 1.	User inputs a new command (single or multi-line) and sends it to the backend
# 2.	Next thing will be the execution using exec(), in order to get the new variable values. What we need for this is the current state of the variables in the specific session (retrieved from the latest CommandWrapper of the session).
# 3.	Call “exec_module_from_history” using the current state of variables and retrieve the new state of the variables.
# If an error is thrown -> return this error to the frontend and stop
# 4.	No error -> create a new “CommandWrapper” object and set the “command” property to be the user input (once again, can be single or multiple line), the “variables” property to be current state of variables (returned from exec) and also create a timestamp and set the token sent from the user.
# 5.	Fetch all of the command attributes of all the CommandWrapper objects of the session (as a history basically) -> needed for 6
# 6.	Execute a Jupyter Notebook and retrieve the output of the last, newest cell (get_output_of_last_cell)
# 7.	Save the output to the new CommandWrapper
# 8.	Parse the input using the parse_module function and retrieve the nodes and edges.
# 9.	Save the nodes and edges to the CommandWrapper
# 10.	Save the CommandWrapper to the list (f. ex. LinkedList) to be accessed later on
# 11.	Return a list of all CommandWrappers (including variables, outputs, nodes and edges) to the frontent


# 1. User Posts a new command to /api/v1/command
@router.post("", response_model=CommandRead)
async def save_command(
    userinput: UserInput,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
    edge_creator: EdgeCreator = Depends(EdgeCreator),
) -> CommandRead:

    # 2. get the current state of the variables
    # TODO from the LAST CommandWrapper of the current session, FETCH the variables property
    # latest_variables = ...some db call...
    # TODO if no prevoius variables were found (only for the very first user entry), just pass an empty dict
    latest_variables = {}

    # 3. Execute the command (Call “exec_module_from_history” using the current state of variables and retrieve the new state of the variables)
    try:
        new_variables = executor.exec_module_from_history(
            latest_variables
        )
    except Exception as e:
        return {"error": str(e)}

    # 5. Fetch all of the "command" attributes of all the CommandWrapper objects of the session (as a history basically) -> needed for 6
    # TODO from ALL CommandWrapper of the current session, fetch the "COMMAND" properties to create a list of strings containing all previous commands
    # history_of_prev_commands = ...some db call...
    # TODO in case of no prevoius commands being available (only for the very first user entry), just pass an empty list
    history_of_prev_commands = []

    # 6. Execute a Jupyter Notebook and retrieve the output of the last, newest cell (get_output_of_last_cell)
    command_output = jupyter_executor.run_notebook_given_history_and_new_command(history_of_prev_commands, userinput.command)

    # 8. Parse the input using the parse_module function and retrieve the nodes and edges.
    # TODO ensure the nodes are being returned correctly
    # TODO change create_edges to accept nodes
    nodes = parser.parse_module(userinput.command)
    edges = edge_creator.create_edges(nodes)

    command = Command(
        command=userinput.command,
        variables=new_variables,
        edges=edges,
        output=command_output,
        nodes=nodes,
    )

    # 4, 7, 9 Can be one step because we need to only create one "CommandWrapper" object
    # TODO modify the command wrapper to be able to save the command and the variables
    return await crud.command.create(obj_in=command)

    # 10, 11
    # This is the history endpoint, it will return all the "CommandWrappers"
    # TODO the POST should already return all the CommandWrappers (of the specific session, in order)


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
