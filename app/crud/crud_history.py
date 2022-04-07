from typing import List, Optional

from app import crud
from app.crud.base import CRUDBase
from app.models.command import CommandRead
from app.models.command_data import CommandData
from app.models.history import History
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDCommandData(CRUDBase[History, History, History]):
    async def read_all(self) -> History:
        try:
            commands = await crud.command.read_all()
            # TODO create set mechanism
            # sets = await crud.set.read_all()
            return History(nodes=commands)

        except NotFoundError:
            raise HTTPException(status_code=404, detail="There is no History")


history = CRUDCommandData(History)
