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
