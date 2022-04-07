from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.command_data import CommandDataCreate
from app.models.set import Set, SetCreate
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDSet(CRUDBase[SetCreate, SetCreate, Set]):
    async def create(obj_in: SetCreate) -> Set:
        return await obj_in.save()

    async def read_all() -> List[Set]:
        all_pks = [pk async for pk in await SetCreate.all_pks()]

        all_models = []
        for pk in all_pks:
            try:
                set_db = await SetCreate.get(pk)
                all_models.append(
                    Set(**set_db.dict())
                )

            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

        return all_models

    async def update(pk, obj_in: SetCreate
    ) -> Optional[SetCreate]:
        try:

            existing_model = await SetCreate.find(SetCreate.source == pk | SetCreate.pk == pk)

            if existing_model:
                await existing_model(**obj_in.dict())
                return await existing_model.update()

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")
