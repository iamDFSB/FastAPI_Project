from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import HTTPException
from zoneinfo import ZoneInfo
from jwt.exceptions import PyJWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from jwt import decode, encode
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import User

pwd_context = PasswordHash.recommended()
oauth_schema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
EXPIRE_TOKEN_TIME_MINUTES = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data_payload: dict):
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=EXPIRE_TOKEN_TIME_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(
        session: Session = Depends(get_session),
        token:str = Depends(oauth_schema)):

    credential_exception = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate':'Bearer'}
    )
    try:
        payload = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credential_exception
    except PyJWTError:
        raise credential_exception

    user_db = session.scalar(
        select(User).where(User.email == username)
    )

    if not user_db:
        raise credential_exception

    return user_db



