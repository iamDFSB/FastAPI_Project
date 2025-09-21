from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import User
from src.fast_zero.schemas import Token
from src.fast_zero.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SessionAnnotated = Annotated[Session, Depends(get_session)]
FormDataAnnotated = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', status_code=HTTPStatus.CREATED, response_model=Token)
def login_access_token(
        session: SessionAnnotated,
        form_data: FormDataAnnotated
):

    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db or not verify_password(form_data.password, str(user_db.password)):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email or password are incorrect.'
        )

    access_token = create_access_token(data_payload={'sub': user_db.email})

    return Token(
        access_token=access_token,
        token_type='Bearer'
    )
