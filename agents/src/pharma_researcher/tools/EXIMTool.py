from crewai.tools import BaseTool
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field
import requests
from datetime import date


class EXIMToolInput(BaseModel):
    hs_code: str = Field(..., description="HS code (2, 4 or 6 digits). Example: '3004'")
    year: Optional[int] = date.today().year
    flow_code: Optional[str] = None  # M=Import, X=Export
    frequency: Optional[str] = "A"
    max_records: Optional[int] = 500


class EXIMTool(BaseTool):
    name: str = "un_comtrade_exim_tool"
    description: str =  """Fetch EXIM trade data using the UN Comtrade API v1. Supports HS codes, imports/exports, partners, reporters.
    Use these HS Codes for researching
    | **HS Code** | **Category**                                               | **Description (UN Comtrade / WCO)**                                                                                  |
    | ----------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
    | **3001**    | Biological substances                                      | Glands and other organs for organo-therapeutic uses; dried and powdered; extracts thereof                            |
    | **3002**    | Biopharmaceuticals                                         | Human blood; animal blood; antisera, vaccines, toxins, cultures of micro-organisms                                   |
    | **3003**    | Medicinal mixtures (no brand name)                         | Medicaments consisting of two or more constituents mixed for therapeutic or prophylactic uses, not in measured doses |
    | **3004**    | Finished pharmaceuticals                                   | Medicaments in measured doses (tablets, capsules, injectables, etc.) for therapeutic or prophylactic uses            |
    | **3005**    | Medical dressings                                          | Wadding, gauze, bandages impregnated or coated with pharmaceutical substances                                        |
    | **3006**    | Pharmaceutical preparations                                | Including sterile surgical materials, dental cements, chemical contraceptives, etc.                                  |
    | **2936**    | Provitamins and vitamins                                   | Includes vitamin A, B-complex, C, D, E, K and their derivatives used in drug formulation                             |
    | **2937**    | Hormones and derivatives                                   | Including corticosteroids, sex hormones, insulin, etc. used in pharma R&D                                            |
    | **2939**    | Alkaloids and derivatives                                  | Includes caffeine, morphine, quinine, ephedrine, and their salts                                                     |
    | **2941**    | Antibiotics                                                | Penicillins, streptomycins, tetracyclines, and derivatives used in drug development                                  |
    | **2942**    | Organic compounds                                          | Other organic compounds with pharmaceutical potential (e.g., nucleic acids and salts)                                |
    | **2844**    | Radioactive isotopes                                       | For diagnostic use in nuclear medicine and pharmaceutical research                                                   |
    | **3822**    | Diagnostic or laboratory reagents                          | Prepared diagnostic/lab reagents on a backing or in form ready for use                                               |
    | **3821**    | Prepared culture media                                     | Used for microorganism growth and biochemical assays                                                                 |
    | **2933**    | Heterocyclic compounds with nitrogen                       | Includes heterocyclic bases used in synthesis of drugs (antivirals, antitumor agents, etc.)                          |
    | **2934**    | Nucleic acids and derivatives                              | Used in RNA/DNA-based drug research and gene therapy                                                                 |
    | **2935**    | Sulphonamides                                              | Used for antibiotic and antimicrobial compound development                                                           |
    | **3007**    | Vaccines and medical preparations (new category in HS2022) | Including COVID-19 and mRNA vaccines and diagnostic kits                                                             |
    | **3407**    | Chemical reagents for lab use                              | Often used in analytical and preclinical drug screening                                                              |
    | **3808**    | Disinfectants and antiseptics                              | Containing pharmaceutical actives used in clinical environments                                                      |
    
    """

    args_schema: Type[BaseModel] = EXIMToolInput

    def _run(
        self,
        hs_code: str,
        year: Optional[int] = date.today().year,
        flow_code: Optional[str] = None,
        frequency: Optional[str] = "A",
        max_records: Optional[int] = 500
    ) -> Dict[str, Any]:

        base_url = "https://comtradeapi.un.org/public/v1/getDA/{typeCode}/{freqCode}/{clCode}"

        # Set default values for reporter and partner
        reporter_code = "356"  # India
        partner_code = None
        
        # Fix: partner must be "0" for all partners
        partner = partner_code if partner_code else "0"

        # Fix: validate and map flow codes
        rg_code = self._map_flow(flow_code)

        params = {
            "max": min(max_records, 50000),
            "typeCode": "C",               # Commodities
            "freqCode": frequency,         # A or M
            "classificationCode": hs_code,              # HS classification
            "ps": str(year),           # period
            "r": reporter_code,        # reporter
            "p": partner,              # partner
            "rg": rg_code,             # flow
            "cc": hs_code              # HS code
        }

        try:
            headers = {"User-Agent": "pharma-researcher/1.0"}
            response = requests.get(base_url, params=params, headers=headers, timeout=30)

            # Fix: handle rate limit
            if response.status_code == 429:
                return {
                    "error": "Rate limit exceeded. UN Comtrade allows 1 request per second.",
                    "retry_after_seconds": response.headers.get("Retry-After", "1")
                }

            response.raise_for_status()
            data = response.json()

            # No dataset returned
            if "dataset" not in data or not data["dataset"]:
                return {
                    "error": "No trade data available for this query.",
                    "params_used": params,
                    "note": "Try another year, HS code, or flow type."
                }

            records = data["dataset"]

            # Limit
            records = records[:max_records]

            return {
                "results": records,
                "top_partners": self._top_partners(records),
                "_query_metadata": {
                    "hs_code": hs_code,
                    "reporter": reporter_code,
                    "partner": partner_code,
                    "year": year,
                    "flow": flow_code,
                    "frequency": frequency,
                    "records_returned": len(records),
                    "params_used": params
                }
            }

        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error {e.response.status_code}",
                "response": e.response.text[:300],
                "params_used": params
            }
        except Exception as e:
            return {
                "error": str(e),
                "params_used": params
            }

    # ---------------------------
    # Helper: Flow mapping
    # ---------------------------
    def _map_flow(self, flow_code: Optional[str]) -> str:
        """
        Map user-friendly flow code to Comtrade codes.
        """
        if flow_code == "M":
            return "1"   # imports
        if flow_code == "X":
            return "2"   # exports
        return "all"      # import+export combined (still valid for API v1)

    # ---------------------------
    # Helper: Top partners
    # ---------------------------
    def _top_partners(self, records: List[Dict[str, Any]], n: int = 5):
        values = {}

        for r in records:
            partner = r.get("ptTitle", "Unknown")
            val = r.get("TradeValue", 0)
            values[partner] = values.get(partner, 0) + val

        sorted_vals = sorted(values.items(), key=lambda x: x[1], reverse=True)

        return [{"partner": k, "value_usd": v} for k, v in sorted_vals[:n]]


# Singleton
india_exim_data = EXIMTool()
