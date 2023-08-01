import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from db.database import Base

from . import type


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    media = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

    schedules = relationship("Schedule", back_populates="subject")

    author_id = Column(String(36), ForeignKey("users.id"))
    author = relationship("User", back_populates="subjects")

    # quiz_id = Column(Integer, ForeignKey("quiz.id"))
