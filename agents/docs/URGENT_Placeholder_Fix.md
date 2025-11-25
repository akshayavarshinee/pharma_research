# URGENT FIX: Agent Using Literal Placeholders

## Problem

The agent is literally using `"[drug name from query]"` instead of extracting actual drug names from the user's query.

## Root Cause

The task descriptions use bracket notation like `[drug name from query]` which the agent interprets as literal text to copy, not as instructions to extract values.

## Quick Fix

Replace the `market_insights_task` description section in `tasks.yaml` with this clearer version:

```yaml
market_insights_task:
  description: >
    Research "{query}" using real API data only.

    STEP 1: Extract from the query:
    - Drug/product names (e.g., if query says "Ozempic", extract "Ozempic")
    - Generic names (e.g., if query says "semaglutide", extract "semaglutide")  
    - Disease/condition (e.g., if query says "diabetes", extract "diabetes")

    STEP 2: Call tools with ACTUAL values from Step 1:

    fda_drugsfda_tool examples:
    - If query mentions "Ozempic": brand_name="Ozempic"
    - If query mentions "semaglutide": generic_name="semaglutide"
    - Always add: fields=["products.brand_name", "products.indication", "sponsor_name"]

    fda_adverse_events_tool examples:
    - If drug is "Ozempic": search_query='patient.drug.medicinalproduct:"ozempic"'
    - Add: count="patient.reaction.reactionmeddrapt.exact", serious_only=True

    ema_medicines_tool examples:
    - If drug is "Ozempic": medicine_name="Ozempic"
    - If ingredient is "semaglutide": active_substance="semaglutide"

    CRITICAL RULES:
    - Use ACTUAL drug/disease names from the user's query
    - DO NOT use placeholder text like "[drug name]" in tool calls
    - If tool returns no data, state "No data found" - don't fabricate
    - Cite source for all data: "Source: FDA Drugs@FDA API"
```

## Same Fix Needed For Other Tasks

Apply similar fixes to:

- `patent_landscape_task` - Remove `[disease/drug keywords from query]`
- `clinical_trials_pipeline_task` - Remove `[disease from query]`, `[drug/treatment if specified]`
- `web_intelligence_scan_task` - Remove `[keywords from query]`

## Pattern to Follow

**BAD** (agent copies literally):

```yaml
brand_name="[drug name from query]"
```

**GOOD** (agent understands to extract):

```yaml
If query mentions "Ozempic": brand_name="Ozempic"
If query mentions "semaglutide": generic_name="semaglutide"
```

## Alternative Simple Fix

Add this at the top of each task description:

```
IMPORTANT: When you see examples like "[drug name]", this means:
- Extract the actual drug name from the user's query
- Use that extracted value in your tool call
- DO NOT use the literal text "[drug name]"
```

This makes it explicit that brackets are placeholders, not literal values.
