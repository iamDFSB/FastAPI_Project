from http import HTTPStatus

from fastapi import FastAPI

from src.fast_zero.schemas import Message, UserPublic, UserSchema, UserDB

app = FastAPI()
database = []

@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):

    db_with_id = UserDB(
        id=len(database)+1,
        **user.model_dump()
    )

    return db_with_id

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_app():
    print("OPA")
    return Message(message='Hello Worlds!')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.fast_zero.app:app", host="0.0.0.0", port=8080, reload=True)