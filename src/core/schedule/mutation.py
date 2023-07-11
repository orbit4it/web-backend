# TODO
# 1. create_schedule : bikin row data baru dengan parameter skema
#                     - exception value token harus unique tidak boleh ada duplikat
# 2. edit_schedule : ubah row data dengan parameter id dan skema
# 3. del_schedule : hapus row data dengan parameter id
# 4. toggle_attendance_open : ubah value attendance_is_open menjadi False maupun True dengan parameter id

from dataclasses import asdict

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info
from permissions.auth import AdminAuth

from helpers.types import Error, Success

from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[], description="(admin) membuat jadwal")
    def create_schedule(
        self, info: Info, schedule: type.CreateScheduleInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        new_schedule = model.Schedule(**vars(schedule))

        try:
            db.add(new_schedule)
            db.commit()

            return Success(f"Schedule berhasil ditambahkan!")

        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(admin) edit satu jadwal"
    )
    def edit_schedule(
        self, info: Info, id: str, schedule: type.EditScheduleInput
    ) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Schedule).filter(model.Schedule.id == id)
            count = query.count()

            if count == 0:
                return Error("Schedule tidak ditemukan")

            query.update(
                {
                    model.Schedule.title: schedule.title,
                    model.Schedule.note: schedule.note,
                    model.Schedule.location: schedule.location,
                    model.Schedule.attendance_is_open: schedule.attendance_is_open,
                    model.Schedule.division_id: schedule.division_id,
                    model.Schedule.subject_id: schedule.subject_id,
                }  # type: ignore
            )
            db.commit()

            return Success(f"Schedule berhasil diubah!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(admin) hapus jadwal"
    )
    def del_schedule(self, info: Info, id: str) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Schedule).filter(model.Schedule.id == id)
            count = query.count()
            query.delete()

            db.commit()

            return Success(f"{count} schedule berhasil dihapus")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(admin) buka tutup absensi jadwal"
    )
    def toggle_attendance_open(self, info: Info, id: str) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Schedule).filter(model.Schedule.id == id)
            data: type.ScheduleType = query.first()

            if not data:
                return Error("Schedule tidak ditemukan")

            query.update(
                {
                    model.Schedule.attendance_is_open: not data.attendance_is_open,  # type: ignore
                }
            )

            db.commit()

            return Success(f"schedule berhasil di ubah")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
