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
            userinput.command,
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
        token=userinput.token,
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


# 1. User changes a node and sends a request including NodeID, respective CommandWrapperID and new command (for the node)
@router.put("/{pk}", response_model=CommandRead)
async def put_command(pk: str, command: Command, response: Response) -> CommandRead:

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


    # 10. Now for all CommandWrappers that come AFTER the modified one, execute again
    # temp_vars = [] # create a list to store the variables for each successor wrapper temporarily
    # current_vars = new_variables # start by passing the just fetched vars
    # try:
    #     for wrapper in successors:
    #         current_vars = executor.exec_module_from_history(
    #             wrapper.command, # feed the command of the wrapper
    #             current_vars # and the history of the previous
    #         )
    #         # and then add the just fetched vars to a list
    #         temp_vars.append(current_vars)
    # except Exception as e:
    #     return {"error": str(e)}


    # 11. NO ERROR IS THROWN -> update all the CommandWrappers with the temporary stored values
    # Start with the initially modified one:
    # UPDATE "modified_wrapper" WITH "new_nodes", "new_commandwrapper_command", "new_edges", "new_variables"

    # and then all the successors
    # for i in range(len(successors)):
    #     SAVE temp_vars[i] TO the "variables" of successors[i]


    # 12. Now combine ALL session CommandWrapper and execute them in a Jupyter notebook while receiving the outputs
    # all_wrappers = predecessors + modified_wrapper + successors
    # command_list = [wrapper.command for wrapper in all_wrappers]
    # all_outputs = run_notebook_given_history(command_list)


    # 13. add all the new outputs to all the Wrappers
    # for i in range(len(all_wrappers)):
    #     UPDATE all_wrappers[i] WITH all_outputs[i]


    # 14. SAVE ALL THE WRAPPERS


    # 15. RETURN THE HISTORY OF ALL SESSION WRAPPERS


    try:
        return await crud.command.update(pk=pk, obj_in=command)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Command not found")
