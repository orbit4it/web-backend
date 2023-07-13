import strawberry

from typing import TYPE_CHECKING, Annotated, List, Optional


if TYPE_CHECKING:
    from core.user.type import Users
    from core.schedule.type import ScheduleType
    from core.division.type import DivisionType
#     from core.quiz.type import QuizType


@strawberry.type
class SubjectType:
    id: str
    title: str
    description: str
    speaker: str
    created_at: str
    media: str | None
    cover: str | None

    division: Annotated["DivisionType", strawberry.lazy("core.division.type")] | None
    author: Annotated["Users", strawberry.lazy("core.user.type")] | None

    schedules: List[Annotated["ScheduleType", strawberry.lazy("core.schedule.type")]]


@strawberry.input
class SubjectInput:
    title: str
    description: str
    speaker: str
    division_id: int
