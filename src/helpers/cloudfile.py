from strawberry.file_uploads import Upload
import cloudinary.uploader
from cloudinary.exceptions import (
    BadRequest,
    Error as Cloudinary_error,
    GeneralError as Cloudinary_GeneralError,
    RateLimited,
)


class CloudFileError(Exception):
    def __init__(self, message="Terjadi kesalahan pada file"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


async def cloud_upload_file(
    file: Upload,
    field_name: str = "file",
    max_size: int = 3,
    allowed_formats=["image/jpeg", "image/jpg", "image/png"],
):
    content = await file.read()

    if len(content) > max_size * 1023 * 1024:
        raise CloudFileError(f"Ukuran {field_name} melebihi maksimal {max_size} MB")

    if file.content_type not in allowed_formats:
        raise CloudFileError(f"Format {field_name} tidak diperbolehkan")

    try:
        upload_to_cloud = cloudinary.uploader.upload(content, folder="web-orbit")

        await file.close()

        return upload_to_cloud["secure_url"]

    except (BadRequest, Cloudinary_error, Cloudinary_GeneralError, RateLimited) as e:
        print(e)

        raise CloudFileError(f"Terjadi kesalahan dalam menyimpan {field_name}")


async def cloud_remove_file(field_name: str = "file", url: str = ""):
    try:
        public_id = url.split("/")[-1].split(".")["0"]
        remove = await cloudinary.uploader.destroy(f"web-orbit/{public_id}")

        is_removed = remove["result"] == "ok"

        if is_removed:
            print(f"1 {field_name} berhasil dihapus")
        else:
            print(f'{field_name} dengan id "{public_id}" tidak ditemukan')

        return is_removed

    except (BadRequest, Cloudinary_error, Cloudinary_GeneralError, RateLimited) as e:
        print(e)

        raise CloudFileError(f"Terjadi kesalahan dalam menyimpan {field_name}")
