from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any, Union
from pydantic import BaseModel, Field
import requests
from datetime import datetime
from urllib.parse import quote


class FDAAdverseEventsToolInput(BaseModel):
    """Input schema for FDAAdverseEventsTool."""
    search_query: Optional[str] = Field(
        None,
        description="""
        OpenFDA search query. Use field:value format.
        
        Common fields:
        - patient.drug.medicinalproduct:"metformin"
        - patient.drug.openfda.generic_name:"metformin"
        - patient.reaction.reactionmeddrapt:"nausea"
        - serious:1 or serious:2 (1=serious, 2=non-serious)
        - patient.patientsex:1 (1=Male, 2=Female)
        
        Operators: AND, OR, + (must contain)
        Example: patient.drug.medicinalproduct:"jardiance"+AND+serious:1
        """
    )
    count: Optional[str] = Field(
        None,
        description="""
        Field to count/aggregate by. Returns grouped statistics.
        
        Examples:
        - "patient.reaction.reactionmeddrapt.exact" - Count by reaction type
        - "patient.drug.medicinalproduct.exact" - Count by drug
        - "receivedate" - Count by date
        - "serious" - Count serious vs non-serious
        """
    )
    date_range: Optional[Dict[str, str]] = Field(
        None,
        description="""
        Filter by date range (YYYYMMDD format).
        Example: {"from": "20200101", "to": "20231231"}
        Applies to receivedate field.
        """
    )
    country: Optional[str] = Field(
        None,
        description="Filter by country code. Example: 'US', 'GB', 'IN'"
    )
    serious_only: Optional[bool] = Field(
        None,
        description="If True, only return serious adverse events (serious=1)"
    )
    limit: Optional[int] = Field(
        100,
        description="Maximum number of results (1-1000). Default: 100"
    )
    skip: Optional[int] = Field(
        0,
        description="Number of results to skip for pagination. Default: 0"
    )
    extract_fields: Optional[bool] = Field(
        True,
        description="Extract and simplify key fields for easier consumption. Default: True"
    )


class FDAAdverseEventsTool(BaseTool):
    name: str = "fda_adverse_events_tool"
    description: str = """
    Search FDA Adverse Event Reporting System (FAERS) database for drug safety signals.
    
    Use cases:
    - Find adverse events for specific drugs
    - Analyze reaction patterns and frequencies
    - Compare safety profiles across drugs
    - Identify serious vs non-serious events
    - Track temporal trends in adverse events
    
    Examples:
    1. All events for a drug: search_query='patient.drug.medicinalproduct:"metformin"'
    2. Serious events only: search_query='patient.drug.medicinalproduct:"jardiance"', serious_only=True
    3. Count reactions: count='patient.reaction.reactionmeddrapt.exact'
    4. Date range: date_range={"from": "20230101", "to": "20231231"}
    """
    args_schema: Type[BaseModel] = FDAAdverseEventsToolInput

    def _run(
        self,
        search_query: Optional[str] = None,
        count: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None,
        country: Optional[str] = None,
        serious_only: Optional[bool] = None,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0,
        extract_fields: Optional[bool] = True
    ) -> Dict[str, Any]:
        """
        Execute FDA Adverse Events search.
        
        Returns:
            Dict with results, metadata, and query information
        """
        url = "https://api.fda.gov/drug/event.json"
        
        # Build query parts
        query_parts = []
        
        if search_query:
            query_parts.append(search_query)
        
        if date_range:
            date_from = date_range.get("from", "19000101")
            date_to = date_range.get("to", datetime.now().strftime("%Y%m%d"))
            query_parts.append(f"receivedate:[{date_from}+TO+{date_to}]")
        
        if country:
            query_parts.append(f"occurcountry:{country}")
        
        if serious_only:
            query_parts.append("serious:1")
        
        # Combine query parts
        query_parts = list(dict.fromkeys(query_parts))
        final_query = "+AND+".join(query_parts) if query_parts else None
        
        if not final_query and not count:
            return {"error": "Either search_query or count parameter must be provided"}
        
        # Build parameters
        params: Dict[str, Any] = {}
        
        if final_query:
            params["search"] = final_query
        
        if count:
            params["count"] = count
        else:
            params["limit"] = min(max(1, limit), 1000)
            if skip > 0:
                params["skip"] = skip
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Add metadata
            result = {
                "_query_metadata": {
                    "query": final_query,
                    "count_field": count,
                    "limit": limit,
                    "skip": skip,
                    "total_results": data.get("meta", {}).get("results", {}).get("total", 0)
                }
            }
            
            # Handle count queries
            if count and "results" in data:
                result["aggregations"] = data["results"]
                result["aggregation_count"] = len(data["results"])
                return result
            
            # Handle search queries with field extraction
            if extract_fields and "results" in data and not count:
                simplified = []
                for event in data["results"]:
                    # Extract patient drugs
                    drugs = []
                    for drug in event.get("patient", {}).get("drug", []):
                        drugs.append({
                            "name": drug.get("medicinalproduct"),
                            "indication": drug.get("drugindication"),
                            "role": drug.get("drugcharacterization")  # 1=suspect, 2=concomitant, 3=interacting
                        })
                    
                    # Extract reactions
                    reactions = []
                    for reaction in event.get("patient", {}).get("reaction", []):
                        reactions.append({
                            "term": reaction.get("reactionmeddrapt"),
                            "outcome": reaction.get("reactionoutcome")
                        })
                    
                    simplified.append({
                        "receivedate": event.get("receivedate"),
                        "serious": event.get("serious") == "1",
                        "seriousnesscongenitalanomali": event.get("seriousnesscongenitalanomali"),
                        "seriousnessdeath": event.get("seriousnessdeath"),
                        "seriousnesshospitalization": event.get("seriousnesshospitalization"),
                        "patient_age": event.get("patient", {}).get("patientonsetage"),
                        "patient_sex": event.get("patient", {}).get("patientsex"),  # 1=Male, 2=Female
                        "drugs": drugs,
                        "reactions": reactions,
                        "country": event.get("occurcountry")
                    })
                
                result["results"] = simplified
                result["results_count"] = len(simplified)
                return result
            
            # Return raw data if extraction disabled
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