import libcst as cst
from app.services.parser import Parser


def test_pass_module(parser: Parser):

    user_input = "if 1 == 1: pass"
    module = parser.parse_module(user_input)

    assert isinstance(module, cst.Module)
