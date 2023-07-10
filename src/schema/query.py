import strawberry

from core.attendance.query import Query as AttendanceQuery
from core.schedule.query import Query as ScheduleQuery
from core.division.query import Query as DivisionQuery
from core.grade.query import Query as GradeQuery
from core.user.query import Query as UserQuery


@strawberry.type
class Query(
    UserQuery,
    DivisionQuery,
    GradeQuery,
    ScheduleQuery,
    AttendanceQuery
):
    ...
