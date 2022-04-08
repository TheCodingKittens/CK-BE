from datetime import datetime
from typing import List, Optional

from app.models.command import CommandRead
from app.models.command_data import CommandData
from app.models.set import Set
from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel


class History(BaseModel):
    nodes: List[CommandRead] = Field(title="The Nodes of the Commands", index=True)
    edges: Optional[List[Set]] = Field(
        title="The Edges of the Command Nodes", index=True
    )
