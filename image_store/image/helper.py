import aiohttp

from core.app import Request
from image.schemas import UploadFileSchema
from starlette.responses import StreamingResponse


async def s3_upload_image(request: "Request", file: UploadFileSchema):
    await request.app.store.minio.client.put_object(
        bucket_name=request.app.store.minio.settings.minio_bucket_name,
        object_name=file.filename,
        data=file.file,
        length=file.size,
    )


async def s3_delete_image(request: "Request", object_name: str):
    await request.app.store.minio.client.remove_object(
        bucket_name=request.app.store.minio.settings.minio_bucket_name,
        object_name=object_name,
    )


async def s3_stream_image(request: "Request", object_name: str) -> StreamingResponse:
    session = aiohttp.ClientSession()
    try:
        response = await request.app.store.minio.client.get_object(
            bucket_name=request.app.store.minio.settings.minio_bucket_name,
            object_name=object_name,
            session=session,
        )

        async def stream_iterator():
            async for chunk in response.content:
                yield chunk
            await session.close()

        return StreamingResponse(
            content=stream_iterator(),
            headers=_create_headers(object_name),
        )
    except Exception as e:
        await session.close()
    raise KeyError(f"Object {object_name} not found")


async def s3_update_image(request: "Request", filename: str):
    for b in await request.app.store.minio.client.list_buckets():
        if filename == b:
            print(b)


def _create_headers(filename: str) -> dict:
    return {
        "Content-Disposition": f"attachment filename={filename}",
        "Content-type": "image/jpeg",
    }
