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
        question = data.query.splitlines()[0]
        search_result = await search_tool.ainvoke(question)
        sources = [result['url'] for result in search_result]

        model = get_model(
            model_name="gpt-4o",
            output_model=ItmoResponseSchema
        )
        
        messages = [
            SystemMessage(content="""Вы - информационный агент Университета ИТМО, который предоставляет точную информацию на основе поисковых результатов.

Правила обработки вопросов:
1. Внимательно анализируйте предоставленную информацию из поисковых результатов
2. Вопросы содержат варианты ответов с номерами от 1 до 10
3. Ваша задача:
   - Определить правильный вариант ответа на основе найденной информации
   - Если вопрос без вариантов, вернуть null в поле answer
   - Использовать только проверенные факты из результатов поиска

4. В поле reasoning:
   - Приведите конкретные факты из найденной информации
   - Цитируйте или ссылайтесь на источники
   - Объясните, почему выбран именно этот вариант
   - Укажите год или период, если это важно для ответа
   - В конце добавьте "\nМодель: gpt-4o-mini"

5. Формат ответа должен строго соответствовать JSON:
{
    "answer": число от 1 до 10 или null,
    "reasoning": "На основе [источник], в [год] установлено, что [факт]... \nМодель: gpt-4o-mini"
}"""),
            HumanMessage(content=f"""Найденная информация: {search_result}

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
