from sqlalchemy import Column, Integer, String
from src.db.session import Base

class Division(Base):
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    wa_group_links = Column(String(255), nullable=False)
