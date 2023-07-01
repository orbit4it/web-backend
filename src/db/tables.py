import src.core.user.model
import src.core.grade.model
import src.core.division.model

from .session import Base, engine


Base.metadata.create_all(engine)

def drop_all():
    Base.metadata.drop_all(engine)
