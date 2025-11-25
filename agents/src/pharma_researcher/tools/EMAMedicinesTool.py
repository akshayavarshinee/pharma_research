from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import pandas as pd
import os
from pathlib import Path


class EMAMedicinesToolInput(BaseModel):
    """Input schema for EMAMedicinesTool."""
    medicine_name: Optional[str] = Field(
        None,
        description="Filter by product/medicine name (case-insensitive partial match)"
    )
    active_substance: Optional[str] = Field(
        None,
        description="Filter by active substance/ingredient name"
    )
    therapeutic_area: Optional[str] = Field(
        None,
        description="Filter by therapeutic area or indication"
    )
    authorisation_status: Optional[str] = Field(
        None,
        description="""
        Filter by authorization status.
        Common values: "Authorised", "Refused", "Withdrawn", "Suspended"
        """
    )
    category: Optional[str] = Field(
        None,
        description='Filter by category: "Human", "Veterinary"'
    )
    company: Optional[str] = Field(
        None,
        description="Filter by marketing authorization holder (company name)"
    )
    fields: Optional[List[str]] = Field(
        None,
        description="""
        Select specific columns to return.
        
        Common fields (exact names vary by dataset):
        - Medicine name, Active substance, Therapeutic area
        - Authorisation status, Marketing-authorisation holder
        - Category, First published, Revision date
        - ATC code, Orphan medicine
        
        Example: ["Medicine name", "Active substance", "Authorisation status"]
        """
    )
    max_results: Optional[int] = Field(
        500,
        description="Maximum number of results to return. Default: 500"
    )


class EMAMedicinesTool(BaseTool):
    name: str = "ema_medicines_tool"
    description: str = """
    Search European Medicines Agency (EMA) authorized medicines database.
    
    Use cases:
    - Find EU-approved drugs and their status
    - Check authorization status (approved, withdrawn, refused)
    - Identify active substances and therapeutic areas
    - Find orphan designations
    - Compare marketing authorization holders
    - Track approval/revision dates
    
    Examples:
    1. Find medicine: medicine_name="Ozempic"
    2. By substance: active_substance="semaglutide"
    3. Therapeutic area: therapeutic_area="diabetes"
    4. Company products: company="Novo Nordisk", authorisation_status="Authorised"
    5. Field selection: medicine_name="Jardiance", fields=["Medicine name", "Active substance"]
    """
    args_schema: Type[BaseModel] = EMAMedicinesToolInput

    def _run(
        self,
        medicine_name: Optional[str] = None,
        active_substance: Optional[str] = None,
        therapeutic_area: Optional[str] = None,
        authorisation_status: Optional[str] = None,
        category: Optional[str] = None,
        company: Optional[str] = None,
        fields: Optional[List[str]] = None,
        max_results: Optional[int] = 500
    ) -> Dict[str, Any]:
        """
        Search EMA medicines database with filters.
        
        Returns:
            Dict with medicine data and metadata
        """
        filepath = Path(__file__).parent.parent.parent.parent / "data" / "medicines_output_medicines_en.xlsx"
        
        if not os.path.exists(filepath):
            return {"error": f"EMA medicines file not found: {filepath}"}

        try:
            df = pd.read_excel(filepath)
            df.columns = [col.strip().replace("\n", " ") for col in df.columns]
            
            total_records = len(df)
            
            # Apply filters
            if medicine_name:
                # Find column that contains "medicine" and "name"
                name_col = self._find_column(df, ["medicine", "name", "product"])
                if name_col:
                    df = df[df[name_col].astype(str).str.contains(medicine_name, case=False, na=False)]
            
            if active_substance:
                substance_col = self._find_column(df, ["active", "substance", "ingredient"])
                if substance_col:
                    df = df[df[substance_col].astype(str).str.contains(active_substance, case=False, na=False)]
            
            if therapeutic_area:
                area_col = self._find_column(df, ["therapeutic", "area", "indication"])
                if area_col:
                    df = df[df[area_col].astype(str).str.contains(therapeutic_area, case=False, na=False)]
            
            if authorisation_status:
                status_col = self._find_column(df, ["authorisation", "status"])
                if status_col:
                    df = df[df[status_col].astype(str).str.contains(authorisation_status, case=False, na=False)]
            
            if category:
                category_col = self._find_column(df, ["category"])
                if category_col:
                    df = df[df[category_col].astype(str).str.contains(category, case=False, na=False)]
            
            if company:
                company_col = self._find_column(df, ["marketing", "authorisation", "holder", "company"])
                if company_col:
                    df = df[df[company_col].astype(str).str.contains(company, case=False, na=False)]
            
            # Select specific fields if requested
            if fields:
                available_fields = [f for f in fields if f in df.columns]
                if available_fields:
                    df = df[available_fields]
            
            # Limit results
            df = df.head(max_results)
            
            return {
                "results": df.to_dict(orient="records"),
                "_query_metadata": {
                    "total_in_database": total_records,
                    "results_returned": len(df),
                    "filters_applied": {
                        "medicine_name": medicine_name,
                        "active_substance": active_substance,
                        "therapeutic_area": therapeutic_area,
                        "authorisation_status": authorisation_status,
                        "category": category,
                        "company": company
                    },
                    "fields_selected": fields,
                    "available_columns": list(df.columns) if not fields else None
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to process EMA data: {str(e)}"}
    
    def _find_column(self, df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
        """Find column name containing any of the keywords (case-insensitive)."""
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword.lower() in col_lower for keyword in keywords):
                return col
        return None
