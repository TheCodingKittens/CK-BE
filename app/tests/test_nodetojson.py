import libcst as cst
from app.services.nodetojson import NodeToJSONConverter
from app.services.parser import Parser


def test_if_node(parser: Parser):

    command = """
if a == 3:
    value = 6"""

    parsed_module = parser.parse_module(command)

    if_node = NodeToJSONConverter(parsed_module.body[0])

    assert if_node.json_objects != []


def test_assign_node(parser: Parser):

    command = """a = 3"""

    parsed_module = parser.parse_module(command)

    assign_node = None

    isinstance

    if isinstance(parsed_module.body[0], cst.SimpleStatementLine):
        assign_node = NodeToJSONConverter(parsed_module.body[0].body[0])

    assert assign_node.json_objects != []


def test_for_node(parser: Parser):

    command = """
for i in range(5):
    value = i"""

    parsed_module = parser.parse_module(command)

    for_node = NodeToJSONConverter(parsed_module.body[0])
