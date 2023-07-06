import strawberry
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.helpers import jwt
from src.helpers.types import Error
from src.permissions import NotAuth, SuperAdminAuth, UserAuth

from . import model, type


@strawberry.type
class Query:


    @strawberry.field(permission_classes=[NotAuth])
    def user_auth(
        self, info: Info, email: str, password: str) -> type.Token | Error:
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


    # permission: *
    @strawberry.mutation
    def refresh_token(self, info: Info) -> type.Token | Error:
        cookies = info.context["request"].cookies
        db: Session = info.context["db"]

        if "refresh_token" not in cookies:
            return Error("Refresh token tidak ditemukan")

        user = (db.query(model.User)
            .filter(model.User.refresh_token == cookies["refresh_token"])
            .first())

        if user is None:
            return Error("Refresh token tidak valid")

        token = jwt.encode(
            str(user.id),
            str(user.role.name),
            user.division_id, # type: ignore
        )

        return type.Token(access_token=token)


    # normal user get users
    @strawberry.field(permission_classes=[UserAuth])
    def users(self, info: Info) -> list[type.Users]:
        db = info.context['db']
        users = db.query(model.User).filter(model.User.role != 'superadmin').all()
        return [extract_user_data(user) for user in users]
    

    # get all admin
    @strawberry.field(permission_classes=[SuperAdminAuth])
    def users_admin(self, info: Info)->list[type.Users]:
        db = info.context['db']
        users = db.query(model.User).filter(model.User.role == 'admin').all()
        return [extract_user_data(user) for user in users]
    

    @strawberry.field(permission_classes=[SuperAdminAuth])
    def super_admin(self, info: Info)->list[type.Users]:
        db = info.context['db']
        users = db.query(model.User).filter(model.User.role == 'superadmin').all()
        return [extract_user_data(user) for user in users]
    

    # superadmin get users
    @strawberry.field(permission_classes=[SuperAdminAuth])
    def users_no_restrict(self, info: Info) -> list[type.Users]:
        db = info.context['db']
        users = db.query(model.User).all()
        return [extract_user_data(user) for user in users]
    

    # get users via jwt role
    @strawberry.field(permission_classes=[UserAuth])
    def users_jwt(self, info: Info)->list[type.Users]:
        db = info.context['db']
        payload = info.context['payload']
        role = payload['role']
        if role == 'admin' or role == 'user':
            res = db.query(model.User).filter(model.User.role != 'superadmin').all()
            return [extract_user_data(user) for user in res]
        elif role == 'superadmin':
            res = db.query(model.User).all()
            return [extract_user_data(user) for user in res]
        else:
            return Error('What are you doing here ?')
    

    # get by user id
    @strawberry.field(permission_classes=[NotAuth])
    def user_by_id(self, info: Info, id: str)->type.Users:
        db = info.context['db']
        user = db.query(model.User).filter(model.User.id == id).first()
        if user is None:
            return Error('User not found')
        return extract_user_data(user)
    

    # @strawberry.field(permission_classes=[UserAuth])
    @strawberry.field
    def me(self, info: Info)->type.Users:
        db = info.context['db']
        payload = info.context['payload']
        user = payload['sub']
        result = db.query(model.User).filter(model.User.id == user).first()
        if result is None:
            return Error('Users do not exist')
        return extract_user_data(result)

    

   



def extract_user_data(user):
    user_data = type.Users(
        id=user.id,
        name=user.name,
        role=extract_role(user.role),
        division=user.division,
        grade=user.grade
    )
    return user_data

def extract_role(role):
    if isinstance(role, str):
        if role.startswith("Role."):
            return role.split(".")[-1]
    return getattr(role, "name", None) or getattr(role, "value", None) or role