from typing import Generator

import pytest
from app.main import get_application
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(get_application) as c:
        yield
