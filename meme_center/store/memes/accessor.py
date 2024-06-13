from uuid import UUID

from base.base_accessor import BaseAccessor


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

    async def create_meme(self):
        return None
