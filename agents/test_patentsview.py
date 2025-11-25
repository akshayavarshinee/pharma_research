"""
Quick test script for PatentsViewTool
Run with: python test_patentsview.py
"""

from src.pharma_researcher.tools.PatentsViewTool import PatentsViewTool

def test_basic_search():
    """Test basic patent search"""
    tool = PatentsViewTool()
    
    print("=" * 80)
    print("Test 1: Search for a specific patent")
    print("=" * 80)
    result = tool._run(
        query={"patent_id": "7861317"}
    )
    print(f"Total results: {result.get('_query_metadata', {}).get('total_results', 'N/A')}")
    print(f"Status: {'✓ Success' if 'error' not in result else '✗ Error'}")
    if 'error' in result:
        print(f"Error: {result['error']}")
    print()

def test_respiratory_patents():
    """Test searching respiratory disease patents"""
    tool = PatentsViewTool()
    
    print("=" * 80)
    print("Test 2: Search for respiratory disease patents (2020+)")
    print("=" * 80)
    result = tool._run(
        query={
            "_and": [
                {"_text_any": {"patent_abstract": "respiratory asthma COPD"}},
                {"_gte": {"patent_date": "2020-01-01"}}
            ]
        },
        fields=[
            "patent_id",
            "patent_title",
            "patent_date",
            "assignees.assignee_organization"
        ],
        size=5
    )
    
    print(f"Total results: {result.get('_query_metadata', {}).get('total_results', 'N/A')}")
    print(f"Results returned: {result.get('_query_metadata', {}).get('results_returned', 'N/A')}")
    print(f"Status: {'✓ Success' if 'error' not in result else '✗ Error'}")
    
    if 'error' not in result and 'patents' in result:
        print("\nFirst 3 patents:")
        for i, patent in enumerate(result['patents'][:3], 1):
            print(f"\n  {i}. Patent ID: {patent.get('patent_id')}")
            print(f"     Title: {patent.get('patent_title', 'N/A')[:80]}...")
            print(f"     Date: {patent.get('patent_date')}")
    elif 'error' in result:
        print(f"Error: {result['error']}")
    print()

def test_date_range():
    """Test date range query"""
    tool = PatentsViewTool()
    
    print("=" * 80)
    print("Test 3: Patents in specific date range (2023)")
    print("=" * 80)
    result = tool._run(
        query={
            "_and": [
                {"_gte": {"patent_date": "2023-01-01"}},
                {"_lte": {"patent_date": "2023-12-31"}},
                {"_text_any": {"patent_title": "pharmaceutical"}}
            ]
        },
        size=3
    )
    
    print(f"Total results: {result.get('_query_metadata', {}).get('total_results', 'N/A')}")
    print(f"Status: {'✓ Success' if 'error' not in result else '✗ Error'}")
    if 'error' in result:
        print(f"Error: {result['error']}")
    print()

if __name__ == "__main__":
    print("\n🔬 Testing PatentsView API Tool\n")
    
    try:
        test_basic_search()
        test_respiratory_patents()
        test_date_range()
        
        print("=" * 80)
        print("✓ All tests completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
