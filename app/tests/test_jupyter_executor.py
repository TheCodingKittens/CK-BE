import base64

from app.models.base64 import Base64Type
from app.services.jupyter_executor import ExecutorJuypter


def test_jupyter_output1(jupyterexecutor: ExecutorJuypter):

    # specify the commands to be executed
    command1 = b"""1 + 1"""
    command2 = b"""2 + 2"""
    command3 = b"""a = 3
print(a)
print(1 + 3)
2+2"""

    commands = []
    commands.append(Base64Type(base64.b64encode(command1)))
    commands.append(Base64Type(base64.b64encode(command2)))
    commands.append(Base64Type(base64.b64encode(command3)))

    # actually execute the notebook
    outputs = jupyterexecutor.run_notebook(commands)

    assert len(outputs) == 3
    assert outputs[0] == "2"
    assert outputs[1] == "4"
    assert outputs[2] == "3\n4\n"


def test_jupyter_output2(jupyterexecutor: ExecutorJuypter):
    commands = []

    commands.append(Base64Type(base64.b64encode(b"a = 2")))
    commands.append(Base64Type(base64.b64encode(b"a")))
    commands.append(Base64Type(base64.b64encode(b"1 + 1")))
    commands.append(Base64Type(base64.b64encode(b"a = 3")))
    commands.append(Base64Type(base64.b64encode(b"a")))
    commands.append(Base64Type(base64.b64encode(b"b = 4")))
    commands.append(Base64Type(base64.b64encode(b"a = b + 1")))
    commands.append(Base64Type(base64.b64encode(b"a")))
    commands.append(Base64Type(base64.b64encode(b"a + b")))
    commands.append(Base64Type(base64.b64encode(b"c = a + b")))

    outputs = jupyterexecutor.run_notebook(commands)

    assert len(outputs) == 5
    assert outputs[0] == "2"
    assert outputs[1] == "2"
    assert outputs[2] == "3"
    assert outputs[3] == "5"
    assert outputs[4] == "9"


def test_jupyter_output_new_entry(jupyterexecutor: ExecutorJuypter):
    history = []

    history.append(Base64Type(base64.b64encode(b"a = 2")))
    history.append(Base64Type(base64.b64encode(b"a")))
    history.append(Base64Type(base64.b64encode(b"1 + 4")))
    history.append(Base64Type(base64.b64encode(b"a = 3")))
    history.append(Base64Type(base64.b64encode(b"a")))
    history.append(Base64Type(base64.b64encode(b"b = 4")))

    jupyterexecutor.run_notebook(history)

    new_command = b"""if b > 3:
    print("b is",b)
else:
    print("Else")"""
    new_command_encoded = Base64Type(base64.b64encode(new_command))

    outputs = jupyterexecutor.run_new_command(new_command_encoded)

    assert len(outputs) == 4
    assert outputs[0] == "2"
    assert outputs[1] == "5"
    assert outputs[2] == "3"
    assert outputs[3] == "b is 4\n"
