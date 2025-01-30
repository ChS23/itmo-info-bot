from litestar import Controller, post

from app.domain.itmo.schemas import RequestSchema, ResponseSchema


class ItmoController(Controller):
    @post("/request")
    async def get_itmo_info(
            self,
            data: RequestSchema
    ) -> ResponseSchema:
        return ResponseSchema(
            id=data.id,
            answer=1,
            reasoning="",
            sources=[]
        )
