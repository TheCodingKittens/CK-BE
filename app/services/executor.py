import contextlib
import sys
from io import StringIO
from typing import List

from app.models.base64 import Base64Type
from fastapi import HTTPException

"""
Class to execute the incoming strings from the frontend
"""


# @contextlib.contextmanager
# def stdoutIO(stdout=None):
#     old = sys.stdout
#     if stdout is None:
#         stdout = StringIO()
#     sys.stdout = stdout
#     yield stdout
#     sys.stdout = old


class Executor:
    def __init__(self):
        pass

    # def exec_expression(self, endoced_expression: Base64Type):
    #     try:

    #         expression = endoced_expression.decode_str()
    #         exec(f"""locals()['temp'] = {expression}""")

    #         return locals()["temp"]
    #     except Exception as e:
    #         return e

    # def exec_stdout(self, module: Base64Type):
    #     try:
    #         with stdoutIO() as s:
    #             exec(module.decode_str())
    #             return s.getvalue()

    #     except Exception as e:
    #         return e

    # def exec_command(self, command: Base64Type):
    #     try:
    #         simple_expression = self.exec_expression(command)
    #         if not isinstance(simple_expression, Exception):
    #             return simple_expression
    #         else:
    #             return self.exec_module(command)

    #     except Exception as e:
    #         return e

    def exec_module(self, module: Base64Type):
        try:
            # Get the Output of the module
            # stdout = {"stdout": self.exec_stdout(module)}

            # Creating the exec
            # globalsParameter = {"__builtins__": None}
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
            # Get the Output of the module
            # stdout = {"stdout": self.exec_stdout(module)}

            # Creating the exec
            # globalsParameter = {"__builtins__": None}
            localsParameter = history

            # Get the Variables of the module
            exec(module.decode_str(), globals(), localsParameter)

            # return dict(localsParameter | stdout)
            return localsParameter

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
