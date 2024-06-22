from typing import Annotated, Any

from icecream import ic

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
async def get_meme_by_id(request: "Request", meme_id: MEME_ID) -> Any:
    if meme := await request.app.store.memes.get_meme_by_id(meme_id.hex):
        return await request.app.store.s3.download(str(meme.id))
    raise KeyError(f"Meme for id {meme_id} not found")


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
    request.app.logger.warning(request.url)
    meme = await request.app.store.memes.create_meme(text)
    await request.app.store.s3.upload(str(meme.id), file.file.read())
    return OkSchema(message="Мем добавлен, id: " + str(meme.id))


@memes_route.put("/{id}", summary="обновить мем", response_model=OkSchema)
async def update_mem(
    request: "Request",
    meme_id: MEME_ID,
    text: Annotated[str, Form()] = None,
    file: Annotated[UploadFileSchema, File()] = None,
) -> Any:
    if text:
        await request.app.store.memes.update_meme(meme_id.hex, text)
    if file:
        await request.app.store.s3.upload(str(meme_id), file.file.read())

    return OkSchema(message="Мем успешно облаплен, id: " + str(meme_id))


@memes_route.delete("/{id}", summary="удалить мем", response_model=OkSchema)
async def delete_mem(
    request: "Request",
    meme_id: MEME_ID,
) -> Any:
    await request.app.store.s3.delete(str(meme_id))
    await request.app.store.memes.delete_meme(meme_id.hex)
    return OkSchema(message="Мем успешно удалён, id: " + str(meme_id))
