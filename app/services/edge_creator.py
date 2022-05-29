import json
from dataclasses import dataclass


@dataclass
class IndentationItem:
    data: dict
    command_number: int
    indentation_level: int


class EdgeCreator:
    def __init__(self, json_data):
        self.json = json_data
        self.edges = []
        self.indentation_levels = {}
        self.all_indentation_items = []
        self.command_number = 0
        self.connections = {}
        self.parents = {}
        self.readable_edges = []
        self.variables_dict = {}
        self.executed_edges = []

    def create_indentation_levels(self, json_object, indentation_level):
        indentation_item = IndentationItem(
            json_object,
            self.command_number,
            indentation_level,
        )
        self.all_indentation_items.append(indentation_item)

        if indentation_level in self.indentation_levels:
            self.indentation_levels[indentation_level].append(indentation_item)
        else:
            self.indentation_levels[indentation_level] = [indentation_item]

        self.command_number += 1

        if json_object["nodes"]:
            for inner_json_object in json_object["nodes"]:
                self.create_indentation_levels(inner_json_object, indentation_level + 1)

    def get_test_source_code(self, current_indentation_item):
        test_source_code = ""
        current_node = current_indentation_item.data

        excluded_nodes = ["For.body", "If.body", "While.body", "If.else"]
        passed_current_node = False

        for index, indentation_item in enumerate(self.all_indentation_items):
            if indentation_item.data["type"] not in excluded_nodes:
                if passed_current_node:
                    if (
                        indentation_item.indentation_level
                        == current_indentation_item.indentation_level
                    ):
                        for _ in range(current_indentation_item.indentation_level + 1):
                            test_source_code += "\t"
                        test_source_code += "test_passed = True"
                        break
                    elif index == len(self.all_indentation_items) - 1:
                        if "command" in indentation_item.data:
                            for _ in range(indentation_item.indentation_level):
                                test_source_code += "\t"
                            test_source_code += indentation_item.data["command"] + "\n"
                        else:
                            for _ in range(indentation_item.indentation_level):
                                test_source_code += "\t"
                            test_source_code += indentation_item.data["type"] + "\n"

                        for _ in range(current_indentation_item.indentation_level + 1):
                            test_source_code += "\t"
                        test_source_code += "test_passed = True"
                        break

                if indentation_item.data["node_id"] == current_node["node_id"]:
                    passed_current_node = True

                if "command" in indentation_item.data:
                    for _ in range(indentation_item.indentation_level):
                        test_source_code += "\t"
                    test_source_code += indentation_item.data["command"] + "\n"
                else:
                    for _ in range(indentation_item.indentation_level):
                        test_source_code += "\t"
                    test_source_code += indentation_item.data["type"] + "\n"

        return test_source_code

    def find_connections(self, json_object):
        connections = []
        json_object_type = json_object["type"]

        for indentation_item in self.all_indentation_items:
            if indentation_item.data["node_id"] == json_object["node_id"]:
                current_indentation_item: IndentationItem = indentation_item

        start_command_number = current_indentation_item.command_number
        next_indentation_item: IndentationItem = None
        previous_indentation_item: IndentationItem = None

        for key, indentation_items_list in self.indentation_levels.items():
            for indentation_item in indentation_items_list:
                if indentation_item.command_number == start_command_number + 1:
                    next_indentation_item = indentation_item
                elif indentation_item.command_number == start_command_number - 1:
                    previous_indentation_item = indentation_item

        if not next_indentation_item:
            return None

        if next_indentation_item:
            if (
                next_indentation_item.indentation_level
                <= current_indentation_item.indentation_level - 1
            ):
                return None

        if json_object_type == "Line":
            connections.append(next_indentation_item.data)
            exec(json_object["command"], {}, self.variables_dict)

            if current_indentation_item.indentation_level == 0:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )

        elif json_object_type == "If.test":
            # this is the body connection
            connections.append(next_indentation_item.data)
            same_indentation_level_connection = None

            for indentation_item in self.all_indentation_items:
                if (
                    indentation_item.command_number > start_command_number
                    and current_indentation_item.indentation_level
                    == indentation_item.indentation_level
                ):
                    if indentation_item.data not in connections:
                        same_indentation_level_connection = indentation_item.data
                        connections.append(indentation_item.data)
                        # this is the next connection
                        break

            test_source_code = self.get_test_source_code(current_indentation_item)
            temp_variables_dict = dict(self.variables_dict)
            exec(test_source_code, {}, temp_variables_dict)

            if "test_passed" in temp_variables_dict:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )
            else:
                if same_indentation_level_connection:
                    self.executed_edges.append(
                        {
                            "from": json_object["node_id"],
                            "to": same_indentation_level_connection["node_id"],
                        }
                    )

        elif json_object_type == "If.body":
            same_indentation_level_connection = None

            for indentation_item in self.all_indentation_items:
                if (
                    indentation_item.command_number > start_command_number
                    and current_indentation_item.indentation_level
                    == indentation_item.indentation_level
                    and indentation_item.data["type"] != "If.else"
                ):
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        same_indentation_level_connection = indentation_item.data
                        break

            if same_indentation_level_connection:
                for from_connection, to_connections in self.connections.items():
                    if to_connections:
                        for to_connection in to_connections:
                            if to_connection["node_id"] == json_object["node_id"]:
                                for executed_edge_pair in self.executed_edges:
                                    if (
                                        executed_edge_pair["to"]
                                        == json_object["node_id"]
                                    ):
                                        self.executed_edges.append(
                                            {
                                                "from": json_object["node_id"],
                                                "to": same_indentation_level_connection[
                                                    "node_id"
                                                ],
                                            }
                                        )

        elif json_object_type == "If.else":
            same_indentation_level_connection = None

            for indentation_item in self.all_indentation_items:
                if (
                    indentation_item.command_number > start_command_number
                    and current_indentation_item.indentation_level
                    == indentation_item.indentation_level
                ):
                    if indentation_item.data not in connections:
                        same_indentation_level_connection = indentation_item.data
                        connections.append(indentation_item.data)
                        break

            if same_indentation_level_connection:
                for from_connection, to_connections in self.connections.items():
                    if to_connections:
                        for to_connection in to_connections:
                            if to_connection["node_id"] == json_object["node_id"]:
                                for executed_edge_pair in self.executed_edges:
                                    if (
                                        executed_edge_pair["to"]
                                        == json_object["node_id"]
                                    ):
                                        self.executed_edges.append(
                                            {
                                                "from": json_object["node_id"],
                                                "to": same_indentation_level_connection[
                                                    "node_id"
                                                ],
                                            }
                                        )

        elif json_object_type == "While.test":
            connections.append(next_indentation_item.data)
            same_indentation_level_connection = None

            for indentation_item in self.all_indentation_items:
                if (
                    indentation_item.command_number > start_command_number
                    and current_indentation_item.indentation_level
                    == indentation_item.indentation_level
                ):
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        same_indentation_level_connection = indentation_item.data
                        break

            test_source_code = self.get_test_source_code(current_indentation_item)
            temp_variables_dict = dict(self.variables_dict)
            exec(test_source_code, {}, temp_variables_dict)

            if "test_passed" in temp_variables_dict:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )

            if same_indentation_level_connection:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": same_indentation_level_connection["node_id"],
                    }
                )

        elif json_object_type == "While.body":
            connections.append(previous_indentation_item.data)

            for executed_edge_pair in self.executed_edges:
                if (
                    executed_edge_pair["from"]
                    == previous_indentation_item.data["node_id"]
                    and executed_edge_pair["to"] == json_object["node_id"]
                ):
                    self.executed_edges.append(
                        {
                            "from": json_object["node_id"],
                            "to": previous_indentation_item.data["node_id"],
                        }
                    )

        elif json_object_type == "For.test":
            connections.append(next_indentation_item.data)
            # this is the body connection
            same_indentation_level_connection = None

            for indentation_item in self.all_indentation_items:
                if (
                    indentation_item.command_number > start_command_number
                    and current_indentation_item.indentation_level
                    == indentation_item.indentation_level
                ):
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        same_indentation_level_connection = indentation_item.data
                        # this is the next connection
                        break

            test_source_code = self.get_test_source_code(current_indentation_item)
            temp_variables_dict = dict(self.variables_dict)
            print(test_source_code)
            exec(test_source_code, {}, temp_variables_dict)

            if "test_passed" in temp_variables_dict:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )

            if same_indentation_level_connection:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": same_indentation_level_connection["node_id"],
                    }
                )

        elif json_object_type == "For.body":
            connections.append(previous_indentation_item.data)

            for executed_edge_pair in self.executed_edges:
                if (
                    executed_edge_pair["from"]
                    == previous_indentation_item.data["node_id"]
                    and executed_edge_pair["to"] == json_object["node_id"]
                ):
                    self.executed_edges.append(
                        {
                            "from": json_object["node_id"],
                            "to": previous_indentation_item.data["node_id"],
                        }
                    )

        return connections

    def create_connections(self, json_object):
        self.connections[json_object["node_id"]] = self.find_connections(json_object)

        if json_object["nodes"]:
            for inner_json_object in json_object["nodes"]:
                self.create_connections(inner_json_object)

    def get_json_object_for_id(self, json_object_id):
        for indentation_item in self.all_indentation_items:
            if indentation_item.data["node_id"] == json_object_id:
                return indentation_item.data

    def create_parent(self, json_object):
        """
        Logic: a node will only have a parent if it is on the outer most level, i.e. indentation_level is 0.
        To find the parent node of an indented node, find the first node that has a command_number before that node
        AND is one indenation level before the node in question.
        :param json_object: the current node being examined
        """

        for indentation_item in self.all_indentation_items:
            if indentation_item.data["node_id"] == json_object["node_id"]:
                if indentation_item.indentation_level >= 1:
                    for inner_indentation_item in self.all_indentation_items[::-1]:
                        if (
                            inner_indentation_item.command_number
                            < indentation_item.command_number
                            and inner_indentation_item.indentation_level
                            == indentation_item.indentation_level - 1
                        ):
                            self.parents[
                                json_object["node_id"]
                            ] = inner_indentation_item.data
                            break

            if json_object["nodes"]:
                for inner_json_object in json_object["nodes"]:
                    self.create_parent(inner_json_object)

    def create_edges(self):
        for json_object in self.json:
            self.create_indentation_levels(json_object, 0)

        for json_object in self.json:
            self.create_connections(json_object)

        for json_object in self.json:
            self.create_parent(json_object)

        for json_object_id, connections in self.connections.items():
            if connections:
                for connection in connections:
                    if connection:
                        connection_detail = {
                            "from": json_object_id,
                            "to": connection["node_id"],
                            "parent": None,
                        }

                        for from_json_object_id, parent in self.parents.items():
                            if from_json_object_id == json_object_id:
                                connection_detail["parent"] = parent["node_id"]

                        connection_detail["executed"] = False

                        for executed_edge in self.executed_edges:
                            if (
                                executed_edge["from"] == json_object_id
                                and executed_edge["to"] == connection["node_id"]
                            ):
                                connection_detail["executed"] = True

                        self.edges.append(connection_detail)

        updated_edges = []

        for edge in self.edges:
            updated_edge = {
                "from": edge["from"],
                "to": edge["to"],
                "parent": edge["parent"],
                "executed": edge["executed"],
            }

            if edge["parent"]:
                parent_is_executed = False
                for executed_edge in self.executed_edges:
                    if edge["parent"] == executed_edge["to"]:
                        parent_is_executed = True

                if not parent_is_executed:
                    updated_edge["executed"] = False

                from_json_object = self.get_json_object_for_id(edge["from"])
                if from_json_object["type"] == "Line":
                    if edge["parent"]:
                        for executed_edge_pair in self.executed_edges:
                            if executed_edge_pair["to"] == edge["parent"]:
                                updated_edge["executed"] = True

            updated_edges.append(updated_edge)

        self.edges = list(updated_edges)

    def display_readable_edges(self):

        for edge in self.edges:
            from_json_object = self.get_json_object_for_id(edge["from"])
            to_json_object = self.get_json_object_for_id(edge["to"])
            parent_json_object = self.get_json_object_for_id(edge["parent"])

            readable_edge = {}

            if "command" in from_json_object:
                readable_edge["from"] = from_json_object["command"]
            else:
                readable_edge["from"] = from_json_object["type"]

            if "command" in to_json_object:
                readable_edge["to"] = to_json_object["command"]
            else:
                readable_edge["to"] = to_json_object["type"]

            if parent_json_object:
                readable_edge["parent"] = parent_json_object["type"]
            else:
                readable_edge["parent"] = None

            readable_edge["executed"] = edge["executed"]

            self.readable_edges.append(readable_edge)

        print(json.dumps(self.readable_edges, indent=4))
