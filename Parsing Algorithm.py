import libcst
import libcst as cst
from typing import List, Tuple, Dict, Optional
import json
import uuid
import re


class NodeToJSONConverter:
    def __init__(self, node):
        self.node = node
        self.json_objects = []
        if isinstance(node, libcst._nodes.statement.Assign):
            self.create_json_object_assign()

    @staticmethod
    def extract_field(string, start_string, end_string):
        pattern = '{0}(.*?){1}'.format(start_string, end_string)
        return re.search(pattern, string).group(1)

    def create_json_object_assign(self):
        targets = self.node.targets
        value = self.node.value

        # Multiple assignments on one line, e.g. a,b=2,3
        if hasattr(value, 'elements'):
            value_elements = value.elements
            target_elements = targets[0].target.elements

            for (value_element, target_element) in zip(value_elements, target_elements):
                var_value = self.extract_field(str(value_element), 'value=', ',')
                var_name = self.extract_field(str(target_element), 'value=', ',')
                var_type = self.extract_field(str(value_element), 'value=', '\\(')

                data = {'id': str(uuid.uuid4()), 'type': var_type, 'name': var_name, 'value': var_value}
                self.json_objects.append(data)
        # One assignment only, e.g. a=3
        else:
            var_value = self.extract_field(str(value), 'value=', ',')
            var_name = self.extract_field(str(targets[0]), 'value=', ',')
            var_type = self.extract_field(str(self.node), 'value=', '\\(')

            data = {'id': str(uuid.uuid4()), 'type': var_type, 'name': var_name, 'value': var_value}
            self.json_objects.append(data)

        return {}


class CustomVisitor(cst.CSTVisitor):
    def visit_Assign(self, node: "Assign") -> Optional[bool]:
        nodeToJSONConverter = NodeToJSONConverter(node)
        json_objects = nodeToJSONConverter.json_objects
        for json_object in json_objects:
            print(json.dumps(json_object, indent=4, sort_keys=False))

    def visit_For(self, node: "For") -> Optional[bool]:
        print(node)


class TypingCollector(cst.CSTVisitor):
    def __init__(self):
        # stack for storing the canonical name of the current function
        self.stack: List[Tuple[str, ...]] = []
        # store the annotations
        self.annotations: Dict[
            Tuple[str, ...],  # key: tuple of canonical class/function name
            Tuple[cst.Parameters, Optional[cst.Annotation]],  # value: (params, returns)
        ] = {}

    # def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
    #     self.stack.append(node.name.value)
    #
    # def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
    #     self.stack.append(node.name.value)
    #     self.annotations[tuple(self.stack)] = (node.params, node.returns)
    #     return (
    #         False
    #     )  # pyi files don't support inner functions, return False to stop the traversal.
    #
    # def visit_Assign(self, node: "Assign") -> Optional[bool]:
    #     self.annotations[tuple(self.stack)] = (node.value, node.targets)
    #     self.stack.append(node)
    #
    # def visit_For(self, node: "For") -> Optional[bool]:
    #     self.stack.append(node)
    #
    # def visit_For_body(self, node: "For") -> None:
    #     self.stack.append(node.body)

    def on_visit(self, node: "CSTNode") -> bool:
        for child in node.children:
            if not isinstance(child, libcst._nodes.whitespace.EmptyLine):
                print(child.children)


py_source = '''
a=2
for i in range(5):
    value = i
'''

demo = libcst.parse_module(py_source)
# print(libcst.parse_module(py_source))
customVisitor = TypingCollector()
_ = demo.visit(customVisitor)
stack = customVisitor.stack

print(customVisitor.annotations)
