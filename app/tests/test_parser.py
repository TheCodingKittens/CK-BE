from typing import List

import libcst as cst
from app.models.base64 import Base64Type
from app.services.parser import Parser


def test_parse_module(parser: Parser):

    user_input = "if 1 == 1: pass"

    module = cst.parse_module(user_input)
    # the parse_module function from libcst returns Module
    assert isinstance(module, cst.Module)

    base64_command = Base64Type(user_input.encode())

    module = parser.parse_module(base64_command)
    # the parse_module function from our parser returns a list of JSON objects
    assert isinstance(module, List)



