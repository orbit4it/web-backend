import core.attendance.model
import core.schedule.model
import core.user.model
import core.grade.model
import core.division.model
import core.subject.model

from .database import Base, engine

Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)
