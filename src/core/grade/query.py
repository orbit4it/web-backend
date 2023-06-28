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
    def grades(self, info: Info) -> List[type.GradeType]:
        db: Session = info.context["db"]

        return db.query(model.Grade)  # type: ignore

    # permission: admin, superadmin
    @strawberry.field
    def del_grade(self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Grade).filter(model.Grade.id == id)
            count = query.count()
            query.delete()

            db.commit()

            return Success(f"{count} grade berhasil dihapus")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")
