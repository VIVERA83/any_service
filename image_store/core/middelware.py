from core.app import Application


def setup_middleware(app: Application):
    """Sets up the middleware for the FastAPI application.

    Args:
        app (Application): The FastAPI application.

    Raises:
        Exception: If the middleware cannot be set up.
    """
