import strawberry

from core.division.mutation import Mutation as DivisionMutation
from core.grade.mutation import Mutation as GradeMutation
from core.user.mutation import Mutation as UserMutation


@strawberry.type
class Mutation(
    UserMutation,
    GradeMutation,
    DivisionMutation
):
    ...
