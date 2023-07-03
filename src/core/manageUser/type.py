import enum
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

    