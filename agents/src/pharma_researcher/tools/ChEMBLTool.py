from crewai.tools import BaseTool
from typing import Optional, Type, Dict, Any, List, Union
from pydantic import BaseModel, Field
import requests
import urllib.parse


class ChEMBLToolInput(BaseModel):
    resource: str = Field(
        ...,
        description=(
            "ChEMBL resource to query. Options: molecule, target, assay, activity, "
            "drug, drug_indication, mechanism, biotherapeutic, cell_line, document, "
            "tissue, organism, protein_classification, atc_class, binding_site, "
            "compound_record, metabolism, similarity, substructure, image, status"
        )
    )
    chembl_id: Optional[str] = Field(
        default=None,
        description="Specific ChEMBL ID to retrieve (e.g., CHEMBL25 for aspirin)"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Filter parameters as key-value pairs. "
            "Examples: {'pref_name__contains': 'cyclin'}, "
            "{'molecule_properties__mw_freebase__lte': 300}, "
            "{'pref_name__iendswith': 'nib'}. "
            "Supported filter types: exact, iexact, contains, icontains, "
            "startswith, istartswith, endswith, iendswith, regex, iregex, "
            "gt, gte, lt, lte, range, in, isnull"
        )
    )
    search_query: Optional[str] = Field(
        default=None,
        description=(
            "Full text search query (uses Elasticsearch). "
            "Example: 'aspirin' or 'lipoxygenase'"
        )
    )
    smiles: Optional[str] = Field(
        default=None,
        description=(
            "SMILES string for chemical structure searches. "
            "Used with 'similarity' or 'substructure' resources. "
            "Example: 'CC(=O)Oc1ccccc1C(=O)O' for aspirin"
        )
    )
    similarity_cutoff: Optional[int] = Field(
        default=80,
        description="Tanimoto similarity cutoff (0-100) for similarity searches"
    )
    limit: Optional[int] = Field(
        default=20,
        description="Number of results per page (pagination)"
    )
    offset: Optional[int] = Field(
        default=0,
        description="Offset for pagination"
    )
    order_by: Optional[str] = Field(
        default=None,
        description="Field to order results by. Prefix with '-' for descending order"
    )
    only: Optional[List[str]] = Field(
        default=None,
        description=(
            "Select specific properties to return. "
            "Example: ['molecule_chembl_id', 'pchembl_value']"
        )
    )


