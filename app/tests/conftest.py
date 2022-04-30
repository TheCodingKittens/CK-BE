from typing import Generator

import pytest
from app.main import get_application
from app.services.nodetojson import NodeToJSONConverter
from app.services.parser import Parser
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(get_application) as c:
        yield


@pytest.fixture(scope="module")
def parser() -> Generator:
    return Parser()


# TODO implemented the creation of the Node
# @pytest.fixture(scope="module")
# def node_to_json_converter() -> Generator:
#     with NodeToJSONConverter(node) as converter:
#         yield converter
