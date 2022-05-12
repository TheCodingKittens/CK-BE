import contextlib
import sys
from io import StringIO

from app.models.base64 import Base64Type

"""
Class to execute the incoming strings from the frontend
"""


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class Executor:
    def __init__(self):
        pass

    def exec_expression(self, endoced_expression: Base64Type):
        try:

            expression = endoced_expression.decode_str()
            exec(f"""locals()['temp'] = {expression}""")
            print(locals)
            return locals()["temp"]
        except Exception as e:
            return e

    def exec_stdout(self, module: Base64Type):
        try:
            with stdoutIO() as s:
                exec(module.decode_str())
                return s.getvalue()

        except Exception as e:
            return e

    def exec_module(self, module: Base64Type):
        try:
            stdout = {"stdout": self.exec_stdout(module)}
            # globalsParameter = {"__builtins__": None}
            localsParameter = {}
            exec(module.decode_str(), globals(), localsParameter)

            return dict(localsParameter | stdout)

        except Exception as e:
            return e

    def exec_command(self, command: Base64Type):

        try:
            simple_expression = self.exec_expression(command)
            if not isinstance(simple_expression, Exception):
                return simple_expression
            else:
                return self.exec_module(command)

        except Exception as e:
            return e
