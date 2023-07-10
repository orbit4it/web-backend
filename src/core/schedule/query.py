# TODO
# 1. get_schedules: ambil semua row schedules
# 2. get_schedules_division: ambil semua row schedules dengan division_id
from typing import List
from sqlalchemy import or_, text

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from helpers.types import Error, Success
from permissions.auth import UserAuth

from . import model, type


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[UserAuth], description="(Login) list jadwal tersedia"
    )
    def schedules(
        self,
        info: Info,
        search: str = "",
        limit: int = 20,
        page: int = 1,
        is_open: int = 2,
        order_by: str = "date",
        sort: str = "asc",
    ) -> List[type.ScheduleType]:
        db: Session = info.context["db"]

        query = (
            db.query(model.Schedule).filter(
                or_(
                    model.Schedule.note.like(f"%{search}%"),
                    model.Schedule.location.like(f"%{search}%"),
                )
            )
            if search != ""
            else db.query(model.Schedule)
        )

        if is_open == 0 or is_open == 1:
            query = query.filter(
                or_(
                    model.Schedule.attendance_is_open == True if is_open == 1 else False
                )
            )

        return query.order_by(text(order_by + " " + sort)).offset((page - 1) * limit).limit(limit)  # type: ignore
