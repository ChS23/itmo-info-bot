from __future__ import annotations
from litestar import Router

from typing import TYPE_CHECKING

from app.domain.itmo.controllers import ItmoController

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler


route_handlers: list[ControllerRouterHandler] = [
    ItmoController
]

api_router = Router(path="/api", route_handlers=route_handlers)

routers_list: list[Router] = [
    api_router
]

__all__ = [
    "routers_list"
]
