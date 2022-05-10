from typing import List

import libcst as cst
from app.services.parser import Parser


def test_parse_module(parser: Parser):

    user_input = "if 1 == 1: pass"

    module = cst.parse_module(user_input)
    # the parse_module function from libcst returns Module
    assert isinstance(module, cst.Module)

    module = parser.parse_module(user_input)
    # the parse_module function from our parser returns a list of JSON objects
    assert isinstance(module, List)
