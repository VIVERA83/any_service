from typing import Annotated, Any
from uuid import UUID

from core.app import Request
from fastapi import APIRouter, File, Form

from memes.schemes import ID, OkSchema, UploadFileSchema, PAGE, PAGE_SIZE, MemeSchema

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
    description="Получить данные о меме по его id "
)
async def get_meme_by_id(request: "Request", id: Annotated[UUID, ID]) -> Any:
    if meme := await request.app.store.memes.get_meme_by_id(id.hex):
        return await request.app.store.s3.download(str(meme.id))
    raise KeyError(f"Meme for id {id} not found")


@memes_route.post(
    "",
    summary="Добавить мем",
    description="Добавить новый мем (с картинкой и текстом)",
    response_model=OkSchema,
)
async def add_meme(request: "Request",
                   file: Annotated[UploadFileSchema, File()],
                   text: Annotated[str, Form()]) -> Any:
    request.app.logger.warning(request.url)
    meme = await request.app.store.memes.create_meme(text)
    await request.app.store.s3.upload(str(meme.id), file.file.read())
    return OkSchema(message="Мем добавлен, id: " + str(meme.id))


@memes_route.put(
    "/{id}",
    summary="обновить мем",
    response_model=OkSchema)
async def update_mem(request: "Request",
                     id: Annotated[UUID, UUID],
                     text: Annotated[str, Form()] = None,
                     file: Annotated[UploadFileSchema, File()] = None,
                     ) -> Any:
    if text:
        await request.app.store.memes.update_meme(id.hex, text)
    if file:
        pass

    return OkSchema(message="Мем успешно облаплен, id: " + str(id))
