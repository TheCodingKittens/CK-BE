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


# User Posts a new command to /api/v1/command
@router.post("", response_model=List[Command])
async def save_command(
    userinput: UserInput,
    parser: Parser = Depends(Parser),
    executor: Executor = Depends(Executor),
    jupyter_executor: ExecutorJuypter = Depends(ExecutorJuypter),
) -> Command:

    # get the session history of all command_wrappers
    current_state = await crud.command.read_all_by_token(userinput.token)

    # get the latest command from current_state.. if empty set to []
    latest_command = current_state[-1] if current_state else []

    # fetch the current state of variables
    latest_variables = {}

    if latest_command:
        for x in latest_command.variables:
            value = int(x.value) if x.value.isnumeric() else x.value
            latest_variables[x.var_name] = value

    # Execute the command using the current state of variables and retrieve the new state of the variables
    new_variables = executor.exec_module_from_history(
        module=userinput.command, history=latest_variables
    )

    # Fetch all of the "command" attributes of all the CommandWrapper objects of the session (as a history basically) -> needed for 6
    history_of_prev_commands = [command.command for command in current_state]

    # Execute a Jupyter Notebook and retrieve the output of the last, newest cell (get_output_of_last_cell)
    command_output = jupyter_executor.run_notebook_given_history_and_new_command(
        history_of_prev_commands, userinput.command
    )

    # Parse the input using the parse_module function and retrieve the nodes and edges
    # TODO return pydantic node objects

    nodes = parser.parse_module(userinput.command)

    # create the commandwrapper object
    db_command = await crud.command.create(
        obj_in=CommandCreate(
            token=userinput.token,
            command=userinput.command.data(),
            output=command_output,
        )
    )

    # create and save variables
    for key, item in new_variables.items():
        await crud.variable.create(
            Variable(command_pk=db_command.pk, var_name=key, value=item)
        )

    # create and save nodes
    # TODO

    db_nodes = await crud.node.create_bulk(
        nodes=nodes, parent_pk=None, command_pk=db_command.pk
    )

    # create and save edges
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

    # return the history of all commandwrapper fiven the token
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


# 1. User changes a node and sends a request including NodeID, respective CommandWrapperID and new command (for the node)
@router.put("/{pk}", response_model=Command)
async def put_command(pk: str, command: Command, response: Response) -> Command:

    # 2. Fetch ALL session wrappers
    # session_wrappers = ... some db call ...

    # 3. Fetch the modified CommandWrapper given the CommandWrapper ID
    # modified_wrapper = LOOK FOR CORRECT ONE IN "session_wrappers"

    # 4. Create a list of successors and predecessor (also needed later on)
    # successors = session_wrappers AFTER THE MODIFIED ONE
    # predecessors = session_wrappers BEFORE THE MODIFIED ONE

    # 5. Call a function (Grigor’s work) to create a new TEMPORARY JSON-tree (for the “nodes” of the commandwrapper) with the updates made
    # current_nodes = modified_wrapper GET "nodes" JSON
    # new_nodes = CALL FUNTION

    # 6. Create the updated command property of the CommandWrapper by calling a function that creates the code from the temporary JSON tree (Grigor’s work)
    # new_commandwrapper_command = create_python_code(new_nodes) -> CALL FUNTION

    # 7. Recreate edges (again, just temporarily save them)
    # new_edges = edge_creator.create_edges(new_nodes)

    # 8. Fetch the state of the variables from the PREVIOUS commandwrapper (the one before the modified one)
    # latest_variables = predecessors[-1].variables

    # 9. Call the exec function for the temporary command of the CommandWrapper with the previously fetched variables as input and temporarily save the variables.
    # try:
    #     new_variables = executor.exec_module_from_history(
    #         new_commandwrapper_command,
    #         latest_variables
    #     )
    # except Exception as e:
    #     return {"error": str(e)}

    # 10. Now for all successor CommandWrappers, execute again
    # temp_vars = [] # create a list to store the variables for each successor wrapper temporarily
    # current_vars = new_variables # start by passing the just fetched vars from the modified wrapper
    # try:
    #     for wrapper in successors:
    #         current_vars = executor.exec_module_from_history(
    #             wrapper.command, # feed the command of the wrapper
    #             current_vars # and the history of the previous
    #         )
    #         # and then add the received variables to a list
    #         temp_vars.append(current_vars)
    # except Exception as e:
    #     return {"error": str(e)}

    # 11. Now combine ALL commands (including the updated one) and execute them in a Jupyter notebook to receive the outputs
    # predecessor_commands = [wrapper.command for wrapper in predecessors]
    # successor_commands = [wrapper.command for wrapper in successors]
    # all_wrapper_commands = predecessor_commands + new_commandwrapper_command + successor_commands

    # try:
    #     all_outputs = run_notebook_given_history(all_wrapper_commands)
    # except Exception as e:
    #     return {"error": str(e)}
    # relevant_outputs = all_outputs[-(1+len(successors)):] # fetch all outputs for the modified_wrapper and all successors

    # 12. NO ERROR WAS THROWN SO FAR -> Create new CommandWrappers and delete the old ones
    # Start with the initially modified one:
    # CREATE "modified_wrapper" WITH "new_nodes", "new_commandwrapper_command", "new_edges", "new_variables", "relevant_outputs[0]"
    # REPLACE "modified_wrapper" with the newly created wrapper

    # and then all the successors (CREATE NEW ONES, REPLACING THE VARIABLES AND OUTPUTS, REST SHOULD STAY THE SAME)
    # for i in range(len(successors)):
    #     CREATE NEW WRAPPER with "temp_vars[i]" for variables, "relevant_outputs[i+1]" for outputs and all other parameters from successors[i]
    #     REPLACE successors[i] with the newly created wrapper

    # 13. SAVE ALL THE NEWLY CREATED WRAPPERS AND DELETE THE OLD ONES

    # 14. RETURN THE HISTORY OF ALL SESSION WRAPPERS

    try:
        return await crud.command.update(pk=pk, obj_in=command)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")
