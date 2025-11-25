from crewai.tools import BaseTool
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field
import requests
import json


class OpenTargetsToolInput(BaseModel):
    endpoint: str = Field(
        ...,
        description=(
            "GraphQL endpoint to query. Options: target, disease, drug, variant, "
            "studies, credibleSet, search"
        )
    )
    entity_id: Optional[str] = Field(
        default=None,
        description=(
            "Entity identifier for the query. "
            "For target: Ensembl gene ID (e.g., 'ENSG00000169083' for AR). "
            "For disease: EFO ID (e.g., 'EFO_0000685' for rheumatoid arthritis). "
            "For drug: ChEMBL ID (e.g., 'CHEMBL1201583'). "
            "For variant: variant ID (e.g., 'rs7903146'). "
            "For studies: study ID. "
            "For credibleSet: credible set ID. "
            "Not required for 'search' endpoint."
        )
    )
    query_type: Optional[str] = Field(
        default="basic",
        description=(
            "Type of query to run. Options: "
            "basic (general info), "
            "tractability (target tractability assessments), "
            "genetic_constraint (genetic constraint data), "
            "expression (baseline expression data), "
            "associated_diseases (diseases associated with target), "
            "associated_targets (targets associated with disease), "
            "known_drugs (known drugs for disease/target), "
            "mechanisms (drug mechanisms of action), "
            "pharmacovigilance (adverse events), "
            "custom (provide your own GraphQL query)"
        )
    )
    custom_query: Optional[str] = Field(
        default=None,
        description=(
            "Custom GraphQL query string. Required when query_type='custom'. "
            "Use GraphQL syntax with variables like $ensemblId, $efoId, etc."
        )
    )
    search_query: Optional[str] = Field(
        default=None,
        description="Search query string for the 'search' endpoint"
    )
    page_size: Optional[int] = Field(
        default=10,
        description="Number of results to return for paginated queries"
    )
    page_index: Optional[int] = Field(
        default=0,
        description="Page index for paginated queries (0-based)"
    )


