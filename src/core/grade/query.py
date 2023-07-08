from typing import List

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from helpers.types import Error, Success

from . import model, type


@strawberry.type
class Query:
    @strawberry.field
    def grades(self, info: Info) -> List[type.GradeType]:
        db: Session = info.context["db"]

        return db.query(model.Grade)  # type: ignore