class ChEMBLTool(BaseTool):
    name: str = "chembl_api_tool"
    description: str = (
        "Search and retrieve data from the ChEMBL database - a comprehensive bioactivity database. "
        "Use this tool to find molecules, targets, assays, drugs, clinical trials, and bioactivity data. "
        "Supports chemical structure searches (substructure, similarity), keyword searches, and filtering. "
        "\n\nCommon use cases:\n"
        "- Find molecules by properties (molecular weight, logP, etc.)\n"
        "- Search for drug targets and mechanisms\n"
        "- Get drug indications and warnings\n"
        "- Perform chemical similarity or substructure searches\n"
        "- Retrieve bioactivity data and assay results\n"
        "- Get molecule images and structural representations"
    )
    args_schema: Type[BaseModel] = ChEMBLToolInput

    def _run(
        self,
        resource: str,
        chembl_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        search_query: Optional[str] = None,
        smiles: Optional[str] = None,
        similarity_cutoff: Optional[int] = 80,
        format: str = "json",
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        order_by: Optional[str] = None,
        only: Optional[List[str]] = None
    ) -> Union[Dict[str, Any], str]:
        """
        Query the ChEMBL API for pharmaceutical and bioactivity data.
        
        Examples:
        
        1. Get all molecules:
           resource='molecule'
        
        2. Search for targets containing 'cyclin':
           resource='target', filters={'pref_name__contains': 'cyclin'}
        
        3. Find molecules with MW <= 300:
           resource='molecule', filters={'molecule_properties__mw_freebase__lte': 300}
        
        4. Find molecules with MW <= 300 AND name ending with 'nib':
           resource='molecule', 
           filters={'molecule_properties__mw_freebase__lte': 300, 'pref_name__iendswith': 'nib'}
        
        5. Get image for CHEMBL25 (aspirin):
           resource='image', chembl_id='CHEMBL25', format='svg'
        
        6. Substructure search with aspirin SMILES:
           resource='substructure', smiles='CC(=O)Oc1ccccc1C(=O)O'
        
        7. Similarity search (80% cutoff):
           resource='similarity', smiles='CC(=O)Oc1ccccc1C(=O)O', similarity_cutoff=80
        
        8. Full text search for 'aspirin':
           resource='molecule', search_query='aspirin'
        
        9. Get specific drug by ChEMBL ID:
           resource='drug', chembl_id='CHEMBL25'
        
        10. Get drug indications:
            resource='drug_indication', filters={'molecule_chembl_id': 'CHEMBL25'}
        """
        
        base_url = "https://www.ebi.ac.uk/chembl/api/data"
        
        # Valid resources
        valid_resources = [
            'activity', 'assay', 'atc_class', 'binding_site', 'biotherapeutic',
            'cell_line', 'chembl_id_lookup', 'compound_record', 'compound_structural_alert',
            'document', 'document_similarity', 'document_term', 'drug', 'drug_indication',
            'drug_warning', 'go_slim', 'image', 'mechanism', 'metabolism', 'molecule',
            'molecule_form', 'organism', 'protein_classification', 'similarity',
            'source', 'status', 'substructure', 'target', 'target_component',
            'target_relation', 'tissue', 'xref_source'
        ]
        
        if resource not in valid_resources:
            return {
                "error": f"Invalid resource '{resource}'",
                "valid_resources": valid_resources
            }
        
        # Build URL
        url = self._build_url(base_url, resource, chembl_id, smiles, similarity_cutoff, format)
        
        # Build query parameters
        params = self._build_params(filters, search_query, limit, offset, order_by, only, format)
        
        # Execute request
        try:
            headers = {
                "User-Agent": "pharma-researcher/1.0",
                "Accept": self._get_accept_header(format)
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Handle different response formats
            if format == "json":
                data = response.json()
                
                # Add metadata for paginated responses
                if isinstance(data, dict) and "page_meta" in data:
                    return data
                
                # Add custom metadata
                return {
                    "data": data,
                    "_query_metadata": {
                        "resource": resource,
                        "chembl_id": chembl_id,
                        "filters": filters,
                        "search_query": search_query,
                        "url": url,
                        "params": params,
                        "total_results": len(data) if isinstance(data, list) else 1
                    }
                }
                
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
    
    def _build_url(
        self,
        base_url: str,
        resource: str,
        chembl_id: Optional[str],
        smiles: Optional[str],
        similarity_cutoff: int,
        format: str
    ) -> str:
        """Build the request URL based on resource type and parameters."""
        
        # Special handling for chemical searches
        if resource == "similarity" and smiles:
            encoded_smiles = urllib.parse.quote(smiles, safe='')
            return f"{base_url}/similarity/{encoded_smiles}/{similarity_cutoff}.{format}"
        
        if resource == "substructure" and smiles:
            encoded_smiles = urllib.parse.quote(smiles, safe='')
            return f"{base_url}/substructure/{encoded_smiles}.{format}"
        
        # Image resource
        if resource == "image" and chembl_id:
            return f"{base_url}/image/{chembl_id}.{format}"
        
        # Standard resource with specific ID
        if chembl_id:
            return f"{base_url}/{resource}/{chembl_id}.{format}"
        
        # Standard resource without ID
        return f"{base_url}/{resource}.{format}"
    
    def _build_params(
        self,
        filters: Optional[Dict[str, Any]],
        search_query: Optional[str],
        limit: int,
        offset: int,
        order_by: Optional[str],
        only: Optional[List[str]],
        format: str
    ) -> Dict[str, Any]:
        """Build query parameters."""
        
        params = {}
        
        # Add filters
        if filters:
            params.update(filters)
        
        # Add search query
        if search_query:
            params['q'] = search_query
        
        # Add pagination
        params['limit'] = limit
        params['offset'] = offset
        
        # Add ordering
        if order_by:
            params['order_by'] = order_by
        
        # Add field selection
        if only:
            params['only'] = ','.join(only)
        
        # Format parameter (if not in URL extension)
        if format and format != "json":
            params['format'] = format
        
        return params
    
    def _get_accept_header(self, format: str) -> str:
        """Get appropriate Accept header based on format."""
        
        format_headers = {
            "json": "application/json",
            "xml": "application/xml",
            "yaml": "application/yaml",
            "svg": "image/svg+xml",
            "sdf": "chemical/x-mdl-sdfile"
        }
        
        return format_headers.get(format, "application/json")


# Singleton instance
chembl_tool = ChEMBLTool()
