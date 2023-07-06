import asyncio
from datetime import datetime, timedelta

import strawberry
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.helpers import email, token
from src.helpers.types import Error, Success
from src.permissions import AdminAuth, NotAuth, SuperAdminAuth

from . import model, type


@strawberry.type
class Mutation:


    @strawberry.mutation(permission_classes=[NotAuth])
    def create_user_pending(
        self, info: Info, user_pending: type.UserPendingInput
    ) -> Success:
        db: Session = info.context["db"]

        user_pending_db = model.UserPending(**vars(user_pending))
        db.add(user_pending_db)
        db.commit()

        return Success("Akun sedang diverifikasi, mohon tunggu email verifikasi")


    @strawberry.mutation(permission_classes=[NotAuth])
    def create_user(
        self, info: Info, registration_token: str, password: str
    ) -> Success | Error:
        db: Session = info.context["db"]

        if len(password) < 8:
            return Error("Password minimal 8 karakter")

        user_pending_query = (db.query(model.UserPending)
            .filter(model.UserPending.registration_token == registration_token))

        user_pending = user_pending_query.first()

        if user_pending is None or user_pending.expired_at < datetime.now(): # type: ignore
            return Error("Token registrasi tidak valid")

        user = model.User(
            name=user_pending.name,
            email=user_pending.email,
            password=bcrypt.hash(password),
            nis=user_pending.nis,
            division_id=user_pending.division_id,
            grade_id=user_pending.grade_id,
            refresh_token=token.generate(64)
        )

        try:
            user_pending_query.delete()
            db.add(user)
            db.commit()

            return Success("Registrasi berhasil, kamu bisa login sekarang!")

        except IntegrityError as e:
            db.rollback()
            if "for key 'email'" in str(e):
                return Error("Email sudah digunakan")
            elif "for key 'nis'" in str(e):
                return Error("NIS sudah digunakan")

            return Error("Terjadi kesalahan")


    # permission: admin, superadmin
    @strawberry.mutation(permission_classes=[AdminAuth])
    async def confirm_user(self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]

        registration_token = token.generate(64)
        query = db.query(model.UserPending).filter(model.UserPending.id == id)
        query.update({
            model.UserPending.registration_token: registration_token,
            model.UserPending.expired_at: datetime.now() + timedelta(days=7)
        }) # type: ignore
        db.commit()

        user_pending = query.first()
        if user_pending is None:
            db.rollback()
            return Error("User pending tidak ditemukan")

        asyncio.create_task(email.send(
            user_pending.email, # type: ignore
            user_pending.division.name,
            registration_token
        ))

        return Success("Mengirim email verifikasi")
    

    @strawberry.mutation(permission_classes=[AdminAuth])
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
    

    @strawberry.mutation(permission_classes=[SuperAdminAuth])
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
    

    @strawberry.mutation(permission_classes=[SuperAdminAuth])
    def promote_user(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try: 
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id:  {id}")
        
            query.role = 'admin'
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menaikan user: {e} ditemukan")
        
        except Exception as e: 
            db.rollback()
            return Error(f"Gagal menaikan user: {e} ditemukan")
        return Success('Berhasil menaikan user')
    

    @strawberry.mutation(permission_classes=[SuperAdminAuth])
    def demote_admin(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try: 
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id: {id}")
        
            query.role = 'user'
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menurunkan admin: {e} ditemukan")
        
        except Exception as e: 
            db.rollback()
            return Error(f"Gagal menurunkan admin: {e} ditemukan")
        return Success('Berhasil menurunkan admin')
    

    @strawberry.mutation(permission_classes=[SuperAdminAuth])
    def promote_admin(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try: 
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id: {id}")
        
            query.role = 'superadmin'
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menaikan admin: {e} ditemukan")
        
        except Exception as e: 
            db.rollback()
            return Error(f"Gagal menikan admin: {e} ditemukan")
        return Success('Berhasil menaikan admin')
    

    @strawberry.mutation(permission_classes=[SuperAdminAuth])
    def demote_super_admin(self, info: Info, id:str)-> Success | Error:
        db: Session = info.context["db"]
        try: 
            query = db.query(model.User).filter(model.User.id == id).first()

            if query is None:
                return Error(f"Tidak ada user dengan Id: {id}")
            
            query.role = 'admin'
            db.commit()

        except IntegrityError as e:
            db.rollback()
            return Error(f"Gagal menurunkan superadmin: {e} ditemukan")
        
        except Exception as e: 
            db.rollback()
            return Error(f"Gagal menurunkan superadmin: {e} ditemukan")
        return Success('Berhasil menurunkan superadmin')

    