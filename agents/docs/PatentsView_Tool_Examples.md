# PatentsView API Tool - Usage Examples

## Overview

The PatentsView API Tool provides comprehensive access to US patent data with support for complex queries, field selection, sorting, and pagination.

## Basic Examples

### 1. Find a Specific Patent

```python
{
    "query": {"patent_id": "7861317"}
}
```

### 2. Search by Inventor Name

```python
{
    "query": {"inventors.inventor_name_last": "Whitney"}
}
```

### 3. Search Multiple Inventors

```python
{
    "query": {"inventors.inventor_name_last": ["Whitney", "Hopper"]}
}
```

## Date Range Queries

### Patents Granted in 2007

```python
{
    "query": {
        "_and": [
            {"_gte": {"patent_date": "2007-01-01"}},
            {"_lte": {"patent_date": "2007-12-31"}}
        ]
    }
}
```

### Patents After a Specific Date

```python
{
    "query": {"_gte": {"patent_date": "2020-01-01"}}
}
```

## Text Search Examples

### Search Patent Titles (Any Word Match)

```python
{
    "query": {
        "_text_any": {"patent_title": "respiratory COPD asthma"}
    }
}
```

### Search Patent Abstracts (All Words)

```python
{
    "query": {
        "_text_all": {"patent_abstract": "drug delivery inhalation"}
    }
}
```

### Search for Exact Phrase

```python
{
    "query": {
        "_text_phrase": {"patent_title": "cotton gin"}
    }
}
```

## Complex Pharmaceutical Research Queries

### Respiratory Disease Patents (Recent, Active)

```python
{
    "query": {
        "_and": [
            {"_text_any": {"patent_abstract": "respiratory asthma COPD bronchitis"}},
            {"_gte": {"patent_date": "2015-01-01"}},
            {"_not": {"patent_type": "design"}}
        ]
    },
    "fields": [
        "patent_id",
        "patent_title",
        "patent_date",
        "inventors.inventor_name_last",
        "assignees.assignee_organization",
        "patent_num_claims",
        "patent_num_times_cited_by_us_patents"
    ],
    "sort": [{"patent_num_times_cited_by_us_patents": "desc"}],
    "size": 50
}
```

### Find Patents by Company (Assignee)

```python
{
    "query": {
        "_and": [
            {"assignees.assignee_organization": "AstraZeneca"},
            {"_text_any": {"patent_abstract": "inhaler respiratory"}},
            {"_gte": {"patent_date": "2018-01-01"}}
        ]
    },
    "fields": [
        "patent_id",
        "patent_title",
        "patent_date",
        "patent_abstract",
        "assignees.assignee_organization"
    ]
}
```

### Patents by Multiple Companies

```python
{
    "query": {
        "_and": [
            {"assignees.assignee_organization": ["Pfizer", "Novartis", "GSK"]},
            {"_text_any": {"patent_title": "pharmaceutical drug"}}
        ]
    }
}
```

### Exclude Specific Patent Types

```python
{
    "query": {
        "_and": [
            {"_text_any": {"patent_abstract": "diabetes insulin"}},
            {"_not": {"patent_type": "design"}},
            {"_gte": {"patent_date": "2010-01-01"}}
        ]
    }
}
```

## Advanced Field Selection

### Comprehensive Patent Details

```python
{
    "query": {"patent_id": "7861317"},
    "fields": [
        "patent_id",
        "patent_number",
        "patent_title",
        "patent_abstract",
        "patent_date",
        "patent_type",
        "patent_num_claims",
        "patent_num_us_application_citations",
        "patent_num_foreign_citations",
        "patent_num_times_cited_by_us_patents",
        "inventors.inventor_name_first",
        "inventors.inventor_name_last",
        "inventors.inventor_city",
        "inventors.inventor_country",
        "assignees.assignee_organization",
        "assignees.assignee_type",
        "cpcs.cpc_group_title",
        "uspc.uspc_class",
        "uspc.uspc_subclass"
    ]
}
```

## Sorting Examples

### Most Cited Patents First

```python
{
    "sort": [{"patent_num_times_cited_by_us_patents": "desc"}]
}
```

### Newest Patents First, Then by Citation

```python
{
    "sort": [
        {"patent_date": "desc"},
        {"patent_num_times_cited_by_us_patents": "desc"}
    ]
}
```

## Pagination Examples

### Get First 100 Results

```python
{
    "query": {"_text_any": {"patent_title": "pharmaceutical"}},
    "size": 100
}
```

### Get Next Page (Cursor Pagination)

```python
{
    "query": {"_text_any": {"patent_title": "pharmaceutical"}},
    "size": 100,
    "after": "2020-01-15",  # Use last patent_date from previous page
    "sort": [{"patent_date": "desc"}]
}
```

## Options Examples

### Pad Patent IDs

```python
{
    "query": {"patent_id": "7245826"},
    "pad_patent_id": True  # Returns "07245826"
}
```

### Include Withdrawn Patents

```python
{
    "query": {"_text_any": {"patent_title": "medical device"}},
    "exclude_withdrawn": False
}
```

## Real-World Pharma Research Scenarios

### 1. Competitive Patent Landscape for Diabetes Drugs

```python
{
    "query": {
        "_and": [
            {"_text_any": {"patent_abstract": "diabetes glucose insulin metformin"}},
            {"assignees.assignee_organization": ["Eli Lilly", "Novo Nordisk", "Sanofi"]},
            {"_gte": {"patent_date": "2015-01-01"}}
        ]
    },
    "fields": [
        "patent_id",
        "patent_title",
        "patent_date",
        "assignees.assignee_organization",
        "patent_num_claims",
        "patent_num_times_cited_by_us_patents"
    ],
    "sort": [{"patent_date": "desc"}],
    "size": 200
}
```

### 2. Find Expiring Patents (Pre-2010)

```python
{
    "query": {
        "_and": [
            {"_text_any": {"patent_title": "respiratory treatment"}},
            {"_gte": {"patent_date": "2000-01-01"}},
            {"_lt": {"patent_date": "2010-01-01"}}
        ]
    },
    "sort": [{"patent_date": "asc"}]
}
```

### 3. Innovation Analysis - Recent High-Impact Patents

```python
{
    "query": {
        "_and": [
            {"_text_any": {"patent_abstract": "novel drug delivery"}},
            {"_gte": {"patent_date": "2020-01-01"}},
            {"_gte": {"patent_num_times_cited_by_us_patents": 10}}
        ]
    },
    "sort": [{"patent_num_times_cited_by_us_patents": "desc"}],
    "size": 50
}
```

## Available Endpoints

- `patent` (default): Patent data
- `inventor`: Inventor information
- `assignee`: Patent assignee/owner data
- `cpc_subsection`: Cooperative Patent Classification
- `uspc`: US Patent Classification
- `location`: Geographic data
- `citation`: Patent citation data

## Common Fields Available

- `patent_id`, `patent_number`
- `patent_title`, `patent_abstract`
- `patent_date`, `patent_type`
- `patent_num_claims`
- `patent_num_times_cited_by_us_patents`
- `inventors.inventor_name_last`, `inventors.inventor_name_first`
- `assignees.assignee_organization`
- `cpcs.cpc_group_title`
- And many more...
