from sqlalchemy import Column, INTEGER, VARCHAR, ForeignKey

from .base import BaseModel


class UserCoin(BaseModel):
    __tablename__ = 'user_coin'
    user_id: int = Column(INTEGER, ForeignKey("user.id"), unique=False, nullable=False, primary_key=True)
    coin: str = Column(VARCHAR(255), unique=False, nullable=False, primary_key=True)

    def __str__(self):
        return f'Pair: {self.username}'
