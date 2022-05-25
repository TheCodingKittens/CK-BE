import json
import re
import uuid
from typing import Dict, List, Optional, Tuple

import libcst as cst

"""
Class to visit all the nodes relevant for the project
"""


class CustomVisitor(cst.CSTVisitor):
    def __init__(self):
        # store all the JSON content in a stack
        self.stack: List[Tuple[str, ...]] = []
        # initiate a JSON-Converter to create the JSON structure
        self.nodeToJSONConverter = NodeToJSONConverter()

    # ------------------------- GENERAL VISIT_NODE METHOD ----------------------
    def visit_node(self, node) -> Optional[bool]:
        json_objects = self.nodeToJSONConverter.create_json(node)
        if json_objects:
            for json_object in json_objects:
                self.stack.append(json_object)
                # print(json.dumps(json_object, indent=4, sort_keys=False))
        return False

    def visit_Assign(self, node: "Assign") -> Optional[bool]:
        return self.visit_node(node)

    def visit_AugAssign(self, node: "AugAssign") -> Optional[bool]:
        return self.visit_node(node)

    def visit_For(self, node: "For") -> Optional[bool]:
        return self.visit_node(node)

    def visit_If(self, node: "If") -> Optional[bool]:
        return self.visit_node(node)

    def visit_While(self, node: "While") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Comparison(self, node: "Comparison") -> Optional[bool]:
        return self.visit_node(node)

    def visit_BooleanOperation(self, node: "BooleanOperation") -> Optional[bool]:
        return self.visit_node(node)

    def visit_BinaryOperation(self, node: "BinaryOperation") -> Optional[bool]:
        return self.visit_node(node)

    def visit_UnaryOperation(self, node: "UnaryOperation") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Call(self, node: "Call") -> Optional[bool]:
        return self.visit_node(node)

    def visit_List(self, node: "List") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Dict(self, node: "Dict") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Subscript(self, node: "Subscript") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Tuple(self, node: "Tuple") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Expr(self, node: "Expr") -> Optional[bool]:
        json_objects = self.nodeToJSONConverter.create_json(node)
        if not json_objects:
            return True
        else:
            for json_object in json_objects:
                self.stack.append(json_object)
            return False


