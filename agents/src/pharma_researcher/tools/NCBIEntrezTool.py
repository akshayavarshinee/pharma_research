from crewai.tools import BaseTool
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
import xml.etree.ElementTree as ET
import json
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class NCBIEntrezToolInput(BaseModel):
    """Input schema for NCBIEntrezTool."""
    database: str = Field(
        "pubmed",
        description="""
        NCBI database to search.
        
        Common databases:
        - "pubmed" - PubMed citations/abstracts
        - "pmc" - PubMed Central full-text articles
        - "gene" - Gene database
        - "protein" - Protein sequences
        - "nucleotide" - Nucleotide sequences
        - "clinvar" - Clinical variants
        - "mesh" - Medical Subject Headings
        - "omim" - Online Mendelian Inheritance in Man
        
        Default: "pubmed"
        """
    )
    search_term: str = Field(
        ...,
        description="""
        Search query term.
        
        PubMed examples:
        - "diabetes mellitus type 2"
        - "COPD[Title/Abstract] AND treatment"
        - "metformin[Title] AND cardiovascular"
        - "asthma AND (children OR pediatric)"
        
        Can use field tags: [Title], [Abstract], [Author], [Journal], etc.
        """
    )
    retmax: Optional[int] = Field(
        20,
        description="Maximum number of search results to return (1-10000). Default: 20"
    )
    retstart: Optional[int] = Field(
        0,
        description="Sequential index of first result to retrieve (for pagination). Default: 0"
    )
    retmode: Optional[str] = Field(
        "xml",
        description='Return format: "xml" or "json". Default: "xml"'
    )
    sort: Optional[str] = Field(
        None,
        description="""
        Sort order for results.
        Options: "relevance" (default), "pub_date" (publication date), "Author", "JournalName"
        """
    )
    date_range: Optional[Dict[str, str]] = Field(
        None,
        description="""
        Filter by publication date range (YYYY/MM/DD format).
        Example: {"mindate": "2020/01/01", "maxdate": "2023/12/31"}
        """
    )
    utility: Optional[str] = Field(
        "esearch",
        description="""
        Entrez utility to use:
        - "esearch" - Search and retrieve IDs
        - "esummary" - Get document summaries
        - "efetch" - Fetch full records
        - "elink" - Find related records
        - "einfo" - Get database statistics
        
        Default: "esearch"
        """
    )
    ids: Optional[List[str]] = Field(
        None,
        description="List of NCBI IDs (PMIDs) for efetch/esummary. Use with utility='efetch' or 'esummary'"
    )
    parse_results: Optional[bool] = Field(
        True,
        description="Parse XML/JSON into structured format. Default: True"
    )


