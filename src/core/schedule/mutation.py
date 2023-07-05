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

from src.helpers.types import Error, Success

from . import model, type

@strawberry.type
class Mutation:
    ...
    @strawberry.mutation
    def create_schedule(
        self, info: Info, schedule: type.NewScheduleInput) -> Success | Error:
        db: Session = info.context["db"]
        new_schedule = model.Schedule(**vars(schedule))

        try: 
            db.add(new_schedule)
            db.commit()

            return Success(f"Schedule {schedule.name} berhasil ditambahkan!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
        
    @strawberry.mutation
    def edit_schedule(
        self, info: Info, id: int, schedule: type.EditScheduleInput) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Schedule).filter(model.Schedule.id == id)
            count = query.count()

            if count == 0:
                return Error("Schedule tidak ditemukan")
            
            query.update(
                {
                    model.Schedule.note: schedule.note,
                    model.Schedule.date: schedule.date,
                    model.Schedule.location: schedule.location,
                    model.Schedule.token: schedule.token,
                    model.Schedule.attendance_is_open: schedule.attendance_is_open,
                }
            )
            db.commit()

            return Success(f"Schedule berhasil diubah!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
    
    @strawberry.mutation
    def del_schedule(
        self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Schedule).filter(model.Schedule.id == id)
            count = query.count()
            query.delete()

            db.commit()

            return Success(f"{count}schedule berhasil dihapus")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
        
    
    @strawberry.mutation
    def toggle_attendance_open(
        self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Schedule).filter(model.Schedule.id == id)
            data = query.first()
            not data.is_open


            return Success(f"{data}schedule berhasil di ubah")
        except IntegrityError as e: 
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
