from typing import Annotated

from litestar import Controller, post
from litestar.params import Body
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from litestar.openapi.spec import Example

from app.domain.itmo.schemas import RequestSchema, ResponseSchema, ItmoResponseSchema
from app.lib.utils.get_model import get_model
from app.lib.utils.tavily_tools import search_tool
from app.services.agents.promts import ANSWER_PROMPT


class ItmoController(Controller):
    @post("/request")
    async def get_itmo_info(
            self,
            data: Annotated[
                RequestSchema,
                Body(
                    examples=[
                        Example(
                            summary="Пример запроса",
                            value={
                                "id": 1,
                                "query": "В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?\n1. ARWU (Shanghai Ranking)\n2. Times Higher Education (THE) World University Rankings\n3. QS World University Rankings\n4. U.S. News & World Report Best Global Universities"
                            }
                        )
                    ]
                )
            ]
    ) -> ResponseSchema:
        search_result = await search_tool.ainvoke(data.query.splitlines()[0])

        model = get_model(
            model_name="gpt-4o",
            output_model=ItmoResponseSchema
        )
        
        messages = [
            SystemMessage(content=ANSWER_PROMPT),
            HumanMessage(content=f"""Найденная информация: {search_result}

Вопрос: {data.query}""")
        ]
        
        result: AIMessage = await model.ainvoke(messages)
        response: ItmoResponseSchema = result.additional_kwargs['parsed']
        
        return ResponseSchema(
            id=data.id,
            answer=response.answer,
            reasoning=response.reasoning,
            sources=[item['url'] for item in search_result][:3]
        )
