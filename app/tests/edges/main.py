import json
import uuid

import libcst as cst
import jsonpickle
from EdgeCreator import EdgeCreator
from JSONToSourceCodeConverter import JSONToSourceCodeConverter
from NodeToJSONConverter import NodeToJSONConverter
from NodeEditor import NodeEditor
from NodeEditVerifier import NodeEditVerifier
from typing import List, Optional, Tuple
import re
import unittest


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

    # TODO create an overall method that is called for every node type
    # def on_visit(self, node: cst.CSTNode) -> bool:
    #     self.visit_node(node)


"""
[
    {
        "id": "3ab52d3a-28b8-49a1-818b-456a960dd03e",
        "type": "Line",
        "command": "a = 2"
    },
    {
        "id": "187db028-c64d-4089-9062-690f97c1e9e5",
        "type": "Line",
        "command": "b = 3"
    },
    {
        "id": "40980123-964a-49c3-9962-1b9e862b9903",
        "type": "If.test",
        "command": "if a > 2:"
    },
    {
        "id": "daf771f5-84ed-472d-a03f-f0425a9fd43e",
        "type": "If.body",
        "value": [
            {
                "id": "2e841dc9-d631-429c-b0a0-511e2a40c7b2",
                "type": "If.test",
                "command": "if a > 4:"
            },
            {
                "id": "4d6998a3-0442-4fec-8ae5-466e608a627e",
                "type": "If.body",
                "value": [
                    {
                        "id": "7e19e44a-afb3-49b5-a63d-8f4ee4fad791",
                        "type": "Line",
                        "command": "b = 5"
                    }
                ]
            },
            {
                "id": "844da790-6bbb-4a33-8e35-fa85402e7279",
                "type": "Line",
                "command": "a = 4"
            }
        ]
    },
    {
        "id": "2ff72c7e-ad36-47e3-8dd1-1c57e30202c8",
        "type": "If.test",
        "command": "if b > 20:"
    },
    {
        "id": "9de84851-fe88-422b-ae72-e2021b120daa",
        "type": "If.body",
        "value": [
            {
                "id": "da8cace0-bea2-443c-9f09-b68314534a1e",
                "type": "While.test",
                "command": "while a > 10:"
            },
            {
                "id": "e83088a2-95fe-47f3-9faf-8599f3aaf3a6",
                "type": "While.body",
                "value": [
                    {
                        "id": "6d83436d-198d-475d-9057-56822bf7b53d",
                        "type": "Line",
                        "command": "a = 1"
                    }
                ]
            },
            {
                "id": "87b3aa68-4419-4ef0-8f34-c71ce0b9e485",
                "type": "Line",
                "command": "c = 19"
            }
        ]
    },
    {
        "id": "c25c4365-c6d1-48fe-a5da-f9542e3ec4bf",
        "type": "Line",
        "command": "c = 1"
    },
    {
        "id": "be8b68d5-c5a4-4b48-bfed-8785230788a8",
        "type": "If.test",
        "command": "if a > b:"
    },
    {
        "id": "e16cc61a-ffd9-4fb3-bf33-7b49d3836e71",
        "type": "If.body",
        "value": [
            {
                "id": "853b1b79-61a6-4e19-9df6-da6e6fe42f47",
                "type": "While.test",
                "command": "while c > 10:"
            },
            {
                "id": "90fd5fd6-2609-4108-9f2b-cfbe2dd5d772",
                "type": "While.body",
                "value": [
                    {
                        "id": "6a7806bc-b336-4a92-abbf-55964b5761cc",
                        "type": "Line",
                        "command": "b = 40"
                    }
                ]
            }
        ]
    },
    {
        "id": "22e4d6cd-a577-45fa-9aa1-7c75dad5f559",
        "type": "Line",
        "command": "isValid = False"
    }
]
"""

