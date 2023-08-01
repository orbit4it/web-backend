from sqlalchemy import and_
import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from permissions.auth import AdminAuth, UserAuth
from helpers.types import Error, Success

from ..schedule.model import Schedule as ScheduleModel
from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(admin) hapus data kehadiran"
    )
    def del_attendance_by_id(self, info: Info, id: str) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Attendance).filter(model.Attendance.id == id)
            count = query.count()
            query.delete()

            db.commit()

            return Success(f"{count} kehadiran berhasil dihapus")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    @strawberry.mutation(
        permission_classes=[UserAuth], description="Isi kehadiran user"
    )
    def fill_attendance(
        self, info: Info, attendance: type.FillAttendanceInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            query = db.query(ScheduleModel).filter(
                and_(
                    ScheduleModel.date == attendance.date,
                    ScheduleModel.division_id == attendance.division_id,
                )
            )
            schedule = query.first()

            if not schedule:
                return Error("Jadwal tidak ditemukan")

            if not schedule.attendance_is_open:  # type: ignore
                return Error("Isi kehadiran jadwal ini ditutup")

            if not (0 < attendance.rating <= 5):
                return Error("Rating harus di rentang 1-5")

            query = db.query(model.Attendance).filter(
                model.Attendance.user_id == user_id
                and model.Attendance.schedule_id == attendance.schedule_id  # type: ignore
            )
            attendance_exist = query.first()

            if attendance_exist:
                return Error(
                    f"Kehadiran sudah diisi dengan status {attendance_exist.status.upper()}"
                )

            new_attendance = model.Attendance(
                user_id=user_id,
                status=attendance.status,
                rating=attendance.rating,
                feedback=attendance.feedback,
                suggestion=attendance.suggestion,
                reason=attendance.reason,
                schedule_id=schedule.id,
            )

            db.add(new_attendance)
            db.commit()

            return Success("Berhasil mengisi kehadiran")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
