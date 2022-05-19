from typing import List, Optional

from app import crud
from app.crud.base import CRUDBase
from app.models.command import CommandRead
from app.models.history import History
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDHistory(CRUDBase[History, History, History]):
    async def read_all(self) -> History:
        try:
            commands = await crud.command.read_all()

            return History(commands=commands)

        except NotFoundError:
            raise HTTPException(status_code=404, detail="There is no History")

    async def read_all_by_token(self, token: str) -> History:
        try:
            commands = await crud.command.read_all_by_token(token=token)

            # order by timestamp
            commands = sorted(commands, key=lambda x: x.created_at, reverse=True)

            return History(commands=commands)

        except NotFoundError:
            raise HTTPException(
                status_code=404,
                detail="There is no History with the Matching Session Token",
            )


history = CRUDHistory(History)
