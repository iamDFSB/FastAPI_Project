from http import HTTPStatus

from fastapi import FastAPI

from src.fast_zero.routers import auth, users
from src.fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_app():
    return Message(message='Hello World!')


if __name__ == '__main__':  # pragma: no cover
    import uvicorn
    uvicorn.run('src.fast_zero.app:app',
                host='0.0.0.0',
                port=8080,
                reload=True)
