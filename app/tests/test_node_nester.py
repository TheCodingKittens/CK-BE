
import json

from app.services.node_nester import NodeNester


def test_node_nesting():

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
            "parent_node_pk": "3",
            "command_pk": "100",
            "created_at": "2022-05-19T21:14:33.711784",
            "id": "",
            "type": "If.test",
            "command": "if a < 4:",
            "value": ""
        },
        {
            "pk": "5",
            "parent_node_pk": "3",
            "command_pk": "100",
            "created_at": "2022-05-19T21:14:33.712846",
            "id": "",
            "type": "If.body",
            "command": "",
            "value": ""
        },
        {
            "pk": "6",
            "parent_node_pk": "5",
            "command_pk": "100",
            "created_at": "2022-05-19T21:14:33.713855",
            "id": "",
            "type": "Line",
            "command": "print(\"InnerIf\")",
            "value": ""
        },
        {
            "pk": "7",
            "parent_node_pk": "3",
            "command_pk": "100",
            "created_at": "2022-05-19T21:14:33.714921",
            "id": "",
            "type": "Line",
            "command": "print(\"OuterIf\")",
            "value": ""
        },
        {
            "pk": "8",
            "parent_node_pk": "3",
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
    new_nodes = node_nester.nest_nodes()
    print(json.dumps(new_nodes, sort_keys=False, indent=4))

    assert new_nodes[0]["value"] == ""
    assert new_nodes[1]["value"] == ""
    assert len(new_nodes[2]["value"]) == 4   # If.body has 4 children
    assert new_nodes[2]["value"][0]["value"] == ""
    assert len(new_nodes[2]["value"][1]["value"]) == 1   # If.body has 1 child
    assert new_nodes[2]["value"][1]["value"][0]["value"] == ""
    assert new_nodes[2]["value"][2]["value"] == ""
    assert new_nodes[2]["value"][3]["value"] == ""
    assert new_nodes[3]["value"] == ""
