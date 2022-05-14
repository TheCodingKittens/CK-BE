from datetime import datetime
from typing import List, Optional

from app.models.command import CommandRead
from app.models.command_data import CommandData
from app.models.edge import Edge
from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel


# TODO modify to yse List of Command because now it contains the nodes
class History(BaseModel):
    Commands: List[CommandRead] = Field(title="The List of Commands", index=True)
