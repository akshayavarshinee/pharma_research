from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests


class ClinicalTrialsToolInput(BaseModel):
    condition: Optional[str] = None
    intervention: Optional[str] = None
    phase: Optional[List[str]] = None
    status: Optional[List[str]] = None
    sponsor: Optional[str] = None
    location: Optional[str] = None
    study_type: Optional[str] = None
    fields: Optional[List[str]] = None
    page_size: Optional[int] = 20
    page_token: Optional[str] = None
    sort: Optional[List[str]] = None


class ClinicalTrialsTool(BaseTool):
    name: str = "clinical_trials_api_tool"
    description: str = "Search ClinicalTrials.gov API v2 for trial data."
    args_schema: Type[BaseModel] = ClinicalTrialsToolInput

    def _run(
        self,
        condition: Optional[str] = None,
        intervention: Optional[str] = None,
        phase: Optional[List[str]] = None,
        status: Optional[List[str]] = None,
        sponsor: Optional[str] = None,
        location: Optional[str] = None,
        study_type: Optional[str] = None,
        fields: Optional[List[str]] = None,
        page_size: Optional[int] = 20,
        page_token: Optional[str] = None,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:

        url = "https://clinicaltrials.gov/api/v2/studies"

        params: Dict[str, Any] = {
            "format": "json",
            "pageSize": min(max(page_size, 1), 1000)
        }

        # -----------------------------
        # Query parameters
        # -----------------------------
        if condition:
            params["query.cond"] = condition

        if intervention:
            params["query.intr"] = intervention

        if sponsor:
            params["query.lead"] = sponsor

        if location:
            params["query.locn"] = location

        if study_type:
            params["query.type"] = study_type

        # -----------------------------
        # Advanced filters (correct v2 format)
        # -----------------------------
        filter_parts = []

        if phase:
            filter_parts.append(f"phase:{','.join(phase)}")

        if status:
            filter_parts.append(f"overallStatus:{','.join(status)}")

        if filter_parts:
            params["filter.advanced"] = " AND ".join(filter_parts)

        # -----------------------------
        # Field selection
        # -----------------------------
        if fields:
            params["fields"] = ",".join(fields)

        # Pagination
        if page_token:
            params["pageToken"] = page_token

        # Sorting
        if sort:
            params["sort"] = ",".join(sort)

        # Must have at least one search parameter
        if not any([condition, intervention, sponsor, location, study_type, phase, status]):
            return {"error": "At least one search parameter must be provided"}

        headers = {"User-Agent": "pharma-researcher/1.0"}

        # -----------------------------
        # Execute request
        # -----------------------------
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            result = {
                "_query_metadata": {
                    "condition": condition,
                    "intervention": intervention,
                    "phase": phase,
                    "status": status,
                    "sponsor": sponsor,
                    "location": location,
                    "study_type": study_type,
                    "fields": fields,
                    "page_size": page_size,
                    "total_count": data.get("totalCount"),
                    "returned": len(data.get("studies", [])),
                    "next_page_token": data.get("nextPageToken")
                }
            }

            result.update(data)
            return result

        except requests.exceptions.HTTPError as e:
            return {
                "error": f"ClinicalTrials.gov API HTTP {e.response.status_code}",
                "details": e.response.text[:500],
                "params": params
            }

        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "params": params
            }
