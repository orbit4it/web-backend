import uuid
import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum, Text, func
from sqlalchemy.orm import relationship

from src.db.session import Base

class Role(enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    profile_picture = Column(String(255))
    role = Column(Enum(Role), nullable=False, default=Role.user)
    nis = Column(String(10), unique=True)
    refresh_token = Column(String(64), nullable=False)
    score = Column(Integer, default=0)
    bio = Column(Text)
    phone_number = Column(String(13))
    created_at = Column(DateTime, default=func.now())

    division_id = Column(Integer, ForeignKey("divisions.id"))
    division = relationship("Division", back_populates="members")

    grade_id = Column(Integer, ForeignKey("grades.id"))
    grade = relationship("Grade", back_populates="students")

class UserPending(Base):
    __tablename__ = "users_pending"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    motivation = Column(Text, nullable=False)
    nis = Column(String(10))
    registration_token = Column(String(64))
    expired_at = Column(DateTime)

    division_id = Column(Integer, ForeignKey("divisions.id"))
    division = relationship("Division")

    grade_id = Column(Integer, ForeignKey("grades.id"))
    grade = relationship("Grade")
