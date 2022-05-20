import uuid
import libcst as cst
from typing import List, Optional, Tuple
import re


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

    def visit_Call(self, node: "Call") -> Optional[bool]:
        return self.visit_node(node)

    def visit_List(self, node: "List") -> Optional[bool]:
        return self.visit_node(node)

    def visit_Dict(self, node: "Dict") -> Optional[bool]:
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

    @staticmethod
    def extract_field(string, start_string, end_string):
        pattern = "{0}(.*?){1}".format(start_string, end_string)
        return re.search(pattern, string).group(1)

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
        else:
            print("ERROR: Unknown node type")

        return json_objects

    # ---------------------------- ASSIGN --------------------------
    def create_json_object_assign(self, node):

        targets = node.targets
        value = node.value
        json_objects = []

        # GRIGOR: Multiple assignments on one line, e.g. a,b=2,3
        if hasattr(value, "elements"):
            value_elements = value.elements
            target_elements = targets[0].target.elements

            for (value_element, target_element) in zip(value_elements, target_elements):
                var_value = self.extract_field(str(value_element), "value='", "',")
                var_name = self.extract_field(str(target_element), "value='", "',")

                data = {
                    "id": str(uuid.uuid4()),
                    "type": "Line",
                    "command": var_name + " = " + var_value
                }

                json_objects.append(data)

        # GRIGOR: One assignment only, e.g. a=3 / a=3+3
        else:

            if value.__class__.__name__ == "BinaryOperation" or value.__class__.__name__ == "Comparison":
                customVisitor = CustomVisitor()
                value.visit(customVisitor)
                var_value = customVisitor.stack[0]["command"]
            else:
                var_value = value.value
            var_name = targets[0].target.value

            data = {
                "id": str(uuid.uuid4()),
                "type": "Line",
                "command": var_name + " = " + var_value
            }

            json_objects.append(data)

        return json_objects

    # ---------------------------- AUGMENTED ASSIGN ----------------------------
    def create_json_object_aug_assign(self, node):

        json_objects = []

        left = node.target.value
        if node.value.__class__.__name__ == "BinaryOperation":
            customVisitor = CustomVisitor()
            node.value.visit(customVisitor)
            right = customVisitor.stack[0]["command"]
        else:
            right = node.value.value
        type = node.operator.__class__.__name__
        type_text = node.operator._get_token()

        data = {
            "id": str(uuid.uuid4()),
            "type": "Line",
            "command": left + " " + type_text + " " + right
        }

        json_objects.append(data)
        return json_objects

    # --------------------------------- IF / WHILE -------------------------------
    def create_json_if_while(self, node):

        test = node.test
        body = node.body
        elseNode = node.orelse
        json_objects = []

        # recursive calls to parse the test and body sections
        customVisitor = CustomVisitor()
        test.visit(customVisitor)
        value_test = customVisitor.stack[0]["command"]

        customVisitor = CustomVisitor()
        body.visit(customVisitor)
        value_body = customVisitor.stack

        # For the If's, also include the else (if there) - with a recursive call
        if node.__class__.__name__ == "If" and elseNode is not None:
            customVisitor = CustomVisitor()
            visited_else = elseNode.visit(customVisitor)
            value_else = customVisitor.stack
            elseNode = {
                "id": str(uuid.uuid4()),
                "type": "If.else",  # no need to extract, always the same
                "value": value_else,  # NESTED
                "command": "else:"
            }

        type_test = node.__class__.__name__ + "." + "test"
        type_body = node.__class__.__name__ + "." + "body"

        test = {
            "id": str(uuid.uuid4()),
            "type": type_test,
            "command": node.__class__.__name__.lower() + " " + value_test + ":"
        }
        body = {
            "id": str(uuid.uuid4()),
            "type": type_body,
            "value": value_body  # NESTED
        }

        json_objects.append(test)
        json_objects.append(body)
        if elseNode is not None:
            json_objects.append(elseNode)

        return json_objects

    # --------------------------------- FOR -------------------------------
    def create_json_for(self, node):

        json_objects = []

        test_target = node.target.value
        test_function = node.iter
        body = node.body

        # recursive calls to parse the test and body sections
        if test_function.__class__.__name__ == "Call":
            customVisitor = CustomVisitor()
            test_function.visit(customVisitor)
            value_test = customVisitor.stack[0]["command"]
        else:
            value_test = test_function.value

        customVisitor = CustomVisitor()
        body.visit(customVisitor)
        value_body = customVisitor.stack

        test = {
            "id": str(uuid.uuid4()),
            "type": "For.test",  # no need to extract, always the same
            "command": node.__class__.__name__.lower() + " " + test_target + " in " + value_test + ":"
        }
        body = {
            "id": str(uuid.uuid4()),
            "type": "For.body",  # no need to extract, always the same
            "value": value_body  # NESTED
        }

        json_objects.append(test)
        json_objects.append(body)

        return json_objects

    # --------------------------------- COMPARISON -------------------------------
    def create_json_comparison(self, node):

        json_objects = []

        name = node.left.value
        comparator = node.comparisons[0].comparator.value
        comparison_type = (
                node.__class__.__name__
                + "."
                + node.children[1].children[0].__class__.__name__
        )
        type_text = node.comparisons[0].operator._get_token()

        data = {
            "id": str(uuid.uuid4()),
            "type": "Line",
            "command": name + " " + type_text + " " + comparator
        }

        json_objects.append(data)
        return json_objects

    # --------------------------------- BOOLEAN / BINARY OPERATION -------------------------------
    def create_json_boolean_binary_operation(self, node):

        json_objects = []

        if node.left.__class__.__name__ == "BinaryOperation":
            customVisitor = CustomVisitor()
            node.left.visit(customVisitor)
            left = customVisitor.stack[0]["command"]
        else:
            left = node.left.value

        right = node.right.value
        type = node.operator.__class__.__name__
        type_text = node.operator._get_token()

        data = {
            "id": str(uuid.uuid4()),
            "type": "Line",
            "command": left + " " + type_text + " " + right
        }

        json_objects.append(data)
        return json_objects

    # -------------------------------------- CALL --------------------------------
    def create_json_call(self, node):

        json_objects = []

        type = node.func.value
        # args are empty
        if not node.args:
            value = ""
        else:
            paramType = node.args[0].value.__class__.__name__
            if (
                    paramType == "BinaryOperation"
                    or paramType == "BooleanOperation"
                    or paramType == "Comparison"
            ):
                customVisitor = CustomVisitor()
                node.args[0].value.visit(customVisitor)
                value = customVisitor.stack[0]["command"]
            else:
                value = node.args[0].value.value

        data = {
            "id": str(uuid.uuid4()),
            "type": "Line",
            "command": type + "(" + value + ")",
        }

        json_objects.append(data)
        return json_objects

    # ------------------------------------ LIST ------------------------------------
    def create_json_list(self, node):

        json_objects = []

        return json_objects

    # ------------------------------------ DICT ------------------------------------
    def create_json_dict(self, node):

        json_objects = []

        return json_objects

    # ------------------------------------ EXPR ------------------------------------
    def create_json_value_check(self, node):

        # return false in case any other Expression than "Name" is found (ignore the Expr-node)
        if node.value.__class__.__name__ != "Name":
            return False

        json_objects = []

        data = {
            "id": str(uuid.uuid4()),
            "type": "Line",
            "command": node.value.value,
        }

        json_objects.append(data)
        return json_objects
