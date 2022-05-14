from typing import List, Optional

from app import crud
from app.crud.base import CRUDBase
from app.models.command import Command, CommandCreate, CommandRead
from app.models.variable import VariableCreate
from app.utils.deps import create_parser
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDCommand(CRUDBase[CommandCreate, CommandCreate, Command]):
    async def create(self, obj_in: Command) -> CommandRead:

        createCommand = CommandCreate(command=obj_in.command)
        await createCommand.save()

        created_variable_objects = []

        for data in obj_in.data:
            created_variable = await crud.variable.create(
                obj_in=VariableCreate(**data.dict(), command_pk=createCommand.pk)
            )
            created_variable_objects.append(created_variable)

        return CommandRead(**createCommand.dict(), data=created_variable_objects)

    async def read(self, pk: str) -> Optional[CommandRead]:
        try:
            command_db = await CommandCreate.get(pk)
            variable_db_objects = await crud.variable.get_all_by_command_pk(
                command_pk=pk
            )

            return CommandRead(
                **command_db.dict(),
                data=variable_db_objects,
            )

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def read_all(self) -> Optional[List[CommandRead]]:
        all_pks = [pk async for pk in await CommandCreate.all_pks()]

        all_models = []
        for pk in all_pks:
            try:
                variable_objects = await crud.variable.get_all_by_command_pk(
                    command_pk=pk
                )
                command_db = await CommandCreate.get(pk)
                all_models.append(
                    CommandRead(**command_db.dict(), data=variable_objects)
                )
            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

        return all_models

    async def update(self, pk, obj_in: Command) -> Optional[CommandRead]:
        """ Update will not update the command it will just create a new model and overwrite the existing one's location in the set """
        try:
            existing_model = await CommandCreate.get(pk)

            if existing_model.command != obj_in.command:
                parser = create_parser()
                parsed_expression = parser.parse_expression(obj_in.command)
                return await self.create(obj_in=parsed_expression)


        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


command = CRUDCommand(Command)
