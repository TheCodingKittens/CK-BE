from datetime import datetime
from typing import List, Optional

from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel
from pydantic import BaseModel


class Edge(HashModel):
    command_pk: Optional[str] = Field(
        title="The Primary Key of The Command", index=True
    )
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    source_node: str = Field(title="The Source of the Set", index=True)
    target_node: str = Field(title="The Target of the Set", index=True)

    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )
