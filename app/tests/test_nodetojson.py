import base64

from app.models.base64 import Base64Type
from app.services.nodetojson import NodeToJSONConverter
from app.services.parser import Parser


def create_bytecode(command: str) -> Base64Type:
    return Base64Type(base64.b64encode(str.encode(command)))


def test_if(parser: Parser):

    command = """
if a == 3:
    value = 6"""

    byte_code = create_bytecode(command)

    parsed_command = parser.parse_module(byte_code)

    assert parsed_command[0]["type"] == "If.test"
    assert parsed_command[0]["command"] == "if a == 3:"
    assert parsed_command[1]["type"] == "If.body"
    assert len(parsed_command) == 2


def test_if_else(parser: Parser):

    command = """
if a == 5:
    a = 1
else:
    a = 2"""

    byte_code = create_bytecode(command)

    parsed_command = parser.parse_module(byte_code)

    assert parsed_command[0]["type"] == "If.test"
    assert parsed_command[0]["command"] == "if a == 5:"
    assert parsed_command[1]["type"] == "If.body"
    assert parsed_command[2]["type"] == "If.else"
    assert len(parsed_command) == 3


def test_while(parser: Parser):

    command = """
while a > 3:
    value = 6"""

    byte_code = create_bytecode(command)

    parsed_command = parser.parse_module(byte_code)

    assert parsed_command[0]["type"] == "While.test"
    assert parsed_command[0]["command"] == "while a > 3:"
    assert parsed_command[1]["type"] == "While.body"
    assert len(parsed_command) == 2


def test_assign(parser: Parser):

    command_1 = """a = 3"""
    command_2 = """a,b = 4,c"""

    byte_command_1 = create_bytecode(command_1)
    byte_command_2 = create_bytecode(command_2)

    command1_parsed = parser.parse_module(byte_command_1)
    command2_parsed = parser.parse_module(byte_command_2)

    assert command1_parsed[0]["type"] == "Line"
    assert command1_parsed[0]["command"] == "a = 3"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Line"
    assert command2_parsed[0]["command"] == "a = 4"

    assert command2_parsed[1]["type"] == "Line"
    assert command2_parsed[1]["command"] == "b = c"
    assert len(command2_parsed) == 2


def test_aug_assign(parser: Parser):

    command_1 = """a += 7"""
    command_2 = """b *= 2"""

    byte_command_1 = create_bytecode(command_1)
    byte_command_2 = create_bytecode(command_2)

    command1_parsed = parser.parse_module(byte_command_1)
    command2_parsed = parser.parse_module(byte_command_2)

    assert command1_parsed[0]["type"] == "Line"
    assert command1_parsed[0]["command"] == "a += 7"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Line"
    assert command2_parsed[0]["command"] == "b *= 2"
    assert len(command2_parsed) == 1


def test_assign_binary(parser: Parser):

    command_1 = """a = b + 1"""
    command_2 = """c %= t - 4"""

    byte_command_1 = create_bytecode(command_1)
    byte_command_2 = create_bytecode(command_2)

    command1_parsed = parser.parse_module(byte_command_1)
    command2_parsed = parser.parse_module(byte_command_2)

    assert command1_parsed[0]["type"] == "Line"
    assert command1_parsed[0]["command"] == "a = b + 1"

    assert command2_parsed[0]["type"] == "Line"
    assert command2_parsed[0]["command"] == "c %= t - 4"


def test_comparison(parser: Parser):

    command_1 = """a == 3"""
    command_2 = """b < 5"""
    command_3 = """c >= f"""

    byte_command_1 = create_bytecode(command_1)
    byte_command_2 = create_bytecode(command_2)
    byte_command_3 = create_bytecode(command_3)

    command1_parsed = parser.parse_module(byte_command_1)
    command2_parsed = parser.parse_module(byte_command_2)
    command3_parsed = parser.parse_module(byte_command_3)

    assert command1_parsed[0]["type"] == "Line"
    assert command1_parsed[0]["command"] == "a == 3"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Line"
    assert command2_parsed[0]["command"] == "b < 5"
    assert len(command2_parsed) == 1

    assert command3_parsed[0]["type"] == "Line"
    assert command3_parsed[0]["command"] == "c >= f"
    assert len(command3_parsed) == 1


def test_boolean_operation(parser: Parser):

    command_1 = "x and y"
    command_2 = "a or b"

    byte_command_1 = create_bytecode(command_1)
    byte_command_2 = create_bytecode(command_2)

    command1_parsed = parser.parse_module(byte_command_1)
    command2_parsed = parser.parse_module(byte_command_2)

    assert command1_parsed[0]["type"] == "Line"
    assert command1_parsed[0]["command"] == "x and y"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Line"
    assert command2_parsed[0]["command"] == "a or b"
    assert len(command2_parsed) == 1


def test_binary_operation(parser: Parser):

    command_1 = "1 + 2"
    command_2 = "4 * b"
    command_3 = "c / d"
    command_4 = """a ** 2"""

    byte_command_1 = create_bytecode(command_1)
    byte_command_2 = create_bytecode(command_2)
    byte_command_3 = create_bytecode(command_3)
    byte_command_4 = create_bytecode(command_4)

    command1_parsed = parser.parse_module(byte_command_1)
    command2_parsed = parser.parse_module(byte_command_2)
    command3_parsed = parser.parse_module(byte_command_3)
    command4_parsed = parser.parse_module(byte_command_4)

    assert command1_parsed[0]["type"] == "Line"
    assert command1_parsed[0]["command"] == "1 + 2"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Line"
    assert command2_parsed[0]["command"] == "4 * b"
    assert len(command2_parsed) == 1

    assert command3_parsed[0]["type"] == "Line"
    assert command3_parsed[0]["command"] == "c / d"
    assert len(command3_parsed) == 1

    assert command4_parsed[0]["type"] == "Line"
    assert command4_parsed[0]["command"] == "a ** 2"
    assert len(command4_parsed) == 1


# def test_for_node(parser: Parser):

#     command = """
# for i in range(5):
#     value = i"""

#     parsed_module = parser.parse_module(command)

#     for_node = NodeToJSONConverter(parsed_module.body[0])
