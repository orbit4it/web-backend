from strawberry import BasePermission
from strawberry.types import Info

from helpers import jwt


class BaseAuth(BasePermission):
    message = "Request tidak diperbolehkan"
    allowed_roles = ()

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        headers = info.context["request"].headers

        if "Authorization" not in headers:
            info.context["response"].status_code = 401
            return False

        auth: str = headers["Authorization"]
        auth_split = auth.split(" ")
        if len(auth_split) <= 1 and auth_split[0] != "Bearer":
            info.context["response"].status_code = 401
            return False

        access_token = auth_split[1]

        try:
            payload = jwt.decode(access_token)

            if payload["role"] not in self.allowed_roles:
                info.context["response"].status_code = 401
                return False

            info.context["payload"] = payload
            return True

        except Exception as e:
            if str(e) == "Signature has expired.":
                self.message = "Access token kadaluwarsa"

            info.context["response"].status_code = 401
            return False


class UserAuth(BaseAuth):
    allowed_roles = ("user", "admin", "superadmin")


class AdminAuth(BaseAuth):
    allowed_roles = ("admin", "superadmin")


class SuperAdminAuth(BaseAuth):
    allowed_roles = ("superadmin")
