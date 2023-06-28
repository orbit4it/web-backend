import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from src.db.session import Base

from . import type

# class GradeLevel(enum.Enum):
#     X = 10
#     XI = 11
#     XII = 12


# class Vocational(enum.Enum):
#     TKI = "TKI"
#     TITL = "TITL"
#     ELKA = "ELKA"


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    grade = Column(Enum(type.GradeLevel), nullable=False)
    vocational = Column(Enum(type.Vocational), nullable=False)
    name = Column(String(12), nullable=False)

    students = relationship("User", back_populates="grade")
