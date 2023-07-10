from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.database import Base

from . import type


class Subject(Base):
    __tablename__ = "subject_media"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    media = Column(Text)
    author = Column(String(36), ForeignKey("users.id"))
    description = Column(Text)
    # quiz_id = Column(Integer, ForeignKey("quiz.id"))