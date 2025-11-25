# Enhanced API Tools - Complete Usage Guide

## Overview

All 9 pharma research API tools have been enhanced with:

- ✅ Comprehensive input schemas with detailed parameter descriptions
- ✅ Dynamic query building capabilities
- ✅ Field selection and filtering options
- ✅ Aggregation and count operations (where applicable)
- ✅ Pagination support
- ✅ Improved error handling with metadata
- ✅ Date range filtering

---

## FDA Tools (5 tools)

### 1. FDAAdverseEventsTool

**Purpose**: Search FDA Adverse Event Reporting System (FAERS) for drug safety signals

**Enhanced Parameters**:

- `search_query` - OpenFDA query string
- `count` - Aggregation field (e.g., reactions, drugs)
- `date_range` - Filter by date (YYYYMMDD format)
- `country` - Filter by country code
- `serious_only` - Boolean for serious events only
- `limit`, `skip` - Pagination
- `extract_fields` - Simplified output format

**Examples**:

```python
# Find serious events for a drug
{
    "search_query": 'patient.drug.medicinalproduct:"jardiance"',
    "serious_only": True,
    "limit": 50
}

# Count reactions by type
{
    "search_query": 'patient.drug.medicinalproduct:"metformin"',
    "count": "patient.reaction.reactionmeddrapt.exact"
}

# Date range with country filter
{
    "search_query": 'patient.drug.openfda.generic_name:"semaglutide"',
    "date_range": {"from": "20230101", "to": "20231231"},
    "country": "US"
}
```

---

### 2. FDADrugsFDATool

**Purpose**: Search FDA Drugs@FDA database for approval information

**Enhanced Parameters**:

- `search_query` - OpenFDA query
- `brand_name` - Shortcut for brand search
- `generic_name` - Shortcut for generic search
- `sponsor` - Filter by manufacturer
- `application_type` - NDA, ANDA, or BLA
- `fields` - Select specific fields to return
- `limit`, `skip` - Pagination

**Examples**:

```python
# Find drug by brand name
{
    "brand_name": "Ozempic",
    "fields": ["products.brand_name", "products.indication", "sponsor_name"]
}

# Generic drug search
{
    "generic_name": "empagliflozin",
    "sponsor": "Boehringer"
}

# Application type filter
{
    "sponsor": "Novo Nordisk",
    "application_type": "NDA",
    "limit": 100
}
```

---

### 3. FDAEnforcementTool

**Purpose**: Search FDA drug recall and enforcement reports

**Enhanced Parameters**:

- `search_query` - OpenFDA query
- `product` - Product name shortcut
- `classification` - Class I, II, or III
- `status` - Ongoing, Completed, Terminated
- `state` - US state code
- `recalling_firm` - Company name
- `date_range` - Date filter (YYYY-MM-DD)
- `count` - Aggregation field

**Examples**:

```python
# Class I recalls
{
    "product": "ranitidine",
    "classification": "Class I"
}

# Count recalls by state
{
    "date_range": {"from": "2023-01-01"},
    "count": "state"
}

# Company recalls
{
    "recalling_firm": "Pfizer",
    "status": "Ongoing"
}
```

---

### 4. FDANDCTool

**Purpose**: Search FDA National Drug Code (NDC) directory

**Enhanced Parameters**:

- `search_query` - OpenFDA query
- `generic_name`, `brand_name`, `labeler` - Search shortcuts
- `route` - Administration route (ORAL, INJECTION, etc.)
- `dosage_form` - TABLET, CAPSULE, etc.
- `marketing_status` - Prescription, OTC, Discontinued
- `package_type` - BOTTLE, CARTON, etc.
- `fields` - Field selection

**Examples**:

```python
# Find NDC by generic name
{
    "generic_name": "semaglutide",
    "route": "SUBCUTANEOUS"
}

# Branded insulin products
{
    "brand_name": "insulin",
    "dosage_form": "INJECTION",
    "labeler": "Novo Nordisk"
}

# Select specific fields
{
    "generic_name": "metformin",
    "fields": ["product_ndc", "generic_name", "labeler_name"]
}
```

---

### 5. FDAProductLabelTool

**Purpose**: Search FDA drug product labels (package inserts)

**Enhanced Parameters**:

- `search_query` - Open FDA query
- `brand_name`, `generic_name`, `manufacturer` - Shortcuts
- `section` - Specific label section
- `section_text` - Text to search within section
- `product_type` - Prescription, OTC, Vaccine
- `fields` - Select label sections to return

**Examples**:

```python
# Get indications only
{
    "brand_name": "Jardiance",
    "fields": ["openfda.brand_name", "indications_and_usage"]
}

# Search in warnings section
{
    "section": "warnings",
    "section_text": "cardiovascular"
}

# Get specific sections
{
    "generic_name": "empagliflozin",
    "fields": ["indications_and_usage", "dosage_and_administration", "warnings"]
}
```

---

## Clinical Research Tools (2 tools)

### 6. ClinicalTrialsTool

**Purpose**: Search ClinicalTrials.gov database

**Enhanced Parameters**:

