from typing import Any, List, Optional

from app.crud.base import CRUDBase
from app.models.node import Node, NodeRead
from aredis_om.model import HashModel, NotFoundError
from fastapi import HTTPException


class CRUDNode(CRUDBase[Node, Node, Node]):
    def __init__(self, nodes: List[NodeRead] = None):
        self.nodes = nodes

    async def create_bulk(
        self,
        nodes: Any,
        parent_pk: Optional[str],
        command_pk: str,
    ) -> List[Node]:

        for node in nodes:
            db_node = await self.create(
                Node(
                    command_pk=command_pk,
                    parent_node_pk=parent_pk,
                    id=node.get("id"),
                    type=node.get("type"),
                    command=node.get("command"),
                )
            )

            if node.get("value"):
                await self.create_bulk(
                    node.get("value"), parent_pk=db_node.pk, command_pk=command_pk
                )

    def get_parent(self, nodes: List[NodeRead], parent_pk: str) -> Optional[NodeRead]:
        for node in nodes:
            if node.pk == parent_pk:
                return node

    def add_child(self, parent: NodeRead, child: NodeRead) -> NodeRead:
        parent.nodes.append(child)
        return parent

    def nest_nodes(self, nodes: List[NodeRead]) -> List[NodeRead]:

        for node in nodes:
            if node.parent_node_pk != "":
                parent = self.get_parent(nodes=nodes, parent_pk=node.parent_node_pk)
                if parent:
                    self.add_child(parent, node)

        return [node for node in nodes if node.parent_node_pk == ""]

    async def get_all_by_command_pk(self, command_pk: str) -> List[NodeRead]:
        try:
            nodes = await Node.find(Node.command_pk == command_pk).all()

            nodes = [NodeRead(**node.dict()) for node in nodes]

            return self.nest_nodes(nodes=nodes)

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Model not found")


node = CRUDNode(Node)
