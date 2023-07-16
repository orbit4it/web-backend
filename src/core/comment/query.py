from typing import List
import strawberry

from strawberry.types import Info
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from permissions.auth import UserAuth

from . import model, type


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[UserAuth], description="(Login) list comments user login"
    )
    def my_comments(self, info: Info) -> List[type.CommentType]:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        return db.query(model.Comment).filter(model.Comment.user_id == user_id).all()
