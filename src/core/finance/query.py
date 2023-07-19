import strawberry
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from strawberry.types import Info

from helpers.types import Success, Error

from . import model, type


@strawberry.type
class Query:
    ...
