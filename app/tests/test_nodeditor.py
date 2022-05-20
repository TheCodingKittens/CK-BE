from NodeEditor import NodeEditor


def test_edit_line():
    original_json = [{'id': '02e88b54-fc85-4773-a8e3-969c4faded2f', 'type': 'Line', 'command': 'a = 2'},
                     {'id': '9f354214-a7d0-4434-bb62-66e64b0d1d5b', 'type': 'Line', 'command': 'b = 3'},
                     {'id': 'f69425df-6d02-43aa-8ac3-8b7da5b102a9', 'type': 'Line', 'command': 'c = False'}]

    nodeEditor = NodeEditor(original_json)
    nodeEditor.edit_node(
        node_id='f69425df-6d02-43aa-8ac3-8b7da5b102a9',
        new_command='c = True'
    )

    edited_json = [{'id': '02e88b54-fc85-4773-a8e3-969c4faded2f', 'type': 'Line', 'command': 'a = 2'},
                   {'id': '9f354214-a7d0-4434-bb62-66e64b0d1d5b', 'type': 'Line', 'command': 'b = 3'},
                   {'id': 'f69425df-6d02-43aa-8ac3-8b7da5b102a9', 'type': 'Line', 'command': 'c = True'}]

    assert edited_json == nodeEditor.json


def test_edit_if_test():
    original_json = [{'id': 'ea1bf960-9190-4b08-90fe-087ed681543f', 'type': 'Line', 'command': 'a = 2'},
                     {'id': '1003a91e-0c84-4a09-a120-ec8b0eab4753', 'type': 'Line', 'command': 'b = 3'},
                     {'id': '3ef4916b-e175-4613-af86-3c4fa9944ab1', 'type': 'If.test', 'command': 'if a > b:'},
                     {'id': '10caffaa-e7c3-485a-a16d-61eb568a7f87', 'type': 'If.body', 'value': [
                         {'id': 'dd93bdaa-6ce5-424a-ade2-0a749f091204', 'type': 'Line',
                          'command': "print('a is larger than b!')"}]}]

    nodeEditor = NodeEditor(original_json)
    nodeEditor.edit_node(
        node_id='3ef4916b-e175-4613-af86-3c4fa9944ab1',
        new_command='if a == b:'
    )

    edited_json = [{'id': 'ea1bf960-9190-4b08-90fe-087ed681543f', 'type': 'Line', 'command': 'a = 2'},
                   {'id': '1003a91e-0c84-4a09-a120-ec8b0eab4753', 'type': 'Line', 'command': 'b = 3'},
                   {'id': '3ef4916b-e175-4613-af86-3c4fa9944ab1', 'type': 'If.test', 'command': 'if a == b:'},
                   {'id': '10caffaa-e7c3-485a-a16d-61eb568a7f87', 'type': 'If.body', 'value': [
                       {'id': 'dd93bdaa-6ce5-424a-ade2-0a749f091204', 'type': 'Line',
                        'command': "print('a is larger than b!')"}]}]

    assert edited_json == nodeEditor.json


def test_edit_for_test():
    original_json = [{'id': '8ab98255-9bad-405a-bccb-23a990ba04df', 'type': 'Line', 'command': 'upper_limit = 100'},
                     {'id': 'd2e41d73-44fc-42a3-a0cb-be405aa44327', 'type': 'For.test',
                      'command': 'for i in range(upper_limit):'},
                     {'id': 'bae85ebb-f0a1-49fc-aba2-f70095e98614', 'type': 'For.body', 'value': [
                         {'id': '4e774ab0-d42b-4346-8304-56a47ec5c60c', 'type': 'Line',
                          'command': "print('The value is:')"}]}]

    nodeEditor = NodeEditor(original_json)
    nodeEditor.edit_node(
        node_id='d2e41d73-44fc-42a3-a0cb-be405aa44327',
        new_command='for i in range(100):'
    )

    edited_json = [{'id': '8ab98255-9bad-405a-bccb-23a990ba04df', 'type': 'Line', 'command': 'upper_limit = 100'},
                   {'id': 'd2e41d73-44fc-42a3-a0cb-be405aa44327', 'type': 'For.test',
                    'command': 'for i in range(100):'},
                   {'id': 'bae85ebb-f0a1-49fc-aba2-f70095e98614', 'type': 'For.body', 'value': [
                       {'id': '4e774ab0-d42b-4346-8304-56a47ec5c60c', 'type': 'Line',
                        'command': "print('The value is:')"}]}]

    assert edited_json == nodeEditor.json


def test_edit_while_test():
    original_json = [{'id': '983f10d1-8d87-4552-9b42-d225f13d0a8e', 'type': 'Line', 'command': 'a = 2'},
                     {'id': 'ce765d56-4756-4251-b155-e1f786002cee', 'type': 'Line', 'command': 'b = 5'},
                     {'id': '7d98222d-b20d-4d97-b358-b5ba59daf907', 'type': 'While.test', 'command': 'while b > a:'},
                     {'id': 'ad07beb7-e98a-4558-a730-7e16fce8da2b', 'type': 'While.body',
                      'value': [{'id': 'f5295b2a-0940-4d4c-8ef3-d8fb7c8be444', 'type': 'Line', 'command': 'a += 1'}]}]

    nodeEditor = NodeEditor(original_json)
    nodeEditor.edit_node(
        node_id='7d98222d-b20d-4d97-b358-b5ba59daf907',
        new_command='while a < b:'
    )

    edited_json = [{'id': '983f10d1-8d87-4552-9b42-d225f13d0a8e', 'type': 'Line', 'command': 'a = 2'},
                   {'id': 'ce765d56-4756-4251-b155-e1f786002cee', 'type': 'Line', 'command': 'b = 5'},
                   {'id': '7d98222d-b20d-4d97-b358-b5ba59daf907', 'type': 'While.test', 'command': 'while a < b:'},
                   {'id': 'ad07beb7-e98a-4558-a730-7e16fce8da2b', 'type': 'While.body',
                    'value': [{'id': 'f5295b2a-0940-4d4c-8ef3-d8fb7c8be444', 'type': 'Line', 'command': 'a += 1'}]}]

    assert edited_json == nodeEditor.json


test_edit_line()
test_edit_if_test()
test_edit_for_test()
test_edit_while_test()
