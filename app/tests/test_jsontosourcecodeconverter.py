import base64

from app.models.base64 import Base64Type
from app.services.json_to_source_code_converter import JSONToSourceCodeConverter
from app.services.parser import Parser


def create_bytecode(command: str) -> Base64Type:
    return Base64Type(base64.b64encode(str.encode(command)))


def test_if(parser: Parser):
    source_code = """
a = 2
b = 3
if a > b:
    print('a is larger than b!')
    """

    byte_code = create_bytecode(source_code)
    json = parser.parse_module(byte_code)

    jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

    generated_source_code = jsonToSourceCodeConverter.generate_source_code()

    assert generated_source_code.replace("\n", "").replace("\t", "").replace(
        " ", ""
    ) == source_code.replace("\n", "").replace("\t", "").replace(" ", "")


def test_if_else(parser: Parser):
    source_code = """
a = 2
b = 3
if a > b:
    print('a is larger than b!')
else:
    print('b is larger than a!')
    """

    byte_code = create_bytecode(source_code)
    json = parser.parse_module(byte_code)

    jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

    generated_source_code = jsonToSourceCodeConverter.generate_source_code()

    assert generated_source_code.replace("\n", "").replace("\t", "").replace(
        " ", ""
    ) == source_code.replace("\n", "").replace("\t", "").replace(" ", "")


def test_for(parser: Parser):
    source_code = """
upper_bound = 100
a = 0
for i in range(upper_bound):
    a += i
    """

    byte_code = create_bytecode(source_code)
    json = parser.parse_module(byte_code)

    jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

    generated_source_code = jsonToSourceCodeConverter.generate_source_code()

    assert generated_source_code.replace("\n", "").replace("\t", "").replace(
        " ", ""
    ) == source_code.replace("\n", "").replace("\t", "").replace(" ", "")


def test_while(parser: Parser):
    source_code = """
isValid = True
while isValid == True:
    print('isValid is true ...')
    """

    byte_code = create_bytecode(source_code)
    json = parser.parse_module(byte_code)

    jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

    generated_source_code = jsonToSourceCodeConverter.generate_source_code()

    assert generated_source_code.replace("\n", "").replace("\t", "").replace(
        " ", ""
    ) == source_code.replace("\n", "").replace("\t", "").replace(" ", "")


def test_block(parser: Parser):
    source_code = """
a = 5
b = 2
isValid = True
if a > b:
    while a > 5:
        b += 1
    isValid = False
c = 50
for i in range(c):
    print('Hello world!')
    if i == c:
        print('we are at the end!')
    else:
        print('we are still going ...')
    """

    byte_code = create_bytecode(source_code)
    json = parser.parse_module(byte_code)

    jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

    generated_source_code = jsonToSourceCodeConverter.generate_source_code()

    assert generated_source_code.replace("\n", "").replace("\t", "").replace(
        " ", ""
    ) == source_code.replace("\n", "").replace("\t", "").replace(" ", "")
