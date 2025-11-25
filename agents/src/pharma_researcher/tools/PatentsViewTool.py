from crewai.tools import BaseTool
from typing import Optional, Type, Dict, List, Union, Any
from pydantic import BaseModel, Field
import requests
import json
import os


class PatentsViewToolInput(BaseModel):
    query: Union[str, Dict[str, Any]] = Field(
        ...,
        description=(
            "PatentsView search query as a JSON object or string. "
            "For keyword matching, use text operators: "
            "_text_any (matches ANY keyword), _text_all (matches ALL keywords), "
            "_text_phrase (exact phrase). "
            "Example for keywords 'cancer treatment': "
            '{"_text_any": {"patent_abstract": "cancer treatment"}} '
            "or for exact phrase: "
            '{"_text_phrase": {"patent_title": "cancer treatment"}}'
        )
    )
    fields: Optional[List[str]] = Field(
        default=None,
        description=(
            "List of fields to return. Common fields: patent_id, patent_title, "
            "patent_abstract, patent_date, inventors, assignees, cpc_group_id"
        )
    )
    sort: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description='Sort order as list of dicts, e.g., [{"patent_date": "desc"}]'
    )
    size: Optional[int] = Field(
        default=100,
        description="Number of results to return (max 1000)"
    )
    after: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Pagination cursor from previous response"
    )
    exclude_withdrawn: Optional[bool] = Field(
        default=True,
        description="Exclude withdrawn patents (patent endpoint only)"
    )
    pad_patent_id: Optional[bool] = Field(
        default=False,
        description="Pad patent IDs with leading zeros"
    )
    endpoint: Optional[str] = Field(
        default="patent",
        description="API endpoint: patent, inventor, assignee, cpc_subsection, etc."
    )


class PatentsViewTool(BaseTool):
    name: str = "patents_view_api_tool"
    description: str = (
        "Search patents using the PatentsView API. "
        "Use this tool to find patents by keywords in title, abstract, or other fields. "
        "For keyword matching, use text operators: "
        "_text_any (matches ANY keyword), _text_all (matches ALL keywords), "
        "_text_phrase (exact phrase match). "
        "Example: To find patents about 'cancer treatment', use: "
        '{"_text_any": {"patent_abstract": "cancer treatment"}}'
    )
    args_schema: Type[BaseModel] = PatentsViewToolInput

    def _run(
        self,
        query: Union[str, Dict[str, Any]],
        fields: Optional[List[str]] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        size: Optional[int] = 100,
        after: Optional[Union[str, List[str]]] = None,
        exclude_withdrawn: Optional[bool] = True,
        pad_patent_id: Optional[bool] = False,
        endpoint: Optional[str] = "patent"
    ) -> Dict[str, Any]:
        """
        Search patents using PatentsView API with keyword matching.
        
        Query Examples for Keyword Matching:
        
        1. Match ANY keyword (OR search):
           query = {"_text_any": {"patent_abstract": "cancer treatment therapy"}}
           Finds patents with "cancer" OR "treatment" OR "therapy" in abstract
        
        2. Match ALL keywords (AND search):
           query = {"_text_all": {"patent_abstract": "cancer treatment therapy"}}
           Finds patents with "cancer" AND "treatment" AND "therapy" in abstract
        
        3. Exact phrase match:
           query = {"_text_phrase": {"patent_title": "cancer treatment"}}
           Finds patents with exact phrase "cancer treatment" in title
        
        4. Search multiple fields:
           query = {"_or": [
               {"_text_any": {"patent_title": "cancer"}},
               {"_text_any": {"patent_abstract": "cancer"}}
           ]}
        
        5. Combine with date filters:
           query = {"_and": [
               {"_text_any": {"patent_abstract": "cancer treatment"}},
               {"_gte": {"patent_date": "2020-01-01"}}
           ]}
        
        Common searchable text fields:
        - patent_title: Patent title
        - patent_abstract: Patent abstract/summary
        - inventor_name_first, inventor_name_last: Inventor names
        - assignee_organization: Company/organization name
        """


        # ------------------------------
        # 1. API Key (required)
        # ------------------------------
        api_key = os.getenv("PATENTS_VIEW_API_KEY")
        if not api_key:
            return {"error": "Missing PATENTS_VIEW_API_KEY environment variable"}

        # ------------------------------
        # 2. Endpoint
        # ------------------------------
        # valid_endpoints = [
        #     "patent", "inventor", "assignee",
        #     "cpc_subsection", "uspc",
        #     "nber_subcat", "location", "citation"
        # ]

        # if endpoint not in valid_endpoints:
        #     return {"error": f"Invalid endpoint. Must be one of {valid_endpoints}"}

        # Correct PatentsView URL - query is passed as parameter, not in URL path
        url = f"https://search.patentsview.org/api/v1/patent"

        # ------------------------------
        # 3. Parse query
        # ------------------------------
        if isinstance(query, str):
            try:
                query_dict = json.loads(query)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON string passed to 'query'"}
        else:
            query_dict = query

        # ------------------------------
        # 4. Build request params
        # ------------------------------
        params = {
            "q": json.dumps(query_dict),
        }

        if fields:
            params["f"] = json.dumps(fields)

        if sort:
            params["s"] = json.dumps(sort)

        options = {
            "size": min(size, 1000),
            "pad_patent_id": pad_patent_id
        }

        if after:
            options["after"] = after

        if endpoint == "patent":
            options["exclude_withdrawn"] = exclude_withdrawn

        params["o"] = json.dumps(options)

        # Required headers (fix for 403)
        headers = {
            "User-Agent": "pharma-researcher/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Api-Key": api_key
        }

        # ------------------------------
        # 5. Execute request
        # ------------------------------
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Determine which key holds results
            key = f"{endpoint}s" if f"{endpoint}s" in data else endpoint
            results = data.get(key, [])

            # Add metadata
            data["_query_metadata"] = {
                "endpoint": endpoint,
                "query": query_dict,
                "total_results": data.get("total_patent_count", data.get("count", 0)),
                "results_returned": len(results),
                "api_url": url,
                "params": params
            }

            return data

        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error {e.response.status_code}",
                "details": e.response.text[:500],
                "url": url,
                "params": params
            }

        except Exception as e:
            return {
                "error": str(e),
                "url": url,
                "params": params
            }
