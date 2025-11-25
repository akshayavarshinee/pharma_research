# Open Targets Platform GraphQL API Tool - Usage Examples

## Target Queries

### 1. Get Basic Target Information

```python
from pharma_researcher.tools.OpenTargetsTool import open_targets_tool

# Get basic info for AR (Androgen Receptor)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='basic'
)
```

### 2. Get Target Tractability Assessment

```python
# Assess druggability of AR
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='tractability'
)
```

### 3. Get Genetic Constraint Data

```python
# Check if AR is under genetic constraint (essential gene)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='genetic_constraint'
)
```

### 4. Get Target Expression Data

```python
# Get baseline expression of AR across tissues
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='expression'
)
```

### 5. Get Diseases Associated with Target

```python
# Find diseases associated with AR
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='associated_diseases',
    page_size=20,
    page_index=0
)
```

### 6. Get Known Drugs for Target

```python
# Find drugs targeting AR
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='known_drugs',
    page_size=50
)
```

### 7. Validate BRCA1 as Cancer Target

```python
# BRCA1 (Breast Cancer 1)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000012048',
    query_type='associated_diseases',
    page_size=10
)
```

### 8. Check EGFR Tractability

```python
# EGFR (Epidermal Growth Factor Receptor)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000146648',
    query_type='tractability'
)
```

### 9. Get TP53 Genetic Constraint

```python
# TP53 (Tumor Protein P53)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000141510',
    query_type='genetic_constraint'
)
```

### 10. Find Drugs Targeting VEGFA

```python
# VEGFA (Vascular Endothelial Growth Factor A)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000112715',
    query_type='known_drugs',
    page_size=30
)
```

## Disease Queries

### 11. Get Basic Disease Information

```python
# Rheumatoid arthritis
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000685',
    query_type='basic'
)
```

### 12. Get Targets Associated with Disease

```python
# Find targets for rheumatoid arthritis
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000685',
    query_type='associated_targets',
    page_size=20,
    page_index=0
)
```

### 13. Get Known Drugs for Disease

```python
# Find drugs for rheumatoid arthritis
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000685',
    query_type='known_drugs',
    page_size=50
)
```

### 14. Find Targets for Type 2 Diabetes

```python
# Type 2 diabetes mellitus
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0001360',
    query_type='associated_targets',
    page_size=30
)
```

### 15. Get Alzheimer's Disease Information

```python
# Alzheimer's disease
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000249',
    query_type='basic'
)
```

### 16. Find Drugs for Breast Cancer

```python
# Breast carcinoma
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000305',
    query_type='known_drugs',
    page_size=100
)
```

### 17. Get Targets for Asthma

```python
# Asthma
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000270',
    query_type='associated_targets',
    page_size=25
)
```

### 18. Find Drugs for Parkinson's Disease

```python
# Parkinson's disease
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0002508',
    query_type='known_drugs',
    page_size=40
)
```

### 19. Get Targets for Crohn's Disease

```python
# Crohn's disease
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000384',
    query_type='associated_targets',
    page_size=20
)
```

### 20. Get Schizophrenia Information

```python
# Schizophrenia
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000692',
    query_type='basic'
)
```

## Drug Queries

### 21. Get Basic Drug Information

```python
# Aspirin
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL25',
    query_type='basic'
)
```

### 22. Get Drug Mechanisms of Action

```python
# Aspirin mechanisms
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL25',
    query_type='mechanisms'
)
```

### 23. Get Drug Adverse Events

```python
# Aspirin adverse events
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL25',
    query_type='pharmacovigilance'
)
```

### 24. Get Imatinib Information

```python
# Imatinib (cancer drug)
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL941',
    query_type='basic'
)
```

### 25. Get Imatinib Mechanisms

```python
# Imatinib mechanisms of action
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL941',
    query_type='mechanisms'
)
```

### 26. Get Metformin Information

```python
# Metformin (diabetes drug)
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1431',
    query_type='basic'
)
```

### 27. Get Adalimumab Mechanisms

