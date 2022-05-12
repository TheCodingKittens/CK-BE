import contextlib

import sys
from io import StringIO



@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def exec_and_return(expression):
    try:
        exec(f"""locals()['temp'] = {expression}""")
        return locals()["temp"]
    except Exception as e:
        return e


def test_unassigned_variables():

    the_code = """1 + 1"""

    result = exec_and_return(the_code)

    assert result == 2


def test_unassigned_variables_syntax_error():

    the_code = """1 y 1"""

    try:
        exec_and_return(the_code)
    except Exception as e:
        assert e == SyntaxError


def test_exe():

    the_code = """
a = 1
b = 2
return_me = a + b
"""

    # TODO research globals vs locals to ensure nothing fishy happens
    loc = {}
    globalsParameter = {"__builtins__": None}
    localsParameter = {}
    exec(the_code, globalsParameter, localsParameter)
    return_workaround = localsParameter["return_me"]
    print(return_workaround)  # 3

    assert return_workaround == 3


def test_func():
    the_code = """
a=3
if a == 3:
    value = 6
"""

    loc = {}

    exec(the_code, globals(), loc)

    assert loc["a"] == 3
    assert loc["value"] == 6


def test_name_error():
    the_code = """
a=3
if b == 3:
    value = 6
"""

    loc = {}

    try:
        exec_and_return(the_code)
    except Exception as e:
        print(e)
        assert True


def test_syntax_error():
    the_code = """
a=3
if b == 3:
value = 6
"""

    loc = {}

    try:
        exec_and_return(the_code)
    except Exception as e:
        print(e)
        assert e == SyntaxError


def test_output():
    command1 = """print(1 + 1)"""

    with stdoutIO() as s1:
        exec(command1)

    value = s1.getvalue()

    assert value == "2\n"


def test__multiple_outputs():
    command1 = """
a = 3
print(a)
b = a + 4
print(b)"""

    command2 = """
a = 5
if a > 4:
    print(a+1)
print(3)"""

    with stdoutIO() as s1:
        exec(command1)

    assert s1.getvalue() == "3\n7\n"

    with stdoutIO() as s2:
        exec(command2)

    assert s2.getvalue() == "6\n3\n"
