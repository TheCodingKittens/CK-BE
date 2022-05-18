from NodeEditor import NodeEditor
from JSONToSourceCodeConverter import JSONToSourceCodeConverter


class NodeEditVerifier:

    # Step 1: using a copy of the json_objects, edit the node in question
    # Step 2: rebuild the python source code using the new json
    # Step 3: execute this source code to check if it throws errors

    def __init__(self, command_wrapper_id, node_to_edit_id, new_command, json_objects):
        self.command_wrapper_id = command_wrapper_id
        self.node_to_edit_id = node_to_edit_id
        self.new_command = new_command
        self.json_objects = list(json_objects)

    def is_legal_edit(self):
        nodeEditor = NodeEditor(
            json_data=self.json_objects
        )

        nodeEditor.edit_node(
            node_id=self.node_to_edit_id,
            new_command=self.new_command
        )

        jsonToSourceCodeConverter = JSONToSourceCodeConverter(json=self.json_objects)
        python_source_code = jsonToSourceCodeConverter.generate_source_code()

        # TODO: Step 3: execute this source code to check if it throws errors

        """
        if errors:
            return False
        else: 
            return True
        """

        pass
