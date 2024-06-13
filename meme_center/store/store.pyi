from core.app import Application

class Store:
    """Data management service"""

    def __init__(self, app: Application):
        """
        Initialize the store.

        Args:
            app (Application): The main application component.
        """

def setup_store(app: Application):
    app.store = Store(app)
