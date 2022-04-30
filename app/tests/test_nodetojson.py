# Broken tests for Now
# def test_create_commander(client: TestClient):
#     response = client.post("/commands", json={"name": "John Doe"})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "name": "John Doe"}


# def test_read_commander(client: TestClient):
#     response = client.get("/commands/1")
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "name": "John Doe"}


import libcst
from app.services.nodetojson import NodeToJSONConverter
from app.services.parser import Parser



def test_assign_node(parser: Parser):

    command = """a = 3"""

    parsed_expression = parser.parse_module(command)

    assign_node = NodeToJSONConverter(libcst._nodes.statement.Assign)

    assert assign_node.json_objects != []


def test_if_Node(parser: Parser):

    command = """ if a == 3:
                    value = 6"""

    parsed_expression = parser.parse_module(command)

    if_node = NodeToJSONConverter(libcst._nodes.statement.If)



    assert if_node.json_objects != []
