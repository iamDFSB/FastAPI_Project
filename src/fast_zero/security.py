from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import User
from src.fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth_schema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = Settings().ALGORITHM
EXPIRE_TOKEN_TIME_MINUTES = Settings().EXPIRE_TOKEN_TIME_MINUTES


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data_payload: dict):
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=EXPIRE_TOKEN_TIME_MINUTES
    )
    to_encode.update({'exp': expire})
    encode_jwt = encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth_schema)):

    credential_exception = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
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