# This class defines a JSON converter, which is used to create JSON objects out of CSTNodes
class NodeToJSONConverter:
    def __init__(self):
        self.nodes = []
        self.revisitable_nodes = [
            "BinaryOperation",
            "BooleanOperation",
            "UnaryOperation",
            "Comparison",
            "Call",
            "Subscript",
            "List",
            "Dict",
            "Tuple",
        ]

    def create_json(self, node):

        json_objects = []

        # Use classname to get the type
        classname = node.__class__.__name__

        if classname == "Assign":
            json_objects = self.create_json_object_assign(node)
        elif classname == "AugAssign":
            json_objects = self.create_json_object_aug_assign(node)
        elif classname == "If" or classname == "While":
            json_objects = self.create_json_if_while(node)
        elif classname == "Comparison":
            json_objects = self.create_json_comparison(node)
        elif classname == "BooleanOperation" or classname == "BinaryOperation":
            json_objects = self.create_json_boolean_binary_operation(node)
        elif classname == "UnaryOperation":
            json_objects = self.create_json_unary_operation(node)
        elif classname == "For":
            json_objects = self.create_json_for(node)
        elif classname == "Call":
            json_objects = self.create_json_call(node)
        elif classname == "List":
            json_objects = self.create_json_list(node)
        elif classname == "Dict":
            json_objects = self.create_json_dict(node)
        elif classname == "Expr":
            json_objects = self.create_json_value_check(node)
        elif classname == "Subscript":
            json_objects = self.create_json_subscript(node)
        elif classname == "Tuple":
            json_objects = self.create_json_tuple(node)
        else:
            print("ERROR: Unknown node type")

        return json_objects

    # ---------------------- REVISIT NODES for a command ------------------
    def revisit_for_command(self, node):
        customVisitor = CustomVisitor()
        node.visit(customVisitor)
        return customVisitor.stack[0]["command"]

    # ---------------------- REVISIT NODES for nested json ------------------
    def revisit(self, node):
        customVisitor = CustomVisitor()
        node.visit(customVisitor)
        return customVisitor.stack

    # ---------------------------- ASSIGN --------------------------
    def create_json_object_assign(self, node):
        targets = node.targets
        value = node.value
        json_objects = []

        if value.__class__.__name__ in self.revisitable_nodes:
            var_value = self.revisit_for_command(value)
        else:
            var_value = value.value

        if targets[0].target.__class__.__name__ in self.revisitable_nodes:
            target_value = self.revisit_for_command(targets[0].target)
        else:
            target_value = targets[0].target.value

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": target_value + " = " + var_value,
            "nodes": [],
        }

        json_objects.append(data)

        return json_objects

    # ---------------------------- AUGMENTED ASSIGN ----------------------------
    def create_json_object_aug_assign(self, node):

        json_objects = []

        left = node.target.value
        if node.value.__class__.__name__ in self.revisitable_nodes:
            right = self.revisit_for_command(node.value)
        else:
            right = node.value.value

        type_text = node.operator._get_token()

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": left + " " + type_text + " " + right,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # --------------------------------- IF / WHILE -------------------------------
    def create_json_if_while(self, node):

        test = node.test
        body = node.body
        elseNode = node.orelse
        json_objects = []

        # if the test is a simple check (f.ex. if True   /   if a)
        if test.__class__.__name__ == "Name":
            value_test = test.value
        else:
            value_test = self.revisit_for_command(test)

        value_body = self.revisit(body)

        # For the If's, also include the else (if there) - with a recursive call
        if node.__class__.__name__ == "If" and elseNode is not None:
            value_else = self.revisit(elseNode)

            elseNode = {
                "node_id": str(uuid.uuid4()),
                "type": "If.else",  # no need to extract, always the same
                "nodes": value_else,  # NESTED
                "command": "else:",
            }

        type_test = node.__class__.__name__ + "." + "test"
        type_body = node.__class__.__name__ + "." + "body"

        test = {
            "node_id": str(uuid.uuid4()),
            "type": type_test,
            "command": node.__class__.__name__.lower() + " " + value_test + ":",
            "nodes": [],
        }
        body = {
            "node_id": str(uuid.uuid4()),
            "type": type_body,
            "nodes": value_body,  # NESTED
        }

        json_objects.append(test)
        json_objects.append(body)
        if elseNode is not None:
            json_objects.append(elseNode)

        return json_objects

    # --------------------------------- FOR -------------------------------
    def create_json_for(self, node):

        json_objects = []

        test_target = node.target
        test_function = node.iter
        body = node.body

        if test_target.__class__.__name__ in self.revisitable_nodes:
            test_target = self.revisit_for_command(test_target)
        else:
            test_target = test_target.value

        if test_function.__class__.__name__ in self.revisitable_nodes:
            test_function = self.revisit_for_command(test_function)
        else:
            test_function = test_function.value

        value_body = self.revisit(body)

        test = {
            "node_id": str(uuid.uuid4()),
            "type": "For.test",  # no need to extract, always the same
            "command": node.__class__.__name__.lower()
            + " "
            + test_target
            + " in "
            + test_function
            + ":",
            "nodes": [],
        }
        body = {
            "node_id": str(uuid.uuid4()),
            "type": "For.body",  # no need to extract, always the same
            "nodes": value_body,  # NESTED
        }

        json_objects.append(test)
        json_objects.append(body)

        return json_objects

    # --------------------------------- COMPARISON -------------------------------
    def create_json_comparison(self, node):

        json_objects = []

        if node.left.__class__.__name__ in self.revisitable_nodes:
            name = self.revisit_for_command(node.left)
        else:
            name = node.left.value

        command = ""
        for comparator in node.comparisons:
            command += " " + comparator.operator._get_token()
            if comparator.comparator.__class__.__name__ in self.revisitable_nodes:
                command += " " + self.revisit_for_command(comparator)
            else:
                command += " " + comparator.comparator.value

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": name + command,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # --------------------------------- BOOLEAN / BINARY OPERATION -------------------------------
    def create_json_boolean_binary_operation(self, node):

        json_objects = []

        if node.left.__class__.__name__ in self.revisitable_nodes:
            left = self.revisit_for_command(node.left)
        else:
            left = node.left.value

        if node.right.__class__.__name__ in self.revisitable_nodes:
            right = self.revisit_for_command(node.right)
        else:
            right = node.right.value

        type_text = node.operator._get_token()

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": left + " " + type_text + " " + right,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------ UNARY OPERATION ------------------------------
    def create_json_unary_operation(self, node):

        json_objects = []
        operator = node.operator._get_token()

        if node.expression.__class__.__name__ in self.revisitable_nodes:
            value = self.revisit_for_command(node.expression)
        else:
            value = node.expression.value

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": operator + value,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # -------------------------------------- CALL --------------------------------
    def create_json_call(self, node):

        json_objects = []

        if node.func.__class__.__name__ == "Name":
            type = node.func.value
        else:
            type = node.func.value.value + "." + node.func.attr.value

        # args are empty
        if not node.args:
            value = ""
        else:
            value = []
            for arg in node.args:
                paramType = arg.value.__class__.__name__
                if paramType in self.revisitable_nodes:
                    value.append(self.revisit_for_command(arg.value))
                else:
                    value.append(arg.value.value)
            value = ", ".join(value)

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": type + "(" + value + ")",
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------------ LIST ------------------------------------
    def create_json_list(self, node):

        json_objects = []
        elements = []

        for i in range(len(node.elements)):
            if node.elements[i].value.__class__.__name__ in self.revisitable_nodes:
                elements.append(self.revisit_for_command(node.elements[i].value))
            else:
                elements.append(node.elements[i].value.value)

        elements_as_string = "[" + ", ".join(elements) + "]"

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": elements_as_string,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------------ DICT ------------------------------------
    def create_json_dict(self, node):

        json_objects = []

        elements = []
        # iterate through key/value pairs
        for element in node.elements:

            if element.key.__class__.__name__ in self.revisitable_nodes:
                key = self.revisit_for_command(element.key)
            else:
                key = element.key.value

            if element.value.__class__.__name__ in self.revisitable_nodes:
                value = self.revisit_for_command(element.value)
            else:
                value = element.value.value

            elements.append(key + ": " + value)

        elements_as_string = "{" + ", ".join(elements) + "}"

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": elements_as_string,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------------ EXPR ------------------------------------
    def create_json_value_check(self, node):

        if node.value.__class__.__name__ in self.revisitable_nodes:
            return False

        json_objects = []

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": node.value.value,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------------ SUBSCRIPT ------------------------------------
    def create_json_subscript(self, node):

        json_objects = []

        element = node.value.value
        content_class = node.slice[0].slice

        if content_class.__class__.__name__ == "Index":
            if content_class.value.__class__.__name__ in self.revisitable_nodes:
                content = self.revisit(content_class.value)
            else:
                content = content_class.value.value

        elif content_class.__class__.__name__ == "Slice":
            if content_class.lower.__class__.__name__ in self.revisitable_nodes:
                lower = self.revisit_for_command(content_class.lower)
            else:
                lower = (
                    str(content_class.lower.value)
                    if content_class.lower != None
                    else ""
                )

            if content_class.upper.__class__.__name__ in self.revisitable_nodes:
                upper = self.revisit_for_command(content_class.upper)
            else:
                upper = (
                    str(content_class.upper.value)
                    if content_class.upper != None
                    else ""
                )

            if content_class.step.__class__.__name__ in self.revisitable_nodes:
                step = self.revisit_for_command(content_class.step)
            else:
                step = (
                    str(content_class.step.value) if content_class.step != None else ""
                )

            first_colon = (
                ":" if content_class.first_colon.__class__.__name__ == "Colon" else ""
            )

            second_colon = (
                ":" if content_class.second_colon.__class__.__name__ == "Colon" else ""
            )

            content = lower + first_colon + upper + second_colon + step

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": element + "[" + content + "]",
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------------ TUPLE ------------------------------------
    def create_json_tuple(self, node):

        json_objects = []

        elements = []
        for element in node.elements:
            if element.value.__class__.__name__ in self.revisitable_nodes:
                elements.append(self.revisit_for_command(element.value))
            else:
                elements.append(element.value.value)

        elements_as_string = "(" + ", ".join(elements) + ")"

        data = {
            "node_id": str(uuid.uuid4()),
            "type": "Line",
            "command": elements_as_string,
            "nodes": [],
        }

        json_objects.append(data)
        return json_objects
