import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from db.database import Base


# TODO
# 1. Tambah field title


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=True)
    note = Column(Text)
    date = Column(DateTime, default=func.now())
    location = Column(Text, nullable=False)
    token = Column(String(8), nullable=False, unique=True)
    attendance_is_open = Column(Boolean, default=False)

    division_id = Column(Integer, ForeignKey("divisions.id"))
    division = relationship("Division", back_populates="schedules")

    subject_id = Column(String(36), ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="schedules")

    attendances = relationship("Attendance", back_populates="schedule")
