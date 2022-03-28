from datetime import datetime
from typing import Optional

from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import HashModel, NotFoundError
from pydantic import Field


class Command(HashModel):
    command: str = Field(title="The User's Command")
    created_at: datetime = Field(title="Created At", default_factory=datetime.utcnow)
    value: str = Field(title="The Value of the Command")
    variable_name: str = Field(title="The Name of the varibable within the Command")
    # Possibly an enum in the future
    current_state: str = Field(title="Current State")

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )
