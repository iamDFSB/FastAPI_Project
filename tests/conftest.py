import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.fast_zero.app import app
from src.fast_zero.database import get_session
from src.fast_zero.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    # Arrange (Organização)
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    table_registry.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        yield session

    table_registry.metadata.drop_all(bind=engine)


@pytest.fixture
def user(session):
    user = User(
        username='Teste',
        email='test@gmail.com',
        password='12345'
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
