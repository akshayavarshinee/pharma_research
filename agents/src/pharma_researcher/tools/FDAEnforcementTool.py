from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
from datetime import datetime
from urllib.parse import quote



class FDAEnforcementToolInput(BaseModel):
    """Input schema for FDAEnforcementTool."""
    search_query: Optional[str] = Field(
        None,
        description="""
        OpenFDA search query for recall/enforcement actions.
        
        Common search fields:
        - product_description:"ranitidine" - Product name/description
        - reason_for_recall:"contamination" - Reason for recall
        - classification:"Class I" - Recall severity (Class I, II, III)
        - status:"Ongoing" - Recall status
        - recalling_firm:"Pfizer" - Company conducting recall
        - state:"CA" - State code where recalled
        
        Example: product_description:"metformin"+AND+classification:"Class I"
        """
    )
    product: Optional[str] = Field(
        None,
        description="Search by product name/description. Shortcut for product_description field."
    )
    classification: Optional[str] = Field(
        None,
        description="""
        Recall classification severity:
        - "Class I" - Dangerous/life-threatening
        - "Class II" - Temporary/reversible health consequences  
        - "Class III" - Unlikely to cause adverse health consequences
        """
    )
    status: Optional[str] = Field(
        None,
        description='Recall status: "Ongoing", "Completed", "Terminated", "Pending"'
    )
    state: Optional[str] = Field(
        None,
        description="US state code where product was recalled (e.g., 'CA', 'NY', 'TX')"
    )
    recalling_firm: Optional[str] = Field(
        None,
        description="Name of company/firm conducting the recall"
    )
    date_range: Optional[Dict[str, str]] = Field(
        None,
        description="""
        Filter by recall initiation date (YYYY-MM-DD format).
        Example: {"from": "2023-01-01", "to": "2023-12-31"}
        """
    )
    count: Optional[str] = Field(
        None,
        description="""
        Field to count/aggregate by. Returns grouped statistics.
        Examples: "classification", "state", "recalling_firm.exact", "status"
        """
    )
    limit: Optional[int] = Field(
        100,
        description="Maximum number of results (1-1000). Default: 100"
    )
    skip: Optional[int] = Field(
        0,
        description="Number of results to skip for pagination"
    )


class FDAEnforcementTool(BaseTool):
    name: str = "fda_recall_tool"
    description: str = """
    Search FDA Drug Recall & Enforcement Reports database.
    
    Use cases:
    - Track drug recalls and safety actions
    - Analyze recall patterns by classification severity
    - Monitor specific drugs or companies
    - Geographic recall distribution analysis
    - Identify recall reasons and trends
    
    Examples:
    1. Product recalls: product="ranitidine", classification="Class I"
    2. Company recalls: recalling_firm="Pfizer", status="Ongoing"
    3. Date range: product="metformin", date_range={"from": "2020-01-01", "to": "2023-12-31"}
    4. Aggregation: count="classification"
    """
    args_schema: Type[BaseModel] = FDAEnforcementToolInput

    def _run(
        self,
        search_query: Optional[str] = None,
        product: Optional[str] = None,
        classification: Optional[str] = None,
        status: Optional[str] = None,
        state: Optional[str] = None,
        recalling_firm: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None,
        count: Optional[str] = None,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0
    ) -> Dict[str, Any]:
        """
        Execute FDA Enforcement/Recall search.
        
        Returns:
            Dict with recall data and metadata
        """
        url = "https://api.fda.gov/drug/enforcement.json"
        
        # Build query
        query_parts = []
        
        if search_query:
            query_parts.append(search_query)
        
        if product:
            product = product.lower()
            query_parts.append(f'product_description:"{product}"')
        
        if classification:
            query_parts.append(f'classification:"{classification}"')
        
        if status:
            query_parts.append(f'status:"{status}"')
        
        if state:
            query_parts.append(f'state:"{state}"')
        
        if recalling_firm:
            query_parts.append(f'recalling_firm:"{recalling_firm}"')
        
        if date_range:
            date_from = date_range.get("from", "1900-01-01").replace("-", "")
            date_to = date_range.get("to", datetime.now().strftime("%Y-%m-%d")).replace("-", "")
            query_parts.append(f"recall_initiation_date:[{date_from}+TO+{date_to}]")

        
        query_parts = list(dict.fromkeys(query_parts))
        final_query = "+AND+".join(query_parts) if query_parts else None
        
        if not final_query and not count:
            return {"error": "At least one search/filter parameter or count must be provided"}
        
        # Build request parameters
        params: Dict[str, Any] = {}
        
        if final_query:
            params["search"] = quote(final_query, safe=':"[]()+')
        
        if count:
            params["count"] = count
        else:
            params["limit"] = min(max(1, limit), 1000)
            if skip > 0:
                params["skip"] = skip
        
        try:
            headers = {"User-Agent": "pharma-researcher/1.0"}
            response = requests.get(url, params=params, headers=headers, timeout=30)

            response.raise_for_status()
            data = response.json()
            
            # Add metadata
            result = {
                "_query_metadata": {
                    "query": final_query,
                    "count_field": count,
                    "limit": limit,
                    "skip": skip,
                    "total_results": data.get("meta", {}).get("results", {}).get("total", 0),
                    "results_returned": len(data.get("results", []))
                }
            }
            
            # Handle count queries
            if count and "results" in data:
                result["aggregations"] = data["results"]
                result["aggregation_count"] = len(data["results"])
                return result
            
            result.update(data)
            return result
            
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"FDA API error: {e.response.status_code}",
                "details": e.response.text[:500],
                "url": url,
                "params": params
            }
        except Exception as e:
            return {
                "error": f"Request failed: {str(e)}",
                "url": url,
                "params": params
            }
