from http import HTTPStatus


def test_login_access_token(client, user):
    response = client.post('/auth/token', data={
        'username': user.email,
        'password': user.clean_password
    })
    token = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert token['token_type'] == 'Bearer'
    assert token.get('access_token', False)


def test_login_access_token_bad_request(client, user):
    response = client.post('/auth/token', data={
        'username': user.email,
        'password': '123'
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST
