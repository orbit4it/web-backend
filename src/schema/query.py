import strawberry

from src.core.division import Query as DivisionQuery
from src.core.grade import Query as GradeQuery
from src.core.user import Query as UserQuery


@strawberry.type
class Query(
    UserQuery,
    DivisionQuery,
    GradeQuery
    
):
    ...
