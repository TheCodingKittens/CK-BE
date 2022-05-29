import base64

from app.models.base64 import Base64Type
from app.services.edge_creator import EdgeCreator
from app.services.parser import Parser


def create_bytecode(command: str) -> Base64Type:
    return Base64Type(base64.b64encode(str.encode(command)))


def test_edge_creation(parser: Parser):
    source_code = """
a = 2
b = 3

if a > 2:
    if a > 4:
        b = 5
    a = 4

if b > 20:
    while a > 10:
        a = 1
    c = 19

c = 1

if a > b:
    a = 100
    for i in range(10):
        print(i)

isValid = False
    """

    byte_code = create_bytecode(source_code)
    json_objects = parser.parse_module(byte_code)

    edgeCreator = EdgeCreator(json_data=json_objects)
    edgeCreator.create_edges()
    edgeCreator.create_readable_edges(show_ids=False)

    correct_edges = [
        {"from": "a = 2", "to": "b = 3"},
        {"from": "b = 3", "to": "if a > 2:"},
        {"from": "if a > 2:", "to": "If.body"},
        {"from": "if a > 2:", "to": "if b > 20:"},
        {"from": "If.body", "to": "if b > 20:"},
        {"from": "if a > 4:", "to": "If.body", "parent": "If.body"},
        {"from": "if a > 4:", "to": "a = 4", "parent": "If.body"},
        {"from": "If.body", "to": "a = 4", "parent": "If.body"},
        {"from": "b = 5", "to": None},
        {"from": "a = 4", "to": None},
        {"from": "if b > 20:", "to": "If.body"},
        {"from": "if b > 20:", "to": "c = 1"},
        {"from": "If.body", "to": "c = 1"},
        {"from": "while a > 10:", "to": "While.body", "parent": "If.body"},
        {"from": "while a > 10:", "to": "c = 19", "parent": "If.body"},
        {"from": "While.body", "to": "while a > 10:", "parent": "If.body"},
        {"from": "a = 1", "to": None},
        {"from": "c = 19", "to": None},
        {"from": "c = 1", "to": "if a > b:"},
        {"from": "if a > b:", "to": "If.body"},
        {"from": "if a > b:", "to": "isValid = False"},
        {"from": "If.body", "to": "isValid = False"},
        {"from": "a = 100", "to": "for i in range(10):", "parent": "If.body"},
        {"from": "for i in range(10):", "to": "For.body", "parent": "If.body"},
        {"from": "For.body", "to": "for i in range(10):", "parent": "If.body"},
        {"from": "print(i)", "to": None},
        {"from": "isValid = False", "to": None},
    ]

    assert correct_edges == edgeCreator.readable_edges


def test_parent_assignment(parser: Parser):
    source_code = """
if a > b:
    if c > d:
        for i in range(10):
            a = 2
            b = 3
            c = 4
    """

    byte_code = create_bytecode(source_code)
    json_objects = parser.parse_module(byte_code)

    edgeCreator = EdgeCreator(json_data=json_objects)
    edgeCreator.create_edges()
    edgeCreator.create_readable_edges(show_ids=False)

    parents = []

    for edge in edgeCreator.readable_edges:
        if "parent" in edge:
            parents.append(edge)

    correct_parents = [
        {"from": "if c > d:", "to": "If.body", "parent": "If.body"},
        {"from": "for i in range(10):", "to": "For.body", "parent": "If.body"},
        {"from": "For.body", "to": "for i in range(10):", "parent": "If.body"},
        {"from": "a = 2", "to": "b = 3", "parent": "For.body"},
        {"from": "b = 3", "to": "c = 4", "parent": "For.body"},
    ]

    assert correct_parents == parents


def test_executed_edges(parser: Parser):
    source_code = """
a = 4
b = 2
if a > b:
    print('a is larger than b!')
else:
    print('a is smaller than :(')
finished = True
    """

    byte_code = create_bytecode(source_code)
    json_objects = parser.parse_module(byte_code)

    edgeCreator = EdgeCreator(json_data=json_objects)
    edgeCreator.create_edges()
    edgeCreator.create_readable_edges(show_ids=False)

    correct_edges = [
        {"from": "a = 4", "to": "b = 2", "executed": True},
        {"from": "b = 2", "to": "if a > b:", "executed": True},
        {"from": "if a > b:", "to": "If.body", "executed": True},
        {"from": "if a > b:", "to": "else:", "executed": False},
        {"from": "If.body", "to": "finished = True", "executed": False},
        {"from": "else:", "to": "finished = True", "executed": False},
    ]

    assert correct_edges == edgeCreator.readable_edges


def test_executed_edges(parser: Parser):
    source_code = """
a = 4
b = 2
if a > b:
    print('a is larger than b!')
    """

    byte_code = create_bytecode(source_code)
    json_objects = parser.parse_module(byte_code)

    edgeCreator = EdgeCreator(json_data=json_objects)
    edgeCreator.create_edges()
    edgeCreator.create_readable_edges(show_ids=False)

    correct_edges = [
        {"from": "a = 4", "to": "b = 2", "executed": True},
        {"from": "b = 2", "to": "if a > b:", "executed": True},
        {"from": "if a > b:", "to": "If.body", "executed": True},
        {"from": "if a > b:", "to": "else:", "executed": False},
        {"from": "If.body", "to": "finished = True", "executed": False},
        {"from": "else:", "to": "finished = True", "executed": False},
    ]

    assert correct_edges == edgeCreator.readable_edges
