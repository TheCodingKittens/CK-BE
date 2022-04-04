# from app.main import app
# from fastapi.testclient import TestClient

# client = TestClient(app)


# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}


def test_simple_addition():
    total = 1 + 1
    assert total == 2
