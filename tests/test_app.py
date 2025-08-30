from http import HTTPStatus
from http.client import responses


def test_1_app_should_return_ok(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmar)
    assert response.json() == {'message': 'Hello World!'}


def test_2_app_create_user(client):
    response = client.post(
        '/user',
        json={
            'username': 'testuser',
            'email': 'user@test.com',
            'password': '1234usertest',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'user@test.com',
    }


def test_3_read_users(client):
    response = client.get('/user')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [
        {
            'id': 1,
            'username': 'testuser',
            'email': 'user@test.com',
        }
    ]}


def test_4_update_user(client):
    user_id = 1
    response = client.put(f'/user/{user_id}', json={
        'username': 'testuserUPDATE',
        'email': 'user@test.com',
        'password': '1234usertestUPDATE',
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testuserUPDATE',
        'email': 'user@test.com'
    }


def test_5_get_user_by_id(client):
    user_id = 1
    response = client.get(f'/user/{user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testuserUPDATE',
        'email': 'user@test.com'
    }


def test_6_delete_user(client):
    user_id = 1
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testuserUPDATE',
        'email': 'user@test.com'
    }


def test_get_not_found_user_by_id(client):
    user_id = 40
    response = client.get(f'/user/{user_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_not_found_user(client):
    user_id = 40
    response = client.put(f'/user/{user_id}', json={
        'username': 'testuserUPDATE',
        'email': 'user@test.com',
        'password': '1234usertestUPDATE',
    })

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_not_found_user(client):
    user_id = 40
    response = client.delete(f'/user/{user_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND