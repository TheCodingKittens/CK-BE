import base64

from app.models.base64 import Base64Type
from app.services.executor import Executor


def test_simple_expression(executor: Executor):
    command = Base64Type(b"1 + 1 + 1")

    result = executor.exec_expression(command)

    assert result == 3


def test_simple_expression_with_error(executor: Executor):
    command = Base64Type(b"1 +")

    result = executor.exec_expression(command)

    assert isinstance(result, Exception)


def test_complex_expression(executor: Executor):
    command = Base64Type(
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

    result = executor.exec_expression(command)

    assert isinstance(result, SyntaxError)


def test_complex_expression_with_error(executor: Executor):
    command = Base64Type(
        b"""
a = 1
b = 2
return_me = a + b"""
    )

    result = executor.exec_expression(command)

    assert isinstance(result, Exception)


def test_simple_stdout(executor: Executor):
    command = Base64Type(
        b"""
a = 3
print(a)
b = a + 4
print(b)"""
    )

    result = executor.exec_stdout(command)

    assert result == "3\n7\n"


def test_complex_stdout(executor: Executor):
    command = Base64Type(
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

    result = executor.exec_stdout(command)

    assert result == "3\n7\n6\n3\n"


def test_simple_module(executor: Executor):
    command = Base64Type(
        b"""
a = 3
print(a)
b = a + 4
print(b)"""
    )

    result = executor.exec_module(command)

    assert result == {"a": 3, "b": 7, "stdout": "3\n7\n"}


def test_complex_module(executor: Executor):
    command = Base64Type(
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

    result = executor.exec_module(command)

    assert result == {"a": 5, "b": 7, "stdout": "3\n7\n6\n3\n"}


def test_complex_module_with_error(executor: Executor):
    command = Base64Type(
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

    result = executor.exec_module(command)

    assert isinstance(result, Exception)


def test_command(executor: Executor):
    command = Base64Type(
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

    result = executor.exec_command(command)

    assert result == {"a": 5, "b": 7, "stdout": "3\n7\n6\n3\n"}


def test_command_with_error(executor: Executor):
    command = Base64Type(b"1 y")

    result = executor.exec_command(command)

    assert isinstance(result, Exception)


def test_command_with_complex_syntax_error(executor: Executor):

    command = Base64Type(
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

    result = executor.exec_command(command)

    assert isinstance(result, SyntaxError)
