from typing import List

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from permissions.auth import UserAuth
from helpers.types import Error, Success

from ..schedule.model import Schedule as modelSchedule
from ..user.model import User as modelUser
from . import model, type


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Persentase kehadiran user di setiap schedule divisi",
    )
    def my_attendance_score(self, info: Info) -> type.MyAttendanceScore | Error:
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

            return type.MyAttendanceScore(
                division_id=user_div,
                attendances=count_attendance,
                schedules=count_schedule,
            )

        except IntegrityError as e:
            print(e)

            return Error("Terjadi kesalahan")

    @strawberry.field(
        permission_classes=[UserAuth],
        description="Persentase kehadiran user dalam satu schedule",
    )
    def attendance_schedule_score(
        self, info: Info, schedule_id: str
    ) -> type.AttendanceScheduleScore | Error:
        db: Session = info.context["db"]

        try:
            schedule = (
                db.query(modelSchedule).filter(modelSchedule.id == schedule_id).first()
            )

            if not schedule:
                return Error("Schedule tidak ditemukan")

            count_attendance = (
                db.query(model.Attendance)
                .filter(model.Attendance.schedule_id == schedule_id)
                .count()
            )

            count_user = (
                db.query(modelUser)
                .filter(modelUser.division_id == schedule.division_id)
                .count()
            )

            return type.AttendanceScheduleScore(division_id=schedule.division_id, users=count_user, attendances=count_attendance)  # type: ignore

        except IntegrityError as e:
            print(e)

            return Error("Terjadi kesalahan")
