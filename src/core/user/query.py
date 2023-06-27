import strawberry

from strawberry.types import Info

@strawberry.type
class Query:

    @strawberry.field
    def login(self, info: Info) -> str:
        return "Login"
