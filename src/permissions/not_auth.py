from strawberry import BasePermission
from strawberry.types import Info


class NotAuth(BasePermission):
    message = "User sudah login"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        cookies = info.context["request"].cookies
        return not "refresh_token" in cookies
