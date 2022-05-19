from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.edge import Edge
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDEdge(CRUDBase[Edge, Edge, Edge]):
    async def read_all() -> List[Edge]:
        all_pks = [pk async for pk in await Edge.all_pks()]

        all_models = []
        for pk in all_pks:
            try:
                Edge_db = await Edge.get(pk)
                all_models.append(Edge(**Edge_db.dict()))

            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

        return all_models

    async def get_all_by_command_pk(self, command_pk: str) -> List[Edge]:
        try:
            return await Edge.find(Edge.command_pk == command_pk).all()
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def update(pk, obj_in: Edge) -> Optional[Edge]:
        try:

            existing_model = await Edge.find(Edge.source == pk | Edge.pk == pk)

            if existing_model:
                await existing_model(**obj_in.dict())
                return await existing_model.update()

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


edge = CRUDEdge(Edge)
