import json

import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

# create an ExecutePreprocessor
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
# create notebook
nb_in = nbf.v4.new_notebook()


def test_jupyter_output():

    # specify the commands to be executed
    command1 = """1 + 1"""
    command2 = """2 + 2"""
    command3 = """a = 3
print(a)
print(1 + 3)
2+2"""

    # add the command into a code cell
    nb_in['cells'] = [nbf.v4.new_code_cell(command1), 
                    nbf.v4.new_code_cell(command2), 
                    nbf.v4.new_code_cell(command3)]

    # actually execute the notebook
    nb_out = ep.preprocess(nb_in)

    # receive the cell outputs
    outputs = []
    for cell in nb_out[0]["cells"]:
        if cell["outputs"][0]["output_type"] == "stream":
            outputs.append(cell["outputs"][0]["text"])
        elif cell["outputs"][0]["output_type"] == "execute_result":
            outputs.append(cell["outputs"][0]["data"]["text/plain"])

    # print(json.dumps(outputs, indent=4))

    assert len(outputs) == 3
    assert outputs[0] == "2"
    assert outputs[1] == "4"
    assert outputs[2] == "3\n4\n"

    # print(nb_out)
    # print(type(nb_out[0]))
    # print(json.dumps(nb_out[0]["cells"], indent=4))
