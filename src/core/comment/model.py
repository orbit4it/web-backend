import uuid
from click import DateTime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from db.database import Base

from . import type


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")

    subject_id = Column(String(36), ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="comments")
