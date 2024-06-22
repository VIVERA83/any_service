from typing import Any
from uuid import UUID

from core.app import Request
from fastapi import APIRouter

from .helper import s3_delete_image, s3_stream_image, s3_upload_image, s3_update_image
from .schemas import OkSchema, UploadFileSchema

image_route = APIRouter()


@image_route.post(
    "/upload",
    response_model=OkSchema,
)
async def upload_image(request: "Request", file: UploadFileSchema) -> Any:
    await s3_upload_image(request, file)
    return OkSchema()


@image_route.post("/download")
async def download(request: "Request", meme_id: str) -> Any:
    return await s3_stream_image(request, meme_id)


@image_route.delete("/delete")
async def delete(request: "Request", file_name: str) -> Any:
    await s3_delete_image(request, file_name)
    return OkSchema()


@image_route.put("/update")
async def update(request: "Request", meme_id: UUID) -> Any:
    await s3_update_image(request, meme_id.hex)
    return OkSchema()
