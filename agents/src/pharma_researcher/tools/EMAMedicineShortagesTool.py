from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import pandas as pd
import os
from pathlib import Path
from datetime import datetime


class EMAMedicineShortagesToolInput(BaseModel):
    """Input schema for EMAMedicineShortages Tool."""
    medicine_name: Optional[str] = Field(
        None,
        description="Filter by medicine/product name (case-insensitive partial match)"
    )
    active_substance: Optional[str] = Field(
        None,
        description="Filter by active substance/ingredient name"
    )
    therapeutic_area: Optional[str] = Field(
        None,
        description="Filter by therapeutic area"
    )
    country: Optional[str] = Field(
        None,
        description="Filter by affected country/market"
    )
    status: Optional[str] = Field(
        None,
        description="""
        Filter by shortage status.
        Common values: "Active", "Resolved", "Ongoing", "Temporary"
        """
    )
    shortage_reason: Optional[str] = Field(
        None,
        description="Filter by reason for shortage (e.g., 'manufacturing', 'supply chain')"
    )
    date_range: Optional[Dict[str, str]] = Field(
        None,
        description="""
        Filter by shortage start date (YYYY-MM-DD format).
        Example: {"from": "2023-01-01", "to": "2023-12-31"}
        """
    )
    fields: Optional[List[str]] = Field(
        None,
        description="""
        Select specific columns to return.
        
        Common fields:
        - Medicine Name, Active Substance, Therapeutic Area
        - Country, Status, Shortage Start Date
        - Shortage End Date, Reason for Shortage
        - Expected Resolution Date
        
        Example: ["Medicine Name", "Country", "Status", "Shortage Start Date"]
        """
    )
    max_results: Optional[int] = Field(
        500,
        description="Maximum number of results to return. Default: 500"
    )


class EMAMedicineShortagesTool(BaseTool):
    name: str = "ema_medicine_shortages_tool"
    description: str = """
    Search European Medicines Agency (EMA) medicine supply shortages database.
    
    Use cases:
    - Track current and historical drug shortages in EU
    - Identify shortages by therapeutic area
    - Monitor shortages by country/market
    - Analyze shortage reasons and patterns
    - Forecast shortage resolution dates
    - Compare shortage severity across regions
    
    Examples:
    1. Current shortages: status="Active"
    2. Specific drug: medicine_name="metformin", status="Active"
    3. By country: country="Germany", therapeutic_area="antibiotics"
    4. Recent: date_range={"from": "2024-01-01"}
    5. Field selection: status="Active", fields=["Medicine Name", "Country", "Status"]
    """
    args_schema: Type[BaseModel] = EMAMedicineShortagesToolInput

    def _run(
        self,
        medicine_name: Optional[str] = None,
        active_substance: Optional[str] = None,
        therapeutic_area: Optional[str] = None,
        country: Optional[str] = None,
        status: Optional[str] = None,
        shortage_reason: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None,
        fields: Optional[List[str]] = None,
        max_results: Optional[int] = 500
    ) -> Dict[str, Any]:
        """
        Search EMA medicine shortages database with filters.
        
        Returns:
            Dict with shortage data and metadata
        """
        filepath = Path(__file__).parent.parent.parent.parent / "data" / "medicine_shortages_en.xlsx"
        
        if not os.path.exists(filepath):
            return {"error": f"EMA shortages file not found: {filepath}"}

        try:
            df = pd.read_excel(filepath)
            df.columns = [col.strip().replace("\n", " ") for col in df.columns]
            
            total_records = len(df)
            
            # Apply filters
            if medicine_name:
                name_col = self._find_column(df, ["medicine", "name", "product"])
                if name_col:
                    df = df[df[name_col].astype(str).str.contains(medicine_name, case=False, na=False)]
            
            if active_substance:
                substance_col = self._find_column(df, ["active", "substance", "ingredient"])
                if substance_col:
                    df = df[df[substance_col].astype(str).str.contains(active_substance, case=False, na=False)]
            
            if therapeutic_area:
                area_col = self._find_column(df, ["therapeutic", "area"])
                if area_col:
                    df = df[df[area_col].astype(str).str.contains(therapeutic_area, case=False, na=False)]
            
            if country:
                country_col = self._find_column(df, ["country", "market"])
                if country_col:
                    df = df[df[country_col].astype(str).str.contains(country, case=False, na=False)]
            
            if status:
                status_col = self._find_column(df, ["status"])
                if status_col:
                    df = df[df[status_col].astype(str).str.contains(status, case=False, na=False)]
            
            if shortage_reason:
                reason_col = self._find_column(df, ["reason", "shortage"])
                if reason_col:
                    df = df[df[reason_col].astype(str).str.contains(shortage_reason, case=False, na=False)]
            
            # Date range filter
            if date_range:
                date_col = self._find_column(df, ["shortage", "start", "date"])
                if date_col:
                    # Convert to datetime
                    df = df.copy()
                    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                    
                    if "from" in date_range:
                        from_date = pd.to_datetime(date_range["from"])
                        df = df[df[date_col] >= from_date]
                    
                    if "to" in date_range:
                        to_date = pd.to_datetime(date_range["to"])
                        df = df[df[date_col] <= to_date]
            
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
                        "country": country,
                        "status": status,
                        "shortage_reason": shortage_reason,
                        "date_range": date_range
                    },
                    "fields_selected": fields,
                    "available_columns": list(df.columns) if not fields else None
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to process EMA shortages data: {str(e)}"}
    
    def _find_column(self, df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
        """Find column name containing any of the keywords (case-insensitive)."""
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword.lower() in col_lower for keyword in keywords):
                return col
        return None
