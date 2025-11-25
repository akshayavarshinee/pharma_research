# Open Targets Drug Indication Tool - Usage Examples

## Basic Drug Queries

### 1. Get All Indications for Aspirin

```python
from pharma_researcher.tools.OpenTargetsDrugIndicationTool import open_targets_drug_indication_tool

# Get all indications for aspirin
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25'
)
```

### 2. Get Approved Indications Only

```python
# Get only approved indications for aspirin
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    approved_only=True
)
```

### 3. Get Indications in Clinical Trials

```python
# Get indications in phase 2 or higher
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    min_phase=2
)
```

### 4. Get Late-Stage Clinical Trials

```python
# Get indications in phase 3 or approved
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    min_phase=3
)
```

### 5. Check Specific Drug-Disease Pair

```python
# Check if aspirin is approved for myocardial infarction
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    disease_id='EFO_0000612'  # Myocardial infarction
)
```

## Cancer Drug Examples

### 6. Get Imatinib Indications

```python
# Imatinib (Gleevec) - cancer drug
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL941'
)
```

### 7. Get Pembrolizumab Approved Indications

```python
# Pembrolizumab (Keytruda) - immunotherapy
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL3301610',
    approved_only=True
)
```

### 8. Get Trastuzumab Indications

```python
# Trastuzumab (Herceptin) - breast cancer antibody
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201585'
)
```

### 9. Get Bevacizumab Clinical Trials

```python
# Bevacizumab (Avastin) - VEGF inhibitor
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201580',
    min_phase=2
)
```

### 10. Get Nivolumab Indications

```python
# Nivolumab (Opdivo) - PD-1 inhibitor
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL3301637'
)
```

## Antibody Drug Examples

### 11. Get Adalimumab Indications

```python
# Adalimumab (Humira) - TNF inhibitor
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201583'
)
```

### 12. Get Rituximab Approved Uses

```python
# Rituximab (Rituxan) - CD20 antibody
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201572',
    approved_only=True
)
```

### 13. Get Infliximab Indications

```python
# Infliximab (Remicade) - TNF inhibitor
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201571'
)
```

## Small Molecule Drug Examples

### 14. Get Metformin Indications

```python
# Metformin - diabetes drug
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1431'
)
```

### 15. Get Atorvastatin Indications

```python
# Atorvastatin (Lipitor) - statin
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1487'
)
```

### 16. Get Warfarin Indications

```python
# Warfarin - anticoagulant
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1464'
)
```

### 17. Get Sildenafil Indications

```python
# Sildenafil (Viagra) - PDE5 inhibitor
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL192'
)
```

## Disease-Based Queries

### 18. Find All Drugs for Rheumatoid Arthritis

```python
# Get all drugs for rheumatoid arthritis
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000685'
)
```

### 19. Find Approved Drugs for Rheumatoid Arthritis

```python
# Get only approved drugs
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000685',
    approved_only=True
)
```

### 20. Find Drugs in Clinical Trials for Alzheimer's

```python
# Alzheimer's disease - drugs in phase 2+
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000249',
    min_phase=2
)
```

### 21. Find Approved Drugs for Type 2 Diabetes

```python
# Type 2 diabetes mellitus
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0001360',
    approved_only=True
)
```

### 22. Find Drugs for Breast Cancer

```python
# Breast carcinoma
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000305',
    limit=50
)
```

### 23. Find Approved Drugs for Asthma

```python
# Asthma
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000270',
    approved_only=True
)
```

### 24. Find Drugs for Parkinson's Disease

```python
# Parkinson's disease
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0002508'
)
```

### 25. Find Late-Stage Drugs for Crohn's Disease

```python
# Crohn's disease - phase 3+
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000384',
    min_phase=3
)
```

### 26. Find Drugs for Lung Cancer

```python
# Lung carcinoma
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0001071',
    limit=100
)
```

### 27. Find Approved Drugs for Hypertension

```python
# Hypertension
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000537',
    approved_only=True,
    limit=50
)
```

## Drug Repurposing Examples

### 28. Find Off-Label Uses for Metformin

```python
# Get all indications (approved and investigational)
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1431'  # Metformin
)
# Compare approved vs investigational indications
```

### 29. Find Repurposing Candidates for COVID-19

```python
# COVID-19 (if available in database)
result = open_targets_drug_indication_tool._run(
    disease_id='MONDO_0100096',
    min_phase=2
)
```

### 30. Find Aspirin Uses Beyond Pain

```python
# Get all aspirin indications
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25'
)
# Look for cardiovascular, cancer prevention, etc.
```

## Competitive Intelligence Examples

### 31. Compare TNF Inhibitors for Rheumatoid Arthritis

```python
# Adalimumab
adalimumab = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201583',
    disease_id='EFO_0000685'
)

# Infliximab
infliximab = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201571',
    disease_id='EFO_0000685'
)

# Compare phases and references
```

### 32. Find All PD-1/PD-L1 Inhibitors for Cancer

```python
# Search by disease and filter by mechanism
# Example: Lung cancer
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0001071',
    min_phase=3
)
# Then filter by mechanism of action in results
```

### 33. Track Clinical Progress for Specific Drug

```python
# Get all indications and check phases
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL3301610'  # Pembrolizumab
)
# Analyze maxPhaseForIndication for each disease
```

## Market Analysis Examples

### 34. Count Approved Drugs for Disease Area

```python
# Rheumatoid arthritis market
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000685',
    approved_only=True,
    limit=200
)
# Check approvedDrugCount in response
```

