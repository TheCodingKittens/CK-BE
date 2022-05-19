from datetime import datetime
from typing import List, Optional

from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel


class Node(HashModel):
    command_pk: str = Field(title="The Primary Key of the Command", index=True)
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    id: str = Field(title="The ID of the Node", index=True)
    type: str = Field(title="The Type of the Node")
    command: str = Field(title="The Command")

    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )
