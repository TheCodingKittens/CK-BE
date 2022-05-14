import base64

from app.models.base64 import Base64Type
from app.models.command import UserInput


def test_create_userinput():
    command_type = Base64Type(b"1 + 1")

    userinput = UserInput(command=command_type, token="Diego")

    assert userinput.command.encode_str() == "MSArIDE="


def test_create_userinput_base64():
    command_type = Base64Type(b"MSArIDE=")
    userinput = UserInput(command=command_type, token="Diego")

    assert userinput.command.decode_str() == "1 + 1"
