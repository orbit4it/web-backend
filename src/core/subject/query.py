import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.type import Info

from . import model, type


@strawberry.type
class Query:


    @strawberry.field
    def subjects(self, info: Info):
        return 0