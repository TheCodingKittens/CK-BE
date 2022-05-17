from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.user import User
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDUser(CRUDBase[User, User, User]):
    async def get_by_username(username: str) -> User:
        try:
            return await User.get(username)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


user = CRUDUser(User)
