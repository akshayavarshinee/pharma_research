from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AgentBaseOutput(BaseModel):
    agent_name: str
    session_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    summary: Optional[str] = None
    insights: Optional[List[str]] = None
    tables: Optional[List[Dict[str, Any]]] = None
    charts: Optional[List[str]] = None  # base64 images or file paths
    references: Optional[List[Dict[str, Any]]] = None
    raw_data: Optional[Dict[str, Any]] = None

# IQVIA
class IQVIAMetric(BaseModel):
    metric_name: str
    value: float
    unit: Optional[str] = None

class IQVIATrend(BaseModel):
    year: int
    value: float

class IQVIAInsightsOutput(AgentBaseOutput):
    market_size: Optional[float] = None
    cagr: Optional[float] = None
    top_countries: Optional[List[str]] = None
    sales_trends: Optional[List[IQVIATrend]] = None
    numerical_insights: Optional[List[IQVIAMetric]] = None

# EXIM TRADE
class TradeFlow(BaseModel):
    country: str
    import_volume: Optional[float] = None
    export_volume: Optional[float] = None
    unit: Optional[str] = None

class EXIMTrendsOutput(AgentBaseOutput):
    trade_flows: Optional[List[TradeFlow]] = None
    dependency_index: Optional[float] = None
    sourcing_risks: Optional[List[str]] = None

# PATENTS
class PatentEntry(BaseModel):
    patent_id: str
    assignee: Optional[str] = None
    status: Optional[str] = None  # active / expired / pending
    expiry_date: Optional[str] = None
    filing_date: Optional[str] = None

class PatentLandscapeOutput(AgentBaseOutput):
    patents: Optional[List[PatentEntry]] = None
    ft_o_risk: Optional[str] = None
    competitive_filers: Optional[List[str]] = None
    expiry_summary: Optional[Dict[str, Any]] = None

# CLINICAL TRAILS
class ClinicalTrial(BaseModel):
    trial_id: str
    title: Optional[str] = None
    phase: Optional[str] = None
    status: Optional[str] = None
    sponsor: Optional[str] = None
    start_date: Optional[str] = None
    locations: Optional[List[str]] = None

class ClinicalTrialsOutput(AgentBaseOutput):
    trials: Optional[List[ClinicalTrial]] = None
    phase_distribution: Optional[Dict[str, int]] = None
    sponsor_summary: Optional[List[str]] = None

# INTERNAL KNOWLEDGE
class DocumentInsight(BaseModel):
    document_name: str
    key_points: List[str]
    strategic_themes: Optional[List[str]] = None

class InternalKnowledgeOutput(AgentBaseOutput):
    documents: Optional[List[DocumentInsight]] = None
    themes: Optional[List[str]] = None

# WEB INTELLIGENCE
class WebSource(BaseModel):
    title: Optional[str]
    url: Optional[str]
    snippet: Optional[str]
    source_type: Optional[str]  # guideline / publication / news

class WebIntelligenceOutput(AgentBaseOutput):
    findings: Optional[List[WebSource]] = None
    guideline_updates: Optional[List[str]] = None
    competitive_news: Optional[List[str]] = None

# REPORT GENERATION
class ReportOutput(AgentBaseOutput):
    report_markdown: Optional[str] = None
    report_pdf_path: Optional[str] = None
    report_tables: Optional[List[Dict[str, Any]]] = None
    report_charts: Optional[List[str]] = None  # base64 or file paths
