# import libcst as cst

# from CustomVisitor import CustomVisitor
# from EdgeCreator import EdgeCreator


# def test_edge_creation():
#     source_code = '''
# a = 2
# b = 3

# if a > 2:
#     if a > 4:
#         b = 5
#     a = 4

# if b > 20:
#     while a > 10:
#         a = 1
#     c = 19

# c = 1

# if a > b:
#     a = 100
#     for i in range(10):
#         print(i)

# isValid = False
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json_objects = customVisitor.stack

#     edgeCreator = EdgeCreator(json_data=json_objects)
#     edgeCreator.create_edges()
#     edgeCreator.create_readable_edges(show_ids=False)

#     correct_edges = [
#         {'from': 'a = 2', 'to': 'b = 3'},
#         {'from': 'b = 3', 'to': 'if a > 2:'},
#         {'from': 'if a > 2:', 'to': 'If.body'},
#         {'from': 'if a > 2:', 'to': 'if b > 20:'},
#         {'from': 'If.body', 'to': 'if b > 20:'},
#         {'from': 'if a > 4:', 'to': 'If.body', 'parent': 'If.body'},
#         {'from': 'if a > 4:', 'to': 'a = 4', 'parent': 'If.body'},
#         {'from': 'If.body', 'to': 'a = 4', 'parent': 'If.body'},
#         {'from': 'b = 5', 'to': None},
#         {'from': 'a = 4', 'to': None},
#         {'from': 'if b > 20:', 'to': 'If.body'},
#         {'from': 'if b > 20:', 'to': 'c = 1'},
#         {'from': 'If.body', 'to': 'c = 1'},
#         {'from': 'while a > 10:', 'to': 'While.body', 'parent': 'If.body'},
#         {'from': 'while a > 10:', 'to': 'c = 19', 'parent': 'If.body'},
#         {'from': 'While.body', 'to': 'while a > 10:', 'parent': 'If.body'},
#         {'from': 'a = 1', 'to': None},
#         {'from': 'c = 19', 'to': None},
#         {'from': 'c = 1', 'to': 'if a > b:'},
#         {'from': 'if a > b:', 'to': 'If.body'},
#         {'from': 'if a > b:', 'to': 'isValid = False'},
#         {'from': 'If.body', 'to': 'isValid = False'},
#         {'from': 'a = 100', 'to': 'for i in range(10):', 'parent': 'If.body'},
#         {'from': 'for i in range(10):', 'to': 'For.body', 'parent': 'If.body'},
#         {'from': 'For.body', 'to': 'for i in range(10):', 'parent': 'If.body'},
#         {'from': 'print(i)', 'to': None},
#         {'from': 'isValid = False', 'to': None}
#     ]

#     assert correct_edges == edgeCreator.readable_edges


# def test_parent_assignment():
#     source_code = '''
# if a > b:
#     if c > d:
#         for i in range(10):
#             a = 2
#             b = 3
#             c = 4
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json_objects = customVisitor.stack

#     edgeCreator = EdgeCreator(json_data=json_objects)
#     edgeCreator.create_edges()
#     edgeCreator.create_readable_edges(show_ids=False)

#     parents = []

#     for edge in edgeCreator.readable_edges:
#         if 'parent' in edge:
#             parents.append(edge)

#     correct_parents = [
#         {'from': 'if c > d:', 'to': 'If.body', 'parent': 'If.body'},
#         {'from': 'for i in range(10):', 'to': 'For.body', 'parent': 'If.body'},
#         {'from': 'For.body', 'to': 'for i in range(10):', 'parent': 'If.body'},
#         {'from': 'a = 2', 'to': 'b = 3', 'parent': 'For.body'},
#         {'from': 'b = 3', 'to': 'c = 4', 'parent': 'For.body'}
#     ]

#     assert correct_parents == parents


# test_edge_creation()
# test_parent_assignment()
