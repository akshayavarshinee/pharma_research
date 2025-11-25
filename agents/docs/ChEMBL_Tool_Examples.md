# ChEMBL API Tool - Usage Examples

## Basic Queries

### 1. Get All Molecules (with pagination)

```python
from pharma_researcher.tools.ChEMBLTool import chembl_tool

result = chembl_tool._run(
    resource='molecule',
    limit=20,
    offset=0
)
```

### 2. Get Specific Molecule by ChEMBL ID

```python
# Get aspirin (CHEMBL25)
result = chembl_tool._run(
    resource='molecule',
    chembl_id='CHEMBL25'
)
```

### 3. Get Molecule Image

```python
# Get SVG image of aspirin
result = chembl_tool._run(
    resource='image',
    chembl_id='CHEMBL25',
    format='svg'
)
```

## Keyword Searches

### 4. Search Targets Containing 'Cyclin'

```python
result = chembl_tool._run(
    resource='target',
    filters={'pref_name__contains': 'cyclin'}
)
```

### 5. Full Text Search for 'Aspirin'

```python
result = chembl_tool._run(
    resource='molecule',
    search_query='aspirin'
)
```

### 6. Search Targets for 'Lipoxygenase'

```python
result = chembl_tool._run(
    resource='target',
    search_query='lipoxygenase'
)
```

## Property-Based Filtering

### 7. Find Molecules with Molecular Weight <= 300

```python
result = chembl_tool._run(
    resource='molecule',
    filters={'molecule_properties__mw_freebase__lte': 300}
)
```

### 8. Find Molecules with MW <= 300 AND Name Ending with 'nib'

```python
result = chembl_tool._run(
    resource='molecule',
    filters={
        'molecule_properties__mw_freebase__lte': 300,
        'pref_name__iendswith': 'nib'
    }
)
```

### 9. Find Molecules in a Molecular Weight Range

```python
result = chembl_tool._run(
    resource='molecule',
    filters={'molecule_properties__full_mwt__range': '200,500'}
)
```

### 10. Find Molecules with LogP <= 5

```python
result = chembl_tool._run(
    resource='molecule',
    filters={'molecule_properties__alogp__lte': 5}
)
```

## Chemical Structure Searches

### 11. Substructure Search with Aspirin SMILES

```python
result = chembl_tool._run(
    resource='substructure',
    smiles='CC(=O)Oc1ccccc1C(=O)O'
)
```

### 12. Substructure Search with ChEMBL ID

```python
result = chembl_tool._run(
    resource='substructure',
    chembl_id='CHEMBL25'  # Aspirin
)
```

### 13. Similarity Search (80% Cutoff) with SMILES

```python
result = chembl_tool._run(
    resource='similarity',
    smiles='CC(=O)Oc1ccccc1C(=O)O',
    similarity_cutoff=80
)
```

### 14. Similarity Search with ChEMBL ID

```python
result = chembl_tool._run(
    resource='similarity',
    chembl_id='CHEMBL25',
    similarity_cutoff=80
)
```

### 15. High Similarity Search (95% Cutoff)

```python
# Find very similar molecules
result = chembl_tool._run(
    resource='similarity',
    smiles='CN1C(=O)C=C(c2cccc(Cl)c2)c3cc(ccc13)[C@@](N)(c4ccc(Cl)cc4)c5cncn5C',
    similarity_cutoff=95
)
```

## Drug Information

### 16. Get All Approved Drugs

```python
result = chembl_tool._run(
    resource='drug',
    limit=50
)
```

### 17. Get Drug Indications for Specific Drug

```python
result = chembl_tool._run(
    resource='drug_indication',
    filters={'molecule_chembl_id': 'CHEMBL25'}
)
```

### 18. Get Drug Warnings

```python
result = chembl_tool._run(
    resource='drug_warning',
    limit=20
)
```

### 19. Get Drug Mechanism of Action

```python
result = chembl_tool._run(
    resource='mechanism',
    filters={'molecule_chembl_id': 'CHEMBL25'}
)
```

## Target and Assay Queries

### 20. Search Targets Starting with 'Serotonin'

```python
result = chembl_tool._run(
    resource='target',
    filters={'pref_name__istartswith': 'serotonin'}
)
```

### 21. Get Assays by Type

```python
result = chembl_tool._run(
    resource='assay',
    filters={'assay_type__exact': 'B'}  # Binding assay
)
```

### 22. Search Assays with 'Toxicity' in Description

```python
result = chembl_tool._run(
    resource='assay',
    filters={'description__icontains': 'toxicity'}
)
```

### 23. Get Protein Classification

```python
result = chembl_tool._run(
    resource='protein_classification',
    limit=50
)
```

## Activity Data

### 24. Get Activity Data for Specific Targets

```python
result = chembl_tool._run(
    resource='activity',
    filters={
        'target_chembl_id__in': 'CHEMBL5552,CHEMBL1075195',
        'pchembl_value__gte': 5,
        'assay_type': 'B'
    },
    only=['molecule_chembl_id', 'pchembl_value']
)
```

### 25. Get High-Quality Activity Data

