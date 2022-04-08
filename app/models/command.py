from datetime import datetime
from typing import List, Optional

from app.models.command_data import CommandData
from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel



class CommandCreate(HashModel):
    command: str = Field(title="The User's Command", index=True)
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    # data: List[CommandData] = Field(title="The Data of the Command")

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )


class Command(BaseModel):
    command: str = Field(title="The User's Command", index=True)
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    data: List[CommandData] = Field(title="The Data of the Command", index=True)


class CommandRead(Command):
    """Pydantic Command Object"""
    pk: str = Field(title="Primary Key", index=True)
