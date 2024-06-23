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


@image_route.post("/download/{meme_id}")
async def download(request: "Request", meme_id: UUID) -> Any:
    return await s3_stream_image(request, str(meme_id))


@image_route.delete("/delete/{meme_id}")
async def delete(request: "Request", meme_id: UUID) -> Any:
    await s3_delete_image(request, str(meme_id))
    return OkSchema()


@image_route.put("/update/{meme_id}")
async def update(request: "Request", meme_id: UUID) -> Any:
    await s3_update_image(request, str(meme_id))
    return OkSchema()
