import strawberry
import enum

from datetime import datetime
from typing import TYPE_CHECKING, Annotated


if TYPE_CHECKING:
    from core.division.type import DivisionType
    from core.grade.type import GradeType


@strawberry.enum
class Role(enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"


@strawberry.type
class Users:
    id: str
    name: str
    role: Role
    division: Annotated["DivisionType", strawberry.lazy("core.division.type")]
    grade: Annotated["GradeType", strawberry.lazy("core.grade.type")]
    created_at: str


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
    nis: str
    registration_token: str
    expired_at: datetime
    division_id: int
    grade_id: int


@strawberry.type
class Token:
    access_token: str
