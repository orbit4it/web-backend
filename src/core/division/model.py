from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base


class Division(Base):
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    wa_group_link = Column(String(255), nullable=False)

    members = relationship("User", back_populates="division")
