import strawberry
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.core.user import model
from src.helpers import jwt
from src.helpers.types import Error
from src.permissions import AdminAuth, NotAuth, SuperAdminAuth, UserAuth

from . import type


@strawberry.type
class Query:
    # authentication

    # normal user get users
    @strawberry.field(permission_classes=[UserAuth])
    def get_users(self, info: Info) -> list[type.Users]:
        db = info.context["db"]
        users = (
            db.query(model.User)
            .filter(model.User.role != "superadmin" or model.User.role != "admin")
            .all()
        )
        return [extract_user_data(user) for user in users]

    # get all admin
    @strawberry.field(permission_classes=[SuperAdminAuth])
    def get_users_admin(self, info: Info) -> list[type.Users]:
        db = info.context["db"]
        users = db.query(model.User).filter(model.User.role == "admin").all()
        return [extract_user_data(user) for user in users]

    # superadmin get users
    @strawberry.field(permission_classes=[SuperAdminAuth])
    def get_users_ultimate(self, info: Info) -> list[type.Users]:
        db = info.context["db"]
        users = db.query(model.User).all()
        return [extract_user_data(user) for user in users]

    # get users by division
    @strawberry.field(permission_classes=[UserAuth])
    def get_users_divisions(self, info: Info, division_id: int) -> list[type.Users]:
        db = info.context["db"]
        users = (
            db.query(model.User)
            .filter(
                model.User.division_id == division_id
                and model.User.role != "superadmin"
            )
            .all()
        )
        return [extract_user_data(user) for user in users]

    # get by user id
    @strawberry.field(permission_classes=[NotAuth])
    def get_users_by_id(self, info: Info, id: str) -> type.Users:
        db = info.context["db"]
        user = db.query(model.User).filter(model.User.id == id).first()
        if user is None:
            return Error("User not found")
        return extract_user_data(user)


def extract_user_data(user):
    user_data = type.Users(
        id=user.id,
        name=user.name,
        role=extract_role(user.role),
        division=user.division,
        grade=user.grade,
    )
    return user_data


def extract_role(role):
    if isinstance(role, str):
        if role.startswith("Role."):
            return role.split(".")[-1]
    return getattr(role, "name", None) or getattr(role, "value", None) or role
