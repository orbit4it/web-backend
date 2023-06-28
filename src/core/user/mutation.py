import strawberry
import asyncio

from datetime import datetime, timedelta
from strawberry.types import Info
from sqlalchemy.orm import Session

from src.helpers import token, email
from src.helpers.types import Success, Error
from . import model, type

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user_pending(self, info: Info, user_pending: type.UserPendingInput) -> Success:
        db: Session = info.context["db"]

        db_user_pending = model.UserPending(**vars(user_pending))
        db.add(db_user_pending)
        db.commit()
        db.refresh(db_user_pending)

        return Success("Akun sedang diverifikasi, mohon tunggu konfirmasi email")

    @strawberry.mutation
    def create_user(self, info: Info) -> str:
        return "Create user"

    @strawberry.mutation
    async def confirm_user(self, info: Info, id: int) -> Success | Error:
        db: Session = info.context["db"]
        verif_token = token.generate(64)
        query = db.query(model.UserPending).filter(model.UserPending.id == id)
        query.update({
            model.UserPending.token: verif_token,
            model.UserPending.expired_at: datetime.now() + timedelta(days=7)
        }) # type: ignore
        db.commit()

        db_user_pending = query.first()
        if db_user_pending is None:
            return Error("User pending tidak ditemukan")

        asyncio.create_task(email.send(
            db_user_pending.email, # type: ignore
            db_user_pending.division.name,
            verif_token
        ))

        return Success("Mengirim email verifikasi")
