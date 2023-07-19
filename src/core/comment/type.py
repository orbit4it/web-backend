import strawberry
from typing import TYPE_CHECKING, Annotated, List

if TYPE_CHECKING:
    from core.subject.type import SubjectType
    from core.user.type import Users


@strawberry.type
class CommentType:
    id: str
    content: str
    rating: int
    created_at: str
    user: Annotated["Users", strawberry.lazy("core.user.type")] | None
    subject: Annotated["SubjectType", strawberry.lazy("core.subject.type")] | None


@strawberry.input
class CommentInput:
    content: str
    rating: int
