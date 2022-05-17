from datetime import datetime
from typing import List, Optional

from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel


class User(HashModel):
    username: str = Field(
        title="The Name of the varibable within the Command", index=True
    )
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )

    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )
