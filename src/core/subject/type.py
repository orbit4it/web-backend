import strawberry 

# from typing import TYPE_CHECKING, Annotated, List, Optional


# if TYPE_CHECKING:
#     from core.quiz.type import QuizType

@strawberry.type
class SubjectType:
    id: int
    title: str
    media: str
    # author: Annotated["QuizType", strawberry.lazy("core.quiz.type")]


@strawberry.input
class SubjectInput:
    title: str
    media: str

    