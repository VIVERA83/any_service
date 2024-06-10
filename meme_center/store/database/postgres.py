from dataclasses import dataclass
from typing import Optional, Type

from base.base_accessor import BaseAccessor
from core.settings import PostgresSettings
from sqlalchemy import (
    DATETIME,
    TIMESTAMP,
    MetaData,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.decl_api import MappedAsDataclass


@dataclass
class Base(MappedAsDataclass, DeclarativeBase):
    """Setting up metadata.

    In particular, we specify a schema for storing tables.
    """

    metadata = MetaData(
        schema=PostgresSettings().postgres_schema,
        quote_schema=True,
    )
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    created: Mapped[DATETIME] = mapped_column(
        TIMESTAMP,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    modified: Mapped[DATETIME] = mapped_column(
        TIMESTAMP,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        init=False,
    )

    def __repr__(self):
        """Redefinition.

        Returns:
            object: new instance name
        """
        return "{class_name}(id={id})".format(
            id=self.id,
            class_name=self.__class__.__name__,
        )

    __str__ = __repr__


class Postgres(BaseAccessor):
    """Description of the rules for connecting.

    PostgresSQL to the Fast-Api application.
    """

    _engine: Optional[AsyncEngine] = None
    _db: Optional[Type[DeclarativeBase]] = None
    settings: Optional[PostgresSettings] = None

    async def connect(self):
        """Configuring the connection to the database."""
        self.settings = PostgresSettings()
        self._db = Base
        self._engine = create_async_engine(
            self.settings.dsn(True),
            echo=False,
            future=True,
        )
        self.logger.info(f"{self.__class__.__name__} {self.settings.dsn()} connected")

    async def disconnect(self):
        """Closing the connection to the database."""
        if self._engine:
            await self._engine.dispose()
        self.logger.info(f"{self.__class__.__name__} disconnected")

    @property
    def session(self) -> AsyncSession:
        """Get the async session for the database.

        Returns:
            AsyncSession: the async session for the database
        """
        return AsyncSession(self._engine, expire_on_commit=False)
