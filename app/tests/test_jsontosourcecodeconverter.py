# import libcst as cst

# from CustomVisitor import CustomVisitor
# from JSONToSourceCodeConverter import JSONToSourceCodeConverter


# def test_if():
#     source_code = '''
# a = 2
# b = 3
# if a > b:
#     print('a is larger than b!')
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json = customVisitor.stack

#     jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

#     generated_source_code = jsonToSourceCodeConverter.generate_source_code()

#     assert generated_source_code.replace("\n", "").replace("\t", "").replace(" ", "") == \
#            source_code.replace("\n", "").replace("\t", "").replace(" ", "")


# def test_if_else():
#     source_code = '''
# a = 2
# b = 3
# if a > b:
#     print('a is larger than b!')
# else:
#     print('b is larger than a!')
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json = customVisitor.stack

#     jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

#     generated_source_code = jsonToSourceCodeConverter.generate_source_code()

#     assert generated_source_code.replace("\n", "").replace("\t", "").replace(" ", "") == \
#            source_code.replace("\n", "").replace("\t", "").replace(" ", "")


# def test_for():
#     source_code = '''
# upper_bound = 100
# a = 0
# for i in range(upper_bound):
#     a += i
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json = customVisitor.stack

#     jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

#     generated_source_code = jsonToSourceCodeConverter.generate_source_code()

#     assert generated_source_code.replace("\n", "").replace("\t", "").replace(" ", "") == \
#            source_code.replace("\n", "").replace("\t", "").replace(" ", "")


# def test_while():
#     source_code = '''
# isValid = True
# while isValid == True:
#     print('isValid is true ...')
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json = customVisitor.stack

#     jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

#     generated_source_code = jsonToSourceCodeConverter.generate_source_code()

#     assert generated_source_code.replace("\n", "").replace("\t", "").replace(" ", "") == \
#            source_code.replace("\n", "").replace("\t", "").replace(" ", "")


# def test_block():
#     source_code = '''
# a = 5
# b = 2
# isValid = True
# if a > b:
#     while a > 5:
#         b += 1
#     isValid = False
# c = 50
# for i in range(c):
#     print('Hello world!')
#     if i == c:
#         print('we are at the end!')
#     else:
#         print('we are still going ...')
#     '''

#     demo = cst.parse_module(source_code)
#     customVisitor = CustomVisitor()
#     _ = demo.visit(customVisitor)
#     json = customVisitor.stack

#     jsonToSourceCodeConverter = JSONToSourceCodeConverter(json)

#     generated_source_code = jsonToSourceCodeConverter.generate_source_code()

#     assert generated_source_code.replace("\n", "").replace("\t", "").replace(" ", "") == \
#            source_code.replace("\n", "").replace("\t", "").replace(" ", "")


# test_if()
# test_for()
# test_while()
# test_if_else()
# test_block()
