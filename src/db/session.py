from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import config


DB_URL = f"mysql+pymysql://\
{config['DB_USER']}\
:{config['DB_PASSWORD']}\
@{config['DB_HOST']}\
/{config['DB_NAME']}"\

engine = create_engine(DB_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
