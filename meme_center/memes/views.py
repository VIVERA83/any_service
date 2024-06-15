from io import BytesIO
from typing import Any, Annotated
from uuid import UUID

from icecream import ic

from core.app import Request
from memes.schemes import OkSchema, UploadFileSchema, ID
from fastapi import APIRouter

memes_route = APIRouter(prefix="/memes", tags=["MEMES"])


@memes_route.get("", response_model=OkSchema)
async def list_memes(request: "Request") -> Any:
    return OkSchema()


@memes_route.get("/{id}", response_model=OkSchema)
async def list_memes(request: "Request", id: Annotated[UUID, ID]) -> Any:
    return OkSchema()


@memes_route.post(
    "",
    description="Добавить новый мем (с картинкой и текстом)",
    response_model=OkSchema,
)
async def list_memes(request: "Request", file: UploadFileSchema, text: str) -> Any:
    meme = await request.app.store.memes.create_meme(text)
    filename = f"{meme.id.hex}.jpg"
    await request.app.store.s3.upload(filename, file.file.read())
    return OkSchema(message="Мем добавлен, id: " + filename)


@memes_route.put("/{id}", response_model=OkSchema)
async def list_memes(request: "Request", id: Annotated[UUID, ID]) -> Any:
    return OkSchema()


@memes_route.delete("/{id}", response_model=OkSchema)
async def list_memes(request: "Request", id: Annotated[UUID, ID]) -> Any:
    return OkSchema()
