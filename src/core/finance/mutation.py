import strawberry
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from strawberry.types import Info

from helpers.types import Error, Success
from permissions.auth import AdminAuth

from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[AdminAuth],
        description="(Admin) menambahkan transaksi kas baru",
    )
    def add_balance(self, info: Info, input: type.NewBalanceInput) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            new_balance = model.Balance(user_id=user_id, **vars(input))

            db.add(new_balance)
            db.commit()

            return Success("Transaksi kas baru berhasil ditambahkan")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(Admin) edit satu transaksi kas"
    )
    def edit_balance(
        self, info: Info, id: str, input: type.EditBalanceInput
    ) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Balance).filter(model.Balance.id == id)
            data = query.first()

            if not data:
                return Error("Transaksi kas tidak ditemukan")

            query.update(
                {
                    model.Balance.title: input.title,
                    model.Balance.date: input.date,
                    model.Balance.note: input.note,
                    model.Balance.amount: input.amount,
                    model.Balance.flow: input.flow,
                    model.Balance.level: input.level,
                }
            )

            db.commit()
            return Success("Transaksi kas berhasil diubah")

        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahan")

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(Admin) hapus satu transaksi kas"
    )
    def del_balance(self, info: Info, id: str) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Balance).filter(model.Balance.id == id)
            data = query.first()

            if not data:
                return Error("Transaksi kas tidak ditemukan")

            query.delete()

            db.commit()
            return Success("Transaksi kas berhasil dihapus")

        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error("Terjadi kesalahand")
