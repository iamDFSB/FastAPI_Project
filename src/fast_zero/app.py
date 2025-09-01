from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import User
from src.fast_zero.schemas import (
    ListUsers,
    Message,
    UserPublic,
    UserSchema, Token,
)
from src.fast_zero.security import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI()


@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    condition_response = session.scalar(select(User).where(
        (User.username == user.username) | (User.email == user.email)
    ))

    if condition_response:
        if condition_response.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exist.'
            )
        elif condition_response.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User email already exist.'
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/user', status_code=HTTPStatus.OK, response_model=ListUsers)
def read_users(
        limit: int = 10,
        offset: int = 0,
        session: Session = Depends(get_session),
        current_user = Depends(get_current_user)):

    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )

    return {'users': users}


@app.put('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user_by_id(user_id: int,
                      user: UserSchema,
                      session: Session = Depends(get_session),
                      current_user = Depends(get_current_user)):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permission'
        )

    current_user.email = str(user.email)
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/user/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user_by_id(user_id: int,
                      session: Session = Depends(get_session),
                      current_user = Depends(get_current_user)):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return Message(message='User deleted')


@app.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user_by_id(user_id: int,
                   current_user = Depends(get_current_user)):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permission'
        )

    return current_user


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_app():
    return Message(message='Hello World!')


@app.post('/token', status_code=HTTPStatus.CREATED, response_model=Token)
def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)):

    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db or not verify_password(form_data.password, str(user_db.password)):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email or password are incorrect.'
        )

    access_token = create_access_token(data_payload={'sub':user_db.email})

    return Token(
        access_token=access_token,
        token_type='Bearer'
    )


if __name__ == '__main__': #pragma: no cover
    import uvicorn
    uvicorn.run('src.fast_zero.app:app',
                host='0.0.0.0',
                port=8080,
                reload=True)
