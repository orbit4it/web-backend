import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from permissions.auth import UserAuth
from src.helpers.types import Error, Success

from ..schedule.model import Schedule as ScheduleModel
from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[UserAuth])
    def fill_attendance(
        self, info: Info, schedule_id: str, attendance: type.FillAttendanceInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            query = db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id)
            schedule = query.first()

            if not schedule:
                return Error("Jadwal tidak ditemukan")

            if not schedule.attendance_is_open:  # type: ignore
                return Error("Isi kehadiran jadwal ini ditutup")

            query = db.query(model.Attendance).filter(
                model.Attendance.user_id
                == user_id & model.Attendance.schedule_id
                == schedule_id
            )
            attendance_exist = query.first()

            if attendance_exist:
                return Error(
                    f"Kehadiran sudah diisi dengan status {attendance_exist.status.upper()}"
                )

            new_attendance = model.Attendance(**vars(attendance))

            db.add(new_attendance)
            db.commit()

            return Success("Berhasil mengisi kehadiran")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
