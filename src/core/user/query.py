from passlib.hash import bcrypt
import strawberry

from sqlalchemy.orm import Session
from strawberry.types import Info

from src.permissions import NotAuth
from src.helpers.types import Error
from src.helpers import jwt
from . import model, type


@strawberry.type
class Query:

    @strawberry.field(permission_classes=[NotAuth])
    def user_auth(self, info: Info, email: str, password: str) -> type.Token | Error:
        db: Session = info.context["db"]

        user = db.query(model.User).filter(model.User.email == email).first()
        db.close()

        if user is None or not bcrypt.verify(password, str(user.password)):
            return Error("Email/Password salah")

        token = jwt.encode(
            str(user.id),
            str(user.role.name),
            user.division_id, # type: ignore
        )

        info.context["response"].set_cookie(
            key="refresh_token",
            value=user.refresh_token,
            httponly=True,
        )

        return type.Token(access_token=token)

    @strawberry.mutation
    def refresh_token(self, info: Info) -> type.Token | Error:
        cookies = info.context["request"].cookies
        db: Session = info.context["db"]

        if "refresh_token" not in cookies:
            return Error("Refresh token tidak ditemukan")

        user = db.query(model.User).filter(model.User.refresh_token == cookies["refresh_token"]).first()
        if user is None:
            return Error("Refresh token tidak valid")

        token = jwt.encode(
            str(user.id),
            str(user.role.name),
            user.division_id, # type: ignore
        )

        return type.Token(access_token=token)
