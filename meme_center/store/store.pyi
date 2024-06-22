from core.app import Application
from store.memes.accessor import MemAccessor
from store.s3.accessor import S3Accessor

class Store:
    """Data management service"""

    memes: MemAccessor
    s3: S3Accessor

    def __init__(self, app: Application):
        """
        Initialize the store.

        Args:
            app (Application): The main application component.
        """

def setup_store(app):
    """Configuring the connection and disconnection of storage.

    Here we inform the application about the databases of the database and other
    data sources which we run when the application is launched,
    and how to disable them.

    Args:
        app: The application
    """
