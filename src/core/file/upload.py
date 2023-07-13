import cloudinary.uploader
from fastapi import APIRouter, UploadFile

from helpers.types import Error, Success

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()
    if len(content) > 3 * 1024 * 1024:
        return Error("Ukuran cover terlalu besar")

    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        return Error("Format file tidak diperbolehkan")

    upload = cloudinary.uploader.upload(content, folder="web-orbit")

    await file.close()

    return upload
