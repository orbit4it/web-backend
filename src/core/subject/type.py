import strawberry

from typing import TYPE_CHECKING, Annotated, List, Optional


if TYPE_CHECKING:
    from core.user.type import Users
    from core.schedule.type import ScheduleType
#     from core.quiz.type import QuizType


@strawberry.type
class SubjectType:
    id: str
    title: str
    media: str | None
    description: str

    author: Annotated["Users", strawberry.lazy("core.user.type")]
    schedules: List[Annotated["ScheduleType", strawberry.lazy("core.schedule.type")]]


@strawberry.input
class SubjectInput:
    title: str
    description: str
