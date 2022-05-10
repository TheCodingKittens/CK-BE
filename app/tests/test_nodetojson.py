from app.services.nodetojson import NodeToJSONConverter
from app.services.parser import Parser


def test_if(parser: Parser):

    command = """
if a == 3:
    value = 6"""

    parsed_command = parser.parse_module(command)

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

    parsed_command = parser.parse_module(command)

    assert parsed_command[0]["type"] == "If.test"
    assert parsed_command[0]["command"] == "if a == 5:"
    assert parsed_command[1]["type"] == "If.body"
    assert parsed_command[2]["type"] == "If.else"
    assert len(parsed_command) == 3


def test_while(parser: Parser):

    command = """
while a > 3:
    value = 6"""

    parsed_command = parser.parse_module(command)

    assert parsed_command[0]["type"] == "While.test"
    assert parsed_command[0]["command"] == "while a > 3:"
    assert parsed_command[1]["type"] == "While.body"
    assert len(parsed_command) == 2


def test_assign(parser: Parser):

    command1 = """a = 3"""
    command2 = """a,b = 4,c"""

    command1_parsed = parser.parse_module(command1)
    command2_parsed = parser.parse_module(command2)

    assert command1_parsed[0]["type"] == "Assign"
    assert command1_parsed[0]["left"] == "a"
    assert command1_parsed[0]["right"] == "3"
    assert command1_parsed[0]["command"] == "a = 3"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Assign"
    assert command2_parsed[0]["left"] == "a"
    assert command2_parsed[0]["right"] == "4"
    assert command2_parsed[0]["command"] == "a = 4"

    assert command2_parsed[1]["type"] == "Assign"
    assert command2_parsed[1]["left"] == "b"
    assert command2_parsed[1]["right"] == "c"
    assert command2_parsed[1]["command"] == "b = c"
    assert len(command2_parsed) == 2


def test_aug_assign(parser: Parser):

    command1 = """a += 7"""
    command2 = """b *= 2"""

    command1_parsed = parser.parse_module(command1)
    command2_parsed = parser.parse_module(command2)

    assert command1_parsed[0]["type"] == "AddAssign"
    assert command1_parsed[0]["left"] == "a"
    assert command1_parsed[0]["right"] == "7"
    assert command1_parsed[0]["command"] == "a += 7"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "MultiplyAssign"
    assert command2_parsed[0]["left"] == "b"
    assert command2_parsed[0]["right"] == "2"
    assert command2_parsed[0]["command"] == "b *= 2"
    assert len(command2_parsed) == 1


def test_assign_binary(parser: Parser):

    command1 = """a = b + 1"""
    command2 = """c %= t - 4"""

    command1_parsed = parser.parse_module(command1)
    command2_parsed = parser.parse_module(command2)

    assert command1_parsed[0]["type"] == "Assign"
    assert command1_parsed[0]["left"] == "a"
    assert command1_parsed[0]["right"] == "b + 1"
    assert command1_parsed[0]["command"] == "a = b + 1"

    assert command2_parsed[0]["type"] == "ModuloAssign"
    assert command2_parsed[0]["left"] == "c"
    assert command2_parsed[0]["right"] == "t - 4"
    assert command2_parsed[0]["command"] == "c %= t - 4"


def test_comparison(parser: Parser):

    command1 = """a == 3"""
    command2 = """b < 5"""
    command3 = """c >= f"""

    command1_parsed = parser.parse_module(command1)
    command2_parsed = parser.parse_module(command2)
    command3_parsed = parser.parse_module(command3)

    assert command1_parsed[0]["type"] == "Comparison.Equal"
    assert command1_parsed[0]["left"] == "a"
    assert command1_parsed[0]["right"] == "3"
    assert command1_parsed[0]["command"] == "a == 3"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Comparison.LessThan"
    assert command2_parsed[0]["left"] == "b"
    assert command2_parsed[0]["right"] == "5"
    assert command2_parsed[0]["command"] == "b < 5"
    assert len(command2_parsed) == 1

    assert command3_parsed[0]["type"] == "Comparison.GreaterThanEqual"
    assert command3_parsed[0]["left"] == "c"
    assert command3_parsed[0]["right"] == "f"
    assert command3_parsed[0]["command"] == "c >= f"
    assert len(command3_parsed) == 1


def test_boolean_operation(parser: Parser):

    command1 = "x and y"
    command2 = "a or b"

    command1_parsed = parser.parse_module(command1)
    command2_parsed = parser.parse_module(command2)

    assert command1_parsed[0]["type"] == "And"
    assert command1_parsed[0]["left"] == "x"
    assert command1_parsed[0]["right"] == "y"
    assert command1_parsed[0]["command"] == "x and y"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Or"
    assert command2_parsed[0]["left"] == "a"
    assert command2_parsed[0]["right"] == "b"
    assert command2_parsed[0]["command"] == "a or b"
    assert len(command2_parsed) == 1


def test_binary_operation(parser: Parser):

    command1 = "1 + 2"
    command2 = "4 * b"
    command3 = "c / d"
    command4 = """a ** 2"""

    command1_parsed = parser.parse_module(command1)
    command2_parsed = parser.parse_module(command2)
    command3_parsed = parser.parse_module(command3)
    command4_parsed = parser.parse_module(command4)

    assert command1_parsed[0]["type"] == "Add"
    assert command1_parsed[0]["left"] == "1"
    assert command1_parsed[0]["right"] == "2"
    assert command1_parsed[0]["command"] == "1 + 2"
    assert len(command1_parsed) == 1

    assert command2_parsed[0]["type"] == "Multiply"
    assert command2_parsed[0]["left"] == "4"
    assert command2_parsed[0]["right"] == "b"
    assert command2_parsed[0]["command"] == "4 * b"
    assert len(command2_parsed) == 1

    assert command3_parsed[0]["type"] == "Divide"
    assert command3_parsed[0]["left"] == "c"
    assert command3_parsed[0]["right"] == "d"
    assert command3_parsed[0]["command"] == "c / d"
    assert len(command3_parsed) == 1

    assert command4_parsed[0]["type"] == "Power"
    assert command4_parsed[0]["left"] == "a"
    assert command4_parsed[0]["right"] == "2"
    assert command4_parsed[0]["command"] == "a ** 2"
    assert len(command4_parsed) == 1


# def test_for_node(parser: Parser):

#     command = """
# for i in range(5):
#     value = i"""

#     parsed_module = parser.parse_module(command)

#     for_node = NodeToJSONConverter(parsed_module.body[0])
