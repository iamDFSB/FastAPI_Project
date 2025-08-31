from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import User
from src.fast_zero.schemas import (
    ListUsers,
    Message,
    UserPublic,
    UserSchema,
)

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

    db_user = User(username=user.username, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/user', status_code=HTTPStatus.OK, response_model=ListUsers)
def read_users(
        limit: int = 10,
        offset: int = 0,
        session: Session = Depends(get_session)):

    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )

    return {'users': users}


@app.put('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user_by_id(user_id: int,
                      user: UserSchema,
                      session: Session = Depends(get_session)):

    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    user_db.email = user.email
    user_db.username = user.username
    user_db.password = user.password

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete('/user/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user_response = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_response:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    session.delete(user_response)
    session.commit()

    return Message(message='User deleted')


@app.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):

    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    return user_db


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_app():
    return Message(message='Hello World!')


if __name__ == '__main__': #pragma: no cover
    import uvicorn
    uvicorn.run('src.fast_zero.app:app',
                host='0.0.0.0',
                port=8080,
                reload=True)
