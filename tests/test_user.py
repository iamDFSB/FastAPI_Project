from http import HTTPStatus

from src.fast_zero.schemas import UserPublic


def test_app_create_user(client):
    response = client.post(
        '/users/user',
        json={
            'username': 'testuser',
            'email': 'user@test.com',
            'password': '1234usertest',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["username"] == 'testuser'


def test_read_users_with_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    user_schema = UserPublic.model_validate(user)
    user_id = user_schema.id
    response = client.put(f'/users/user/{user_id}', json={
        'username': 'testuserUPDATE',
        'email': 'user@test.com',
        'password': '1234usertestUPDATE',
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user_id,
        'username': 'testuserUPDATE',
        'email': 'user@test.com'
    }


def test_get_user_by_id(client, user, token):
    user_id = user.id
    response = client.get(f'/users/user/{user_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user_id,
        'username': 'Teste',
        'email': 'test@gmail.com',
    }


def test_delete_user(client, user, token):
    user_id = user.id
    response = client.delete(f'/users/user/{user_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted'
    }


def test_get_not_found_user_by_id(client, token):
    user_id = 40
    response = client.get(f'/users/user/{user_id}', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_not_found_user(client, token):
    user_id = 40
    response = client.put(f'/users/user/{user_id}', json={
        'username': 'testuserUPDATE',
        'email': 'user@test.com',
        'password': '1234usertestUPDATE',
    }, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_not_found_user(client, token):
    user_id = 40
    response = client.delete(f'/users/user/{user_id}', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_create_user_bad_request_username(client, user):
    response = client.post('/users/user', json={
        'username': 'Teste',
        'email': 'test@gmail.com',
        'password': '12345'
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_bad_request_email(client, user):
    response = client.post('/users/user', json={
        'username': 'Teste2',
        'email': 'test@gmail.com',
        'password': '12345'
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_unauthorized_token_delete(client):
    user_id = 1
    response = client.put(f'/users/user/{user_id}', headers={
        'Authorization': 'Bearer invalido'
    }, json={
        'username': 'testuserUPDATE',
        'email': 'user@testiiii.com',
        'password': '1234usertestUPDATE',
    })

    assert response.status_code == HTTPStatus.UNAUTHORIZED