example_sources = {
    'block_1':
        '''
a = 2
b = 3

if a > 2:
    if a > 4:
        b = 5
    a = 4

if b > 20:
    while a > 10:
        a = 1
    c = 19
    
c = 1

if a > b:
    a = 100
    for i in range(10):
        print(i)
    
isValid = False
''',
    'block_2':
        '''
a = 2
b = 3

if a > 2:
    if a > 4:
        b = 5
    a = 4
else:
    c = 5

if b > 20:
    for i in range(10):
        a = 1
    c = 19
    
c = 1

if a > b:
    a = 100
    while c < 10:
        b = 40
    
isValid = False
''',
    'block_3':
        '''
a = 2
b = 3
if a > b:
    while a > b:
        a += 1
c = a + b
''',
    'kyrill_code':
        '''
if a > 1:
    b = 0
    print('it worked!')
c = True
'''
}

print("\n", "--------------- CONTENT: ---------------")
demo = cst.parse_module(example_sources['block_1'])
customVisitor = CustomVisitor()
visited = demo.visit(customVisitor)
json_objects = customVisitor.stack

# ----------------- GENERATING SOURCE CODE FROM JSON -----------------
# jsonToSourceCodeConverter = JSONToSourceCodeConverter(json_objects)
# print(jsonToSourceCodeConverter.generate_source_code())

# ----------------- CREATING EDGES -----------------
# TODO: If.else not working properly ... discuss with group
edgeCreator = EdgeCreator(json_objects)
edgeCreator.create_edges()
edgeCreator.create_readable_edges(show_ids=False, show_output=True)


# ----------------- EDITING NODES -----------------
# node_to_edit_id = json_objects[0]['id']
#
# nodeEditor = NodeEditor(json_objects)
# nodeEditor.edit_node(
#     node_id=node_to_edit_id,
#     new_command='d == 30'
# )

# nodeEditVerifier = NodeEditVerifier(
#     command_wrapper_id=uuid.uuid4(),
#     node_to_edit_id=node_to_edit_id,
#     new_command='g = 22.5',
#     json_objects=json_objects
# )
# is_legal_node_edit = nodeEditVerifier.is_legal_edit()
#
# if is_legal_node_edit:
#     pass  # reflect the changes in the database
# else:
#     pass  # throw an error and display this to the user on the front-end

class TestEdgeCreator(unittest.TestCase):
    def test_edges_correctly_created(self):
        edgeCreator = EdgeCreator(json_data=json_objects)
        edgeCreator.create_edges()
        edgeCreator.create_readable_edges(show_ids=False)

        correct_edges = [
            {'from': 'a = 2', 'to': 'b = 3'},
            {'from': 'b = 3', 'to': 'if a > 2:'},
            {'from': 'if a > 2:', 'to': 'If.body'},
            {'from': 'if a > 2:', 'to': 'if b > 20:'},
            {'from': 'If.body', 'to': 'if b > 20:'},
            {'from': 'if a > 4:', 'to': 'If.body', 'parent': 'If.body'},
            {'from': 'if a > 4:', 'to': 'a = 4', 'parent': 'If.body'},
            {'from': 'If.body', 'to': 'a = 4', 'parent': 'If.body'},
            {'from': 'b = 5', 'to': None},
            {'from': 'a = 4', 'to': None},
            {'from': 'if b > 20:', 'to': 'If.body'},
            {'from': 'if b > 20:', 'to': 'c = 1'},
            {'from': 'If.body', 'to': 'c = 1'},
            {'from': 'while a > 10:', 'to': 'While.body', 'parent': 'If.body'},
            {'from': 'while a > 10:', 'to': 'c = 19', 'parent': 'If.body'},
            {'from': 'While.body', 'to': 'while a > 10:', 'parent': 'If.body'},
            {'from': 'a = 1', 'to': None},
            {'from': 'c = 19', 'to': None},
            {'from': 'c = 1', 'to': 'if a > b:'},
            {'from': 'if a > b:', 'to': 'If.body'},
            {'from': 'if a > b:', 'to': 'isValid = False'},
            {'from': 'If.body', 'to': 'isValid = False'},
            {'from': 'a = 100', 'to': 'for i in range(10):', 'parent': 'If.body'},
            {'from': 'for i in range(10):', 'to': 'For.body', 'parent': 'If.body'},
            {'from': 'For.body', 'to': 'for i in range(10):', 'parent': 'If.body'},
            {'from': 'print(i)', 'to': None},
            {'from': 'isValid = False', 'to': None}
        ]

        self.assertEqual(correct_edges, edgeCreator.readable_edges)


if __name__ == '__main__':
    unittest.main()
