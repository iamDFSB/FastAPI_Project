from http import HTTPStatus

from fastapi import FastAPI

from src.fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_app():
    return Message(message="Hello Worlds!")
