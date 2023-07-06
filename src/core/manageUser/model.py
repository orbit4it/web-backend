import uuid
import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum, Text, func
from sqlalchemy.orm import relationship

from src.db.session import Base

# class UserPending(Base):
#     __tablename__ = "users_pending"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     email = Column(String(255), nullable=False)
#     motivation = Column(Text, nullable=False)
#     nis = Column(String(10))
#     registration_token = Column(String(64))
#     expired_at = Column(DateTime)

#     division_id = Column(Integer, ForeignKey("divisions.id"))
#     division = relationship("Division")

#     grade_id = Column(Integer, ForeignKey("grades.id"))
#     grade = relationship("Grade")
