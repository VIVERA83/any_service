from io import BytesIO
from typing import Any, Annotated
from uuid import UUID

from core.app import Request
from memes.schemes import OkSchema, UploadFileSchema, ID
from fastapi import APIRouter

memes_route = APIRouter(prefix="/memes", tags=["MEMES"])


@memes_route.get(
    "",
    response_model=OkSchema)
async def list_memes(request: "Request") -> Any:
    return OkSchema()


@memes_route.get(
    "/{id}",
    response_model=OkSchema)
async def list_memes(request: "Request", id: Annotated[UUID, ID]) -> Any:
    return OkSchema()


@memes_route.post(
    "",
    response_model=OkSchema)
async def list_memes(request: "Request") -> Any:
    return OkSchema()


@memes_route.put(
    "/{id}",
    response_model=OkSchema)
async def list_memes(request: "Request", id: Annotated[UUID, ID]) -> Any:
    return OkSchema()


@memes_route.delete(
    "/{id}",
    response_model=OkSchema)
async def list_memes(request: "Request", id: Annotated[UUID, ID]) -> Any:
    return OkSchema()
