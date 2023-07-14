import strawberry

from core.attendance.mutation import Mutation as AttMutation
from core.schedule.mutation import Mutation as ScheduleMutation
from core.division.mutation import Mutation as DivisionMutation
from core.grade.mutation import Mutation as GradeMutation
from core.user.mutation import Mutation as UserMutation


@strawberry.type
class Mutation(
    UserMutation, DivisionMutation, GradeMutation, ScheduleMutation, AttMutation
):
    ...
