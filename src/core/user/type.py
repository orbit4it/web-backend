import strawberry
import enum

from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from helpers.types import Paginate


if TYPE_CHECKING:
    from core.division.type import DivisionType
    from core.grade.type import GradeType


@strawberry.enum
class Role(enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"


@strawberry.type
class User:
    id: str
    name: str
    email: str
    profile_picture: str | None
    role: Role
    nis: str | None
    score: str | None
    bio: str | None
    phone_number: str | None
    created_at: str

    division: Annotated["DivisionType", strawberry.lazy("core.division.type")]
    grade: Annotated["GradeType", strawberry.lazy("core.grade.type")]


@strawberry.type
class Users(Paginate):
    users: List[User]


@strawberry.input
class UserPendingInput:
    name: str
    email: str
    motivation: str
    nis: str | None
    division_id: int
    grade_id: int


@strawberry.type
class UserPending:
    id: int
    name: str
    email: str
    motivation: str
    nis: str | None
    registration_token: str | None
    expired_at: datetime | None
    division_id: int
    grade_id: int
    division: Annotated["DivisionType", strawberry.lazy("core.division.type")]
    grade: Annotated["GradeType", strawberry.lazy("core.grade.type")]


@strawberry.type
class Token:
    access_token: str
