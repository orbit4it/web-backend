from datetime import datetime
from typing import TYPE_CHECKING, Annotated

import strawberry

if TYPE_CHECKING:
    from src.core.division.type import DivisionType
    from src.core.grade.type import GradeType


@strawberry.type
class Users:
    id: str
    name: str
    role: str
    division: Annotated["DivisionType", strawberry.lazy("src.core.division.type")]
    grade: Annotated["GradeType", strawberry.lazy("src.core.grade.type")]
    

@strawberry.input
class UserPendingInput:
    name: str
    email: str
    motivation: str
    nis: str
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
