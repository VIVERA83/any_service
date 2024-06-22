from uuid import UUID

from icecream import ic

from base.base_accessor import BaseAccessor

from store.memes.models import MemeModel


class MemAccessor(BaseAccessor):
    """The accessor for the memes."""

    async def get_meme_by_id(self, meme_id: str) -> MemeModel:
        query = self.app.postgres.get_query_select(MemeModel).where(
            MemeModel.id == meme_id
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalar()

    async def get_memes(self, limit: int, offset: int) -> list[MemeModel]:
        query = (
            self.app.postgres.get_query_select(MemeModel).limit(limit).offset(offset)
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalars().all()  # type: ignore

    async def delete_meme(self, meme_id: UUID):
        return None

    async def update_meme(self, meme_id: str, title: str) -> MemeModel:
        query = (self.app.postgres.get_query_update(MemeModel, title=title)
                 .where(MemeModel.id == meme_id)
                 .returning(MemeModel)
                 )
        result = await self.app.postgres.query_execute(query)
        return result.scalars().first()

    async def create_meme(self, title: str) -> MemeModel:
        query = self.app.postgres.get_query_insert(MemeModel, title=title).returning(
            MemeModel
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalars().first()
