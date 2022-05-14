from datetime import datetime
from typing import List, Optional

from app.models.base64 import Base64Type
from app.models.command_data import CommandData
from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel


class Variable(HashModel):
    
    name: str = Field(title="The key of the variable", index=True)
    value: str = Field(title="The value of the Variable", index=True)

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )
