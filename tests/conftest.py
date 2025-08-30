import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.fast_zero.app import app
from src.fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)  # Arrange (Organização)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        yield session

    table_registry.metadata.drop_all(bind=engine)
