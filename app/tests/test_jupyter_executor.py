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

    # actually execute the notebook with all the given commands as cells
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



def test_jupyter_cell_output_individually(jupyterexecutor: ExecutorJuypter):

    history = []

    history.append(Base64Type(base64.b64encode(b"a = 2")))
    history.append(Base64Type(base64.b64encode(b"a")))
    history.append(Base64Type(base64.b64encode(b"1 + 4")))
    history.append(Base64Type(base64.b64encode(b"b = 1")))
    history.append(Base64Type(base64.b64encode(b"""if a == 3:
    print("IF")
else:
    print("ELSE")""")))
    history.append(Base64Type(base64.b64encode(b"3 + 5 + b")))

    nb = jupyterexecutor.create_notebook_from_history(history)
    all_cells_output = jupyterexecutor.get_output_of_each_cell(nb)

    # one output for every cell (even if empty) = num of cells
    assert len(all_cells_output) == 6
    assert all_cells_output[0] == ""
    assert all_cells_output[1] == "2"
    assert all_cells_output[2] == "5"
    assert all_cells_output[3] == ""
    assert all_cells_output[4] == "ELSE\n"
    assert all_cells_output[5] == "9"


# ----- Would be used in case of a new command entry (since all cells before already know their output) -----
def test_jupyter_last_cell_output(jupyterexecutor: ExecutorJuypter):

    history = []

    history.append(Base64Type(base64.b64encode(b"a = 2")))
    history.append(Base64Type(base64.b64encode(b"a")))
    history.append(Base64Type(base64.b64encode(b"1 + 4")))
    history.append(Base64Type(base64.b64encode(b"a = 3")))
    history.append(Base64Type(base64.b64encode(b"a")))

    new_command = (Base64Type(base64.b64encode(b"""if a == 3:
    print("a is 3")
print("Done")""")))

    last_cell_output = jupyterexecutor.run_notebook_given_history_and_new_command(history, new_command)

    assert last_cell_output == "a is 3\nDone\n"


# ----- Would be used in case of a command edit -----
def test_jupyter_run_notebook_given_history(jupyterexecutor: ExecutorJuypter):

    history = []

    history.append(Base64Type(base64.b64encode(b"a = 7")))
    history.append(Base64Type(base64.b64encode(b"a")))
    history.append(Base64Type(base64.b64encode(b"5 + 4 - 1")))
    history.append(Base64Type(base64.b64encode(b"b = 4")))
    history.append(Base64Type(base64.b64encode(b"""if a > 3:
    print("IF")
else:
    print("ELSE")""")))
    history.append(Base64Type(base64.b64encode(b"3 + 5 + b")))
    history.append(Base64Type(base64.b64encode(b"print(1/1)")))

    all_outputs = jupyterexecutor.run_notebook_given_history(history)

    assert len(all_outputs) == 7
    assert all_outputs[0] == ""
    assert all_outputs[1] == "7"
    assert all_outputs[2] == "8"
    assert all_outputs[3] == ""
    assert all_outputs[4] == "IF\n"
    assert all_outputs[5] == "12"
    assert all_outputs[6] == "1.0\n"
