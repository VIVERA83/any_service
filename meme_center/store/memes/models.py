from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from store.database.postgres import Base


class MemeModel(Base):
    __tablename__ = "memes"

    title: Mapped[str] = mapped_column(init=False)
    image_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        default=uuid4().hex,
        server_default=text("gen_random_uuid()"),
    )
