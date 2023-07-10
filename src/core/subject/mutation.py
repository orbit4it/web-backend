import asyncio

import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from helpers.types import Error, Success
from helpers.validation import ValidationError
from permissions import AdminAuth, NotAuth, SuperAdminAuth

from . import model, type


@strawberry.type
class Mutation:


    @strawberry.mutation(
        permission_classes=[AdminAuth],
        description="(AdminAuth) To Create a new Subject"
    )
    def create_subject(self, info:Info, input: type.SubjectInput) -> Success | Error:
        db: Session = info.context['db']

        new_sbuject = model.Subject(**vars(input))

        try:
            db.add(new_sbuject)
            db.commit()

            return Success(f"Materi {input.title} berhasil ditambahkan")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error(f"Terjadi Kesalahan")
        