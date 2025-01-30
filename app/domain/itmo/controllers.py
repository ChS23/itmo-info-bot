from typing import Annotated

from litestar import Controller, post
from litestar.params import Body
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from litestar.openapi.spec import Example
from langchain.agents import AgentExecutor

from app.domain.itmo.schemas import RequestSchema, ResponseSchema, ItmoResponseSchema
from app.lib.utils.get_model import get_model
from app.lib.utils.tavily_tools import search_tool


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
        question = data.query.split('\n')[0]
        search_result = await search_tool.ainvoke(question)
        sources = [result['url'] for result in search_result]

        model = get_model(
            model_name="gpt-4o-mini",
            output_model=ItmoResponseSchema
        )
        
        messages = [
            SystemMessage(content="""Вы - информационный агент Университета ИТМО. Ваша задача - отвечать на вопросы об университете.

Правила обработки вопросов:
1. Используйте предоставленную информацию для ответа на вопрос
2. В поле answer верните ТОЛЬКО номер правильного ответа (число от 1 до 10)
3. В поле reasoning объясните выбор, основываясь на предоставленной информации
4. Используйте предоставленные URL в поле sources

Формат ответа:
{
    "answer": число от 1 до 10,
    "reasoning": "объяснение на основе информации"
}"""),
            HumanMessage(content=f"""Информация: {search_result}

Вопрос: {data.query}""")
        ]
        
        result: AIMessage = await model.ainvoke(messages)
        response: ItmoResponseSchema = result.additional_kwargs['parsed']
        
        return ResponseSchema(
            id=data.id,
            answer=response.answer,
            reasoning=response.reasoning,
            sources=sources[:3]
        )
