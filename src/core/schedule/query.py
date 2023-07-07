# TODO
# 1. get_schedules: ambil semua row schedules
# 2. get_schedules_division: ambil semua row schedules dengan division_id
from typing import List

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.helpers.types import Error, Success

from . import model, type


@strawberry.type
class Query:
    @strawberry.field
    def schedule(self, info: Info) -> List[type.ScheduleType]:
        db: Session = info.context["db"]

        return db.query(model.Schedule)
