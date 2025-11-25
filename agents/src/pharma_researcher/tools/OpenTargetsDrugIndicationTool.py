from crewai.tools import BaseTool
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field
import requests
import json
import os
import tempfile
from pathlib import Path


class OpenTargetsDrugIndicationToolInput(BaseModel):
    drug_id: Optional[str] = Field(
        default=None,
        description=(
            "Open Targets molecule identifier (ChEMBL ID) to query. "
            "Example: 'CHEMBL25' for aspirin, 'CHEMBL1201583' for adalimumab"
        )
    )
    disease_id: Optional[str] = Field(
        default=None,
        description=(
            "Disease identifier (EFO ID) to filter indications. "
            "Example: 'EFO_0000685' for rheumatoid arthritis"
        )
    )
    min_phase: Optional[int] = Field(
        default=None,
        description=(
            "Minimum clinical trial phase (0-4). "
            "0=preclinical, 1-3=clinical phases, 4=approved"
        )
    )
    approved_only: Optional[bool] = Field(
        default=False,
        description="Return only approved indications (phase 4)"
    )
    limit: Optional[int] = Field(
        default=100,
        description="Maximum number of results to return"
    )


class OpenTargetsDrugIndicationTool(BaseTool):
    name: str = "open_targets_drug_indication_tool"
    description: str = (
        "Query Open Targets drug indications dataset to find approved and investigational "
        "indications for drugs. Use this tool to:\n"
        "- Find all indications for a specific drug\n"
        "- Get clinical trial phases for drug-disease pairs\n"
        "- Filter by approved indications only\n"
        "- Find drugs for specific diseases\n"
        "- Get reference sources supporting drug-indication relationships\n"
        "\nData includes ChEMBL drugs with disease indications, clinical phases, and references."
    )
    args_schema: Type[BaseModel] = OpenTargetsDrugIndicationToolInput

    def _run(
        self,
        drug_id: Optional[str] = None,
        disease_id: Optional[str] = None,
        min_phase: Optional[int] = None,
        approved_only: Optional[bool] = False,
        limit: Optional[int] = 100
    ) -> Dict[str, Any]:
        """
        Query Open Targets drug indications data.
        
        Examples:
        
        1. Get all indications for aspirin:
           drug_id='CHEMBL25'
        
        2. Get approved indications only:
           drug_id='CHEMBL25', approved_only=True
        
        3. Get indications in clinical trials (phase >= 2):
           drug_id='CHEMBL941', min_phase=2
        
        4. Find drugs for rheumatoid arthritis:
           disease_id='EFO_0000685'
        
        5. Find approved drugs for a disease:
           disease_id='EFO_0000685', approved_only=True
        
        6. Get drug-disease pair with minimum phase:
           drug_id='CHEMBL1201583', disease_id='EFO_0000685', min_phase=3
        """
        
        # Note: Since the actual parquet file requires special libraries (pyarrow/pandas),
        # we'll use the Open Targets Platform API as an alternative
        # The GraphQL API provides the same drug indication data
        
        base_url = "https://api.platform.opentargets.org/api/v4/graphql"
        
        # Build GraphQL query based on parameters
        if drug_id:
            query_string = self._build_drug_query(approved_only)
            variables = {"chemblId": drug_id}
        elif disease_id:
            query_string = self._build_disease_query(approved_only)
            variables = {"efoId": disease_id, "size": limit}
        else:
            return {
                "error": "Either drug_id or disease_id must be provided"
            }
        
        # Execute GraphQL request
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
                    "details": data["errors"]
                }
            
            # Process and filter results
            results = self._process_results(
                data.get("data", {}),
                drug_id,
                disease_id,
                min_phase,
                approved_only,
                limit
            )
            
            return results
            
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error {e.response.status_code}",
                "details": e.response.text[:500]
            }
        except Exception as e:
            return {
                "error": str(e),
                "type": type(e).__name__
            }
    
    def _build_drug_query(self, approved_only: bool) -> str:
        """Build GraphQL query for drug indications."""
        return """
            query drug($chemblId: String!) {
                drug(chemblId: $chemblId) {
                    id
                    name
                    drugType
                    maximumClinicalTrialPhase
                    indications {
                        count
                        rows {
                            disease {
                                id
                                name
                            }
                            maxPhaseForIndication
                            references {
                                source
                                ids
                            }
                        }
                    }
                }
            }
        """
    
    def _build_disease_query(self, approved_only: bool) -> str:
        """Build GraphQL query for drugs by disease."""
        return """
            query disease($efoId: String!, $size: Int!) {
                disease(efoId: $efoId) {
                    id
                    name
                    knownDrugs(size: $size) {
                        uniqueDrugs
                        count
                        rows {
                            drug {
                                id
                                name
                                drugType
                            }
                            phase
                            status
                            mechanismOfAction
                            references {
                                source
                                ids
                            }
                        }
                    }
                }
            }
        """
    
    def _process_results(
        self,
        data: Dict[str, Any],
        drug_id: Optional[str],
        disease_id: Optional[str],
        min_phase: Optional[int],
        approved_only: bool,
        limit: int
    ) -> Dict[str, Any]:
        """Process and filter GraphQL results."""
        
        if drug_id and "drug" in data:
            drug_data = data["drug"]
            indications = drug_data.get("indications", {}).get("rows", [])
            
            # Filter by phase
            if min_phase is not None:
                indications = [
                    ind for ind in indications
                    if ind.get("maxPhaseForIndication", 0) >= min_phase
                ]
            
            # Filter approved only (phase 4)
            if approved_only:
                indications = [
                    ind for ind in indications
                    if ind.get("maxPhaseForIndication", 0) == 4
                ]
            
            # Filter by disease if specified
            if disease_id:
                indications = [
                    ind for ind in indications
                    if ind.get("disease", {}).get("id") == disease_id
                ]
            
            # Limit results
            indications = indications[:limit]
            
            # Count approved indications
            approved_indications = [
                ind.get("disease", {}).get("id")
                for ind in indications
                if ind.get("maxPhaseForIndication", 0) == 4
            ]
            
            return {
                "drug": {
                    "id": drug_data.get("id"),
                    "name": drug_data.get("name"),
                    "drugType": drug_data.get("drugType"),
                    "maximumClinicalTrialPhase": drug_data.get("maximumClinicalTrialPhase")
                },
                "indications": indications,
                "indicationCount": len(indications),
                "approvedIndications": approved_indications,
                "approvedIndicationCount": len(approved_indications),
                "_query_metadata": {
                    "drug_id": drug_id,
                    "disease_id": disease_id,
                    "min_phase": min_phase,
                    "approved_only": approved_only,
                    "total_indications": drug_data.get("indications", {}).get("count", 0)
                }
            }
        
        elif disease_id and "disease" in data:
            disease_data = data["disease"]
            drugs = disease_data.get("knownDrugs", {}).get("rows", [])
            
            # Filter by phase
            if min_phase is not None:
                drugs = [
                    drug for drug in drugs
                    if drug.get("phase", 0) >= min_phase
                ]
            
            # Filter approved only (phase 4)
            if approved_only:
                drugs = [
                    drug for drug in drugs
                    if drug.get("phase", 0) == 4
                ]
            
            # Filter by drug if specified
            if drug_id:
                drugs = [
                    drug for drug in drugs
                    if drug.get("drug", {}).get("id") == drug_id
                ]
            
            # Limit results
            drugs = drugs[:limit]
            
            # Count approved drugs
            approved_drugs = [
                drug.get("drug", {}).get("id")
                for drug in drugs
                if drug.get("phase", 0) == 4
            ]
            
            return {
                "disease": {
                    "id": disease_data.get("id"),
                    "name": disease_data.get("name")
                },
                "drugs": drugs,
                "drugCount": len(drugs),
                "approvedDrugs": approved_drugs,
                "approvedDrugCount": len(approved_drugs),
                "_query_metadata": {
                    "drug_id": drug_id,
                    "disease_id": disease_id,
                    "min_phase": min_phase,
                    "approved_only": approved_only,
                    "total_drugs": disease_data.get("knownDrugs", {}).get("count", 0),
                    "unique_drugs": disease_data.get("knownDrugs", {}).get("uniqueDrugs", 0)
                }
            }
        
        return {
            "error": "No data found",
            "data": data
        }


# Singleton instance
open_targets_drug_indication_tool = OpenTargetsDrugIndicationTool()
