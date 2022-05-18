from typing import List

from app.models.command import CommandRead
from pydantic import BaseModel, Field


# TODO modify to yse List of Command because now it contains the nodes
class History(BaseModel):
    commands: List[CommandRead] = Field(title="The List of Commands", index=True)
