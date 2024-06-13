from core.app import Application
from memes.views import memes_route


def setup_routes(app: Application):
    """Configuring the connected routes to the application."""
    app.include_router(memes_route)