```python
# Adalimumab (Humira - antibody drug)
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1201583',
    query_type='mechanisms'
)
```

### 28. Get Pembrolizumab Information

```python
# Pembrolizumab (Keytruda - cancer immunotherapy)
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL3301610',
    query_type='basic'
)
```

### 29. Get Warfarin Adverse Events

```python
# Warfarin (anticoagulant)
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1464',
    query_type='pharmacovigilance'
)
```

### 30. Get Atorvastatin Mechanisms

```python
# Atorvastatin (Lipitor - statin)
result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1487',
    query_type='mechanisms'
)
```

## Search Queries

### 31. Search for Breast Cancer

```python
# Search all entities related to breast cancer
result = open_targets_tool._run(
    endpoint='search',
    search_query='breast cancer',
    page_size=20,
    page_index=0
)
```

### 32. Search for EGFR

```python
# Search for EGFR target
result = open_targets_tool._run(
    endpoint='search',
    search_query='EGFR',
    page_size=10
)
```

### 33. Search for Kinase Inhibitors

```python
# Search for kinase inhibitors
result = open_targets_tool._run(
    endpoint='search',
    search_query='kinase inhibitor',
    page_size=30
)
```

### 34. Search for Diabetes

```python
# Search for diabetes-related entities
result = open_targets_tool._run(
    endpoint='search',
    search_query='diabetes',
    page_size=25
)
```

### 35. Search for Immunotherapy

```python
# Search for immunotherapy drugs
result = open_targets_tool._run(
    endpoint='search',
    search_query='immunotherapy',
    page_size=20
)
```

## Custom Queries

### 36. Custom Query for Target with Specific Fields

```python
custom_query = """
query target($ensemblId: String!) {
    target(ensemblId: $ensemblId) {
        id
        approvedSymbol
        approvedName
        biotype
        tractability {
            label
            modality
            value
        }
        geneticConstraint {
            constraintType
            score
        }
    }
}
"""

result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000169083',
    query_type='custom',
    custom_query=custom_query
)
```

### 37. Custom Query for Disease with Therapeutic Areas

```python
custom_query = """
query disease($efoId: String!) {
    disease(efoId: $efoId) {
        id
        name
        description
        therapeuticAreas {
            id
            name
        }
        synonyms {
            terms
        }
    }
}
"""

result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000685',
    query_type='custom',
    custom_query=custom_query
)
```

### 38. Custom Query for Drug with Indications

```python
custom_query = """
query drug($chemblId: String!) {
    drug(chemblId: $chemblId) {
        id
        name
        drugType
        maximumClinicalTrialPhase
        indications {
            rows {
                disease {
                    id
                    name
                }
                maxPhaseForIndication
            }
        }
    }
}
"""

result = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL25',
    query_type='custom',
    custom_query=custom_query
)
```

## Pagination Examples

### 39. Get First Page of Target-Disease Associations

```python
# Get first 10 diseases associated with BRCA1
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000012048',
    query_type='associated_diseases',
    page_size=10,
    page_index=0
)
```

### 40. Get Second Page of Results

```python
# Get next 10 diseases (page 2)
result = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000012048',
    query_type='associated_diseases',
    page_size=10,
    page_index=1
)
```

### 41. Get Large Result Set

```python
# Get 100 targets associated with cancer
result = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000305',  # Breast carcinoma
    query_type='associated_targets',
    page_size=100,
    page_index=0
)
```

## Practical Workflows

### 42. Target Validation Workflow

```python
# Step 1: Get basic target info
target_info = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000146648',  # EGFR
    query_type='basic'
)

# Step 2: Check tractability
tractability = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000146648',
    query_type='tractability'
)

# Step 3: Get disease associations
diseases = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000146648',
    query_type='associated_diseases',
    page_size=20
)

# Step 4: Find existing drugs
drugs = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000146648',
    query_type='known_drugs',
    page_size=30
)
```

### 43. Drug Repurposing Workflow

