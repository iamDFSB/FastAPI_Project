from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.fast_zero.settings import Settings

url = Settings().DATABASE_URL.replace("/src/fast_zero", "")
engine = create_engine(url)


def get_session(): #pragma: no cover
    with Session(engine) as session:
        yield session
