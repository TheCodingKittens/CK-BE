import json


class NodeNester:
    def __init__(self, nodes) -> None:
        self.nodes = nodes

    # MAIN FUNCTION
    def nest_nodes(self):

        for node in self.nodes:
            if "parent_node_pk" in node:
                parent = self.get_parent(node)
                self.add_child(parent, node)

        parent_nodes = [node for node in self.nodes if not "parent_node_pk" in node]
        return parent_nodes

    def add_child(self, parent, child):
        if parent["nodes"] == "":
            parent["nodes"] = [child]
        else:
            parent["nodes"].append(child)

    def get_parent(self, child):
        for node in self.nodes:
            if node["pk"] == child["parent_node_pk"]:
                return node
