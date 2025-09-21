import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.fast_zero.app import app
from src.fast_zero.database import get_session
from src.fast_zero.models import User, table_registry
from src.fast_zero.security import get_password_hash


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
    password = '12345'
    user = User(
        username='Teste',
        email='test@gmail.com',
        password=get_password_hash(password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post('/auth/token', data={
        'username': user.email,
        'password': user.clean_password
    })
    return response.json()['access_token']
