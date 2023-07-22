import strawberry
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from strawberry.types import Info

from helpers.types import Success, Error
from permissions.auth import UserAuth

from . import model, type


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[UserAuth], description="(Login ) list transaksi kas"
    )
    def balances(
        self,
        info: Info,
        search: str = "",
        limit: int = 20,
        page: int = 1,
    ):
        ...
