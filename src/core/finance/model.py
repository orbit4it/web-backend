import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from db.database import Base

from . import type


class Balance(Base):
    __tablename__ = "balances"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    date = Column(DateTime, nullable=False)
    note = Column(Text)
    amount = Column(Integer, nullable=False)

    flow = Column(Enum(type.CashFlow), nullable=False)
    level = Column(Enum(type.CashLevel), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions")
