from sqlalchemy.orm import Mapped, mapped_column
from store.database.postgres import Base


class MemeModel(Base):
    __tablename__ = "memes"

    title: Mapped[str] = mapped_column(init=False)
