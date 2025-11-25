# EXIMTool - UN Comtrade API Integration

## Overview

The **EXIMTool** provides access to the UN Comtrade API for querying international trade statistics, with a focus on pharmaceutical products and Active Pharmaceutical Ingredients (APIs).

## Features

### Comprehensive Parameters

- **hs_code** - Harmonized System code (pharmaceutical specific codes included)
- **reporter_code** - Country reporting the data (default: India)
- **partner_code** - Trade partner country (optional)
- **year** - Year for trade data (2010-2023)
- **flow_code** - Trade direction (Imports "M", Exports "X", or both)
- **frequency** - Annual or Monthly data
- **max_records** - Result limit

### Common Pharmaceutical HS Codes

- `3004` - Medicaments (pharmaceutical formulations)
- `2941` - Antibiotics
- `3002` - Blood fractions and immunological products
- `3003` - Medicaments with 2+ constituents
- `300390` - Medicaments containing hormones

### Automatic Features

- **Summary Statistics** - Total trade value, quantity, number of partners
- **Top Partners Analysis** - Top 5 trading partners by value
- **Country Name Mapping** - Converts country codes to names
- **Flow Descriptions** - Human-readable trade directions

## Usage Examples

### India's Pharmaceutical Exports

```python
{
    "hs_code": "3004",
    "reporter_code": "356",  # India
    "flow_code": "X",        # Exports
    "year": 2023
}
```

### India's Imports from China

```python
{
    "hs_code": "2941",       # Antibiotics
    "reporter_code": "356",  # India
    "partner_code": "156",   # China
    "flow_code": "M",        # Imports
    "year": 2023
}
```

### US Pharmaceutical Imports

```python
{
    "hs_code": "3004",
    "reporter_code": "840",  # USA
    "flow_code": "M",
    "year": 2023
}
```

### Bilateral Trade Analysis

```python
{
    "hs_code": "3004",
    "reporter_code": "356",  # India
    "partner_code": "840",   # USA
    "year": 2023
    # Returns both imports and exports
}
```

## Response Structure

```json
{
    "_query_metadata": {
        "hs_code": "3004",
        "reporter_code": "356",
        "reporter_desc": "India",
        "partner_code": "840",
        "partner_desc": "United States",
        "year": 2023,
        "flow_code": "X",
        "flow_desc": "Exports",
        "records_returned": 12
    },
    "_summary": {
        "total_trade_value_usd": 5234567890,
        "total_quantity": 123456789,
        "number_of_partners": 45,
        "top_partners": [
            {"partner": "United States", "trade_value_usd": 1234567890},
            {"partner": "Germany", "trade_value_usd": 987654321}
        ]
    },
    "data": [
        {
            "partnerCode": "840",
            "partnerDesc": "United States",
            "primaryValue": 1234567890,
            "qty": 12345678,
            "flowCode": "X",
            ...
        }
    ]
}
```

## Common Country Codes

| Code | Country        |
| ---- | -------------- |
| 356  | India          |
| 840  | United States  |
| 156  | China          |
| 276  | Germany        |
| 826  | United Kingdom |
| 392  | Japan          |
| 124  | Canada         |
| 702  | Singapore      |

## Use Cases for Pharma Research

1. **Sourcing Dependencies** - Identify which countries India depends on for API imports
2. **Export Markets** - Find top destinations for Indian pharmaceutical exports
3. **Competitive Analysis** - Compare trade volumes across countries
4. **Supply Chain Risk** - Detect concentration of imports from single sources
5. **Market Opportunities** - Identify growing export markets
6. **Trade Corridor Analysis** - Analyze bilateral pharmaceutical trade flows

## Integration

The tool is integrated into the `exim_trends_agent` and can be used directly:

```python
from pharma_researcher.tools.EXIMTool import EXIMTool

tool = EXIMTool()
result = tool._run(
    hs_code="3004",
    reporter_code="356",
    flow_code="X",
    year=2023
)
```

## Error Handling

The tool includes comprehensive error handling:

- API connection errors
- Invalid HS codes
- Missing data for specific years
- Rate limiting responses

All errors return structured messages with request details for debugging.
