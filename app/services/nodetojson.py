import json
import re
import uuid
from typing import Dict, List, Optional, Tuple

import libcst as cst


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


class NodeToJSONConverter:
    def __init__(self, Node):
        self.json_objects = []
        self.node = Node

        match (self.node.__class__.__name__):
            case "Assign":
                self.create_json_object_assign()
            case "If":
                self.create_json_if()
            case "Comparison":
                self.create_json_comparison()
            case _:
                print("ERROR: Unknown node type")

    @staticmethod
    def extract_field(string, start_string, end_string):
        pattern = "{0}(.*?){1}".format(start_string, end_string)
        return re.search(pattern, string).group(1)

    # --------------------------------- ASSIGN -------------------------------
    def create_json_object_assign(self):
        targets = self.node.targets
        value = self.node.value

        # GRIGOR: Multiple assignments on one line, e.g. a,b=2,3
        if hasattr(value, "elements"):
            value_elements = value.elements
            target_elements = targets[0].target.elements

            for (value_element, target_element) in zip(value_elements, target_elements):
                var_value = self.extract_field(str(value_element), "value=", ",")
                var_name = self.extract_field(str(target_element), "value=", ",")
                var_type = self.extract_field(str(value_element), "value=", "\\(")

                data = {
                    "id": str(uuid.uuid4()),
                    "type": var_type,
                    "name": var_name,
                    "value": var_value,
                }
                self.json_objects.append(data)

        # GRIGOR: One assignment only, e.g. a=3
        else:
            var_value = self.extract_field(str(value), "value=", ",")
            var_name = self.extract_field(str(targets[0]), "value=", ",")
            var_type = self.extract_field(str(self.node), "value=", "\\(")

            data = {
                "id": str(uuid.uuid4()),
                "type": var_type,
                "name": var_name,
                "value": var_value,
            }
            self.json_objects.append(data)

        return {}

    # --------------------------------- IF -------------------------------
    def create_json_if(self):

        test = self.node.test
        body = self.node.body
        # print("TEST:")
        # print(test)
        # print("BODY:")
        # print(body)

        # recursive calls to parse the test and body sections
        customVisitor = CustomVisitor()
        visited_test = test.visit(customVisitor)
        value_test = customVisitor.stack

        customVisitor = CustomVisitor()
        visited_body = body.visit(customVisitor)
        value_body = customVisitor.stack

        # TODO make CommandData objects out of it
        id = str(uuid.uuid4())
        test = {
            "id": id,
            "type": "If.test",  # no need to extract, always the same
            "name": "somename1",  # could probably be empty?
            "value": value_test,
        }
        body = {
            "id": id,
            "type": "If.body",  # no need to extract, always the same
            "name": "somename2",  # could probably be empty?
            "value": value_body,
        }

        self.json_objects.append(test)
        self.json_objects.append(body)

    # --------------------------------- COMPARISON -------------------------------
    def create_json_comparison(self):

        # print("CHILDREN")
        # print(self.node.children)

        # TODO make CommandData objects out of it
        id = str(uuid.uuid4())
        data = {
            "id": id,
            "type": "Comparison.Equal",  # TODO extract (can be different things)
            "left": "a",  # TODO extract
            "right": "3",  # TODO extract
        }
        self.json_objects.append(data)
