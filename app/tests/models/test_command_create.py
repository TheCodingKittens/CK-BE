from app.models.base64 import Base64Type
from app.models.command import CommandCreate, UserInput


def test_create_command():

    user_command = Base64Type(b"MSArIDE=")

    userinput = UserInput(command=user_command, token='01G3DHJGCNQ326S9G324K8XDA0')

    command = CommandCreate(
        command=userinput.command.data(), token=userinput.token, output="2"
    )

    assert command.command == b"MSArIDE="
