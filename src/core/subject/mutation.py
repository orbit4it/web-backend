import strawberry
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info
from helpers.cloudfile import CloudFileError, cloud_remove_file, cloud_upload_file

from helpers.types import Error, Success
from permissions import AdminAuth

from . import model, type


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[AdminAuth],
        description="(Admin) membuat materi baru",
    )
    async def create_subject(
        self, info: Info, input: type.NewSubjectInput
    ) -> Success | Error:
        db: Session = info.context["db"]
        user_id = info.context["payload"]["sub"]

        try:
            upload_cover = await cloud_upload_file(file=input.cover, field_name="cover")
            del input.cover

            new_subject = model.Subject(
                author_id=user_id,
                cover_url=upload_cover,
                **vars(input),
            )

            db.add(new_subject)
            db.commit()
            return Success(f"Materi {input.title} berhasil ditambahkan")

        except IntegrityError as e:
            print(e)

            db.rollback()
            if "FOREIGN KEY (`division_id`) REFERENCES" in str(e):
                return Error("Divisi tidak ditemukan")

            return Error(f"Terjadi Kesalahan")

        except CloudFileError as e:
            return Error(str(e))

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(Admin) edit satu materi"
    )
    async def edit_subject(
        self, info: Info, id: str, input: type.EditSubjectInput
    ) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Subject).filter(model.Subject.id == id)

            if query.count() == 0:
                return Error("Materi tidak ditemukan")

            query.update(
                {
                    model.Subject.title: input.title,
                    model.Subject.description: input.description,
                    model.Subject.speaker: input.speaker,
                    model.Subject.media_url: input.media_url,
                    model.Subject.division_id: input.division_id,
                }
            )

            if input.cover is not None:
                subject = query.first()

                if subject.cover_url is not None:
                    await cloud_remove_file("cover", subject.cover_url)

                upload_new_cover = await cloud_upload_file(
                    file=input.cover, field_name="cover"
                )
                del input.cover

                query.update({model.Subject.cover_url: upload_new_cover})

            db.commit()
            return Success("Materi berhasil diperbarui")

        except IntegrityError as e:
            print(e)

            db.rollback()
            if "FOREIGN KEY (`division_id`) REFERENCES" in str(e):
                return Error("Divisi tidak ditemukan")

            return Error(f"Terjadi kesalahan")

        except CloudFileError as e:
            return Error(str(e))

    @strawberry.mutation(
        permission_classes=[AdminAuth], description="(Admin) hapus satu materi"
    )
    async def del_subject(self, info: Info, id: str) -> Success | Error:
        db: Session = info.context["db"]

        try:
            query = db.query(model.Subject).filter(model.Subject.id == id)

            if query.count() == 0:
                return Error("Materi tidak ditemukan")

            subject = query.first()
            if subject.cover_url is not None:
                await cloud_remove_file("cover", subject.cover_url)

            query.delete()

            db.commit()
            return Success("Materi berhasil dihapus")

        except IntegrityError as e:
            print(e)

            return Error(f"Terjadi kesalahan")
        except CloudFileError as e:
            return Error(str(e))