### 35. Identify Unmet Medical Needs

```python
# Find diseases with few approved drugs
# Example: Rare disease
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000508',  # Example rare disease
    approved_only=True
)
# Low count suggests unmet need
```

### 36. Find Drugs in Development Pipeline

```python
# Get drugs in clinical trials (not yet approved)
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000249',  # Alzheimer's
    min_phase=1
)
# Filter out phase 4 to see pipeline
```

## Regulatory Research Examples

### 37. Get FDA-Approved Indications

```python
# Get approved indications with references
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    approved_only=True
)
# Check references for FDA approval
```

### 38. Find Withdrawn Indications

```python
# Get drug info including withdrawal status
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1464'  # Warfarin
)
# Check drug.hasBeenWithdrawn in response
```

### 39. Track Approval Timeline

```python
# Get all indications and sort by phase
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201583'  # Adalimumab
)
# Analyze progression through phases
```

## Filtering and Limiting Examples

### 40. Get Top 10 Indications

```python
# Limit results to 10
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    limit=10
)
```

### 41. Get Only Phase 3 Trials

```python
# Exactly phase 3 (filter in application logic)
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL941',
    min_phase=3
)
# Then filter for maxPhaseForIndication == 3
```

### 42. Get Large Dataset

```python
# Get up to 200 drugs for disease
result = open_targets_drug_indication_tool._run(
    disease_id='EFO_0000305',  # Breast cancer
    limit=200
)
```

## Cross-Reference Examples

### 43. Validate Drug-Disease Association

```python
# Check if specific drug is used for disease
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201583',  # Adalimumab
    disease_id='EFO_0000685'   # Rheumatoid arthritis
)
# Should return phase 4 if approved
```

### 44. Find Common Indications Across Drugs

```python
# Get indications for multiple drugs
drug1 = open_targets_drug_indication_tool._run(drug_id='CHEMBL1201583')
drug2 = open_targets_drug_indication_tool._run(drug_id='CHEMBL1201571')
# Compare indication lists
```

### 45. Find Drugs with Multiple Indications

```python
# Get all indications
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25'  # Aspirin
)
# Check indicationCount in response
```

## Response Analysis Examples

### 46. Extract Approved Indications List

```python
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25',
    approved_only=True
)

# Access approved indication IDs
approved_ids = result.get('approvedIndications', [])
print(f"Approved for {len(approved_ids)} indications")
```

### 47. Get Reference Sources

```python
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL25'
)

# Extract references
for indication in result.get('indications', []):
    refs = indication.get('references', [])
    for ref in refs:
        print(f"Source: {ref.get('source')}, IDs: {ref.get('ids')}")
```

### 48. Compare Clinical Phases

```python
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL941'
)

# Analyze phase distribution
phases = {}
for ind in result.get('indications', []):
    phase = ind.get('maxPhaseForIndication', 0)
    phases[phase] = phases.get(phase, 0) + 1

print(f"Phase distribution: {phases}")
```

### 49. Find Highest Phase Indication

```python
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL3301610'
)

# Find max phase
max_phase = result.get('drug', {}).get('maximumClinicalTrialPhase', 0)
print(f"Highest phase reached: {max_phase}")
```

### 50. Generate Indication Summary

```python
result = open_targets_drug_indication_tool._run(
    drug_id='CHEMBL1201583'
)

# Summary
drug_name = result.get('drug', {}).get('name')
total = result.get('indicationCount', 0)
approved = result.get('approvedIndicationCount', 0)

print(f"{drug_name}:")
print(f"  Total indications: {total}")
print(f"  Approved indications: {approved}")
print(f"  Investigational: {total - approved}")
```

## Common Drug ChEMBL IDs

```python
common_drugs = {
    # Cancer drugs
    'Imatinib': 'CHEMBL941',
    'Pembrolizumab': 'CHEMBL3301610',
    'Nivolumab': 'CHEMBL3301637',
    'Trastuzumab': 'CHEMBL1201585',
    'Bevacizumab': 'CHEMBL1201580',

    # Antibody drugs
    'Adalimumab': 'CHEMBL1201583',
    'Rituximab': 'CHEMBL1201572',
    'Infliximab': 'CHEMBL1201571',

    # Small molecules
    'Aspirin': 'CHEMBL25',
    'Metformin': 'CHEMBL1431',
    'Atorvastatin': 'CHEMBL1487',
    'Warfarin': 'CHEMBL1464',
    'Sildenafil': 'CHEMBL192'
}
```

## Common Disease EFO IDs

```python
common_diseases = {
    'Rheumatoid Arthritis': 'EFO_0000685',
    'Type 2 Diabetes': 'EFO_0001360',
    'Alzheimer Disease': 'EFO_0000249',
    'Breast Carcinoma': 'EFO_0000305',
    'Asthma': 'EFO_0000270',
    'Parkinson Disease': 'EFO_0002508',
    'Crohn Disease': 'EFO_0000384',
    'Lung Carcinoma': 'EFO_0001071',
    'Hypertension': 'EFO_0000537',
    'Myocardial Infarction': 'EFO_0000612'
}
```

## Notes

- All queries return structured JSON responses
- Use `_query_metadata` to see query parameters and totals
- Clinical phases: 0=preclinical, 1-3=clinical trials, 4=approved
- Some drugs may have different phases for different indications
- References provide supporting evidence from FDA, EMA, etc.
- Limit parameter controls maximum results returned