class NCBIEntrezTool(BaseTool):
    name: str = "ncbi_entrez_tool"
    description: str = """
    Search NCBI databases (PubMed, PMC, Gene, Protein, etc.) using Entrez E-utilities.
    
    Use cases:
    - Search PubMed for scientific literature
    - Find full-text articles in PMC
    - Retrieve gene and protein information
    - Access clinical variant data (ClinVar)
    - Find related articles and citations
    - Get publication metadata
    
    Examples:
    1. PubMed search: database="pubmed", search_term="diabetes treatment", retmax=50
    2. Recent articles: search_term="COVID-19 vaccine", date_range={"mindate": "2023/01/01"}
    3. Gene search: database="gene", search_term="BRCA1[Gene Name] AND human[Organism]"
    4. Fetch articles: utility="efetch", database="pubmed", ids=["12345678"]
    """
    args_schema: Type[BaseModel] = NCBIEntrezToolInput

    def _run(
        self,
        database: str = "pubmed",
        search_term: Optional[str] = None,
        retmax: Optional[int] = 20,
        retstart: Optional[int] = 0,
        retmode: Optional[str] = "xml",
        sort: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None,
        utility: Optional[str] = "esearch",
        ids: Optional[List[str]] = None,
        parse_results: Optional[bool] = True
    ) -> Dict[str, Any]:
        """
        Execute NCBI Entrez E-utilities query.
        
        Returns:
            Dict with search results and metadata
        """
        base_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{utility}.fcgi"
        
        # Build parameters
        params: Dict[str, Any] = {
            "db": database,
            "retmode": retmode
        }
        
        # For search operations
        if utility == "esearch":
            if not search_term:
                return {"error": "search_term is required for esearch"}
            
            params["term"] = search_term
            params["retmax"] = min(max(1, retmax), 10000)
            params["retstart"] = max(0, retstart)
            
            if sort:
                params["sort"] = sort
            
            if date_range:
                if "mindate" in date_range:
                    params["mindate"] = date_range["mindate"]
                if "maxdate" in date_range:
                    params["maxdate"] = date_range["maxdate"]
                params["datetype"] = "pdat"  # publication date
        
        # For fetch/summary operations
        elif utility in ["efetch", "esummary"]:
            if not ids:
                return {"error": f"ids parameter required for {utility}"}
            
            params["id"] = ",".join(ids)
            
            if utility == "efetch":
                params["rettype"] = "abstract" if database == "pubmed" else "full"
        
        # For link operations
        elif utility == "elink":
            if not ids:
                return {"error": "ids parameter required for elink"}
            params["id"] = ",".join(ids)
        
        # For info operations
        elif utility == "einfo":
            # Database info - no additional params needed
            pass
        
        try:
            # polite identifiers and optional api key
            params["tool"] = os.getenv("ENTREZ_TOOL_NAME", "pharma-researcher")
            if os.getenv("ENTREZ_EMAIL"):
                params["email"] = os.getenv("ENTREZ_EMAIL")
            if os.getenv("ENTREZ_API_KEY"):
                params["api_key"] = os.getenv("ENTREZ_API_KEY")

            headers = {"User-Agent": f"pharma-researcher/1.0 (+{os.getenv('ENTREZ_EMAIL','no-email')})"}
            # setup a requests session with retries/backoff
            session = requests.Session()
            retries = Retry(total=3, backoff_factor=1,
                            status_forcelist=[429, 500, 502, 503, 504],
                            allowed_methods=["GET", "POST"])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse response
            if parse_results:
                if retmode == "xml":
                    result = self._parse_xml_response(response.text, utility, database)
                elif retmode == "json":
                    result = response.json()
                else:
                    result = {"text": response.text}
            else:
                result = {"raw": response.text}
            
            # Add metadata
            result["_query_metadata"] = {
                "database": database,
                "utility": utility,
                "search_term": search_term,
                "retmax": retmax,
                "retstart": retstart,
                "ids": ids,
                "url": base_url,
                "params": params
            }
            
            return result
            
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"NCBI API error: {e.response.status_code}",
                "details": e.response.text[:500],
                "url": base_url,
                "params": params
            }
        except Exception as e:
            return {
                "error": f"Request failed: {str(e)}",
                "url": base_url,
                "params": params
            }
    
    def _parse_xml_response(self, xml_text: str, utility: str, database: str) -> Dict[str, Any]:
        """Parse XML response into structured format."""
        try:
            root = ET.fromstring(xml_text)
            
            if utility == "esearch":
                # Parse search results
                count = root.find(".//Count")
                id_list = root.findall(".//Id")
                
                return {
                    "count": int(count.text) if count is not None else 0,
                    "ids": [id_elem.text for id_elem in id_list],
                    "id_count": len(id_list),
                    "xml_raw": xml_text
                }
            
            elif utility == "esummary":
                # Parse document summaries
                summaries = []
                for doc_sum in root.findall(".//DocSum"):
                    summary = {"id": doc_sum.find("Id").text if doc_sum.find("Id") is not None else None}
                    for item in doc_sum.findall(".//Item"):
                        name = item.get("Name")
                        value = item.text
                        if name and value:
                            summary[name] = value
                    summaries.append(summary)
                
                return {
                    "summaries": summaries,
                    "count": len(summaries),
                    "xml_raw": xml_text
                }
            
            elif utility == "efetch":
                # For PubMed abstracts
                if database == "pubmed":
                    articles = []
                    for article in root.findall(".//PubmedArticle"):
                        pmid_elem = article.find(".//PMID")
                        title_elem = article.find(".//ArticleTitle")
                        abstract_elem = article.find(".//Abstract/AbstractText")
                        journal_elem = article.find(".//Journal/Title")
                        pub_date = article.find(".//PubDate/Year")
                        
                        articles.append({
                            "pmid": pmid_elem.text if pmid_elem is not None else None,
                            "title": title_elem.text if title_elem is not None else None,
                            "abstract": abstract_elem.text if abstract_elem is not None else None,
                            "journal": journal_elem.text if journal_elem is not None else None,
                            "year": pub_date.text if pub_date is not None else None
                        })
                    
                    return {
                        "articles": articles,
                        "count": len(articles),
                        "xml_raw": xml_text
                    }
            
            # Default: return raw XML
            return {"xml_raw": xml_text, "parsed_root": str(root)}
            
        except ET.ParseError as e:
            return {
                "parse_error": str(e),
                "xml_raw": xml_text
            }
