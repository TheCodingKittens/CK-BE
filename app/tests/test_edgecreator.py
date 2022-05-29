import base64

from app.models.base64 import Base64Type
from app.services.edge_creator import EdgeCreator
from app.services.parser import Parser


def create_bytecode(command: str) -> Base64Type:
    return Base64Type(base64.b64encode(str.encode(command)))


def test_edge_creation(parser: Parser):
    source_code = """
numbers = [1, 2, 7, 8, 12, 4, 5, 9]
while numbers:
    number = numbers.pop()
    print(number)
for i in range(20):
    if i == 10:
        print('yay!')
    else:
        print('ney!')
"""

    byte_code = create_bytecode(source_code)
    json_objects = parser.parse_module(byte_code)

    edgeCreator = EdgeCreator(json_data=json_objects)
    edgeCreator.create_edges()

    correct_edges = [
        {
            "from": "numbers = [1, 2, 7, 8, 12, 4, 5, 9]",
            "to": "while numbers:",
            "parent": None,
            "executed": True,
        },
        {
            "from": "while numbers:",
            "to": "While.body",
            "parent": None,
            "executed": True,
        },
        {
            "from": "while numbers:",
            "to": "for i in range(20):",
            "parent": None,
            "executed": True,
        },
        {
            "from": "While.body",
            "to": "while numbers:",
            "parent": None,
            "executed": True,
        },
        {
            "from": "number = numbers.pop()",
            "to": "print(number)",
            "parent": "While.body",
            "executed": True,
        },
        {
            "from": "for i in range(20):",
            "to": "For.body",
            "parent": None,
            "executed": True,
        },
        {
            "from": "For.body",
            "to": "for i in range(20):",
            "parent": None,
            "executed": True,
        },
        {
            "from": "if i == 10:",
            "to": "If.body",
            "parent": "For.body",
            "executed": True,
        },
        {"from": "if i == 10:", "to": "else:", "parent": "For.body", "executed": False},
    ]

    for edge in edgeCreator.readable_edges:
        if not edge["parent"]:
            edge["parent"] = None

        if edge["executed"] == "true":
            edge["executed"] = True
        else:
            edge["executed"] = False

    edgeCreator.display_readable_edges()

    assert correct_edges == edgeCreator.readable_edges
