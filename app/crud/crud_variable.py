from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.variable import Variable
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDVariable(CRUDBase[Variable, Variable, Variable]):
    async def get_all_by_command_pk(self, command_pk: str) -> List[Variable]:

        try:
            return await Variable.find(Variable.command_pk == command_pk).all()
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def update(pk, obj_in: Variable) -> Optional[Variable]:
        try:

            existing_model = await Variable.get(pk)

            if existing_model:
                await existing_model(**obj_in.dict())
                return await existing_model.update()

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


variable = CRUDVariable(Variable)
