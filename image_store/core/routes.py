from core.app import Application
from image.views import image_route


def setup_routes(app: Application):
    """Configuring the connected routes to the application."""
    app.include_router(image_route)
