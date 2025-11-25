from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
from urllib.parse import quote


class FDADrugsFDAToolInput(BaseModel):
    """Input schema for FDADrugsFDATool."""
    search_query: Optional[str] = Field(
        None,
        description="""
        OpenFDA search query for drug approvals and regulatory history.
        
        Common search patterns:
        - By brand name: 'products.brand_name:"Jardiance"'
        - By generic name: 'openfda.generic_name:"empagliflozin"'
        - By indication: 'products.indication:"diabetes"'
        - By sponsor: 'sponsor_name:"Boehringer"'
        - By application type: 'application_type:"NDA"' (NDA, ANDA, BLA)
        
        Use + for AND, | for OR
        Example: 'products.brand_name:"Jardiance"+AND+sponsor_name:"Boehringer"'
        """
    )
    brand_name: Optional[str] = Field(
        None,
        description="Search by brand/trade name. Shortcut for products.brand_name search."
    )
    generic_name: Optional[str] = Field(
        None,
        description="Search by generic/active ingredient name. Shortcut for openfda.generic_name."
    )
    sponsor: Optional[str] = Field(
        None,
        description="Search by sponsor/manufacturer name."
    )
    application_type: Optional[str] = Field(
        None,
        description="Filter by application type: NDA (New Drug), ANDA (Generic), BLA (Biologic)"
    )
    fields: Optional[List[str]] = Field(
        None,
        description="""
        Select specific fields to return. Reduces response size.
        
        Available fields:
        - application_number, sponsor_name, submission_type
        - products.brand_name, products.active_ingredients
        - products.marketing_status, products.dosage_form
        - products.route, products.indication
        - openfda.generic_name, openfda.brand_name
        - openfda.manufacturer_name, openfda.substance_name
        
        Example: ["application_number", "products.brand_name", "sponsor_name"]
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


class FDADrugsFDATool(BaseTool):
    name: str = "fda_drugsfda_tool"
    description: str = """
    Search FDA Drugs@FDA database for drug approval information and regulatory history.
    
    Use cases:
    - Find FDA approval details by brand or generic name
    - Check marketing status and approval dates
    - Identify sponsor/manufacturer information
    - Track application types (NDA, ANDA, BLA)
    - Analyze approved indications and dosage forms
    
    Examples:
    1. Find drug by brand: brand_name="Jardiance"
    2. Generic search: generic_name="empagliflozin"
    3. Sponsor search: sponsor="Boehringer", limit=50
    4. With field selection: brand_name="Ozempic", fields=["products.brand_name", "products.indication"]
    """
    args_schema: Type[BaseModel] = FDADrugsFDAToolInput

    def _run(
        self,
        search_query: Optional[str] = None,
        brand_name: Optional[str] = None,
        generic_name: Optional[str] = None,
        sponsor: Optional[str] = None,
        application_type: Optional[str] = None,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0
    ) -> Dict[str, Any]:
        """
        Execute FDA Drugs@FDA search.
        
        Returns:
            Dict with drug approval data and metadata
        """
        url = "https://api.fda.gov/drug/drugsfda.json"
        
        # Build query
        query_parts = []
        
        if search_query:
            query_parts.append(search_query)
        
        if brand_name:
            query_parts.append(f'products.brand_name:"{brand_name}"')
        
        if generic_name:
            query_parts.append(f'openfda.generic_name:"{generic_name}"')
        
        if sponsor:
            query_parts.append(f'(sponsor_name:"{sponsor}"+OR+openfda.manufacturer_name:"{sponsor}")')
        
        if application_type:
            query_parts.append(f'submissions.submission_type.exact:"{application_type}"')
        
        if not query_parts:
            return {"error": "At least one search parameter must be provided"}
        
        query_parts = list(dict.fromkeys(query_parts))
        final_query = "+AND+".join(query_parts)
        
        # Build request parameters
        params: Dict[str, Any] = {
            "search": quote(final_query, safe=':"[]()+'),
            "limit": min(max(1, limit), 1000)
        }
        
        if skip > 0:
            params["skip"] = skip
        
        try:
            headers = {"User-Agent": "pharma-researcher/1.0"}
            response = requests.get(url, params=params, headers=headers, timeout=30)

            response.raise_for_status()
            data = response.json()
            
            # Filter fields if requested
            if fields and "results" in data:
                filtered_results = []
                for item in data["results"]:
                    filtered_item = {}
                    for field in fields:
                        # Handle nested fields (e.g., "products.brand_name")
                        parts = field.split(".")
                        value = item
                        for part in parts:
                            if isinstance(value, list):
                                value = value[0]  # drill into list
                            if isinstance(value, dict):
                                value = value.get(part)
                            else:
                                value = None
                                break


                            if value is None:
                                break
                        if value is not None:
                            # Rebuild nested structure
                            if len(parts) > 1:
                                nested = filtered_item
                                for i, part in enumerate(parts[:-1]):
                                    if part not in nested:
                                        nested[part] = {}
                                    nested = nested[part]
                                nested[parts[-1]] = value
                            else:
                                filtered_item[field] = value
                    filtered_results.append(filtered_item)
                data["results"] = filtered_results
            
            # Add metadata
            result = {
                "_query_metadata": {
                    "query": final_query,
                    "fields": fields,
                    "limit": limit,
                    "skip": skip,
                    "total_results": data.get("meta", {}).get("results", {}).get("total", 0),
                    "results_returned": len(data.get("results", []))
                }
            }
            
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
