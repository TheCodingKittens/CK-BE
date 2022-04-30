from typing import Dict, List, Optional, Tuple

import libcst as cst
from app.models.command import Command
from app.models.command_data import CommandData
from app.services.nodetojson import NodeToJSONConverter


class CustomVisitor(cst.CSTVisitor):
    def __init__(self):
        # store all the JSON content
        self.stack: List[Tuple[str, ...]] = []
        # store the annotations
        # self.annotations: Dict[
        #     Tuple[str, ...],  # key: tuple of canonical class/function name
        #     Tuple[cst.Parameters, Optional[cst.Annotation]],  # value: (params, returns)
        # ] = {}

    # --------------------------------- ASSIGN -------------------------------
    def visit_Assign(self, node: "Assign") -> Optional[bool]:
        print("---------- VISITED ASSIGN! ----------")
        nodeToJSONConverter = NodeToJSONConverter(node)
        json_objects = nodeToJSONConverter.json_objects
        for json_object in json_objects:
            self.stack.append(json_object)
            # print(json.dumps(json_object, indent=4, sort_keys=False))

    # --------------------------------- FOR -------------------------------
    def visit_For(self, node: "For") -> Optional[bool]:
        print("---------- VISITED FOR! ----------")
        nodeToJSONConverter = NodeToJSONConverter(node)
        json_objects = nodeToJSONConverter.json_objects
        for json_object in json_objects:
            self.stack.append(json_object)
            # print(json.dumps(json_object, indent=4, sort_keys=False))

    # --------------------------------- IF -------------------------------
    def visit_If(self, node: "If") -> Optional[bool]:
        print("---------- VISITED IF! ----------")
        nodeToJSONConverter = NodeToJSONConverter(node)
        json_objects = nodeToJSONConverter.json_objects
        for json_object in json_objects:
            self.stack.append(json_object)
            # print(json.dumps(json_object, indent=4, sort_keys=False))

    # --------------------------------- COMPARISON -------------------------------
    def visit_Comparison(self, node: "Comparison") -> Optional[bool]:
        print("---------- VISITED COMPARISON! ----------")
        nodeToJSONConverter = NodeToJSONConverter(node)
        json_objects = nodeToJSONConverter.json_objects
        for json_object in json_objects:
            self.stack.append(json_object)
            # print(json.dumps(json_object, indent=4, sort_keys=False))


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

    def parse_module(self, module: str) -> cst.Module:
        try:

            parsed_module = cst.parse_module(module)
            visted_module = parsed_module.visit(self.visitor)

            return visted_module

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
