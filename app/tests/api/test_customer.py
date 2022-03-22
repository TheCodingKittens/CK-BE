from fastapi.testclient import TestClient

# Broken tests for Now
# def test_create_customer(client: TestClient):
#     response = client.post("/customers", json={"name": "John Doe"})
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "name": "John Doe"}


# def test_read_customer(client: TestClient):
#     response = client.get("/customers/1")
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "name": "John Doe"}
