import pdb


def test_exe():

    the_code = """
a = 1
b = 2
return_me = a + b
"""

    loc = {}
    exec(the_code, globals(), loc)
    return_workaround = loc["return_me"]
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