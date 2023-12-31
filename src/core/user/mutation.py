import asyncio
import strawberry

from datetime import datetime, timedelta
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from helpers import email, token, avatar
from helpers.types import Error, Success
from permissions import AdminAuth, NotAuth, SuperAdminAuth, UserAuth
from helpers.validation import (
    ValidationError,
    validate_edit_user,
    validate_user_pending
)
from . import model, type


@strawberry.type
class Mutation:

    @strawberry.mutation(
        permission_classes=[NotAuth],
        description="(NotAuth) Register to create a pending user which will later be confirmed/verified by the admin"
    )
    def create_user_pending(
        self, info: Info, user_pending: type.UserPendingInput
    ) -> Success | Error:
        db: Session = info.context["db"]

        try:
            validate_user_pending(user_pending)
        except ValidationError as e:
            return Error(str(e))

        user_pending_db = model.UserPending(**vars(user_pending))

        try:
            db.add(user_pending_db)
            db.commit()

            return Success("Akun sedang diverifikasi, mohon tunggu email verifikasi")
        except:
            db.rollback()
            return Error("Terjadi kesalahan")


    @strawberry.mutation(
        permission_classes=[NotAuth],
        description="(NotAuth) After user gets the registration token from email, user can re-register to create account"
    )
    async def create_user(
        self, info: Info, registration_token: str, password: str, grade_id: int
    ) -> Success | Error:
        db: Session = info.context["db"]

        user_pending_query = (db.query(model.UserPending)
            .filter(model.UserPending.registration_token == registration_token))

        user_pending = user_pending_query.first()

        if user_pending is None or user_pending.expired_at < datetime.now(): # type: ignore
            return Error("Token registrasi tidak valid")

        if len(password) < 8:
            return Error("Password minimal 8 karakter")

        user = model.User(
            name=user_pending.name,
            email=user_pending.email,
            password=bcrypt.hash(password),
            nis=user_pending.nis,
            division_id=user_pending.division_id,
            grade_id=grade_id,
            refresh_token=token.generate(64)
        )

        division = user_pending.division

        try:
            user_pending_query.delete()
            db.add(user)
            db.commit()

            asyncio.create_task(email.send_group_link(
                receiver=user.email, # type: ignore
                division_link=division.wa_group_link,
                division_name=division.name,
            ))

            return Success("Registrasi berhasil, kamu bisa login sekarang dan jangan lupa cek email!")

        except IntegrityError as e:
            db.rollback()
            if "for key 'email'" in str(e):
                return Error("Email sudah digunakan")
            elif "for key 'nis'" in str(e):
                return Error("NIS sudah digunakan")

            return Error("Terjadi kesalahan")


    # permission: admin, superadmin
    @strawberry.mutation(
        permission_classes=[AdminAuth],
        description="(Admin) Confirm user pending and send verification email"
    )
    async def confirm_user(self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]

        query = db.query(model.UserPending).filter(model.UserPending.id == id)

        user_pending = query.first()
        if user_pending is None:
            db.rollback()
            return Error("User pending tidak ditemukan")

        registration_token = token.generate(64)
        query.update({
            model.UserPending.registration_token: registration_token,
            model.UserPending.expired_at: datetime.now() + timedelta(days=7)
        }) # type: ignore
        db.commit()

        asyncio.create_task(email.send_verification(
            user_pending.email, # type: ignore
            user_pending.division.name,
            registration_token
        ))

        return Success("Mengirim email verifikasi")


    @strawberry.mutation(
        permission_classes=[AdminAuth],
        description="(Admin) Delete user pending"
    )
    def delete_pending_user(self, info: Info, id:int)-> Success | Error:
        db: Session = info.context["db"]
        try:
            query = db.query(model.UserPending).filter(model.UserPending.id == id).first()
            if query is None:
                return Error('User tidak ditemukan')
            db.delete(query)
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f'Eror menghapus: {e}')

        except Exception as e:
            db.rollback()
            return Error(f'Eror menghapus: {e}')

        return Success('Pending User berhasil dihapus')


    @strawberry.mutation(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Delete user"
    )
    def delete_user(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try:
            query = db.query(model.User).filter(model.User.id == id).first()
            if query is None:
                return Error('User tidak ditemukan')
            db.delete(query)
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f'Eror menghapus: {e}')

        except Exception as e:
            db.rollback()
            return Error(f'Eror menghapus: {e}')

        return Success(' User berhasil dihapus')


    @strawberry.mutation(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Promote user to admin"
    )
    def promote_user(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try:
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id:  {id}")

            query.role = 'admin' # type: ignore
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menaikan user: {e} ditemukan")

        except Exception as e:
            db.rollback()
            return Error(f"Gagal menaikan user: {e} ditemukan")
        return Success('Berhasil menaikan user')


    @strawberry.mutation(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Demote admin to user"
    )
    def demote_admin(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try:
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id: {id}")

            query.role = 'user' # type: ignore
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menurunkan admin: {e} ditemukan")

        except Exception as e:
            db.rollback()
            return Error(f"Gagal menurunkan admin: {e} ditemukan")
        return Success('Berhasil menurunkan admin')


    @strawberry.mutation(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Promote user/admin to superadmin"
    )
    def promote_admin(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try:
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id: {id}")

            query.role = 'superadmin' # type: ignore
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menaikan admin: {e} ditemukan")

        except Exception as e:
            db.rollback()
            return Error(f"Gagal menikan admin: {e} ditemukan")
        return Success('Berhasil menaikan admin')


    @strawberry.mutation(
        permission_classes=[SuperAdminAuth],
        description="(SuperAdmin) Demote superadmin to admin"
    )
    def demote_super_admin(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try:
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id: {id}")

            query.role = 'admin' # type: ignore
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menurunkan superadmin: {e} ditemukan")

        except Exception as e:
            db.rollback()
            return Error(f"Gagal menurunkan superadmin: {e} ditemukan")
        return Success('Berhasil menurunkan superadmin')


    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="(User) Edit user profile"
    )
    def edit_user_profile(
            self, info: Info, user: type.EditUserInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            validate_edit_user(user)
        except ValidationError as e:
            return Error(str(e))

        query = db.query(model.User).filter(model.User.id == user_id)

        if query.count() == 0:
            return Error("User tidak ditemukan")

        try:
            query.update({
                model.User.bio: user.bio,
                model.User.phone_number: user.phone_number,
                model.User.nis: user.nis,
                model.User.website: user.website,
                model.User.facebook: user.facebook,
                model.User.instagram: user.instagram,
                model.User.linkedin: user.linkedin,
                model.User.twitter: user.twitter,
                model.User.github: user.github,
            }) # type: ignore
            db.commit()
            return Success("Profile berhasil diubah")

        except Exception as e:
            db.rollback()
            return Error("Terjadi kesalahan")


    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="(User) Update user avatar",
    )
    def update_user_avatar(
        self, info: Info, avatar_id: int
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        if avatar_id < 1 or avatar_id > 20:
            return Error("Avatar yang dipilih tidak ditemukan")

        query = db.query(model.User).filter(model.User.id == user_id)
        if query.count() == 0:
            return Error("User tidak ditemukan")

        try:
            query.update({
                model.User.profile_picture: avatar.url(avatar_id)
            }) # type: ignore
            db.commit()
            return Success("Foto profil berhasil diubah")
        except:
            db.rollback()
            return Error("Terjadi kesalahan")
