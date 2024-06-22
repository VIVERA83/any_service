from uuid import UUID

from sqlalchemy.exc import NoResultFound

from base.base_accessor import BaseAccessor
from store.memes.exeptions import MemNotFoundException

from store.memes.models import MemeModel


def exception_handler(func):

    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except NoResultFound as e:
            raise MemNotFoundException(exception=e)

    return wrapper


class MemAccessor(BaseAccessor):
    """The accessor for the memes."""

    @exception_handler
    async def get_meme_by_id(self, meme_id: str) -> MemeModel:
        query = self.app.postgres.get_query_select(MemeModel).where(
            MemeModel.id == meme_id
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalar_one()

    async def get_memes(self, limit: int, offset: int) -> list[MemeModel]:
        query = (
            self.app.postgres.get_query_select(MemeModel).limit(limit).offset(offset)
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalars().all()  # type: ignore

    @exception_handler
    async def delete_meme(self, meme_id: UUID):
        query = (
            self.app.postgres.get_query_delete(MemeModel)
            .where(MemeModel.id == meme_id)
            .returning(MemeModel)
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalar_one()

    @exception_handler
    async def update_meme(self, meme_id: str, title: str) -> MemeModel:
        query = (
            self.app.postgres.get_query_update(MemeModel, title=title)
            .where(MemeModel.id == meme_id)
            .returning(MemeModel)
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalar_one()

    async def create_meme(self, title: str) -> MemeModel:
        query = self.app.postgres.get_query_insert(MemeModel, title=title).returning(
            MemeModel
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalar_one()
