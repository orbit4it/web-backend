from typing import List

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.helpers.types import Error, Success

from . import model, type


@strawberry.type
class Query:
    @strawberry.field
    def divisions(
        self,
        info: Info,
    ) -> List[type.DivisionType]:
        db: Session = info.context["db"]

        return db.query(model.Division)  # type: ignore

    # permission: admin, superadmin
    @strawberry.field
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
