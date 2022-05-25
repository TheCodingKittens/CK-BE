class JSONToSourceCodeConverter:
    def __init__(self, json):
        self.json = json
        self.valid_node_types = [
            "If.test",
            "If.body",
            "If.else",
            "While.test",
            "While.body",
            "For.test",
            "For.body",
            "Line",
        ]

        self.irrelevant_nodes = ["If.body", "While.body", "For.body"]

        self.line_number = 0
        self.lines = []

    def create_lines(self, json_object, indentation_level):
        json_object_type = json_object["type"]
        json_object_id = json_object["node_id"]

        json_object_command = None

        if "command" in json_object:
            json_object_command = json_object["command"]

        if json_object_type in self.valid_node_types:
            if json_object_type not in self.irrelevant_nodes:
                self.lines.append(
                    (
                        indentation_level,
                        json_object_type,
                        json_object_command,
                        self.line_number,
                        json_object_id,
                    )
                )
                self.line_number += 1

            if json_object["nodes"] != [] and isinstance(json_object["nodes"], dict):
                for key, value in json_object["nodes"].items():
                    self.create_lines(value, indentation_level + 1)
            elif json_object["nodes"] != [] and isinstance(json_object["nodes"], list):
                for value in json_object["nodes"]:
                    self.create_lines(value, indentation_level + 1)

    def generate_source_code(self):
        python_source_code = ""

        for json_object in self.json:
            self.create_lines(json_object, 0)

        for index, line in enumerate(self.lines):
            indentation_level, _, command, _, _ = line

            for _ in range(indentation_level):
                python_source_code += "\t"

            python_source_code += command

            if index != len(self.lines) - 1:
                python_source_code += "\n"

        return python_source_code
