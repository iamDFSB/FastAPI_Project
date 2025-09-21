from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import User
from src.fast_zero.schemas import ListUsers, Message, UserPublic, UserSchema
from src.fast_zero.security import get_current_user, get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['users']
)

SessionAnnotated = Annotated[Session, Depends(get_session)]
CurrentUserAnnotated = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=HTTPStatus.OK, response_model=ListUsers)
def read_users(
        session: SessionAnnotated,
        limit: int = 10,
        offset: int = 0):

    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )

    return {'users': users}


@router.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: SessionAnnotated):

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


@router.put('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user_by_id(user_id: int,
                      user: UserSchema,
                      current_user: CurrentUserAnnotated,
                      session: SessionAnnotated):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permission'
        )

    current_user.email = str(user.email)
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/user/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user_by_id(user_id: int,
                      session: SessionAnnotated,
                      current_user: CurrentUserAnnotated):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return Message(message='User deleted')


@router.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user_by_id(user_id: int,
                   current_user: CurrentUserAnnotated):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permission'
        )

    return current_user
