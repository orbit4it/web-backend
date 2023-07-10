from typing import List

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from permissions.auth import UserAuth
from src.helpers.types import Error, Success

from ..schedule.model import Schedule as modelSchedule
from ..user.model import User as modelUser
from . import model, type


@strawberry.type
class Query:
    ...

    # TODO
    # my_attendance_score
    # count schedule where schedule.div == user.div
    # count attendace where schedule.user == user.id
    # attendance / schedule * 100
    @strawberry.field(permission_classes=[UserAuth])
    def my_attendance_score(self, info: Info) -> float | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]
        user_div = info.context["payload"]["div"]

        try:
            count_schedule = (
                db.query(modelSchedule)
                .filter(modelSchedule.division_id == user_div)
                .count()
            )
            count_attendance = (
                db.query(model.Attendance)
                .filter(model.Attendance.user_id == user_id)
                .count()
            )

            percentage = count_attendance / count_schedule * 100

            return percentage

        except IntegrityError as e:
            print(e)

            return Error("Terjadi kesalahan")

    # attendance_score (schedule.id)
    # get
    # count attendance where attendance.sche == sche.id
    # count user where user
    @strawberry.field
    def attendance_schedule_score(self, info: Info, schedule_id: str) -> float | Error:
        db: Session = info.context["db"]

        try:
            schedule = (
                db.query(modelSchedule).filter(modelSchedule.id == schedule.id).first()
            )

            count_attendance = (
                db.query(model.Attendance)
                .filter(model.Attendance.schedule_id == schedule_id)
                .count()
            )

            count_user = db.query(modelUser).filter()

        except IntegrityError as e:
            print(e)

            return Error("Terjadi kesalahan")
