from typing import List

import nbformat as nbf
from app.models.base64 import Base64Type
from fastapi import HTTPException
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor


class ExecutorJuypter:
    def __init__(self):
        # create an ExecutePreprocessor
        self.ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    def create_cell(self, command: Base64Type):
        self.cells.append(nbf.v4.new_code_cell(command.decode_str()))

    def pre_process(self):
        return self.ep.preprocess(self.nb_in)

    def run_new_command(self, command: Base64Type):
        self.create_cell(command)
        self.nb_out = self.pre_process()
        return self.fetch_output()

    def run_notebook(self, commands: List[Base64Type]):

        # create new notebook
        self.nb_in = nbf.v4.new_notebook()
        self.cells = self.nb_in["cells"]

        for command in commands:
            self.create_cell(command)
        # execute the notebook and return the output
        self.nb_out = self.pre_process()
        return self.fetch_output()

    def fetch_output(self):
        outputs = []
        for cell in self.nb_out[0]["cells"]:
            if not cell["outputs"]:
                continue
            if cell["outputs"][0]["output_type"] == "stream":
                outputs.append(cell["outputs"][0]["text"])
            elif cell["outputs"][0]["output_type"] == "execute_result":
                outputs.append(cell["outputs"][0]["data"]["text/plain"])

        return outputs

    # ------------ CREATE A NOTEBOOK FROM A HISTORY OF COMMANDS -------------
    def create_notebook_from_history(self, commands: List[Base64Type]):
        nb_in = nbf.v4.new_notebook()
        for command in commands:
            cell = nbf.v4.new_code_cell(command.decode_str())
            nb_in["cells"].append(cell)

        return nb_in

    # ------------ EXECUTE A GIVEN NOTEBOOK ------------
    def execute_notebook(self, nb):
        try:
            out = self.ep.preprocess(nb)
            return out
        except Exception as error:
            if isinstance(error, CellExecutionError):
                raise HTTPException(
                    status_code=400,
                    detail=f"{error.ename}: {error.evalue}",
                )
            raise HTTPException(status_code=400, detail=str(error))

    # ----- RUN NOTEBOOK FROM HISTORY AND NEW COMMAND. RETURNS OUTPUT OF NEW COMMAND -----
    def run_notebook_given_history_and_new_command(
        self, commandHistory: List[Base64Type], newCommand: Base64Type
    ):
        nb_in = nbf.v4.new_notebook()

        # create cells for the entire history
        for command in commandHistory:
            cell = nbf.v4.new_code_cell(command.decode_str())
            nb_in["cells"].append(cell)

        # create a cell for the new command
        newCell = nbf.v4.new_code_cell(newCommand.decode_str())
        nb_in["cells"].append(newCell)

        # execute the notebook
        nb_out = self.execute_notebook(nb_in)

        # get and return the outputs of the last cell
        return self.get_output_of_last_cell(nb_out)

    # ----- RUN NOTEBOOK FROM HISTORY. RETURNS ALL OUTPUTS -----
    def run_notebook_given_history(self, commandHistory: List[Base64Type]):
        nb_in = nbf.v4.new_notebook()

        # create cells for the entire history
        for command in commandHistory:
            cell = nbf.v4.new_code_cell(command.decode_str())
            nb_in["cells"].append(cell)

        # execute the notebook
        nb_out = self.execute_notebook(nb_in)

        # get and return the outputs of each cell
        return self.get_output_of_each_cell(nb_out)

    # -------------------- MAY BE USED FOR NEW COMMANDS ---------------------
    def get_output_of_last_cell(self, nb_out):

        # access the last cell
        last_cell = nb_out[0]["cells"][-1]

        # return the output (if available)
        if not last_cell["outputs"]:
            return ""
        elif last_cell["outputs"][0]["output_type"] == "stream":
            return last_cell["outputs"][0]["text"]
        elif last_cell["outputs"][0]["output_type"] == "execute_result":
            return last_cell["outputs"][0]["data"]["text/plain"]

    # -------------------- MAY BE USED FOR EDITING NODES ---------------------
    def get_output_of_each_cell(self, nb_out):

        # create a list containing an entry for EVERY cell
        all_outputs = []

        # add an output for every cell (even if empty)
        for cell in nb_out[0]["cells"]:
            if not cell["outputs"]:
                all_outputs.append("")
                continue
            if cell["outputs"][0]["output_type"] == "stream":
                all_outputs.append(cell["outputs"][0]["text"])
            elif cell["outputs"][0]["output_type"] == "execute_result":
                all_outputs.append(cell["outputs"][0]["data"]["text/plain"])

        return all_outputs
