from sqlalchemy import Column, INTEGER, VARCHAR

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    id: int = Column(INTEGER, unique=True, nullable=False, primary_key=True)
    telegram_id: int = Column(INTEGER, unique=True, nullable=False)
    full_name: str = Column(VARCHAR(255), unique=False, nullable=False)
    username: str = Column(VARCHAR(255), unique=True, nullable=False)

    def __str__(self):
        return f'User: {self.username}'
