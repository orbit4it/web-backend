from typing import List
from sqlalchemy import or_, text
import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from . import model, type


@strawberry.type
class Query:
    @strawberry.field
    def subjects(
        self,
        info: Info,
        search: str = "",
        page: int = 1,
        limit: int = 20,
        division_id: int = 0,
        order_by: str = "created_at",
        sort: str = "desc",
    ) -> List[type.SubjectType]:
        db: Session = info.context["db"]

        query = (
            db.query(model.Subject).filter(
                or_(
                    model.Subject.title.like(f"%{search}%"),
                    model.Subject.description.like(f"%{search}%"),
                )
            )
            if search
            else db.query(model.Subject)
        )

        if division_id != 0:
            query = query.filter(or_(model.Subject.division_id == division_id))

        return (
            query.order_by(text(order_by + " " + sort))
            .offset((page - 1) * limit)
            .limit(limit)
        )
