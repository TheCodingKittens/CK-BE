from typing import List

import nbformat as nbf
from app.models.base64 import Base64Type
from nbconvert.preprocessors import ExecutePreprocessor


class ExecutorJuypter():
    def __init__(self):
        # create an ExecutePreprocessor
        self.ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        # create notebook
        self.nb_in = nbf.v4.new_notebook()
        self.cells = self.nb_in['cells']


    def create_cell(self, command: Base64Type):
        self.cells.append(nbf.v4.new_code_cell(command.decode_str()))


    def pre_process(self):
        return self.ep.preprocess(self.nb_in)
    

    # method to create a new cell and run the notebook again
    # MAY BE USED FOR NEW ENTRIES
    def run_new_command(self, command: Base64Type):
        self.create_cell(command)
        self.nb_out = self.pre_process()
        return self.fetch_output()


    # method to create a new notebook and run everything
    # MAY BE USED INITIALLY AND FOR CHANGES IN THE HISTORY
    def run_notebook(self, commands: List[Base64Type]):

        # create new notebook
        self.nb_in = nbf.v4.new_notebook()
        self.cells = self.nb_in['cells']

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



