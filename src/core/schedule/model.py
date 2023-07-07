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

from src.db.session import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    note = Column(Text)
    date = Column(DateTime, default=func.now())
    location = Column(Text, nullable=False)
    token = Column(String(8), nullable=False, unique=True)
    attendance_is_open = Column(Boolean, default=False)

    division_id = Column(Integer, ForeignKey("divisions.id"))
    division = relationship("Division", back_populates="schedules")

    attendances = relationship("Attendance", back_populates="schedule")
