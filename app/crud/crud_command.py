from typing import List, Optional

from app import crud
from app.crud.base import CRUDBase
from app.models.command import Command, CommandCreate
from app.models.variable import Variable
from app.utils.deps import create_parser
from aredis_om.model import HashModel, NotFoundError
from click import command
from fastapi import HTTPException


class CRUDCommand(CRUDBase[CommandCreate, CommandCreate, Command]):
    async def create(self, obj_in: CommandCreate) -> CommandCreate:
        return await obj_in.save()

    async def read(self, pk: str) -> Optional[Command]:
        try:
            command_db = await CommandCreate.get(pk)

            variable_db_objects = await crud.variable.get_all_by_command_pk(
                command_pk=pk
            )
            node_db_objects = await crud.node.get_all_by_command_pk(command_pk=pk)

            edges = await crud.edge.get_all_by_command_pk(command_pk=pk)

            return Command(
                **command_db.dict(),
                variables=variable_db_objects,
                nodes=node_db_objects,
                edges=edges,
            )

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def read_all(self) -> Optional[List[Command]]:
        all_pks = [pk async for pk in await CommandCreate.all_pks()]

        all_models = []
        for pk in all_pks:
            try:
                variable_db_objects = await crud.variable.get_all_by_command_pk(
                    command_pk=pk
                )
                node_db_objects = await crud.node.get_all_by_command_pk(command_pk=pk)

                edges = await crud.edge.get_all_by_command_pk(command_pk=pk)

                command_db = await CommandCreate.get(pk)
                all_models.append(
                    Command(
                        **command_db.dict(),
                        variables=variable_db_objects,
                        nodes=node_db_objects,
                        edges=edges,
                    )
                )
            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

        return all_models

    async def read_all_by_token(self, token: str) -> List[Command]:
        all_pks = [pk async for pk in await CommandCreate.all_pks()]

        matching_token_models = []

        for pk in all_pks:
            try:
                command_db = await CommandCreate.get(pk)
                if command_db.token == token:
                    variable_db_objects = await crud.variable.get_all_by_command_pk(
                        command_pk=command_db.pk
                    )
                    node_db_objects = await crud.node.get_all_by_command_pk(
                        command_pk=command_db.pk
                    )

                    edge_db_objects = await crud.edge.get_all_by_command_pk(
                        command_pk=command_db.pk
                    )

                    matching_token_models.append(
                        Command(
                            **command_db.dict(),
                            variables=variable_db_objects,
                            nodes=node_db_objects,
                            edges=edge_db_objects,
                        )
                    )
            except NotFoundError:
                raise HTTPException(status_code=404, detail="Unable to filter on Token")

        return sorted(matching_token_models, key=lambda x: x.created_at, reverse=False)

    async def delete(self, pk: str) -> None:
        try:
            db_object = await CommandCreate.get(pk)
            await db_object.delete()
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def delete_all_by_token(self, token: str) -> None:
        all_pks = [pk async for pk in await CommandCreate.all_pks()]

        for pk in all_pks:
            try:
                command_db = await CommandCreate.get(pk)
                if command_db.token == token:
                    await command_db.delete()
            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

    async def update(self, pk, obj_in: Command) -> Optional[Command]:
        """Update will not update the command it will just create a new model and overwrite the existing one's location in the set"""
        try:
            existing_model = await CommandCreate.get(pk)

            if existing_model.command != obj_in.command:
                parser = create_parser()
                parsed_expression = parser.parse_expression(obj_in.command)
                return await self.create(obj_in=parsed_expression)

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def update_tokens(self, temp_token: str, existing_token: str) -> None:

        db_commands = await self.read_all_by_token(token=temp_token)

        try:
            for command_db in db_commands:

                update_command = await CommandCreate.get(command_db.pk)

                await update_command.update(token=existing_token)

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


command = CRUDCommand(Command)
