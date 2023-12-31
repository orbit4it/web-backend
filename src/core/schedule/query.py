# TODO
#

from typing import List
from sqlalchemy import Date, cast, func, or_, text

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from helpers.types import Error, Success
from permissions.auth import AdminAuth, UserAuth

from . import model, type


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[], description="(Login) list jadwal tersedia")
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
                    model.Schedule.title.like(f"%{search}%"),
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

    @strawberry.field(permission_classes=[], description="(Login) data satu jadwal")
    def schedule_by_id(self, info: Info, id: str) -> List[type.ScheduleType]:
        db: Session = info.context["db"]

        return db.query(model.Schedule).filter(model.Schedule.id == id)

    @strawberry.field(
        permission_classes=[],
        description="(Admin) count list jadwal yang di group dengan tanggal",
    )
    def schedules_group_date(
        self, info: Info, start: str = "", end: str = ""
    ) -> List[type.ScheduleGroupDateType]:
        db: Session = info.context["db"]

        query = db.query(
            cast(model.Schedule.date, Date).label("date"),
            func.count(model.Schedule.date).label("count"),
        )

        if start != "" and end != "":
            query = query.filter(model.Schedule.date.between(start, end))

        return query.group_by(cast(model.Schedule.date, Date)).all()

    @strawberry.field(
        permission_classes=[],
        description="(Admin) list jadwal berdasarkan tanggal",
    )
    def schedules_by_date(self, info: Info, date: str) -> List[type.ScheduleByDateType]:
        db: Session = info.context["db"]

        return db.query(model.Schedule).filter(model.Schedule.date.like(f"{date}%"))
