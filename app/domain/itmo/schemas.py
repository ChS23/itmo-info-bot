import datetime

import msgspec


class RequestSchema(msgspec.Struct):
    query: str
    id: int


class ResponseSchema(msgspec.Struct):
    id: int
    answer: int | None
    reasoning: str
    sources: list[str] | None
