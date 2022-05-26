"""
A class do take a dictionary and return a list of variables (in form of tuples)
"""


class VariableTransformer:
    def __init__(self):
        pass

    def transform_variables(self, variables: dict):
        # create a list of dicts (containing key, value and type for each variable)
        transformed_variables = []

        for key, value in variables.items():
            type = "general"
            if isinstance(value, list):
                type = "list"
                value = self.transform_list(value)
            elif isinstance(value, dict):
                type = "dict"
                value = self.transform_dict(value)

            var_as_dict = {}
            var_as_dict["key"] = key
            var_as_dict["value"] = value
            var_as_dict["type"] = type
            transformed_variables.append(var_as_dict)

        return transformed_variables

    def transform_list(self, value: list):
        list_elements = []
        for element in value:
            if isinstance(element, str):
                list_elements.append('"' + element + '"')
            elif isinstance(element, list):
                list_elements.append(self.transform_list(element))  # recursion
            elif isinstance(element, dict):
                list_elements.append(self.transform_dict(element))  # recursion
            else:
                list_elements.append(str(element))
        return "[" + ", ".join(list_elements) + "]"

    def transform_dict(self, dict_value: dict):
        dict_values = []
        for key, value in dict_value.items():
            value_as_string = ""
            if isinstance(value, str):
                value_as_string += '"' + value + '"'
            elif isinstance(value, list):
                value_as_string += self.transform_list(value)  # recursion
            elif isinstance(value, dict):
                value_as_string += self.transform_dict(value)  # recursion
            else:
                value_as_string += str(value)

            if isinstance(key, str):
                key = '"' + key + '"'

            dict_values.append(key + ": " + value_as_string)

        return "{" + ", ".join(dict_values) + "}"
