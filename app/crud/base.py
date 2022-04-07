from typing import Generic, List, Optional, TypeVar

from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException

ModelType = TypeVar("ModelType", bound=HashModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=HashModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=HashModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model):
        self.model = model

    def create(self, obj_in: ModelType) -> HashModel:
        return obj_in.save()

    async def read(self, pk: str) -> Optional[HashModel]:
        try:
            return self.model.get(pk)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    async def read_all(self) -> Optional[List[HashModel]]:
        all_pks = [pk async for pk in await self.model.all_pks()]

        all_models = []
        for pk in all_pks:
            try:
                all_models.append(await self.model.get(pk))
            except NotFoundError:
                raise HTTPException(status_code=404, detail="Model not found")

    async def update(self, pk, obj_in: UpdateSchemaType) -> Optional[HashModel]:
        try:
            existing_model = await self.model.get(pk)

            if existing_model:
                await existing_model.update(**obj_in.dict())
                return existing_model

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")

    # TODO Delete
    def delete(self, id):
        return self.model.delete(id)
