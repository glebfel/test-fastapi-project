from src.database import get_db
from src.exceptions import DatabaseElementNotFoundError
from src.users.models import User


def get_user_by_email(email: str) -> User:
    with get_db() as session:
        if not (user := session.query(User).filter_by(email=email).first()):
            raise DatabaseElementNotFoundError(f"User with email '{email}' not found")
        return user


def get_all_users() -> list[User]:
    with get_db() as session:
        return session.query(User).all()


def add_new_user(first_name: str, last_name, email: str, username: str, hashed_password: str) -> User:
    with get_db() as session:
        user = User(
            first_name=first_name, last_name=last_name, username=username, email=email, hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def update_user_by_email(email: str, **kwargs):
    with get_db() as session:
        session.query(User).filter_by(email=email).update(kwargs)
        session.commit()
