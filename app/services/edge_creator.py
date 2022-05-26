import json
import re
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

            pattern = "{0}(.*?){1}".format("if ", ":")
            test_to_execute = re.search(pattern, json_object["command"]).group(1)
            test_passed = eval(test_to_execute, {}, self.variables_dict)

            if test_passed:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )
            else:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": same_indentation_level_connection["node_id"],
                    }
                )

        elif json_object_type == "If.body":
            for indentation_item in self.all_indentation_items:
                if (
                    indentation_item.command_number > start_command_number
                    and current_indentation_item.indentation_level
                    == indentation_item.indentation_level
                    and indentation_item.data["type"] != "If.else"
                ):
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        break

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

            for from_connection, to_connections in self.connections.items():
                if to_connections:
                    for to_connection in to_connections:
                        if to_connection["node_id"] == json_object["node_id"]:
                            for executed_edge_pair in self.executed_edges:
                                if executed_edge_pair["to"] == json_object["node_id"]:
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

            pattern = "{0}(.*?){1}".format("while ", ":")
            test_to_execute = re.search(pattern, json_object["command"]).group(1)
            test_passed = eval(test_to_execute, {}, self.variables_dict)

            if test_passed:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )

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

            temp_variables_dict = dict(self.variables_dict)
            test_to_execute = json_object["command"] + "\n\ttest_passed = True"
            exec(test_to_execute, {}, temp_variables_dict)

            if "test_passed" in temp_variables_dict:
                self.executed_edges.append(
                    {
                        "from": json_object["node_id"],
                        "to": next_indentation_item.data["node_id"],
                    }
                )

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

    def create_readable_edges(self, show_ids=True, show_output=False):
        edges_to_print = []

        for edge_pair in self.edges:
            from_id = edge_pair["from"]
            to_id = edge_pair["to"]
            from_node = self.get_json_object_for_id(from_id)
            parent_node = None
            to_node = self.get_json_object_for_id(to_id)
            if "parent" in edge_pair:
                parent_node = self.get_json_object_for_id(edge_pair["parent"])
                pass
            edge_pair_print_format = {"from": None, "to": None}

            if not show_ids:
                if from_node:
                    if "command" in from_node:
                        edge_pair_print_format["from"] = from_node["command"]
                    else:
                        edge_pair_print_format["from"] = from_node["type"]

                if to_node:
                    if "command" in to_node:
                        edge_pair_print_format["to"] = to_node["command"]
                    else:
                        edge_pair_print_format["to"] = to_node["type"]

                if parent_node:
                    if "command" in parent_node:
                        edge_pair_print_format["parent"] = parent_node["command"]
                    else:
                        edge_pair_print_format["parent"] = parent_node["type"]
            else:
                edge_pair_print_format["from"] = from_id
                edge_pair_print_format["to"] = to_id

            edge_pair_print_format["executed"] = False

            for executed_edge in self.executed_edges:
                if executed_edge["from"] == from_id and executed_edge["to"] == to_id:
                    edge_pair_print_format["executed"] = True

            edges_to_print.append(edge_pair_print_format)

            if show_output:
                print(json.dumps(edge_pair_print_format, indent=4))

            self.readable_edges.append(edge_pair_print_format)
