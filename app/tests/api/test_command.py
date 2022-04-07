from fastapi.testclient import TestClient

# Broken tests for Now
# def test_create_commander(client: TestClient):
#     response = client.post("/commands", json={"name": "John Doe"})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "name": "John Doe"}


# def test_read_commander(client: TestClient):
#     response = client.get("/commands/1")
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "name": "John Doe"}
