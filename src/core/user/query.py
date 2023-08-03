import math
import strawberry
from passlib.hash import bcrypt
from strawberry.types import Info
from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session, aliased

from helpers import jwt, avatar
from helpers.types import Error, Success
from permissions import NotAuth, SuperAdminAuth, UserAuth

from core.attendance.model import Attendance as AttendanceModel
from core.schedule.model import Schedule as ScheduleModel
from core.division.model import Division as DivisionModel
from core.grade.model import Grade as GradeModel
from . import model, type


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[NotAuth],
        description="(NotAuth) Login to get access and refresh token",
    )
    def user_auth(self, info: Info, email: str, password: str) -> type.Token | Error:
        db: Session = info.context["db"]

        user = db.query(model.User).filter(model.User.email == email).first()
        db.close()

        if user is None or not bcrypt.verify(password, str(user.password)):
            return Error("Email/Password salah")

        token = jwt.encode(
            str(user.id),
            str(user.role.name),
            user.division_id,  # type: ignore
        )

        info.context["response"].set_cookie(
            key="refresh_token",
            value=user.refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
        )

        return type.Token(access_token=token)

    @strawberry.field(description="Use refresh token cookie to get new access token")
    def refresh_token(self, info: Info) -> type.Token | Error:
        cookies = info.context["request"].cookies
        db: Session = info.context["db"]

        if "refresh_token" not in cookies:
            return Error("Refresh token tidak ditemukan")

        user = (
            db.query(model.User)
            .filter(model.User.refresh_token == cookies["refresh_token"])
            .first()
        )

        if user is None:
            return Error("Refresh token tidak valid")

        token = jwt.encode(
            str(user.id),
            str(user.role.name),
            user.division_id,  # type: ignore
        )

        return type.Token(access_token=token)

    @strawberry.field(
        permission_classes=[UserAuth],
        description="(Auth) Logout with clear refresh_token cookie",
    )
    def user_logout(self, info: Info) -> Success | Error:
        cookies = info.context["request"].cookies

        if "refresh_token" not in cookies:
            return Error("Refresh token tidak ditemukan")

        info.context["response"].delete_cookie(
            key="refresh_token", samesite="None", secure=True
        )
        return Success("Logout berhasil")

    # normal user get users
    @strawberry.field(
        permission_classes=[UserAuth], description="(Auth) Get all user and admin"
    )
    def users(
        self,
        info: Info,
        search: str = "",
        limit: int = 20,
        page: int = 1,
        order_by: str = "created_at",
        sort: str = "asc",
        start_at: str = "",
        division_id: int = 0,
        grade_id: int = 0,
        end_at: str = "",
    ) -> type.Users:
        db: Session = info.context["db"]

        AttendanceAlias = aliased(AttendanceModel)
        ScheduleAlias = aliased(ScheduleModel)

        query = (
            db.query(
                model.User,
                DivisionModel,
                GradeModel,
                (
                    (
                        db.query(func.count(AttendanceAlias.id))
                        .join(ScheduleAlias, AttendanceAlias.schedule)
                        .filter(AttendanceAlias.user_id == model.User.id)
                        .filter(ScheduleAlias.division_id == ScheduleAlias.division_id)
                    ).scalar_subquery()
                    / func.count(ScheduleAlias.id)
                    * 100
                ).label("attendance_percentage"),
            )
            .join(DivisionModel, DivisionModel.id == model.User.division_id)
            .join(GradeModel, GradeModel.id == model.User.grade_id)
            .group_by(model.User.id)
        )

        if search != "":
            query = query.filter(
                or_(
                    model.User.name.like(f"%{search}%"),
                    model.User.email.like(f"{search}%"),
                )
            )

        if division_id:
            query = query.filter(model.User.division_id == division_id)

        if grade_id:
            query = query.filter(model.User.grade_id == grade_id)

        if start_at != "" and end_at != "":
            query = query.filter(model.User.created_at.between(start_at, end_at))

        count = query.count()
        total_pages = math.ceil(count / limit)

        query = (
            query.order_by(text(order_by + " " + sort))
            .offset((page - 1) * limit)
            .limit(limit)
        ) # type: ignore

        results = []
        for user, division, grade, attendance_percentage in query.all():
            results.append(
                type.UserWithAttendance(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    profile_picture=user.profile_picture,
                    role=user.role,
                    nis=user.nis,
                    score=user.score,
                    bio=user.bio,
                    phone_number=user.phone_number,
                    website=user.website,
                    facebook=user.website,
                    instagram=user.instagram,
                    linkedin=user.linkedin,
                    twitter=user.twitter,
                    created_at=user.created_at,
                    attendance_percentage=attendance_percentage,
                    division=division,
                    grade=grade,
                )
            )

        return type.Users(
            total_data=count,
            total_pages=total_pages,
            page=page,
            limit=limit,
            has_next_page=page < total_pages,
            has_prev_page=page > 1,
            users=results,
        )

    # get all admin
    @strawberry.field(
        permission_classes=[SuperAdminAuth], description="(SuperAdmin) Get all admin"
    )
    def users_admin(self, info: Info) -> list[type.User]:
        db = info.context["db"]
        users = db.query(model.User).filter(model.User.role == "admin").all()
        return users

    @strawberry.field(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Get all superadmin",
    )
    def super_admin(self, info: Info) -> list[type.User]:
        db = info.context["db"]
        users = db.query(model.User).filter(model.User.role == "superadmin").all()
        return users

    # superadmin get users
    @strawberry.field(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) get all user, admin, and superadmin",
    )
    def users_no_restrict(self, info: Info) -> list[type.User]:
        db = info.context["db"]
        users = db.query(model.User).all()
        return users

    # get users via jwt role
    @strawberry.field(
        permission_classes=[UserAuth], description="(Auth) Get all user via role in jwt"
    )
    def users_jwt(self, info: Info) -> list[type.User]:
        db = info.context["db"]
        payload = info.context["payload"]
        role = payload["role"]
        if role == "superadmin":
            res = db.query(model.User).all()
            return res
        else:
            res = db.query(model.User).filter(model.User.role != "superadmin").all()
            return res

    # get by user id
    @strawberry.field(
        permission_classes=[UserAuth], description="(NotAuth) Get user by id"
    )
    def user_by_id(self, info: Info, id: str) -> type.User:
        db = info.context["db"]
        user = db.query(model.User).filter(model.User.id == id).first()
        return user

    @strawberry.field(
        permission_classes=[UserAuth], description="(Auth) Get user by auth jwt"
    )
    def me(self, info: Info) -> type.User:
        db = info.context["db"]
        payload = info.context["payload"]
        user = payload["sub"]
        result = db.query(model.User).filter(model.User.id == user).first()
        return result

    @strawberry.field(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Get all pending user",
    )
    def pending_users(
        self,
        info: Info,
        search: str = "",
        limit: int = 20,
        page: int = 1,
        order_by: str = "id",
        sort: str = "asc",
    ) -> type.UsersPending:
        db: Session = info.context["db"]

        query = (
            db.query(model.UserPending).filter(
                or_(
                    model.UserPending.name.like(f"%{search}%"),
                    model.UserPending.email.like(f"{search}%"),
                )
            )
            if search != ""
            else db.query(model.UserPending)
        )

        count = query.count()
        total_pages = math.ceil(count / limit)

        return type.UsersPending(
            total_data=count,
            total_pages=total_pages,
            page=page,
            limit=limit,
            has_next_page=page < total_pages,
            has_prev_page=page > 1,
            users_pending=query.order_by(text(order_by + " " + sort))
            .offset((page - 1) * limit)
            .limit(limit), # type: ignore
        )


    @strawberry.field(description="Get all avatar url")
    def user_avatars(self) -> list[str]:
        return avatar.all()
