import strawberry

from src.core.attendance import Query as attQuery
from src.core.division import Query as divQuery
from src.core.grade import Query as gradeQuery
from src.core.schedule import Query as scheduleQuery
from src.core.user import Query as UserQuery


@strawberry.type
class Query(UserQuery, divQuery, gradeQuery, scheduleQuery, attQuery):
    ...
