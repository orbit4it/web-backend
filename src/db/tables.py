import src.core.attendance.model
import src.core.division.model
import src.core.grade.model
import src.core.schedule.model
import src.core.user.model

from .session import Base, engine

Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)
