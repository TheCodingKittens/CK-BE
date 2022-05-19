from typing import List

from app.models.command import Command
from pydantic import BaseModel, Field


# TODO modify to yse List of Command because now it contains the nodes
class History(BaseModel):
    commands: List[Command] = Field(title="The List of Commands", index=True)
