from datetime import datetime
from typing import List, Optional

from app.models.command_data import CommandData
from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel


class SetCreate(HashModel):
    source: str = Field(title="The Source of the Set", index=True)
    target: str = Field(title="The Target of the Set", index=True)

    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )


class Set(BaseModel):
    pk: Optional[str] = Field(title="The Primary Key of The Set", index=True)
    source: str = Field(title="The Source of the Set", index=True)
    target: str = Field(title="The Target of the Set", index=True)
