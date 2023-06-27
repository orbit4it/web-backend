import uuid
import enum

from sqlalchemy import Column, DateTime, Integer, String, Enum, Text, func

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
    role = Column(Enum(Role), nullable=False)
    nis = Column(String(10))
    refresh_token = Column(String(64), nullable=False)
    score = Column(Integer, default=0)
    bio = Column(Text)
    phone_number = Column(String(13))
    created_at = Column(DateTime, default=func.now())

    division_id = Column(Integer)
    classes_id = Column(Integer)

class UserPending(Base):
    __tablename__ = "users_pending"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    motivation = Column(Text, nullable=False)
    nis = Column(String(10))
    token = Column(String(64))
    expired_at = Column(DateTime)

    division_id = Column(Integer)
    classes_id = Column(Integer)
