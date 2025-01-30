from litestar.plugins.structlog import StructlogPlugin
from litestar_granian import GranianPlugin

from app.config.log import log


structlog = StructlogPlugin(config=log)
granian = GranianPlugin()

plugins = [structlog, granian]
