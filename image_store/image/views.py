from typing import Any

from icecream import ic

from .helper import s3_upload_image, s3_stream_image, s3_delete_image
from .schemas import UploadFileSchema, OkSchema

from core.app import Request
from fastapi import APIRouter

image_route = APIRouter()


@image_route.post(
    "/upload",
    response_model=OkSchema,
)
async def upload_image(request: "Request", file: UploadFileSchema) -> Any:
    await s3_upload_image(request, file)
    return OkSchema()


@image_route.post(
    "/download",
)
async def download(request: "Request", file_name: str) -> Any:
    return await s3_stream_image(request, file_name)


@image_route.post("/remove")
async def remove(request: "Request", file_name: str) -> Any:
    await s3_delete_image(request, file_name)
    return OkSchema()
