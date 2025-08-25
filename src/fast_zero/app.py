from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_app():
    return {'message': 'Hello World!'}
