import json
import re
import uuid
from typing import Dict, List, Optional, Tuple

from app.services.visitor import CustomVisitor


# This class defines a JSON converter, which is used to create JSON objects out of CSTNodes
class NodeToJSONConverter:
    def __init__(self):
        self.nodes = []

    @staticmethod
    def extract_field(string, start_string, end_string):
        pattern = "{0}(.*?){1}".format(start_string, end_string)
        return re.search(pattern, string).group(1)

    # --------------------------------- ASSIGN -------------------------------
    # TODO change structure so that "type" is "Assign"
    def create_json(self, node):

        json_objects = []

        match (node.__class__.__name__):
            case "Assign":
                json_objects = self.create_json_object_assign(node)
            case "If":
                json_objects = self.create_json_if(node)
            case "Comparison":
                json_objects = self.create_json_comparison(node)
            case _:
                print("ERROR: Unknown node type")

        return json_objects

    def create_json_object_assign(self, node):

        targets = node.targets
        value = node.value
        json_objects = []

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
                json_objects.append(data)

        # GRIGOR: One assignment only, e.g. a=3
        else:
            var_value = self.extract_field(str(value), "value=", ",")
            var_name = self.extract_field(str(targets[0]), "value=", ",")
            var_type = self.extract_field(str(node), "value=", "\\(")

            data = {
                "id": str(uuid.uuid4()),
                "type": var_type,
                "name": var_name,
                "value": var_value,
            }
            json_objects.append(data)

        return json_objects

    # --------------------------------- IF -------------------------------
    def create_json_if(self, node):

        test = node.test
        body = node.body
        json_objects = []

        # recursive calls to parse the test and body sections
        customVisitor = CustomVisitor()
        visited_test = test.visit(customVisitor)
        value_test = customVisitor.content

        customVisitor = CustomVisitor()
        visited_body = body.visit(customVisitor)
        value_body = customVisitor.content

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

        json_objects.append(test)
        json_objects.append(body)

        return json_objects

    # --------------------------------- COMPARISON -------------------------------
    def create_json_comparison(self, node):

        json_objects = []

        # TODO make CommandData objects out of it
        id = str(uuid.uuid4())
        data = {
            "id": id,
            "type": "Comparison.Equal",  # TODO extract (can be different things)
            "left": "a",  # TODO extract
            "right": "3",  # TODO extract
        }
        json_objects.append(data)

        return json_objects
