from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.variable import VariableCreate
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDVariable(CRUDBase[VariableCreate, VariableCreate, VariableCreate]):
    async def create(obj_in: VariableCreate) -> VariableCreate:
        return await obj_in.save()

    async def get_all_by_command_pk(command_pk: str) -> List[VariableCreate]:

        try:
            return await VariableCreate.find(
                VariableCreate.command_pk == command_pk
            ).all()
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def update(pk, obj_in: VariableCreate) -> Optional[VariableCreate]:
        try:

            existing_model = await VariableCreate.get(pk)

            if existing_model:
                await existing_model(**obj_in.dict())
                return await existing_model.update()

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


variable = CRUDVariable(VariableCreate)
