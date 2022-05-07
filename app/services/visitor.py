from typing import Dict, List, Optional, Tuple

import libcst as cst

# TODO has to be simplified so that
# class CustomVisitor(cst.CSTVisitor):
#     def __init__(self):
#         # store all the JSON content in a stack
#         self.stack: List[Tuple[str, ...]] = []
#         # initiate a JSON-Converter to create the JSON structure
#         self.nodeToJSONConverter = NodeToJSONConverter()

#     # TODO create an overall method that is called for every node type
#     # def on_visit(self, node: cst.CSTNode) -> bool:
#     #     print("HEY")
#     #     json_objects = self.nodeToJSONConverter.create_json(node)
#     #     for json_object in json_objects:
#     #         self.content.append(json_object)
#     #         # print(json.dumps(json_object, indent=4, sort_keys=False))
#     #     return False

#     # --------------------------------- ASSIGN -------------------------------
#     def visit_Assign(self, node: "Assign") -> Optional[bool]:
#         print("---------- VISITED ASSIGN! ----------")
#         json_objects = self.nodeToJSONConverter.create_json(node)
#         for json_object in json_objects:
#             self.stack.append(json_object)
#             # print(json.dumps(json_object, indent=4, sort_keys=False))
#         return False

#     # --------------------------------- FOR -------------------------------
#     def visit_For(self, node: "For") -> Optional[bool]:
#         print("---------- VISITED FOR! ----------")
#         json_objects = self.nodeToJSONConverter.create_json_for(node)
#         for json_object in json_objects:
#             self.stack.append(json_object)
#             # print(json.dumps(json_object, indent=4, sort_keys=False))
#         return False

#     # --------------------------------- IF -------------------------------
#     def visit_If(self, node: "If") -> Optional[bool]:
#         print("---------- VISITED IF! ----------")
#         json_objects = self.nodeToJSONConverter.create_json_if(node)
#         for json_object in json_objects:
#             self.stack.append(json_object)
#             # print(json.dumps(json_object, indent=4, sort_keys=False))
#         return False

#     # --------------------------------- COMPARISON -------------------------------
#     def visit_Comparison(self, node: "Comparison") -> Optional[bool]:
#         print("---------- VISITED COMPARISON! ----------")
#         json_objects = self.nodeToJSONConverter.create_json_comparison(node)
#         for json_object in json_objects:
#             self.stack.append(json_object)
#             # print(json.dumps(json_object, indent=4, sort_keys=False))
#         return False
