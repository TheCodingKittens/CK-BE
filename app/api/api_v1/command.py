from doctest import OutputChecker
from platform import node
from typing import List

# CRUD operations for the Command model
from app import crud

# Models
from app.models.command import Command, CommandCreate, UserInput
from app.models.edge import Edge
from app.models.node import Node
from app.models.variable import Variable

# Services
from app.services.edge_creator import EdgeCreator
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
@router.post("", response_model=List[Command])
async def save_command(
    userinput: UserInput,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
) -> Command:

    # 2. get the current state of the variables
    current_state = await crud.command.read_all_by_token(userinput.token)

    # get the latest command from current_state if empty set to []
    latest_command = current_state[-1] if current_state else []

    # TODO from the LAST CommandWrapper of the current session, FETCH the variables property
    # latest_variables = ...some db call...
    # TODO if no prevoius variables were found (only for the very first user entry), just pass an empty dict

    latest_variables = (
        {x.var_name: x.value for x in latest_command.variables}
        if latest_command
        else {}
    )

    # 3. Execute the command

    # 3. Execute the command (Call “exec_module_from_history” using the current state of variables and retrieve the new state of the variables)

    new_variables = executor.exec_module_from_history(
        module=userinput.command, history=latest_variables
    )

    # 5. Fetch all of the "command" attributes of all the CommandWrapper objects of the session (as a history basically) -> needed for 6
    # TODO from ALL CommandWrapper of the current session, fetch the "COMMAND" properties to create a list of strings containing all previous commands
    # history_of_prev_commands = ...some db call...
    # TODO in case of no prevoius commands being available (only for the very first user entry), just pass an empty list

    history_of_prev_commands = [command.command for command in current_state]

    # 6. Execute a Jupyter Notebook and retrieve the output of the last, newest cell (get_output_of_last_cell)
    command_output = jupyter_executor.run_notebook_given_history_and_new_command(
        history_of_prev_commands, userinput.command
    )

    # 8. Parse the input using the parse_module function and retrieve the nodes and edges.
    # TODO ensure the nodes are being returned correctly
    # TODO change create_edges to accept nodes
    nodes = parser.parse_module(userinput.command)

    # 4, 7, 9 Can be one step because we need to only create one "CommandWrapper" object
    # TODO modify the command wrapper to be able to save the command and the variables
    db_command = await crud.command.create(
        obj_in=CommandCreate(
            token=userinput.token,
            command=userinput.command.data(),
            output=command_output,
        )
    )

    # Create and Save Variables

    for key, item in new_variables.items():
        await crud.variable.create(
            Variable(command_pk=db_command.pk, var_name=key, value=item)
        )

    # Create and Save Nodes

    for node in nodes:

        if node.get("value"):
            nested_nodes = node.get("value")
            # TODO handle nested nodes

            for nested_node in nested_nodes:
                await crud.node.create(
                    Node(
                        command_pk=db_command.pk,
                        id=nested_node.get("id"),
                        type=nested_node.get("type"),
                        command=nested_node.get("command"),
                    )
                )

        await crud.node.create(
            Node(
                command_pk=db_command.pk,
                id=node.get("id"),
                type=node.get("type"),
                command=node.get("command"),
            )
        )

    # Create and Save Edges

    edgeCreator = EdgeCreator(nodes)
    edgeCreator.create_edges()

    for edge in edgeCreator.edges:
        await crud.edge.create(
            obj_in=Edge(
                command_pk=db_command.pk,
                source_node=edge["from"],
                target_node=edge["to"],
                parent_node=edge["parent"],
            )
        )

    return await crud.command.read_all_by_token(token=userinput.token)


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


@router.put("/{pk}", response_model=Command)
async def put_command(pk: str, command: Command, response: Response) -> Command:
    try:
        return await crud.command.update(pk=pk, obj_in=command)

    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")
