import strawberry

from core.attendance.mutation import Mutation as AttMutation
from core.schedule.mutation import Mutation as ScheduleMutation
from core.division.mutation import Mutation as DivisionMutation
from core.grade.mutation import Mutation as GradeMutation
from core.user.mutation import Mutation as UserMutation
from core.finance.mutation import Mutation as FinanceMutation


@strawberry.type
class Mutation(
    UserMutation,
    DivisionMutation,
    GradeMutation,
    ScheduleMutation,
    AttMutation,
    FinanceMutation,
):
    ...
