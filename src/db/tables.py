import core.user.model
import core.grade.model
import core.division.model

from .session import Base, engine


Base.metadata.create_all(engine)

def drop_all():
    Base.metadata.drop_all(engine)
