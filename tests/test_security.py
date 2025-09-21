from jwt import decode

from src.fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_encode_token_jwt():
    data = {
        'sub': 'dandan@gmail.com'
    }
    token_jwt = create_access_token(data)
    token_decoded = decode(token_jwt, key=SECRET_KEY, algorithms=[ALGORITHM])
    assert data['sub'] == token_decoded['sub']
    assert token_decoded['exp']
