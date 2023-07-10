import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.session import Base

from . import type


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    status = Column(Enum(type.State), nullable=False)
    rating = Column(Integer, nullable=False)
    feedback = Column(Text)
    suggestion = Column(Text)
    reason = Column(Text)

    schedule_id = Column(String(36), ForeignKey("schedules.id"))
    schedule = relationship("Schedule", back_populates="attendances")

    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="attendances")
