from typing import List

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from helpers.types import Error, Success

from . import model, type


@strawberry.type
class Query:
    @strawberry.field(description="Get all division")
    def divisions(
        self,
        info: Info,
    ) -> List[type.DivisionType]:
        db: Session = info.context["db"]

        return db.query(model.Division)  # type: ignore
