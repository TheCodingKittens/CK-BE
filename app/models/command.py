from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.models.base64 import Base64Type
from app.models.edge import Edge
from app.models.node import Node, NodeRead
from app.models.variable import Variable
from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel, NotFoundError
from pydantic import BaseModel

# •	We need some sort of CommandWrapper which contains:
# o	Command (user input – single or multi-line) ✅ - Base64Type
# o	Timestamp ✅
# o	Token ✅
# o	Current state of variables (will be sent to the frontend) ✅ (CommandData Object)
# o	Outputs (will be sent to the frontend) TODO assign output to this value
# o	Edges (only the ones of that Wrapper, will be sent to frontend) TODO assign edges to this value
# o	Nodes (only the ones of that Wrapper, will be sent to frontend) TODO assign nodes to this value


class UserInput(BaseModel):
    command: Base64Type
    token: str = Field(title="The token of the user")


class CommandCreate(HashModel):
    command: bytes = Field(title="The User's Command", index=True)
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    token: Optional[str] = Field(title="Token")
    output: Optional[str] = Field(title="Output of the command")

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )


class Command(BaseModel):
    pk: str = Field(title="The Primary Key")
    command: Base64Type = Field(title="The User's Command", index=True)
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    token: str = Field(title="Token")
    output: Optional[str] = Field(title="The Output of the Command")
    variables: Optional[List[Variable]] = Field(
        title="The Data of the Command", index=True
    )
    edges: Optional[List[Edge]] = Field(title="The Edges of the Command")
    nodes: Optional[List[NodeRead]] = Field(title="The Nodes of the Command")
