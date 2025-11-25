from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
from urllib.parse import quote



class FDAProductLabelToolInput(BaseModel):
    """Input schema for FDAProductLabelTool."""
    search_query: Optional[str] = Field(
        None,
        description="""
        OpenFDA search query for drug product labels (package inserts).
        
        Common search fields:
        - openfda.brand_name:"Jardiance" - Brand name
        - openfda.generic_name:"empagliflozin" - Generic name
        - openfda.manufacturer_name:"Boehringer" - Manufacturer
        - indications_and_usage:"diabetes" - Search in indications section
        - warnings:"cardiovascular" - Search in warnings section
        - dosage_and_administration:"once daily" - Search in dosage section
        - product_type:"HUMAN PRESCRIPTION DRUG" - Product type
        
        Example: openfda.brand_name:"Ozempic"+AND+indications_and_usage:"diabetes"
        """
    )
    brand_name: Optional[str] = Field(
        None,
        description="Search by brand/trade name. Shortcut for openfda.brand_name."
    )
    generic_name: Optional[str] = Field(
        None,
        description="Search by generic/active ingredient name. Shortcut for openfda.generic_name."
    )
    manufacturer: Optional[str] = Field(
        None,
        description="Search by manufacturer name."
    )
    section: Optional[str] = Field(
        None,
        description="""
        Search within specific label section:
        - "indications_and_usage" - Therapeutic indications
        - "warnings" - Warnings and precautions
        - "dosage_and_administration" - Dosing information
        - "adverse_reactions" - Side effects
        - "drug_interactions" - Drug interactions
        - "clinical_pharmacology" - Pharmacology
        - "contraindications" - When not to use
        
        Provide section name and search_text to search within that section.
        """
    )
    section_text: Optional[str] = Field(
        None,
        description="Text to search for within the specified section (use with 'section' parameter)"
    )
    product_type: Optional[str] = Field(
        None,
        description='Product type: "HUMAN PRESCRIPTION DRUG", "HUMAN OTC DRUG", "VACCINE"'
    )
    fields: Optional[List[str]] = Field(
        None,
        description="""
        Select specific label sections to return. Reduces response size significantly.
        
        Available sections:
        - openfda.brand_name, openfda.generic_name, openfda.manufacturer_name
        - indications_and_usage, dosage_and_administration
        - warnings, warnings_and_cautions, boxed_warning
        - adverse_reactions, drug_interactions
        - contraindications, clinical_pharmacology
        - description, active_ingredient
        
        Example: ["openfda.brand_name", "indications_and_usage", "warnings"]
        """
    )
    limit: Optional[int] = Field(
        10,
        description="Maximum number of results (1-100). Default: 10. Labels can be large."
    )
    skip: Optional[int] = Field(
        0,
        description="Number of results to skip for pagination"
    )


class FDAProductLabelTool(BaseTool):
    name: str = "fda_product_label_tool"
    description: str = """
    Search FDA Drug Product Labels (package inserts, prescribing information).
    
    Use cases:
    - Extract prescribing information
    - Find indications and usage
    - Review warnings and precautions
    - Check dosage and administration
    - Identify drug interactions
    - Review adverse reactions
    - Access clinical pharmacology data
    
    Examples:
    1. Get label: brand_name="Jardiance"
    2. Specific section: brand_name="Ozempic", fields=["indications_and_usage", "warnings"]
    3. Search in section: section="indications_and_usage", section_text="diabetes"
    4. Manufacturer: manufacturer="Novo Nordisk", limit=5
    """
    args_schema: Type[BaseModel] = FDAProductLabelToolInput

    def _run(
        self,
        search_query: Optional[str] = None,
        brand_name: Optional[str] = None,
        generic_name: Optional[str] = None,
        manufacturer: Optional[str] = None,
        section: Optional[str] = None,
        section_text: Optional[str] = None,
        product_type: Optional[str] = None,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = 10,
        skip: Optional[int] = 0
    ) -> Dict[str, Any]:
        """
        Execute FDA Product Label search.
        
        Returns:
            Dict with label data and metadata
        """
        url = "https://api.fda.gov/drug/label.json"
        
        # Build query
        query_parts = []
        
        if search_query:
            query_parts.append(search_query)
        
        if brand_name:
            query_parts.append(f'openfda.brand_name:"{brand_name}"')
        
        if generic_name:
            query_parts.append(f'openfda.generic_name:"{generic_name}"')
        
        if manufacturer:
            query_parts.append(f'openfda.manufacturer_name:"{manufacturer}"')
        
        if product_type:
            query_parts.append(f'product_type:"{product_type}"')
        
        if section and section_text:
            query_parts.append(f'{section.lower()}:"{section_text}"')
        
        if not query_parts:
            return {"error": "At least one search parameter must be provided"}
        
        query_parts = list(dict.fromkeys(query_parts))
        final_query = "+AND+".join(query_parts)
        
        # Build request parameters
        params: Dict[str, Any] = {
            "search": quote(final_query, safe=':"[]()+'),
            "limit": min(max(1, limit), 100)  # Labels are large, cap at 100
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
                                value = value[0]      # take first entry
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
