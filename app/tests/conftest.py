from typing import Generator

import pytest

from fastapi.testclient import TestClient
# from app.main import get_application


# @pytest.fixture(scope="module")
# def client() -> Generator:
#     with TestClient(get_application) as c:
#         yield
