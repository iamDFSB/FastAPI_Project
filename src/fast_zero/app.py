from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from src.fast_zero.schemas import Message, UserDB, UserPublic, UserSchema, ListUsers

app = FastAPI()
database = []


@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    db_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(db_with_id)

    return db_with_id


@app.get('/user', status_code=HTTPStatus.OK, response_model=ListUsers)
def read_users():
    return {'users': database}


@app.put('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user_by_id(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    user_with_id = UserDB(
        id=user_id,
        **user.model_dump()
    )

    database[user_id-1] = user_with_id

    return user_with_id


@app.delete('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def delete_user_by_id(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    user_with_id = database.pop(user_id - 1)

    return user_with_id


@app.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user_by_id(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    user = database[user_id - 1]
    return user


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_app():
    return Message(message='Hello World!')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('src.fast_zero.app:app', host='0.0.0.0', port=8080, reload=True)