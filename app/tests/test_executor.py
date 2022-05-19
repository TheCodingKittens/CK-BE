import base64

from app.models.base64 import Base64Type
from app.services.executor import Executor

# def test_simple_expression(executor: Executor):
#     command = Base64Type(base64.b64encode(b"1 + 1"))

#     output = executor.exec_expression(command)

#     assert result == 2


# def test_simple_expression_with_error(executor: Executor):
#     command = Base64Type(base64.b64encode(b"1 +"))

#     result = executor.exec_expression(command)

#     assert isinstance(result, Exception)


# def test_complex_expression(executor: Executor):
#     command = Base64Type(
#         base64.b64encode(
#             b"""
# a = 3
# print(a)
# b = a + 4
# print(b)
# a = 5
# if a > 4:
#     print(a+1)
# print(3)"""
#         )
#     )

#     result = executor.exec_expression(command)

#     assert isinstance(result, SyntaxError)


# def test_complex_expression_with_error(executor: Executor):
#     command = Base64Type(
#         base64.b64encode(
#             b"""
# a = 1
# b = 2
# return_me = a + b"""
#         )
#     )

#     result = executor.exec_expression(command)

#     assert isinstance(result, Exception)


# def test_simple_stdout(executor: Executor):
#     command = Base64Type(
#         base64.b64encode(
#             b"""
# a = 3
# print(a)
# b = a + 4
# print(b)"""
#         )
#     )

#     result = executor.exec_stdout(command)

#     assert result == "3\n7\n"


# def test_complex_stdout(executor: Executor):
#     command = Base64Type(
#         base64.b64encode(
#             b"""
# a = 3
# print(a)
# b = a + 4
# print(b)
# a = 5
# if a > 4:
#     print(a+1)
# print(3)"""
#         )
#     )

#     result = executor.exec_stdout(command)

#     assert result == "3\n7\n6\n3\n"


def test_simple_module(executor: Executor):
    command = Base64Type(
        base64.b64encode(
            b"""
a = 3
print(a)
b = a + 4
print(b)"""
        )
    )

    result = executor.exec_module(command)

    # assert result == {"a": 3, "b": 7, "stdout": "3\n7\n"}
    assert result == {"a": 3, "b": 7}


def test_complex_module(executor: Executor):
    command = Base64Type(
        base64.b64encode(
            b"""
a = 3
print(a)
b = a + 4
print(b)
a = 5
if a > 4:
    print(a+1)
print(3)"""
        )
    )

    result = executor.exec_module(command)

    # assert result == {"a": 5, "b": 7, "stdout": "3\n7\n6\n3\n"}
    assert result == {"a": 5, "b": 7}


def test_complex_module_with_error(executor: Executor):
    command = Base64Type(
        base64.b64encode(
            b"""
a = 3
print(a)
b = a + 4
print(b)
a = 5
if a > 4:
print(a+1)
print(3)"""
        )
    )

    result = executor.exec_module(command)

    assert isinstance(result, Exception)



def test_command_with_error(executor: Executor):
    command = Base64Type(base64.b64encode(b"1 y"))

    result = executor.exec_module(command)

    assert isinstance(result, Exception)



def test_dupicate_variable(executor: Executor):
    command = Base64Type(
        base64.b64encode(
            b"""
1 + 1
print(1 + 1)
a = 2
    """
        )
    )

    result = executor.exec_module(command)

    # assert result == {"a": 2, "stdout": "2\n"}
    assert result == {"a" : 2}


# def test_dupicate_variable(executor: Executor):
#     command = Base64Type(
#         base64.b64encode(
#             b"""
# 1 + 1
#     """
#         )
#     )

#     result = executor.exec_expression(command)

#     assert result == 2


def test_multiple_commands(executor: Executor):
    command1 = b"""1 + 1"""
    command2 = b"""2 + 2"""
    command3 = b"""a = 3
print(a)
print(1 + 3)
2+2"""

    result_1 = executor.exec_module(Base64Type(base64.b64encode(command1)))
    result_2 = executor.exec_module(Base64Type(base64.b64encode(command2)))
    result_3 = executor.exec_module(Base64Type(base64.b64encode(command3)))

    # assert result_1 == 2
    # assert result_2 == 4
    # assert result_3 == {"a": 3, "stdout": "3\n4\n"}
    assert result_1 == {}
    assert result_2 == {}
    assert result_3 == {"a": 3}


def test_pass_chain(executor: Executor):
    command_1 = b"""b = 2"""
    command_2 = b"""2 + 2"""
    command_3 = b"""a = 3
print(a)
print(1 + 3)
2+2"""

    history = []
    history.append(Base64Type(base64.b64encode(command_1)))
    history.append(Base64Type(base64.b64encode(command_2)))
    history.append(Base64Type(base64.b64encode(command_3)))

    result = executor.exec_command_history(history)

    # assert result == {"a": 3, "stdout": "3\n4\n"}
    assert result == {"a": 3, "b" : 2}


def test_execute_module(executor: Executor):
    
    command = b"""a = 3"""

    result = executor.exec_module(Base64Type(base64.b64encode(command)))

    assert result == {"a" : 3}


def test_execute_long_module(executor: Executor):
    
    command = b"""a = 5
b = 2 + 2
if a > 4:
    c = 3"""

    result = executor.exec_module(Base64Type(base64.b64encode(command)))
    
    assert result == {"a" : 5, "b" : 4, "c" : 3}


def test_multiple_modules(executor: Executor):

    command1 = b"2 + 1"
    command2 = b"a = 5"
    command3 = b"b = a"
    new_command = b"""if b == 5:
    c = b + 1
    a = 4"""

    history = []
    history.append(Base64Type(base64.b64encode(command1)))
    history.append(Base64Type(base64.b64encode(command2)))
    history.append(Base64Type(base64.b64encode(command3)))

    # fetch the old variables
    vars_until_command3 = executor.exec_command_history(history)
    assert vars_until_command3 == {"a" : 5, "b" : 5}

    # execute the new command with the old variables as a basis
    decoded_new_command = Base64Type(base64.b64encode(new_command))
    new_vars = executor.exec_module_from_history(decoded_new_command, vars_until_command3)

    assert new_vars == {"a" : 4, "b" : 5, "c" : 6}

