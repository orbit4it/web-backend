import strawberry

from src.core.user import Mutation as UserMutation

@strawberry.type
class Mutation(UserMutation):
    ...
