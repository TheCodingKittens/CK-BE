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
        if parent["value"] == "":
            parent["value"] = [child]
        else:
            parent["value"].append(child)


    def get_parent(self, child):
        for node in self.nodes:
            if node["pk"] == child["parent_node_pk"]:
                return node



# --------------- COMMAND FOR TESTING ---------------
# a = 3
# if a == 3:
#     if a < 4:
#         print("InnerIf")
#     print("OuterIf")
#     print("RANDOM")
# print("Base")

dummy_nodes = [
    {
        "pk": "1",
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.709506",
        "id": "",
        "type": "Line",
        "command": "a = 3",
        "value": ""
    },
    {
        "pk": "2",
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.710455",
        "id": "",
        "type": "If.test",
        "command": "if a == 3:",
        "value": ""
    },
    {
        "pk": "3",
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.711136",
        "id": "",
        "type": "If.body",
        "command": "",
        "value": ""
    },
    {
        "pk": "4",
        "parent_node_pk": "3",     # ADDED MANUALLY FOR NOW
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.711784",
        "id": "",
        "type": "If.test",
        "command": "if a < 4:",
        "value": ""
    },
    {
        "pk": "5",
        "parent_node_pk": "3",     # ADDED MANUALLY FOR NOW
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.712846",
        "id": "",
        "type": "If.body",
        "command": "",
        "value": ""
    },
    {
        "pk": "6",
        "parent_node_pk": "5",     # ADDED MANUALLY FOR NOW
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.713855",
        "id": "",
        "type": "Line",
        "command": "print(\"InnerIf\")",
        "value": ""
    },
    {
        "pk": "7",
        "parent_node_pk": "3",     # ADDED MANUALLY FOR NOW
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.714921",
        "id": "",
        "type": "Line",
        "command": "print(\"OuterIf\")",
        "value": ""
    },
    {
        "pk": "8",
        "parent_node_pk": "3",     # ADDED MANUALLY FOR NOW
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.715929",
        "id": "",
        "type": "Line",
        "command": "print(\"RANDOM\")",
        "value": ""
    },
    {
        "pk": "9",
        "command_pk": "100",
        "created_at": "2022-05-19T21:14:33.717036",
        "id": "",
        "type": "Line",
        "command": "print(\"Base\")",
        "value": ""
    }
]

node_nester = NodeNester(dummy_nodes)
NEW_NODES = node_nester.nest_nodes()
print(json.dumps(NEW_NODES, sort_keys=False, indent=4))
