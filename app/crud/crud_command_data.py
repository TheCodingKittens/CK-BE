from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.command_data import CommandDataCreate
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDCommandData(
    CRUDBase[CommandDataCreate, CommandDataCreate, CommandDataCreate]
):
    async def create(obj_in: CommandDataCreate) -> CommandDataCreate:
        return await obj_in.save()

    async def get_all_by_command_pk(command_pk: str) -> List[CommandDataCreate]:

        try:
            return await CommandDataCreate.find(
                CommandDataCreate.command_pk == command_pk
            ).all()
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def update(pk, obj_in: CommandDataCreate
    ) -> Optional[CommandDataCreate]:
        try:

            existing_model = await CommandDataCreate.get(pk)

            if existing_model:
                await existing_model(**obj_in.dict())
                return await existing_model.update()

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


command_data = CRUDCommandData
