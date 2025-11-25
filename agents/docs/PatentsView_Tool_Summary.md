# PatentsView API Tool - Summary

## ✅ What Was Created

### 1. **PatentsViewTool.py**

Location: `src/pharma_researcher/tools/PatentsViewTool.py`

A comprehensive CrewAI tool that interfaces with the PatentsView API (https://search.patentsview.org/api/v1/).

**Features:**

- ✅ All query operators (equals, comparison, negation, text search)
- ✅ Complex query building with `_and`, `_or` operators
- ✅ Value arrays for multiple criteria
- ✅ Full-text search (`_text_all`, `_text_any`, `_text_phrase`)
- ✅ Field selection (choose exactly which data to return)
- ✅ Sorting (single or multi-field)
- ✅ Pagination with cursor support
- ✅ Options (exclude_withdrawn, pad_patent_id)
- ✅ Support for all endpoints (patent, inventor, assignee, etc.)
- ✅ Helpful metadata in responses
- ✅ Comprehensive error handling

### 2. **Integration with Crew**

- Imported `PatentsViewTool` in `crew.py`
- Added to `patent_landscape_agent` tools list
- Updated agent backstory to mention PatentsView API access

### 3. **Documentation**

- **Usage Guide**: `docs/PatentsView_Tool_Examples.md` with 25+ examples
- **Test Script**: `test_patentsview.py` for quick verification

## 🎯 How to Use

### Basic Query

```python
{
    "query": {"patent_id": "7861317"}
}
```

### Pharmaceutical Research Query

```python
{
    "query": {
        "_and": [
            {"_text_any": {"patent_abstract": "respiratory COPD asthma"}},
            {"_gte": {"patent_date": "2020-01-01"}},
            {"assignees.assignee_organization": ["AstraZeneca", "GSK"]}
        ]
    },
    "fields": ["patent_id", "patent_title", "patent_date", "assignees.assignee_organization"],
    "sort": [{"patent_num_times_cited_by_us_patents": "desc"}],
    "size": 50
}
```

## 🚀 Testing

Run the test script:

```bash
cd d:\vscode\coe_intern\pharma_research\pharma_researcher
python test_patentsview.py
```

## 📊 What the Agent Can Now Do

The `patent_landscape_agent` can now:

1. Search US patents by molecule name, indication, or keyword
2. Find patents by company (assignee) or inventor
3. Filter by date ranges to identify expiring patents
4. Analyze competitive patent landscapes
5. Track patent citations and impact
6. Identify Freedom-to-Operate (FTO) risks
7. Generate patent filing trend analysis

## 🔗 API Endpoints Available

- `patent` (default) - Patent data
- `inventor` - Inventor information
- `assignee` - Company/organization data
- `citation` - Patent citation data
- `cpc_subsection` - Patent classifications
- And more...

## 📝 Common Use Cases for Pharma Research

1. **Competitive Intelligence**: Find all patents by competitors for a specific drug class
2. **FTO Analysis**: Identify active patents that might block new drug development
3. **Expiry Tracking**: Find patents expiring soon for generic opportunities
4. **Innovation Monitoring**: Track recent high-impact patents in therapeutic areas
5. **Technology Trends**: Analyze patent filing patterns over time

## ✨ Next Steps

The tool is fully integrated and ready to use. The `patent_landscape_agent` will automatically use it when executing patent research tasks.

For your original multi-model setup:

- ✅ `master_agent` now uses GPT-4o-mini
- ✅ All other agents use ollama/deepseek-r1:latest
- ✅ Sequential process eliminates delegation errors
