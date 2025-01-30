import msgspec
from pydantic import BaseModel, Field
from typing import List


class RequestSchema(msgspec.Struct):
    id: int
    query: str


class ResponseSchema(msgspec.Struct):
    id: int
    answer: int
    reasoning: str
    sources: List[str]


class ItmoResponseSchema(BaseModel):
    answer: int = Field(description="Номер правильного ответа (1-10)")
    reasoning: str = Field(description="Объяснение выбора ответа")
    sources: List[str] = Field(description="Список источников информации")
    