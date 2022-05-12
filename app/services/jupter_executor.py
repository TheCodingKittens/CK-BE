import json

import nbformat as nbf
from app.models.base64 import Base64Type
from nbconvert.preprocessors import ExecutePreprocessor
from typing import List


class ExecutorJuypter():
    def __init__(self):
        # create an ExecutePreprocessor
        self.ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        # create notebook
        self.nb_in = nbf.v4.new_notebook()
        self.cells = ['cells'] 

    def create_cell(self, command: Base64Type ):
        self.cells.append(nbf.v4.new_code_cell(command.decode_str()))

    
    def pre_process(self, command: str):
        self.ep.preprocess(self.nb_in)

    def run_notebook(self, commands: List[Base64Type]):
        
        for command in commands:
            self.create_cell(command)
        self.pre_process(self.nb_in)



