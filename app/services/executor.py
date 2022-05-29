import copy
import types
from io import StringIO
from typing import List

from app.models.base64 import Base64Type
from fastapi import HTTPException

"""
Class to execute the incoming strings from the frontend
"""


class Executor:
    def __init__(self):
        pass

    def exec_module(self, module: Base64Type):
        try:

            localsParameter = {}

            # Get the Variables of the module
            exec(module.decode_str(), globals(), localsParameter)

            # return dict(localsParameter | stdout)
            return localsParameter

        except Exception as e:
            return e

    def exec_command_history(self, command_history: List[Base64Type]):
        output = {}
        try:
            for command in command_history:
                output = dict(self.exec_module_from_history(command, output))

            return output
        except Exception as e:
            return e

    # executes a module, taking a dict with variables as an input
    def exec_module_from_history(self, module: Base64Type, history: dict):
        try:
            localsParameter = copy.deepcopy(history)
            # Execute the module to get the new variables
            exec(module.decode_str(), globals(), localsParameter)

        except Exception as error:
            if isinstance(error, SyntaxError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Syntax Error: {error}, msg: {error.text}",
                )
            raise HTTPException(status_code=400, detail=str(error))

        self.check_for_classes_and_functions(localsParameter)

        return localsParameter

    def check_for_classes_and_functions(self, vars: dict):

        # If any class or function definition is encountered -> throw an error
        for var_value in vars.values():
            if isinstance(var_value, type):
                raise HTTPException(
                    status_code=400, detail="Class definitions are not allowed!"
                )
            elif isinstance(var_value, types.FunctionType):
                raise HTTPException(
                    status_code=400, detail="Function definitions are not allowed!"
                )
