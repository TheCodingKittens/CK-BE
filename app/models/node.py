from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.utils.config import settings
from aredis_om.connections import get_redis_connection
from aredis_om.model import Field, HashModel
from attr import validate
from pydantic import BaseModel, validator


class Node(HashModel):
    command_pk: str = Field(title="The Primary Key of the Command", index=True)
    parent_node_pk: Optional[str] = Field(
        title="The Primary Key of the Parent Node", index=True
    )
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    node_id: Optional[str] = Field(title="The ID of the Node", index=True)
    type: Optional[str] = Field(title="The Type of the Node")
    command: Optional[str] = Field(title="The Command")

    class Meta:
        database = get_redis_connection(
            url=settings.REDIS_DATA_URL, decode_responses=True
        )


class NodeRead(BaseModel):
    pk: str = Field(title="The Primary Key of the Parent Node", index=True)
    command_pk: str = Field(title="The Primary Key of the Command", index=True)
    parent_node_pk: str = Field(title="The Primary Key of the Parent Node", index=True)
    created_at: datetime = Field(
        title="Created At", default_factory=datetime.utcnow, index=True
    )
    node_id: Optional[str] = Field(title="The ID of the Node", index=True)
    type: Optional[str] = Field(title="The Type of the Node")
    command: Optional[str] = Field(title="The Command")
    nodes: Optional[List[NodeRead]] = Field([], title="The Value of the Node")
