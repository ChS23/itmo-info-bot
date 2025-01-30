from functools import lru_cache
from langchain_community.tools import TavilySearchResults


search_tool = TavilySearchResults(
    name="search",
    max_results=3,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False
)
