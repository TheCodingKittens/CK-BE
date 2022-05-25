# Models
import uuid
from typing import List

from app import crud
from app.models.command import Command, CommandCreate, UserInput
from app.models.edge import Edge
from app.models.node import Node
from app.models.variable import Variable

#  Services
from app.services.edge_creator import EdgeCreator
from app.services.executor import Executor
from app.services.jupyter_executor import ExecutorJuypter
from app.services.parser import Parser


class CommandController:
    async def save(
        self,
        user_input: UserInput,
        parser: Parser,
        executor: Executor,
        jupyter_executor: ExecutorJuypter,
    ) -> Command:
        # get the session history of all command_wrappers
        current_state = await crud.command.read_all_by_token(user_input.token)

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
            module=user_input.command, history=latest_variables
        )

        # Fetch all of the "command" attributes of all the CommandWrapper objects of the session (as a history basically) -> needed for 6
        history_of_prev_commands = [command.command for command in current_state]

        # Execute a Jupyter Notebook and retrieve the output of the last, newest cell (get_output_of_last_cell)
        command_output = jupyter_executor.run_notebook_given_history_and_new_command(
            history_of_prev_commands, user_input.command
        )

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
        for key, item in new_variables.items():
            await crud.variable.create(
                Variable(command_pk=db_command.pk, var_name=key, value=item)
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

    async def delete(self, token: str) -> Command:
        await crud.command.delete_all_by_token(token)
        return await crud.command.read_all_by_token(token)

    async def update(
        self,
        pk: str,
        user_input: UserInput,
        parser: Parser,
        executor: Executor,
        jupyter_executor: ExecutorJuypter,
    ) -> List[Command]:

        # 2. Fetch ALL session wrappers ✅
        session_commands = await crud.command.read_all_by_token(user_input.token)

        # 3. Fetch the modified CommandWrapper given the CommandWrapper ID ✅
        update_index = 0
        for i, command in enumerate(session_commands):
            if command.pk == pk:
                update_index = i
                break

        # 4. Create a list of successors and predecessor (also needed later on) ✅
        predecessors = session_commands[0:update_index]
        successors = session_commands[update_index + 1 :]

        # Save predecessors and successors to the database with a new token

        temp_token = str(uuid.uuid4())

        for command in predecessors:
            await self.save(
                user_input=UserInput(token=temp_token, command=command.command),
                parser=parser,
                executor=executor,
                jupyter_executor=jupyter_executor,
            )

        await self.save(
            user_input=UserInput(token=temp_token, command=user_input.command),
            parser=parser,
            executor=executor,
            jupyter_executor=jupyter_executor,
        )

        for command in successors:
            await self.save(
                user_input=UserInput(token=temp_token, command=command.command),
                parser=parser,
                executor=executor,
                jupyter_executor=jupyter_executor,
            )

        # 5. Delete the old CommandWrapper ✅
        await crud.command.delete_all_by_token(user_input.token)

        await crud.command.update_tokens(
            temp_token=temp_token, existing_token=user_input.token
        )

        return await crud.command.read_all_by_token(token=user_input.token)