- `condition` - Disease/condition
- `intervention` - Drug/intervention name
- `phase` - Study phase (PHASE1, PHASE2, PHASE3, PHASE4)
- `status` - Recruitment status (RECRUITING, COMPLETED, etc.)
- `sponsor` - Lead sponsor
- `location` - Geographic filter
- `study_type` - INTERVENTIONAL, OBSERVATIONAL
- `fields` - Field selection
- `page_size`, `page_token` - Pagination
- `sort` - Sort order

**Examples**:

```python
# Recruiting diabetes trials
{
    "condition": "diabetes",
    "status": ["RECRUITING"],
    "phase": ["PHASE3"]
}

# Trials by drug and sponsor
{
    "intervention": "semaglutide",
    "sponsor": "Novo Nordisk",
    "status": ["COMPLETED", "ACTIVE_NOT_RECRUITING"]
}

# Geographic search with field selection
{
    "condition": "lung cancer",
    "location": "California",
    "fields": ["NCTId", "BriefTitle", "OverallStatus", "Phase"]
}
```

---

### 7. NCBIEntrezTool

**Purpose**: Search NCBI databases (PubMed, PMC, Gene, etc.)

**Enhanced Parameters**:

- `database` - pubmed, pmc, gene, protein, clinvar, etc.
- `search_term` - Query with field tags
- `retmax`, `retstart` - Pagination
- `retmode` - xml or json
- `sort` - relevance, pub_date, Author
- `date_range` - Publication date filter
- `utility` - esearch, efetch, esummary, elink
- `ids` - PMIDs for fetching
- `parse_results` - Auto-parse XML/JSON

**Examples**:

```python
# PubMed search
{
    "database": "pubmed",
    "search_term": "diabetes mellitus type 2 AND metformin",
    "retmax": 50,
    "sort": "pub_date"
}

# Recent articles only
{
    "database": "pubmed",
    "search_term": "COVID-19 vaccine",
    "date_range": {"mindate": "2023/01/01"},
    "retmax": 100
}

# Fetch article details
{
    "database": "pubmed",
    "utility": "efetch",
    "ids": ["12345678", "87654321"]
}

# Gene database search
{
    "database": "gene",
    "search_term": "BRCA1[Gene Name] AND human[Organism]"
}
```

---

## EMA Tools (2 tools)

### 8. EMAMedicinesTool

**Purpose**: Search EMA authorized medicines database

**Enhanced Parameters**:

- `medicine_name` - Product name filter
- `active_substance` - Ingredient filter
- `therapeutic_area` - Indication filter
- `authorisation_status` - Authorised, Refused, Withdrawn
- `category` - Human, Veterinary
- `company` - Marketing authorization holder
- `fields` - Field selection
- `max_results` - Result limit

**Examples**:

```python
# Find by medicine name
{
    "medicine_name": "Ozempic",
    "authorisation_status": "Authorised"
}

# Active substance search
{
    "active_substance": "semaglutide",
    "category": "Human"
}

# Company products
{
    "company": "Novo Nordisk",
    "therapeutic_area": "diabetes",
    "fields": ["Medicine name", "Active substance", "Authorisation status"]
}
```

---

### 9. EMAMedicineShortagesTool

**Purpose**: Search EMA medicine supply shortages database

**Enhanced Parameters**:

- `medicine_name` - Product name filter
- `active_substance` - Ingredient filter
- `therapeutic_area` - Indication filter
- `country` - Affected country
- `status` - Active, Resolved, Ongoing
- `shortage_reason` - Reason for shortage
- `date_range` - Date filter (YYYY-MM-DD)
- `fields` - Field selection
- `max_results` - Result limit

**Examples**:

```python
# Current shortages
{
    "status": "Active",
    "therapeutic_area": "antibiotics"
}

# Country-specific
{
    "medicine_name": "metformin",
    "country": "Germany",
    "status": "Active"
}

# Recent shortages
{
    "date_range": {"from": "2024-01-01"},
    "fields": ["Medicine Name", "Country", "Status", "Shortage Start Date"]
}
```

---

## Key Improvements Across All Tools

### 1. **Consistent Pattern**

All tools now follow the PatentsView tool pattern with:

- Comprehensive input schemas
- Detailed parameter descriptions with examples
- Dynamic query building
- Metadata in responses

### 2. **Field Selection**

Most tools support `fields` parameter to return only needed data, significantly reducing response size.

### 3. **Filtering & Aggregation**

- Multiple filter parameters per tool
- Count/aggregation support (FDA tools)
- Date range filtering where applicable

### 4. **Better Error Handling**

All tools return structured errors with:

- Error message
- Request details (URL, params)
- Helpful context

### 5. **Metadata**

Every response includes `_query_metadata` with:

- Query details
- Result counts
- Pagination info
- Applied filters

---

## Testing the Enhanced Tools

See test script: `tests/test_all_enhanced_tools.py`

Run with:

```bash
python tests/test_all_enhanced_tools.py
```

---

## Migration from Old Tools

The enhanced tools are **backward compatible**. Old usage patterns will continue to work:

```python
# Old way (still works)
{"search_query": "patient.drug.medicinalproduct:metformin", "limit": 50}

# New way (enhanced)
{
    "search_query": "patient.drug.medicinalproduct:metformin",
    "serious_only": True,
    "date_range": {"from": "20230101"},
    "fields": ["reaction", "serious", "outcome"],
    "limit": 50
}
```
