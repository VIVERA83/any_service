from uuid import UUID

from icecream import ic

from base.base_accessor import BaseAccessor
from store.memes.models import MemeModel


class MemAccessor(BaseAccessor):
    """The accessor for the memes."""

    async def get_meme(self, meme_id: UUID):
        return None

    async def get_memes(self):
        return None

    async def delete_meme(self, meme_id: UUID):
        return None

    async def update_meme(self, meme_id: UUID):
        return None

    async def create_meme(self, title: str) -> MemeModel:
        query = self.app.postgres.get_query_insert(MemeModel, title=title).returning(
            MemeModel
        )
        result = await self.app.postgres.query_execute(query)
        return result.scalars().first()
