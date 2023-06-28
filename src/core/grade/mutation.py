from dataclasses import asdict

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.helpers.types import Error, Success

from . import model, type


@strawberry.type
class Mutation:
    # permission: admin, superadmin
    @strawberry.mutation
    def create_grade(self, info: Info, grade: type.NewGradeInput) -> Success | Error:
        db: Session = info.context["db"]
        new_grade = model.Grade(**vars(grade))  # type: ignore

        try:
            db.add(new_grade)
            db.commit()

            return Success(f"Grade {grade.name} berhasil ditambahkan!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    # permission: admin, superadmin
    @strawberry.mutation
    def edit_grade(
        self, info: Info, id: int, grade: type.EditGradeInput
    ) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Grade).filter(model.Grade.id == id)
            count = query.count()

            if count == 0:
                return Error("Grade tidak ditemukan")

            query.update(
                {
                    model.Grade.grade: grade.grade,
                    model.Grade.vocational: grade.vocational,
                    model.Grade.name: grade.name,  # type: ignore
                }
            )
            db.commit()

            return Success(f"{count} grade berhasil diubah!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
