from app.services.variable_transformer import VariableTransformer


def test_variables(variabletransformer: VariableTransformer):

    vars_as_dict = {"a": 7, "b": True, "c": [1, 2, "Hallo"]}
    transformed_vars = variabletransformer.transform_variables(vars_as_dict)

    assert transformed_vars[0]["key"] == "a"
    assert transformed_vars[0]["value"] == 7
    assert transformed_vars[0]["type"] == "general"

    assert transformed_vars[1]["key"] == "b"
    assert transformed_vars[1]["value"] == True
    assert transformed_vars[1]["type"] == "general"

    assert transformed_vars[2]["key"] == "c"
    assert transformed_vars[2]["value"] == """[1, 2, "Hallo"]"""
    assert transformed_vars[2]["type"] == "list"


def test_nested_variables(variabletransformer: VariableTransformer):

    vars_as_dict = {
        "a": {"b": 6, "c": [True, "hey"]},
        "y": [{"a": 9, "x": False}, True, [1]],
        "z": [1, {"r": 4}, [], {}],
    }
    transformed_vars = variabletransformer.transform_variables(vars_as_dict)

    assert transformed_vars[0]["key"] == "a"
    assert transformed_vars[0]["value"] == """{"b": 6, "c": [True, "hey"]}"""
    assert transformed_vars[0]["type"] == "dict"

    assert transformed_vars[1]["key"] == "y"
    assert transformed_vars[1]["value"] == """[{"a": 9, "x": False}, True, [1]]"""
    assert transformed_vars[1]["type"] == "list"

    assert transformed_vars[2]["key"] == "z"
    assert transformed_vars[2]["value"] == """[1, {"r": 4}, [], {}]"""
    assert transformed_vars[2]["type"] == "list"
