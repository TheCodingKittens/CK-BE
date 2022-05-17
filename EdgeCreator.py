import jsonpickle
from dataclasses import dataclass
import json


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

    def create_indentation_levels(self, json_object, indentation_level):
        indentation_item = IndentationItem(json_object, self.command_number, indentation_level, )
        self.all_indentation_items.append(indentation_item)

        if indentation_level in self.indentation_levels:
            self.indentation_levels[indentation_level].append(indentation_item)
        else:
            self.indentation_levels[indentation_level] = [indentation_item]

        self.command_number += 1

        if 'value' in json_object:
            for inner_json_object in json_object['value']:
                self.create_indentation_levels(inner_json_object, indentation_level + 1)

    def find_connections(self, json_object):
        connections = []
        json_object_type = json_object['type']

        for indentation_item in self.all_indentation_items:
            if indentation_item.data['id'] == json_object['id']:
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
            if next_indentation_item.indentation_level <= current_indentation_item.indentation_level - 1:
                return None

        if json_object_type == 'Line':
            connections.append(next_indentation_item.data)

        elif json_object_type == 'If.test':
            connections.append(next_indentation_item.data)

            for indentation_item in self.all_indentation_items:
                if indentation_item.command_number > start_command_number and \
                        current_indentation_item.indentation_level == indentation_item.indentation_level:
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        break

        elif json_object_type == 'If.body':
            for indentation_item in self.all_indentation_items:
                if indentation_item.command_number > start_command_number and \
                        current_indentation_item.indentation_level == indentation_item.indentation_level:
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        break

        elif json_object_type == 'If.else':
            for indentation_item in self.all_indentation_items:
                if indentation_item.command_number > start_command_number and \
                        current_indentation_item.indentation_level == indentation_item.indentation_level:
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        break

        elif json_object_type == 'While.test':
            connections.append(next_indentation_item.data)

            for indentation_item in self.all_indentation_items:
                if indentation_item.command_number > start_command_number and \
                        current_indentation_item.indentation_level == indentation_item.indentation_level:
                    if indentation_item.data not in connections:
                        connections.append(indentation_item.data)
                        break

        elif json_object_type == 'While.body':
            connections.append(previous_indentation_item.data)

        return connections

    def create_connections(self, json_object):
        self.connections[json_object['id']] = self.find_connections(json_object)

        if 'value' in json_object:
            for inner_json_object in json_object['value']:
                self.create_connections(inner_json_object)

    def get_json_object_for_id(self, json_object_id):
        for indentation_item in self.all_indentation_items:
            if indentation_item.data['id'] == json_object_id:
                return indentation_item.data

    def recursively_find_parent_id(self, json_object, from_connection, to_connection, current_parent):
        if json_object['id'] == from_connection['id']:
            if current_parent:
                self.parents[current_parent['id']] = [from_connection, to_connection]

        if json_object['type'] == 'If.body' or json_object['type'] == 'While.body' \
                or json_object['type'] == 'For.body' or json_object['type'] == 'If.else':
            current_parent = json_object

        if 'value' in json_object:
            for inner_json_object in json_object['value']:
                self.recursively_find_parent_id(inner_json_object, from_connection, to_connection, current_parent)

    def create_edges(self):
        for json_object in self.json:
            self.create_indentation_levels(json_object, 0)

        for json_object in self.json:
            self.create_connections(json_object)

        for json_object in self.json:
            for from_connection_id, connections in self.connections.items():
                if connections:
                    for connection in connections:
                        self.recursively_find_parent_id(
                            json_object,
                            self.get_json_object_for_id(from_connection_id),
                            connection,
                            None
                        )

        for json_object_id, connections in self.connections.items():
            if connections:
                for connection in connections:
                    if connection:
                        connection_detail = {
                            'from': json_object_id,
                            'to': connection['id']
                        }

                        for parent_id, edges in self.parents.items():
                            if edges[0]['id'] == json_object_id and edges[1]['id'] == connection['id']:
                                connection_detail['parent'] = parent_id

                        self.edges.append(connection_detail)
            else:
                connection_detail = {
                    'from': json_object_id,
                    'to': None
                }
                self.edges.append(connection_detail)

    def display_connections(self):
        for json_object_id, connections in self.connections.items():
            connections_print_format = [] if connections else None

            if connections:
                for connection in connections:
                    if 'command' in connection:
                        connections_print_format.append(connection['command'])
                    else:
                        connections_print_format.append(connection['type'])

            json_object = self.get_json_object_for_id(json_object_id)

            if 'command' in json_object:
                print(json_object['command'].rjust(40, ' '), '\tconnected to:\t', connections_print_format)
            else:
                print(json_object['type'].rjust(40, ' '), '\tconnected to:\t', connections_print_format)

    def display_edges(self, show_ids=True):
        edges_to_print = []

        for edge_pair in self.edges:
            from_id = edge_pair['from']
            to_id = edge_pair['to']
            from_node = self.get_json_object_for_id(from_id)
            parent_node = None
            to_node = self.get_json_object_for_id(to_id)
            if 'parent' in edge_pair:
                parent_node = self.get_json_object_for_id(edge_pair['parent'])
                pass
            edge_pair_print_format = {'from': None, 'to': None}

            if not show_ids:
                if from_node:
                    if 'command' in from_node:
                        edge_pair_print_format['from'] = from_node['command']
                    else:
                        edge_pair_print_format['from'] = from_node['type']

                if to_node:
                    if 'command' in to_node:
                        edge_pair_print_format['to'] = to_node['command']
                    else:
                        edge_pair_print_format['to'] = to_node['type']

                if parent_node:
                    if 'command' in parent_node:
                        edge_pair_print_format['parent'] = parent_node['command']
                    else:
                        edge_pair_print_format['parent'] = parent_node['type']
            else:
                edge_pair_print_format['from'] = from_id
                edge_pair_print_format['to'] = to_id

            edges_to_print.append(edge_pair_print_format)

        print(json.dumps(edges_to_print, indent=4, sort_keys=False))
