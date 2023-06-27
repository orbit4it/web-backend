import strawberry

from src.core.user import Query as UserQuery

@strawberry.type
class Query(UserQuery):
    ...
