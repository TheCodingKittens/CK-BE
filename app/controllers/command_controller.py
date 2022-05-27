# Models
import base64
import json
import uuid
from ast import literal_eval
from typing import List

from app import crud
from app.models.base64 import Base64Type
from app.models.command import (
    Command,
    CommandCreate,
    UserInput,
    UserInputDelete,
    UserInputSwap,
)
from app.models.edge import Edge
from app.models.node import Node, NodeRead
from app.models.variable import Variable

#  Services
from app.services.edge_creator import EdgeCreator
from app.services.executor import Executor
from app.services.json_to_source_code_converter import JSONToSourceCodeConverter
from app.services.jupyter_executor import ExecutorJuypter
from app.services.node_editor import NodeEditor
from app.services.parser import Parser
from app.services.variable_transformer import VariableTransformer
from fastapi.encoders import jsonable_encoder


class CommandController:

    # ------------------------ SAVE ------------------------
    async def save(
        self,
        user_input: UserInput,
        parser: Parser,
        executor: Executor,
        jupyter_executor: ExecutorJuypter,
        variable_transformer: VariableTransformer,
        output: str,
    ) -> Command:
        # get the session history of all command_wrappers
        current_state = await crud.command.read_all_by_token(user_input.token)

        # get the latest command from current_state.. if empty set to []
        latest_command = current_state[-1] if current_state else []

        # fetch the current state of variables
        latest_variables = {}

        if latest_command:
            for x in latest_command.variables:
                try:
                    value = literal_eval(x.value)
                except ValueError:
                    value = x.value

                latest_variables[x.var_name] = value

        # Execute the command using the current state of variables and retrieve the new state of the variables
        new_variables = executor.exec_module_from_history(
            module=user_input.command, history=latest_variables
        )

        # Fetch all of the "command" attributes of all the CommandWrapper objects of the session (as a history basically) -> needed for 6
        history_of_prev_commands = [command.command for command in current_state]

        # Execute a Jupyter Notebook and retrieve the output of the last, newest cell (get_output_of_last_cell)
        if output == []:
            command_output = (
                jupyter_executor.run_notebook_given_history_and_new_command(
                    history_of_prev_commands, user_input.command
                )
            )
        else:
            command_output = output

        nodes = parser.parse_module(user_input.command)

        # create the commandwrapper object
        db_command = await crud.command.create(
            obj_in=CommandCreate(
                token=user_input.token,
                command=user_input.command.data(),
                output=command_output,
            )
        )

        # create and save variables
        new_variables = variable_transformer.transform_variables(new_variables)
        for var in new_variables:
            await crud.variable.create(
                Variable(
                    command_pk=db_command.pk,
                    var_name=var["key"],
                    value=var["value"],
                    type=var["type"],
                )
            )

        await crud.node.create_bulk(
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
        return await crud.command.read_all_by_token(token=user_input.token)

    # ------------------------ UPDATE ------------------------
    async def update(
        self,
        pk: str,
        user_input: UserInput,
        parser: Parser,
        executor: Executor,
        jupyter_executor: ExecutorJuypter,
        variable_transformer: VariableTransformer,
    ) -> List[Command]:

        # 1. Fetch ALL session wrappers ✅
        session_commands = await crud.command.read_all_by_token(user_input.token)

        # 2. Fetch the modified CommandWrapper given the CommandWrapper ID ✅
        update_index = 0
        for i, command in enumerate(session_commands):
            if command.pk == pk:
                update_index = i
                modified_wrapper = command
                break

        # 3. Create a list of successors and predecessor (also needed later on) ✅
        predecessors = session_commands[0:update_index]
        successors = session_commands[update_index + 1 :]

        # 4. Create an updated json tree ✅
        current_nodes = jsonable_encoder(modified_wrapper.nodes)
        nodeEditor = NodeEditor(current_nodes)
        nodeEditor.edit_node(
            node_id=user_input.node_id,
            new_command=user_input.new_command.decode_str(),
        )
        new_nodes = nodeEditor.json

        # 5. Create the updated command property of the CommandWrapper ✅
        jsonToSourceCodeConverter = JSONToSourceCodeConverter(new_nodes)
        new_commandwrapper_command = jsonToSourceCodeConverter.generate_source_code()
        new_commandwrapper_command = Base64Type(
            base64.b64encode(str.encode(new_commandwrapper_command))
        )

        # 6. Combine ALL commands and execute them in a Jupyter notebook to receive the outputs (why here? only run once!) ✅
        predecessor_commands = [wrapper.command for wrapper in predecessors]
        successor_commands = [wrapper.command for wrapper in successors]
        all_wrapper_commands = (
            predecessor_commands + [new_commandwrapper_command] + successor_commands
        )

        all_outputs = jupyter_executor.run_notebook_given_history(all_wrapper_commands)

        # 7. Run & Save predecessors, updated_command & successors to the database with a new token
        temp_token = str(uuid.uuid4())

        for i, command in enumerate(predecessors):
            await self.save(
                user_input=UserInput(token=temp_token, command=command.command),
                parser=parser,
                executor=executor,
                jupyter_executor=jupyter_executor,
                variable_transformer=variable_transformer,
                output=all_outputs[i],
            )

        await self.save(
            user_input=UserInput(token=temp_token, command=new_commandwrapper_command),
            parser=parser,
            executor=executor,
            jupyter_executor=jupyter_executor,
            variable_transformer=variable_transformer,
            output=all_outputs[len(predecessors)],
        )

        for i, command in enumerate(successors):
            await self.save(
                user_input=UserInput(token=temp_token, command=command.command),
                parser=parser,
                executor=executor,
                jupyter_executor=jupyter_executor,
                variable_transformer=variable_transformer,
                output=all_outputs[i + 1 + len(predecessors)],
            )

        # 8. Delete the existing command_wrappers
        await crud.command.delete_all_by_token(user_input.token)

        # 9. Update the temp token to the original token
        await crud.command.update_tokens(
            temp_token=temp_token, existing_token=user_input.token
        )

        # 10. Return the updated session history
        return await crud.command.read_all_by_token(token=user_input.token)

    # ------------------------ DELETE ------------------------
    async def delete(
        self,
        pk: str,
        user_input: UserInputDelete,
        parser: Parser,
        executor: Executor,
        jupyter_executor: ExecutorJuypter,
        variable_transformer: VariableTransformer,
    ) -> List[Command]:

        # 1. Fetch ALL session wrappers ✅
        session_commands = await crud.command.read_all_by_token(user_input.token)

        # 2. Remove the "to be deleted" CommandWrapper given the CommandWrapper ID ✅
        delete_index = 0
        for i, command in enumerate(session_commands):
            if command.pk == pk:
                delete_index = i
                break

        session_commands.pop(delete_index)

        # 3. Execute them in a Jupyter notebook to receive the outputs (why here? only run once!) ✅
        all_wrapper_commands = [wrapper.command for wrapper in session_commands]
        all_outputs = jupyter_executor.run_notebook_given_history(all_wrapper_commands)

        # 4. Run & Save them to the database with a new token
        temp_token = str(uuid.uuid4())

        for i, command in enumerate(session_commands):
            await self.save(
                user_input=UserInput(token=temp_token, command=command.command),
                parser=parser,
                executor=executor,
                jupyter_executor=jupyter_executor,
                variable_transformer=variable_transformer,
                output=all_outputs[i],
            )

        # 5. No error -> Delete the existing command_wrappers
        await crud.command.delete_all_by_token(user_input.token)

        # 6. Update the temp token to the original token
        await crud.command.update_tokens(
            temp_token=temp_token, existing_token=user_input.token
        )

        # 7. Return the updated session history
        return await crud.command.read_all_by_token(token=user_input.token)

    # ------------------------ SWAP ------------------------
    async def swap(
        self,
        pk: str,
        user_input: UserInputSwap,
        parser: Parser,
        executor: Executor,
        jupyter_executor: ExecutorJuypter,
        variable_transformer: VariableTransformer,
    ) -> List[Command]:

        # 1. Fetch ALL session wrappers ✅
        session_commands = await crud.command.read_all_by_token(user_input.token)

        # 2. Swap the two wrappers given their ID's ✅
        wrapper_1_index = 0
        wrapper_2_index = 0
        for i, command in enumerate(session_commands):
            if command.pk == pk:
                wrapper_1_index = i
            if command.pk == user_input.swapping_wrapper_id:
                wrapper_2_index = i

        session_commands[wrapper_1_index], session_commands[wrapper_2_index] = (
            session_commands[wrapper_2_index],
            session_commands[wrapper_1_index],
        )

        # 3. Execute them in a Jupyter notebook to receive the outputs (why here? only run once!) ✅
        all_wrapper_commands = [wrapper.command for wrapper in session_commands]
        all_outputs = jupyter_executor.run_notebook_given_history(all_wrapper_commands)

        # 4. Run & Save them to the database with a new token
        temp_token = str(uuid.uuid4())

        for i, command in enumerate(session_commands):
            await self.save(
                user_input=UserInput(token=temp_token, command=command.command),
                parser=parser,
                executor=executor,
                jupyter_executor=jupyter_executor,
                variable_transformer=variable_transformer,
                output=all_outputs[i],
            )

        # 5. No error -> Delete the existing command_wrappers
        await crud.command.delete_all_by_token(user_input.token)

        # 6. Update the temp token to the original token
        await crud.command.update_tokens(
            temp_token=temp_token, existing_token=user_input.token
        )

        # 7. Return the updated session history
        return await crud.command.read_all_by_token(token=user_input.token)
