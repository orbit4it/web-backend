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
    def create_division(
        self, info: Info, division: type.NewDivisionInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        new_division = model.Division(**vars(division))  # type: ignore

        try:
            db.add(new_division)
            db.commit()

            return Success(f"Divisi {division.name} berhasil ditambahkan!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    # permission: admin, superadmin
    @strawberry.mutation
    def edit_division(
        self, info: Info, id: int, division: type.EditDivisionInput
    ) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Division).filter(model.Division.id == id)
            div = query.first()

            if not div:
                return Error("Divisi tidak ditemukan")

            query.update(
                {
                    model.Division.name: division.name,
                    model.Division.wa_group_link: division.wa_group_link,  # type: ignore
                }
            )
            db.commit()

            return Success(f"Divisi berhasil diubah!")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
        
    
    # permission: admin, superadmin
    @strawberry.mutation
    def del_division(self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Division).filter(model.Division.id == id)
            count = query.count()
            query.delete()

            db.commit()

            return Success(f"{count} divisi berhasil dihapus")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")