import strawberry

from src.core.division import Mutation as divMutation
from src.core.grade import Mutation as gradeMutation
from src.core.schedule import Mutation as scheduleMutation
from src.core.user import Mutation as UserMutation


@strawberry.type
class Mutation(UserMutation, divMutation, gradeMutation, scheduleMutation):
    ...
