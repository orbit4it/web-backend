import strawberry

from core.attendance import Mutation as AttMutation
from core.schedule import Mutation as scheduleMutation
from core.division.mutation import Mutation as DivisionMutation
from core.grade.mutation import Mutation as GradeMutation
from core.user.mutation import Mutation as UserMutation


@strawberry.type
class Mutation(UserMutation, divMutation, gradeMutation, scheduleMutation, AttMutation):
    ...
