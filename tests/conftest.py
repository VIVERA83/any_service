import pytest
from fastapi.testclient import TestClient
from icecream import ic
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import AppSettings, PostgresSettings
from meme_center.core.app import Application
from meme_center.core.logger import setup_logging
from meme_center.core.middelware import setup_middleware
from meme_center.core.routes import setup_routes
from meme_center.store.store import setup_store
from store.database.postgres import Base


def connect_db(app: Application) -> None:
    """Configuring the connection to the database."""
    app.postgres.settings = PostgresSettings()
    app.postgres._db = Base
    app.postgres._engine = create_async_engine(
        app.postgres.settings.dsn(True),
        echo=False,
        future=True,
    )


@pytest.fixture(autouse=True)
def application() -> Application:
    """Creates and configures the main FastAPI application.

    Returns:
        Application: The main FastAPI application.
    """
    """Creates and configures the main FastAPI application.

       Returns:
           Application: The main FastAPI application.
       """
    settings = AppSettings()
    app = Application(
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        version=settings.version,
        title=settings.title,
        description=settings.description,
    )
    app.settings = settings
    app.logger = setup_logging()
    setup_store(app)
    connect_db(app)
    setup_middleware(app)
    setup_routes(app)
    return app


@pytest.fixture()
def client(application) -> TestClient:
    return TestClient(application)
