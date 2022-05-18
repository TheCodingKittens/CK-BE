import jsonpickle


class JSONToSourceCodeConverter:
    def __init__(self, json):
        self.json = jsonpickle.decode(json)
        self.valid_node_types = ["If.test", "If.body", "If.else", "While.test", "While.body", "Assign"]
        self.irrelevant_nodes = ["If.body", "While.body"]
        self.command_number = 0
        self.lines = []

    def create_lines(self, json_object, indentation_level):
        json_object_type = json_object['type']
        json_object_id = json_object['id']
        if 'command' in json_object:
            json_object_command = json_object['command']
        else:
            json_object_command = None

        if json_object_type in self.valid_node_types:
            if json_object_type not in self.irrelevant_nodes:
                self.lines.append(
                    (indentation_level, json_object_type, json_object_command, self.command_number, json_object_id))
                self.command_number += 1

            if 'value' in json_object and isinstance(json_object['value'], dict):
                for key, value in json_object['value'].items():
                    self.create_lines(value, indentation_level + 1)
            elif 'value' in json_object and isinstance(json_object['value'], list):
                for value in json_object['value']:
                    self.create_lines(value, indentation_level + 1)

    def generate_source_code(self):
        python_source_code = ""

        for json_object in self.json:
            self.create_lines(json_object, 0)

        for line in self.lines:
            indentation_level, command_type, command, line_number, command_id = line
            for _ in range(indentation_level):
                python_source_code += '\t'
            python_source_code += command
            python_source_code += '\n'

        return python_source_code
