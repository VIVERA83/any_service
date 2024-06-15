import aiohttp
from miniopy_async import S3Error

from starlette.responses import StreamingResponse

from core.app import Request
from image.schemas import UploadFileSchema


async def s3_upload_image(request: "Request", file: UploadFileSchema):
    await request.app.store.minio.client.put_object(
        bucket_name=request.app.store.minio.settings.minio_bucket_name,
        object_name=file.filename,
        data=file.file,
        length=file.size,
    )


async def s3_stream_image(request: "Request", object_name: str) -> StreamingResponse:
    return StreamingResponse(
        content=_async_request(request, object_name),
        headers=_create_headers(object_name),
    )


async def s3_delete_image(request: "Request", object_name: str):
    await request.app.store.minio.client.remove_object(
        bucket_name=request.app.store.minio.settings.minio_bucket_name,
        object_name=object_name,
    )


async def _async_request(request: "Request", object_name: str):
    async with aiohttp.ClientSession() as client:
        response = await request.app.store.minio.client.get_object(
            bucket_name=request.app.store.minio.settings.minio_bucket_name,
            object_name=object_name,
            session=client,
        )
        async for chunk in response.content:
            yield chunk


def _create_headers(filename: str) -> dict:
    return {
        "Content-Disposition": f"attachment filename={filename}",
        "Content-type": "image/jpeg",
    }
