from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests


class FDANDCToolInput(BaseModel):
    """Input schema for FDANDCTool."""
    search_query: Optional[str] = Field(
        None,
        description="""
        OpenFDA search query for NDC (National Drug Code) directory.
        
        Common search fields:
        - generic_name:"semaglutide" - Generic/active ingredient name
        - brand_name:"Ozempic" - Brand/trade name
        - labeler_name:"Novo Nordisk" - Manufacturer/labeler
        - product_type:"HUMAN PRESCRIPTION DRUG" - Product type
        - route:"SUBCUTANEOUS" - Route of administration
        - dosage_form:"INJECTION" - Dosage form
        
        Example: generic_name:"metformin"+AND+route:"ORAL"
        """
    )
    generic_name: Optional[str] = Field(
        None,
        description="Search by generic/active ingredient name. Shortcut for generic_name field."
    )
    brand_name: Optional[str] = Field(
        None,
        description="Search by brand/trade name. Shortcut for brand_name field."
    )
    labeler: Optional[str] = Field(
        None,
        description="Search by manufacturer/labeler company name."
    )
    route: Optional[str] = Field(
        None,
        description="""
        Route of administration: ORAL, INJECTION, TOPICAL, INHALATION, SUBCUTANEOUS, etc.
        """
    )
    dosage_form: Optional[str] = Field(
        None,
        description="""
        Dosage form: TABLET, CAPSULE, INJECTION, SOLUTION, CREAM, AEROSOL, etc.
        """
    )
    marketing_status: Optional[str] = Field(
        None,
        description="""
        Marketing status of the product.
        Values: "Prescription", "Over-the-counter", "Discontinued"
        """
    )
    package_type: Optional[str] = Field(
        None,
        description="Package type filter (e.g., BOTTLE, CARTON, BLISTER PACK)"
    )
    fields: Optional[List[str]] = Field(
        None,
        description="""
        Select specific fields to return.
        
        Available fields:
        - product_ndc, generic_name, brand_name
        - labeler_name, product_type, route
        - dosage_form, marketing_status
        - packaging.package_ndc, packaging.description
        - active_ingredients.name, active_ingredients.strength
        
        Example: ["product_ndc", "generic_name", "labeler_name"]
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


class FDANDCTool(BaseTool):
    name: str = "fda_ndc_tool"
    description: str = """
    Search FDA National Drug Code (NDC) Directory for drug product and package information.
    
    Use cases:
    - Find NDC codes by drug name
    - Identify manufacturers/labelers
    - Check dosage forms and routes
    - Verify marketing status
    - Analyze packaging information
    - Search by active ingredients
    
    Examples:
    1. By generic: generic_name="semaglutide"
    2. By brand: brand_name="Ozempic", labeler="Novo Nordisk"
    3. By route: generic_name="insulin", route="SUBCUTANEOUS"
    4. Field selection: brand_name="Jardiance", fields=["product_ndc", "generic_name"]
    """
    args_schema: Type[BaseModel] = FDANDCToolInput

    def _run(
        self,
        search_query: Optional[str] = None,
        generic_name: Optional[str] = None,
        brand_name: Optional[str] = None,
        labeler: Optional[str] = None,
        route: Optional[str] = None,
        dosage_form: Optional[str] = None,
        marketing_status: Optional[str] = None,
        package_type: Optional[str] = None,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0
    ) -> Dict[str, Any]:
        """
        Execute FDA NDC Directory search.
        
        Returns:
            Dict with NDC data and metadata
        """
        url = "https://api.fda.gov/drug/ndc.json"
        
        # Build query
        query_parts = []
        
        if search_query:
            query_parts.append(search_query)
        
        if generic_name:
            query_parts.append(f'generic_name:"{generic_name}"')
        
        if brand_name:
            query_parts.append(f'brand_name:"{brand_name}"')
        
        if labeler:
            query_parts.append(f'labeler_name:"{labeler}"')
        
        if route:
            query_parts.append(f'route:"{route.upper()}"')
        
        if dosage_form:
            query_parts.append(f'dosage_form:"{dosage_form.upper()}"')
        
        if marketing_status:
            query_parts.append(f'marketing_status:"{marketing_status}"')
        
        if package_type:
            query_parts.append(f'packaging.type:"{package_type.upper()}"')
        
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
                        parts = field.split(".")
                        value = item
                        for part in parts:
                            if isinstance(value, list):
                                value = value[0]  # take first entry
                            if isinstance(value, dict):
                                value = value.get(part)
                            else:
                                value = None
                                break

                        if value is not None:
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