class OpenTargetsTool(BaseTool):
    name: str = "open_targets_graphql_tool"
    description: str = (
        "Query the Open Targets Platform GraphQL API to find potential drug targets, "
        "disease associations, drug information, and genetic evidence. "
        "Use this tool to:\n"
        "- Find targets associated with diseases\n"
        "- Get target tractability assessments (druggability)\n"
        "- Retrieve genetic constraint and expression data\n"
        "- Find known drugs for targets or diseases\n"
        "- Get drug mechanisms of action and adverse events\n"
        "- Search for targets, diseases, drugs, or variants\n"
        "\nSupports queries for single entities. For bulk queries, use data downloads."
    )
    args_schema: Type[BaseModel] = OpenTargetsToolInput

    def _run(
        self,
        endpoint: str,
        entity_id: Optional[str] = None,
        query_type: Optional[str] = "basic",
        custom_query: Optional[str] = None,
        search_query: Optional[str] = None,
        page_size: Optional[int] = 10,
        page_index: Optional[int] = 0
    ) -> Dict[str, Any]:
        """
        Query the Open Targets Platform GraphQL API.
        
        Examples:
        
        1. Get basic target information:
           endpoint='target', entity_id='ENSG00000169083', query_type='basic'
        
        2. Get target tractability:
           endpoint='target', entity_id='ENSG00000169083', query_type='tractability'
        
        3. Get genetic constraint for target:
           endpoint='target', entity_id='ENSG00000169083', query_type='genetic_constraint'
        
        4. Get diseases associated with target:
           endpoint='target', entity_id='ENSG00000169083', query_type='associated_diseases'
        
        5. Get basic disease information:
           endpoint='disease', entity_id='EFO_0000685', query_type='basic'
        
        6. Get targets associated with disease:
           endpoint='disease', entity_id='EFO_0000685', query_type='associated_targets'
        
        7. Get known drugs for disease:
           endpoint='disease', entity_id='EFO_0000685', query_type='known_drugs'
        
        8. Get drug information:
           endpoint='drug', entity_id='CHEMBL1201583', query_type='basic'
        
        9. Get drug mechanisms:
           endpoint='drug', entity_id='CHEMBL1201583', query_type='mechanisms'
        
        10. Search for entities:
            endpoint='search', search_query='breast cancer'
        
        11. Custom query:
            endpoint='target', entity_id='ENSG00000169083', query_type='custom',
            custom_query='query target($ensemblId: String!){ target(ensemblId: $ensemblId){ id approvedSymbol }}'
        """
        
        base_url = "https://api.platform.opentargets.org/api/v4/graphql"
        
        # Validate endpoint
        valid_endpoints = ['target', 'disease', 'drug', 'variant', 'studies', 'credibleSet', 'search']
        if endpoint not in valid_endpoints:
            return {
                "error": f"Invalid endpoint '{endpoint}'",
                "valid_endpoints": valid_endpoints
            }
        
        # Build GraphQL query based on endpoint and query_type
        if query_type == "custom":
            if not custom_query:
                return {"error": "custom_query is required when query_type='custom'"}
            query_string = custom_query
        else:
            query_string = self._build_query(endpoint, query_type, page_size, page_index)
        
        if not query_string:
            return {
                "error": f"Invalid query_type '{query_type}' for endpoint '{endpoint}'"
            }
        
        # Build variables
        variables = self._build_variables(endpoint, entity_id, search_query, page_size, page_index)
        
        # Execute request
        try:
            headers = {
                "User-Agent": "pharma-researcher/1.0",
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": query_string,
                "variables": variables
            }
            
            response = requests.post(base_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for GraphQL errors
            if "errors" in data:
                return {
                    "error": "GraphQL query error",
                    "details": data["errors"],
                    "query": query_string,
                    "variables": variables
                }
            
            # Add metadata
            result = {
                "data": data.get("data", {}),
                "_query_metadata": {
                    "endpoint": endpoint,
                    "entity_id": entity_id,
                    "query_type": query_type,
                    "search_query": search_query,
                    "url": base_url,
                    "query": query_string,
                    "variables": variables
                }
            }
            
            return result
            
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error {e.response.status_code}",
                "details": e.response.text[:500],
                "url": base_url,
                "query": query_string,
                "variables": variables
            }
        except Exception as e:
            return {
                "error": str(e),
                "url": base_url,
                "query": query_string if 'query_string' in locals() else None,
                "variables": variables if 'variables' in locals() else None
            }
    
    def _build_query(self, endpoint: str, query_type: str, page_size: int, page_index: int) -> Optional[str]:
        """Build GraphQL query string based on endpoint and query type."""
        
        queries = {
            "target": {
                "basic": """
                    query target($ensemblId: String!) {
                        target(ensemblId: $ensemblId) {
                            id
                            approvedSymbol
                            approvedName
                            biotype
                            genomicLocation {
                                chromosome
                                start
                                end
                                strand
                            }
                            proteinAnnotations {
                                id
                                functions
                            }
                        }
                    }
                """,
                "tractability": """
                    query target($ensemblId: String!) {
                        target(ensemblId: $ensemblId) {
                            id
                            approvedSymbol
                            tractability {
                                label
                                modality
                                value
                            }
                        }
                    }
                """,
                "genetic_constraint": """
                    query target($ensemblId: String!) {
                        target(ensemblId: $ensemblId) {
                            id
                            approvedSymbol
                            geneticConstraint {
                                constraintType
                                exp
                                obs
                                score
                                oe
                                oeLower
                                oeUpper
                            }
                        }
                    }
                """,
                "expression": """
                    query target($ensemblId: String!) {
                        target(ensemblId: $ensemblId) {
                            id
                            approvedSymbol
                            expressions {
                                tissue {
                                    id
                                    label
                                }
                                rna {
                                    value
                                    unit
                                    level
                                }
                                protein {
                                    level
                                }
                            }
                        }
                    }
                """,
                "associated_diseases": """
                    query target($ensemblId: String!, $size: Int!, $index: Int!) {
                        target(ensemblId: $ensemblId) {
                            id
                            approvedSymbol
                            associatedDiseases(page: {size: $size, index: $index}) {
                                count
                                rows {
                                    disease {
                                        id
                                        name
                                    }
                                    score
                                    datatypeScores {
                                        id
                                        score
                                    }
                                }
                            }
                        }
                    }
                """,
                "known_drugs": """
                    query target($ensemblId: String!, $size: Int!) {
                        target(ensemblId: $ensemblId) {
                            id
                            approvedSymbol
                            knownDrugs(size: $size) {
                                uniqueDrugs
                                uniqueDiseases
                                count
                                rows {
                                    drug {
                                        id
                                        name
                                        drugType
                                    }
                                    disease {
                                        id
                                        name
                                    }
                                    mechanismOfAction
                                    phase
                                    status
                                }
                            }
                        }
                    }
                """
            },
            "disease": {
                "basic": """
                    query disease($efoId: String!) {
                        disease(efoId: $efoId) {
                            id
                            name
                            description
                            synonyms {
                                terms
                            }
                            therapeuticAreas {
                                id
                                name
                            }
                        }
                    }
                """,
                "associated_targets": """
                    query disease($efoId: String!, $size: Int!, $index: Int!) {
                        disease(efoId: $efoId) {
                            id
                            name
                            associatedTargets(page: {size: $size, index: $index}) {
                                count
                                rows {
                                    target {
                                        id
                                        approvedSymbol
                                        approvedName
                                    }
                                    score
                                    datatypeScores {
                                        id
                                        score
                                    }
                                }
                            }
                        }
                    }
                """,
                "known_drugs": """
                    query disease($efoId: String!, $size: Int!) {
                        disease(efoId: $efoId) {
                            id
                            name
                            knownDrugs(size: $size) {
                                uniqueDrugs
                                uniqueTargets
                                count
                                rows {
                                    drug {
                                        id
                                        name
                                        drugType
                                    }
                                    target {
                                        id
                                        approvedSymbol
                                    }
                                    mechanismOfAction
                                    phase
                                    status
                                }
                            }
                        }
                    }
                """
            },
            "drug": {
                "basic": """
                    query drug($chemblId: String!) {
                        drug(chemblId: $chemblId) {
                            id
                            name
                            drugType
                            maximumClinicalTrialPhase
                            hasBeenWithdrawn
                            withdrawnNotice {
                                reasons
                                countries
                                year
                            }
                            description
                            synonyms
                        }
                    }
                """,
                "mechanisms": """
                    query drug($chemblId: String!) {
                        drug(chemblId: $chemblId) {
                            id
                            name
                            mechanismsOfAction {
                                rows {
                                    mechanismOfAction
                                    actionType
                                    targets {
                                        id
                                        approvedSymbol
                                        approvedName
                                    }
                                }
                            }
                        }
                    }
                """,
                "pharmacovigilance": """
                    query drug($chemblId: String!) {
                        drug(chemblId: $chemblId) {
                            id
                            name
                            adverseEvents {
                                count
                                criticalValue
                                rows {
                                    name
                                    count
                                    logLR
                                }
                            }
                        }
                    }
                """
            },
            "search": {
                "basic": """
                    query search($queryString: String!, $size: Int!, $index: Int!) {
                        search(queryString: $queryString, page: {size: $size, index: $index}) {
                            total
                            hits {
                                id
                                entity
                                name
                                description
                                score
                            }
                        }
                    }
                """
            }
        }
        
        if endpoint in queries and query_type in queries[endpoint]:
            return queries[endpoint][query_type]
        
        return None
    
    def _build_variables(
        self,
        endpoint: str,
        entity_id: Optional[str],
        search_query: Optional[str],
        page_size: int,
        page_index: int
    ) -> Dict[str, Any]:
        """Build variables object for GraphQL query."""
        
        variables = {}
        
        # Add entity ID based on endpoint
        if endpoint == "target" and entity_id:
            variables["ensemblId"] = entity_id
        elif endpoint == "disease" and entity_id:
            variables["efoId"] = entity_id
        elif endpoint == "drug" and entity_id:
            variables["chemblId"] = entity_id
        elif endpoint == "variant" and entity_id:
            variables["variantId"] = entity_id
        elif endpoint == "studies" and entity_id:
            variables["studyId"] = entity_id
        elif endpoint == "credibleSet" and entity_id:
            variables["studyLocusId"] = entity_id
        elif endpoint == "search" and search_query:
            variables["queryString"] = search_query
        
        # Add pagination
        variables["size"] = page_size
        variables["index"] = page_index
        
        return variables


# Singleton instance
open_targets_tool = OpenTargetsTool()
