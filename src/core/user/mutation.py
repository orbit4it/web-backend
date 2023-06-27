import strawberry

from strawberry.types import Info

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_pending_user(self, info: Info) -> str:
        return "Create pending user"

    @strawberry.mutation
    def create_user(self, info: Info) -> str:
        return "Create user"
