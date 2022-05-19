from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.node import Node
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDNode(CRUDBase[Node, Node, Node]):
    async def get_all_by_command_pk(self, command_pk: str) -> List[Node]:
        try:
            return await Node.find(Node.command_pk == command_pk).all()
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


node = CRUDNode(Node)
