from fastapi import Request
from strawberry import BasePermission
from strawberry.types import Info


class NotAuth(BasePermission):
    message = "User sudah login"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        request: Request = info.context["request"]
        if ("refresh_token" in request.cookies or
            "Authorization" in request.headers):
            info.context["response"].status_code = 401
            return False
        return True
