"""A module describing services for working with data."""

from store.database.postgres import Postgres
from store.memes.accessor import MemAccessor
from store.s3.accessor import S3Accessor


class Store:
    """Data management service"""

    def __init__(self, app):
        """Initializing data sources.

        Args:
            app: The application
        """
        self.memes = MemAccessor(app)
        self.s3 = S3Accessor(app)


def setup_store(app):
    """Configuring the connection and disconnection of storage.

    Here we inform the application about the databases of the database and other
    data sources which we run when the application is launched,
    and how to disable them.

    Args:
        app: The application
    """
    app.postgres = Postgres(app)
    app.store = Store(app)
