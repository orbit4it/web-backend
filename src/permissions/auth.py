from strawberry import BasePermission
from strawberry.types import Info

from helpers import jwt


class BaseAuth(BasePermission):
    message = "Request tidak diperbolehkan"
    allowed_roles = ()

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        headers = info.context["request"].headers

        if "Authorization" not in headers:
            return False

        auth: str = headers["Authorization"]
        auth_split = auth.split(" ")
        if len(auth_split) <= 1 and auth_split[0] != "Bearer":
            return False

        access_token = auth_split[1]

        try:
            payload = jwt.decode(access_token)

            if payload["role"] not in self.allowed_roles:
                return False

            info.context["payload"] = payload
            return True

        except:
            return False


class UserAuth(BaseAuth):
    allowed_roles = ("user", "admin", "superadmin")


class AdminAuth(BaseAuth):
    allowed_roles = ("admin", "superadmin")


class SuperAdminAuth(BaseAuth):
    allowed_roles = ("superadmin")
