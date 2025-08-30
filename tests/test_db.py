from sqlalchemy import select

from src.fast_zero.models import User


def test_create_user(session):
    user = User(username='dandan', email='dn@gmail.com', password='1234')
    session.add(user)
    session.commit()
    # Synchronizes the user variable with the incremental data that is needed.
    # session.refresh(user)
    row = session.scalar(
        select(User).where(User.username == 'dandan')
    )
    assert row.username == 'dandan'
