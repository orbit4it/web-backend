import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

import cloudinary.uploader
from cloudinary.exceptions import (
    BadRequest,
    Error as Cloudinary_error,
    GeneralError as Cloudinary_GeneralError,
    RateLimited,
)
from helpers.types import Error, Success
from permissions import AdminAuth

from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[AdminAuth],
        description="(AdminAuth) To Create a new Subject",
    )
    async def create_subject(
        self, info: Info, input: type.SubjectInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            cover_content = await input.cover.read() # type: ignore

            if len(cover_content) > 3 * 1024 * 1024:
                return Error("Ukuran cover terlalu besar")

            if input.cover.content_type not in ["image/jpeg", "image/jpg", "image/png"]: # type: ignore
                return Error("Format cover tidak diperbolehkan")

            upload_to_cloud = cloudinary.uploader.upload(
                cover_content, folder="web-orbit"
            )

            await input.cover.close() # type: ignore
            del input.cover

            new_subject = model.Subject(
                author_id=user_id,
                cover_url=upload_to_cloud["secure_url"],
                **vars(input),
            )

            db.add(new_subject)
            db.commit()

            return Success(f"Materi {input.title} berhasil ditambahkan")
        except IntegrityError as e:
            print(e)

            db.rollback()
            return Error(f"Terjadi Kesalahan")
        except (
            BadRequest,
            Cloudinary_error,
            Cloudinary_GeneralError,
            RateLimited,
        ) as e:
            print(e)

            return Error(f"Terjadi kesalahan dalam unggah ke cloud")
