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
    score: int
    role: Role
    profile_picture: str | None
    phone_number: str | None
    bio: str | None
    nis: str | None
    website: str | None
    facebook: str | None
    instagram: str | None
    linkedin: str | None
    twitter: str | None
    created_at: str

    division: Annotated["DivisionType", strawberry.lazy("core.division.type")] | None
    grade: Annotated["GradeType", strawberry.lazy("core.grade.type")] | None


@strawberry.type
class UserWithAttendance(User):
    attendance_percentage: float | None


@strawberry.type
class Users(Paginate):
    users: List[UserWithAttendance]


@strawberry.input
class EditUserInput:
    bio: str
    phone_number: str
    nis: str
    website: str
    facebook: str
    instagram: str
    linkedin: str
    twitter: str
    github: str


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
class UsersPending(Paginate):
    users_pending: List[UserPending]


@strawberry.type
class Token:
    access_token: str