```python
# Step 1: Find targets for disease
targets = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0000685',  # Rheumatoid arthritis
    query_type='associated_targets',
    page_size=50
)

# Step 2: For top target, find known drugs
drugs = open_targets_tool._run(
    endpoint='target',
    entity_id='ENSG00000164308',  # Example target from results
    query_type='known_drugs',
    page_size=50
)

# Step 3: Check drug mechanisms
mechanisms = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1201583',  # Example drug from results
    query_type='mechanisms'
)
```

### 44. Competitive Intelligence Workflow

```python
# Step 1: Search for disease area
search_results = open_targets_tool._run(
    endpoint='search',
    search_query='lung cancer',
    page_size=30
)

# Step 2: Get known drugs for disease
drugs = open_targets_tool._run(
    endpoint='disease',
    entity_id='EFO_0001071',  # Lung carcinoma
    query_type='known_drugs',
    page_size=100
)

# Step 3: Check specific drug details
drug_info = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1201862',  # Example drug
    query_type='basic'
)
```

### 45. Safety Assessment Workflow

```python
# Step 1: Get drug info
drug_info = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1464',  # Warfarin
    query_type='basic'
)

# Step 2: Check adverse events
adverse_events = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1464',
    query_type='pharmacovigilance'
)

# Step 3: Get mechanisms to understand risks
mechanisms = open_targets_tool._run(
    endpoint='drug',
    entity_id='CHEMBL1464',
    query_type='mechanisms'
)
```

## Common Gene/Disease IDs

### Popular Target Ensembl IDs

```python
targets = {
    'AR': 'ENSG00000169083',      # Androgen Receptor
    'BRCA1': 'ENSG00000012048',    # Breast Cancer 1
    'EGFR': 'ENSG00000146648',     # Epidermal Growth Factor Receptor
    'TP53': 'ENSG00000141510',     # Tumor Protein P53
    'VEGFA': 'ENSG00000112715',    # Vascular Endothelial Growth Factor A
    'TNF': 'ENSG00000232810',      # Tumor Necrosis Factor
    'IL6': 'ENSG00000136244',      # Interleukin 6
    'BRAF': 'ENSG00000157764',     # B-Raf Proto-Oncogene
    'ALK': 'ENSG00000171094',      # Anaplastic Lymphoma Kinase
    'KRAS': 'ENSG00000133703'      # KRAS Proto-Oncogene
}
```

### Popular Disease EFO IDs

```python
diseases = {
    'Rheumatoid Arthritis': 'EFO_0000685',
    'Type 2 Diabetes': 'EFO_0001360',
    'Alzheimer Disease': 'EFO_0000249',
    'Breast Carcinoma': 'EFO_0000305',
    'Asthma': 'EFO_0000270',
    'Parkinson Disease': 'EFO_0002508',
    'Crohn Disease': 'EFO_0000384',
    'Schizophrenia': 'EFO_0000692',
    'Lung Carcinoma': 'EFO_0001071',
    'Coronary Heart Disease': 'EFO_0001645'
}
```

### Popular Drug ChEMBL IDs

```python
drugs = {
    'Aspirin': 'CHEMBL25',
    'Imatinib': 'CHEMBL941',
    'Metformin': 'CHEMBL1431',
    'Adalimumab': 'CHEMBL1201583',
    'Pembrolizumab': 'CHEMBL3301610',
    'Warfarin': 'CHEMBL1464',
    'Atorvastatin': 'CHEMBL1487',
    'Trastuzumab': 'CHEMBL1201585',
    'Bevacizumab': 'CHEMBL1201580',
    'Rituximab': 'CHEMBL1201572'
}
```

## Notes

- All queries return data in the `data` field of the response
- Use `_query_metadata` to see the actual GraphQL query and variables used
- For custom queries, refer to the [GraphQL Playground](https://platform.opentargets.org/api) for schema documentation
- Pagination is 0-indexed (first page is `page_index=0`)
- Evidence scores range from 0 to 1 (higher is stronger evidence)
- Clinical trial phases: 0 (preclinical), 1, 2, 3, 4 (approved)
