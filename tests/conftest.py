import pytest
from fastapi.testclient import TestClient
from src.fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)  # Arrange (Organização)
