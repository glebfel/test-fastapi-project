from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # to enable case-insensitive search for the 'first_name' field
    @validates('first_name')
    def convert_capitalized(self, key, value):
        return value.capitalize()
