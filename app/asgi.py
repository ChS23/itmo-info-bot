from litestar import Litestar

from app.server import plugins, openapi, routers
from app.config.settings import get_settings

settings = get_settings()


def create_app() -> Litestar:
    
    return Litestar(
        plugins=plugins.plugins,
        openapi_config=openapi.config,
        debug=settings.app.DEBUG,
        route_handlers=routers.routers_list
    )


app = create_app()
