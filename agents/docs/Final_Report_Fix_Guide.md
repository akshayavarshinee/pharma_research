# Final Report Issue - Quick Fix Guide

## Problem

The `generate_final_report_task` in `tasks.yaml` had a vague expected_output that asked for a "JSON-like structure", so the agent just returned JSON metadata instead of a full report.

## Solution

The tasks.yaml file got corrupted during editing. Here's the clean fix:

### Replace the `generate_final_report_task` section with:

```yaml
generate_final_report_task:
  description: >
    Create a comprehensive final report by COPYING and SYNTHESIZING content from all previous task outputs.

    DO NOT just list section names - include actual content from each file.

    Structure:
    1. Title page with report name and date
    2. Executive Summary - synthesize TOP findings from all sections (2-3 paragraphs)
    3. Copy full content from market_insights.md
    4. Copy full content from exim_trade_analysis.md
    5. Copy full content from patent_landscape.md
    6. Copy full content from clinical_trials.md
    7. Copy full content from internal_knowledge.md
    8. Copy full content from web_intelligence.md
    9. Strategic Recommendations based on data above
    10. Data sources summary table

    CRITICAL: Include ALL tables, data, and citations from input files. This is a REAL report, not metadata.

  expected_output: >
    A complete 10-20 page markdown report with:

    # [Report Title Based on Query]

    **Date**: {current_year}

    ## Executive Summary

    [Synthesize key findings - 3-5 bullet points with data]

    ## 1. Market Intelligence

    [FULL content from market_insights.md - all tables preserved]

    ## 2. Trade Analysis

    [FULL content from exim_trade_analysis.md]

    ## 3. Patent Landscape

    [FULL content from patent_landscape.md]

    ## 4. Clinical Trials

    [FULL content from clinical_trials.md]

    ## 5. Internal Knowledge

    [FULL content from internal_knowledge.md]

    ## 6. Web Intelligence

    [FULL content from web_intelligence.md]

    ## Strategic Recommendations

    ### Market Opportunities
    [Based on market + clinical data]

    ### Patent Strategy
    [Based on patent data]

    ### R&D Focus
    [Based on clinical trials]

    ### Supply Chain
    [Based on trade data]

    ## Data Sources Used

    | Area | Tools | Coverage |
    |------|-------|----------|
    | ... | ... | ... |

  agent: report_generation_agent
  output_file: output/final_report.md
  context:
    - market_insights_task
    - exim_trade_analysis_task
    - patent_landscape_task
    - clinical_trials_pipeline_task
    - internal_knowledge_summary_task
    - web_intelligence_scan_task
```

## Quick Manual Fix

If tasks.yaml is corrupted:

1. Open `src/pharma_researcher/config/tasks.yaml`
2. Find the `generate_final_report_task` section (near end of file)
3. Replace it with the YAML above
4. Make sure there are no duplicate task sections
5. Save the file

## Key Changes

**Before**:

- Asked for "JSON-like structure with file_path, file_name, metadata"
- Agent literally returned JSON instead of content

**After**:

- Explicitly says "COPY full content from each file"
- Says "This is a REAL report, not metadata"
- Shows example structure with actual sections
- Emphasizes "Include ALL tables and data"

This will make the report_generation_agent actually synthesize content instead of just returning file metadata.
