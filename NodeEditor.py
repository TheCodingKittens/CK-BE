import jsonpickle
import json


class NodeEditor:
    def __init__(self, json_data):
        self.json = json_data
        self.initial_node = None
        self.edited_node = None
        self.node_to_edit_id = None
        self.new_command = None

    def edit_node(self, node_id, new_command):
        self.node_to_edit_id = node_id
        self.new_command = new_command

        for json_object in self.json:
            self.edit_command(json_object)

    def edit_command(self, json_object):
        if json_object['id'] == self.node_to_edit_id:
            self.initial_node = dict(json_object)
            if 'command' in json_object:
                json_object['command'] = self.new_command
                self.edited_node = json_object

        if 'value' in json_object:
            for inner_json_object in json_object['value']:
                self.edit_command(inner_json_object)

    def display_node_changes(self):

        print('The initial node was:', json.dumps(self.initial_node, indent=4, sort_keys=False))
        print('\n')
        print('After editing, the node is:', json.dumps(self.edited_node, indent=4, sort_keys=False))
