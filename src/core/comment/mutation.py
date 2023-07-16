import strawberry
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError
from strawberry.types import Info
from helpers.types import Error, Success

from permissions.auth import UserAuth

from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="(Login) user memberikan komentar terhadap materi",
    )
    def send_comment(
        self, info: Info, subject_id: str, input: type.CommentInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            if len(input.content) > 230:
                return Error("Komentar maksimal 230 karakter")

            if not (0 < input.rating <= 5):
                return Error("Rating harus di rentang 1-5")

            comment = model.Comment(
                user_id=user_id, subject_id=subject_id, **vars(input)
            )

            db.add(comment)
            db.commit()

            return Success(f"Komen berhasil ditambahkan!")

        except IntegrityError as e:
            db.rollback()
            if "FOREIGN KEY (`subject_id`) REFERENCES" in str(e):
                return Error("Materi tidak ditemukan")

            print(e)
            return Error("Terjadi kesalahan")
