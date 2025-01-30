from litestar import Litestar

from app.server import plugins, openapi, dependencies, routers, cors, startup
from app.config.settings import get_settings

settings = get_settings()


def create_app() -> Litestar:
    
    return Litestar(
        plugins=plugins.plugins,
        openapi_config=openapi.config,
        debug=settings.app.DEBUG,
        route_handlers=routers.routers_list,
        on_startup=[startup.start_http_session]
    )


app = create_app()
