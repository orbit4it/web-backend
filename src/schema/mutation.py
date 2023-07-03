import strawberry

from src.core.division import Mutation as DivisionMutation
from src.core.grade import Mutation as GradeMutation
from src.core.manageUser import Mutation as ManageUserMutation
from src.core.user import Mutation as UserMutation


@strawberry.type
class Mutation(
    UserMutation,
    ManageUserMutation,
    GradeMutation,
    DivisionMutation
):
    ...
