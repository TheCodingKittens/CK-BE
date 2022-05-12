class EdgeCreator:

    def __init__(self, json_tree):
        self.json_tree = json_tree
        self.edges = []
        self.indentation_levels = {}
        self.valid_node_types = ["If", "While", "If.test", "If.body", "If.else", "While.test", "While.body", "Assign"]
        self.irrelevant_nodes = ["If.body", "While.body"]
        self.command_number = 0
        self.connections = {}
        self.create_edges()

    def create_indentation_levels(self, json_object, indentation_level):
        json_object_type = json_object['type']
        json_object_id = json_object['id']
        if 'command' in json_object:
            json_object_command = json_object['command']
        else:
            json_object_command = None

        if json_object_type in self.valid_node_types:
            # print("Visiting element of type:", element_type)

            if json_object_type not in self.irrelevant_nodes:
                if indentation_level in self.indentation_levels:
                    self.indentation_levels[indentation_level].append(
                        (json_object_type, json_object_command, self.command_number, json_object_id))
                else:
                    self.indentation_levels[indentation_level] = [
                        (json_object_type, json_object_command, self.command_number, json_object_id)]
                self.command_number += 1

            if 'value' in json_object and isinstance(json_object['value'], dict):
                for key, value in json_object['value'].items():
                    self.create_indentation_levels(value, indentation_level + 1)
            elif 'value' in json_object and isinstance(json_object['value'], list):
                for value in json_object['value']:
                    self.create_indentation_levels(value, indentation_level + 1)

    def find_next_connection(self, json_object):
        start_command_number = -1
        next_json_object = None
        previous_json_object = None

        for key, value in self.indentation_levels.items():
            for inner_json_object in value:
                (command_type, command, command_number, command_id) = inner_json_object
                if command_id == json_object['id']:
                    start_command_number = command_number

        for key, value in self.indentation_levels.items():
            for inner_json_object in value:
                (command_type, command, command_number, command_id) = inner_json_object
                if command_number == start_command_number + 1:
                    next_json_object = inner_json_object
                if command_number == start_command_number - 1:
                    previous_json_object = inner_json_object

        if not next_json_object:
            return None
        elif not previous_json_object:
            (next_json_object_command_type,
             next_json_object_command,
             next_json_object_command_number,
             next_json_object_command_id) = next_json_object

            return next_json_object_command_id
        else:
            (next_json_object_command_type,
             next_json_object_command,
             next_json_object_command_number,
             next_json_object_command_id) = next_json_object

            (previous_json_object_command_type,
             previous_json_object_command,
             previous_json_object_command_number,
             previous_json_object_command_id) = previous_json_object

            if previous_json_object_command_type == 'While.test':
                return previous_json_object_command_id
            else:
                return next_json_object_command_id

    def create_connection(self, json_object):
        object_type = json_object['type']
        # only If.body and While.body do not have a 'command', this eliminates them from being examined
        if 'command' in json_object:
            if object_type == 'If.test' or object_type == 'If.body' or object_type == 'If.else' or object_type == 'Assign':
                self.connections[json_object['id']] = self.find_next_connection(json_object)

        if 'value' in json_object and isinstance(json_object['value'], dict):
            for key, value in json_object['value'].items():
                self.create_connection(value)
        elif 'value' in json_object and isinstance(json_object['value'], list):
            for value in json_object['value']:
                self.create_connection(value)

    def create_edges(self):
        for element in self.json_tree:
            self.create_indentation_levels(element, 0)

        for json_object in self.json_tree:
            self.create_connection(json_object)

        for key, value in self.connections.items():
            self.edges.append((key, value))
