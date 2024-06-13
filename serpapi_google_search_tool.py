import requests
from app import serp_api_key

from typing import Type, Any
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

class SerpApiGoogleSearchToolSchema(BaseModel):
    q: str = Field(..., description="Parameter defines the query you want to search. You can use anything that you would use in a regular Google search. e.g. inurl:, site:, intitle:.")
    tbs: str = Field("qdr:w2", description="Time filter to limit the search to the last two weeks.")

class SerpApiGoogleSearchTool(BaseTool):
    name: str = "Google Search"
    description: str = "Search the internet"
    args_schema: Type[BaseModel] = SerpApiGoogleSearchToolSchema
    search_url: str = "https://serpapi.com/search"

    def _run(
        self,
        q: str,
        tbs: str = "qdr:w2",
        **kwargs: Any,
    ) -> Any:
        payload = {
            "engine": "google",
            "q": q,
            "tbs": tbs,
            "api_key": serp_api_key,
        }
        headers = {
            'content-type': 'application/json'
        }
    
        response = requests.request("GET", self.search_url, headers=headers, params=payload)
        results = response.json()
    
        summary = ""
        if 'answer_box_list' in results:
            summary += str(results['answer_box_list'])
        elif 'answer_box' in results:
            summary += str(results['answer_box'])
        elif 'organic_results' in results:
            summary += str(results['organic_results'])
        elif 'sports_results' in results:
            summary += str(results['sports_results'])
        elif 'knowledge_graph' in results:
            summary += str(results['knowledge_graph'])
        elif 'top_stories' in results:
            summary += str(results['top_stories'])
        
        print(summary)
        
        return summary
