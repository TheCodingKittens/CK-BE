from typing import Dict, List, Optional, Tuple

import libcst as cst
from app.models.command import Command
from app.models.command_data import CommandData
from app.services.visitor import CustomVisitor


class Parser:
    def __init__(self):
        self.visitor = CustomVisitor()

    def parse_binaryoperation(self, node: cst.BinaryOperation) -> List[CommandData]:
        try:
            left = CommandData(
                var_name=node.left.__class__.__name__,
                value=node.left.value,
                type=node.operator.__class__.__name__,
            )
            right = CommandData(
                var_name=node.right.__class__.__name__,
                value=node.right.value,
                type=node.operator.__class__.__name__,
            )

            result = [left, right]
            return result

        except cst.ParserSyntaxError as e:
            print("Error:", e)

    def parse_expression(self, command: str):
        try:
            return cst.parse_expression(command)

        except cst.ParserSyntaxError as e:
            print("Error:", e)

    def parse_module(self, module: str) -> List[Tuple[str, ...]]:
        try:

            self.visitor = CustomVisitor()

            parsed_module = cst.parse_module(module)
            visted_module = parsed_module.visit(self.visitor)

            return self.visitor.stack
            # return visted_module

        except cst.ParserSyntaxError as e:
            print("Error:", e)


# Example of how to Use the collector and transformer


py_source = '''
class PythonToken(Token):
    def __repr__(self):
        return ('TokenInfo(type=%s, string=%r, start_pos=%r, prefix=%r)' %
                self._replace(type=self.type.name))

def tokenize(code, version_info, start_pos=(1, 0)):
    """Generate tokens from a the source code (string)."""
    lines = split_lines(code, keepends=True)
    return tokenize_lines(lines, version_info, start_pos=start_pos)
'''

pyi_source = """
class PythonToken(Token):
    def __repr__(self) -> str: ...

def tokenize(
    code: str, version_info: PythonVersionInfo, start_pos: Tuple[int, int] = (1, 0)
) -> Generator[PythonToken, None, None]: ...
"""


# TODO: Improve upon these parsers
# source_tree = cst.parse_module(py_source)
# stub_tree = cst.parse_module(pyi_source)

# stub_tree.visit(visitor)
# transformer = TypingTransformer(visitor.annotations)
# modified_tree = source_tree.visit(transformer)

# LibCST Source Code
print("LibCST Source Code:")
# print(modified_tree.code)
