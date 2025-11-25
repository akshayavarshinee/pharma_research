"""
Test script for PatentsView API Tool with keyword search examples.
Run this to verify the tool works correctly with your API key.
"""

from src.pharma_researcher.tools.PatentsViewTool import PatentsViewTool
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the tool
tool = PatentsViewTool()

print("=" * 80)
print("PatentsView API Tool - Keyword Search Examples")
print("=" * 80)

# Example 1: Search for patents with ANY of the keywords
print("\n1. Searching for patents with 'cancer treatment' (ANY keyword match)...")
query1 = {
    "_text_any": {
        "patent_abstract": "cancer treatment"
    }
}

result1 = tool._run(
    query=query1,
    fields=["patent_id", "patent_title", "patent_abstract", "patent_date"],
    size=5  # Get only 5 results for testing
)

if "error" in result1:
    print(f"   ERROR: {result1['error']}")
    if "details" in result1:
        print(f"   Details: {result1['details']}")
else:
    print(f"   ✓ Found {result1.get('_query_metadata', {}).get('total_results', 0)} total patents")
    print(f"   ✓ Returned {result1.get('_query_metadata', {}).get('results_returned', 0)} results")
    
    # Show first result
    patents = result1.get('patents', [])
    if patents:
        print(f"\n   First result:")
        print(f"   - Patent ID: {patents[0].get('patent_id')}")
        print(f"   - Title: {patents[0].get('patent_title', 'N/A')[:100]}...")
        print(f"   - Date: {patents[0].get('patent_date')}")

# Example 2: Search for exact phrase
print("\n2. Searching for exact phrase 'immunotherapy' in title...")
query2 = {
    "_text_phrase": {
        "patent_title": "immunotherapy"
    }
}

result2 = tool._run(
    query=query2,
    fields=["patent_id", "patent_title", "patent_date"],
    size=5
)

if "error" in result2:
    print(f"   ERROR: {result2['error']}")
else:
    print(f"   ✓ Found {result2.get('_query_metadata', {}).get('total_results', 0)} total patents")
    print(f"   ✓ Returned {result2.get('_query_metadata', {}).get('results_returned', 0)} results")

# Example 3: Search with ALL keywords and date filter
print("\n3. Searching for patents with ALL keywords 'drug delivery' since 2020...")
query3 = {
    "_and": [
        {"_text_all": {"patent_abstract": "drug delivery"}},
        {"_gte": {"patent_date": "2020-01-01"}}
    ]
}

result3 = tool._run(
    query=query3,
    fields=["patent_id", "patent_title", "patent_date"],
    size=5,
    sort=[{"patent_date": "desc"}]  # Sort by newest first
)

if "error" in result3:
    print(f"   ERROR: {result3['error']}")
else:
    print(f"   ✓ Found {result3.get('_query_metadata', {}).get('total_results', 0)} total patents")
    print(f"   ✓ Returned {result3.get('_query_metadata', {}).get('results_returned', 0)} results")

# Example 4: Search multiple fields
print("\n4. Searching for 'vaccine' in title OR abstract...")
query4 = {
    "_or": [
        {"_text_any": {"patent_title": "vaccine"}},
        {"_text_any": {"patent_abstract": "vaccine"}}
    ]
}

result4 = tool._run(
    query=query4,
    fields=["patent_id", "patent_title", "patent_date"],
    size=5
)

if "error" in result4:
    print(f"   ERROR: {result4['error']}")
else:
    print(f"   ✓ Found {result4.get('_query_metadata', {}).get('total_results', 0)} total patents")
    print(f"   ✓ Returned {result4.get('_query_metadata', {}).get('results_returned', 0)} results")

print("\n" + "=" * 80)
print("Test complete!")
print("=" * 80)
