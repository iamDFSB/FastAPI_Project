from http import HTTPStatus

from fastapi.testclient import TestClient

from src.fast_zero.app import app


def test_app_should_return_ok():
    client = TestClient(app)  # Arrange (Organização)
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmar)
    assert response.json() == {'message': 'Hello World!'}


client = TestClient(app)