```python
result = chembl_tool._run(
    resource='activity',
    filters={
        'pchembl_value__gte': 7,  # High potency
        'assay_type': 'B'
    },
    limit=100
)
```

## Advanced Filtering

### 26. Multiple Molecules by ChEMBL IDs

```python
result = chembl_tool._run(
    resource='molecule',
    filters={'molecule_chembl_id__in': 'CHEMBL25,CHEMBL941,CHEMBL1000'}
)
```

### 27. Regex Search for Targets

```python
result = chembl_tool._run(
    resource='target',
    filters={'pref_name__iregex': '(cdk1|cdk2)'}
)
```

### 28. Find Molecules with Non-Null HELM Notation

```python
result = chembl_tool._run(
    resource='molecule',
    filters={'helm_notation__isnull': 'false'}
)
```

## Ordering and Field Selection

### 29. Order Targets by Name (Ascending)

```python
result = chembl_tool._run(
    resource='target',
    filters={'pref_name__contains': 'kinase'},
    order_by='pref_name'
)
```

### 30. Order Targets by Name (Descending)

```python
result = chembl_tool._run(
    resource='target',
    filters={'pref_name__contains': 'kinase'},
    order_by='-pref_name'
)
```

### 31. Select Specific Fields Only

```python
result = chembl_tool._run(
    resource='molecule',
    filters={'molecule_properties__mw_freebase__lte': 300},
    only=['molecule_chembl_id', 'pref_name', 'molecule_properties']
)
```

## Specialized Resources

### 32. Get Cell Line Information

```python
result = chembl_tool._run(
    resource='cell_line',
    filters={'cell_source_tissue__iendswith': 'carcinoma'}
)
```

### 33. Get Biotherapeutic Molecules

```python
result = chembl_tool._run(
    resource='biotherapeutic',
    limit=20
)
```

### 34. Get Metabolism Pathways

```python
result = chembl_tool._run(
    resource='metabolism',
    filters={'molecule_chembl_id': 'CHEMBL25'}
)
```

### 35. Get Binding Site Information

```python
result = chembl_tool._run(
    resource='binding_site',
    limit=20
)
```

### 36. Get ATC Classification

```python
result = chembl_tool._run(
    resource='atc_class',
    limit=50
)
```

### 37. Get Tissue Classification

```python
result = chembl_tool._run(
    resource='tissue',
    limit=50
)
```

### 38. Get Organism Information

```python
result = chembl_tool._run(
    resource='organism',
    limit=50
)
```

## Pagination Examples

### 39. Get First Page of Results

```python
result = chembl_tool._run(
    resource='molecule',
    limit=20,
    offset=0
)
```

### 40. Get Second Page of Results

```python
result = chembl_tool._run(
    resource='molecule',
    limit=20,
    offset=20
)
```

### 41. Get Large Dataset

```python
# Get 100 results starting from position 500
result = chembl_tool._run(
    resource='activity',
    limit=100,
    offset=500
)
```

## Different Output Formats

### 42. Get Molecule in SDF Format

```python
result = chembl_tool._run(
    resource='molecule',
    chembl_id='CHEMBL25',
    format='sdf'
)
```

### 43. Get Data in XML Format

```python
result = chembl_tool._run(
    resource='target',
    filters={'pref_name__contains': 'kinase'},
    format='xml'
)
```

### 44. Get Data in YAML Format

```python
result = chembl_tool._run(
    resource='molecule',
    chembl_id='CHEMBL25',
    format='yaml'
)
```

## API Status

### 45. Check API Status

```python
result = chembl_tool._run(
    resource='status'
)
# Returns ChEMBL DB version and API version
```

## Complex Queries

### 46. Find Kinase Inhibitors with Specific Properties

```python
result = chembl_tool._run(
    resource='molecule',
    filters={
        'pref_name__icontains': 'kinase',
        'molecule_properties__mw_freebase__range': '300,600',
        'molecule_properties__alogp__lte': 5
    },
    order_by='-molecule_properties__mw_freebase',
    limit=50
)
```

### 47. Find Recent Drug Approvals

```python
result = chembl_tool._run(
    resource='drug',
    order_by='-first_approval',
    limit=20
)
```

### 48. Search for Cancer-Related Targets

```python
result = chembl_tool._run(
    resource='target',
    search_query='cancer',
    limit=50
)
```

### 49. Find Small Molecule Drugs

```python
result = chembl_tool._run(
    resource='molecule',
    filters={
        'molecule_properties__mw_freebase__lte': 500,
        'molecule_properties__num_ro5_violations': 0
    },
    limit=100
)
```

### 50. Get Document Information

```python
result = chembl_tool._run(
    resource='document',
    filters={'journal__icontains': 'nature'},
    limit=20
)
```

## Notes

- All SMILES strings are automatically URL-encoded
- ChEMBL IDs should be in format `CHEMBL` followed by numbers (e.g., `CHEMBL25`)
- Use `limit` and `offset` for pagination through large result sets
- The `only` parameter helps reduce response size by selecting specific fields
- Chemical searches (similarity/substructure) require valid SMILES or ChEMBL IDs
- Default format is JSON; use `format` parameter for other formats
