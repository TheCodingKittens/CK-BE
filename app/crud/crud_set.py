from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.command_data import CommandDataCreate
from app.models.edge import Edge, EdgeCreate
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDEdge(CRUDBase[EdgeCreate, EdgeCreate, Edge]):
    async def create(obj_in: EdgeCreate) -> Edge:
        return await obj_in.save()

    async def read_all() -> List[Edge]:
        all_pks = [pk async for pk in await EdgeCreate.all_pks()]

        all_models = []
        for pk in all_pks:
            try:
                Edge_db = await EdgeCreate.get(pk)
                all_models.append(
                    Edge(**Edge_db.dict())
                )

            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

        return all_models

    async def update(pk, obj_in: EdgeCreate
    ) -> Optional[EdgeCreate]:
        try:

            existing_model = await EdgeCreate.find(EdgeCreate.source == pk | EdgeCreate.pk == pk)

            if existing_model:
                await existing_model(**obj_in.dict())
                return await existing_model.update()

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")
