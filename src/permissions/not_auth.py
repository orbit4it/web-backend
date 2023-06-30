from fastapi import Request
from strawberry import BasePermission
from strawberry.types import Info


class NotAuth(BasePermission):
    message = "User sudah login"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        request: Request = info.context["request"]
        return ("refresh_token" not in request.cookies and
            "Authorization" not in request.headers)
