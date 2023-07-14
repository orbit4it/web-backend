import strawberry
from strawberry.file_uploads import Upload

from typing import TYPE_CHECKING, Annotated, List


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
    media_url: str | None
    cover_url: str | None

    division: Annotated["DivisionType", strawberry.lazy("core.division.type")] | None
    author: Annotated["Users", strawberry.lazy("core.user.type")] | None

    schedules: List[Annotated["ScheduleType", strawberry.lazy("core.schedule.type")]]


@strawberry.input
class NewSubjectInput:
    title: str
    description: str
    speaker: str
    media_url: str
    cover: Upload

    division_id: int


@strawberry.input
class EditSubjectInput:
    title: str
    description: str
    speaker: str
    media_url: str
    cover: Upload | None

    division_id: int
