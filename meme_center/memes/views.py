import json
from typing import Annotated, Any
from uuid import UUID

from fastapi.responses import StreamingResponse

from core.app import Request
from fastapi import APIRouter, File, Form

from memes.schemes import (
    MEME_ID,
    OkSchema,
    UploadFileSchema,
    PAGE,
    PAGE_SIZE,
    MemeSchema,
)

memes_route = APIRouter(prefix="/memes", tags=["MEMES"])


@memes_route.get(
    "",
    summary="Список мемов",
    description="Получить список мемов",
    response_model=list[MemeSchema],
)
async def list_memes(
        request: "Request", page: int = PAGE, page_size: int = PAGE_SIZE
) -> Any:
    return await request.app.store.memes.get_memes(
        page_size,
        (page - 1) * page_size,
    )


@memes_route.get(
    "/{id}",
    summary="получить мем по id",
    description="Получить данные о меме по его id ",
)
async def get_meme_by_id(request: "Request", id: UUID) -> Any:
    meme = await request.app.store.memes.get_meme_by_id(id.hex)
    meme_data = json.dumps({"text": meme.title})
    response = StreamingResponse(
        content=await request.app.store.s3.download(str(meme.id)),
        headers={
            "Content-Disposition": f"attachment; filename={meme.id}.jpg",
            "Content-ID": meme_data,
        },
        media_type="multipart/mixed",
    )
    return response


@memes_route.post(
    "",
    summary="Добавить мем",
    description="Добавить новый мем (с картинкой и текстом)",
    response_model=OkSchema,
)
async def add_meme(
        request: "Request",
        file: Annotated[UploadFileSchema, File()],
        text: Annotated[str, Form()],
) -> Any:
    meme = await request.app.store.memes.create_meme(text)
    await request.app.store.s3.upload(str(meme.id), file.file.read())
    return OkSchema(message="Мем добавлен, id: " + str(meme.id))


@memes_route.put("/{id}", summary="обновить мем", response_model=OkSchema)
async def update_meme(
        request: "Request",
        id: UUID,
        text: Annotated[str, Form()] = None,
        file: Annotated[UploadFileSchema, File()] = None,
) -> Any:
    if text:
        await request.app.store.memes.update_meme(id.hex, text)
    if file:
        await request.app.store.s3.upload(str(id), file.file.read())

    return OkSchema(message="Мем успешно облаплен, id: " + str(id))


@memes_route.delete("/{id}", summary="удалить мем", response_model=OkSchema)
async def delete_mem(
        request: "Request",
        id: UUID,
) -> Any:
    await request.app.store.s3.delete(str(id))
    await request.app.store.memes.delete_meme(id)
    return OkSchema(message="Мем успешно удалён, id: " + str(id))
