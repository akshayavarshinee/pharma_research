# ChEMBL API Tool - Summary

## Overview

The ChEMBL API Tool provides access to the ChEMBL database, a comprehensive bioactivity database containing information on drug-like molecules, their targets, assays, and clinical data.

## Key Features

- **Molecule Search**: Find compounds by properties, structure, or keywords
- **Target Search**: Search for biological targets (proteins, cells, organisms)
- **Drug Information**: Access approved drug data, indications, warnings, and mechanisms
- **Chemical Structure Search**: Perform similarity and substructure searches
- **Bioactivity Data**: Retrieve assay and activity data
- **Multiple Formats**: Support for JSON, XML, YAML, SVG (images), and SDF (molecules)

## Available Resources

| Resource                 | Description                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `molecule`               | Molecule information, properties, and structural representations |
| `target`                 | Protein and non-protein targets                                  |
| `drug`                   | Approved drugs with patent and research information              |
| `drug_indication`        | Drug-disease relationships with references                       |
| `drug_warning`           | Safety warnings and withdrawal information                       |
| `assay`                  | Assay details from source documents                              |
| `activity`               | Activity values recorded in assays                               |
| `mechanism`              | Mechanism of action for approved drugs                           |
| `similarity`             | Molecule similarity search (requires SMILES)                     |
| `substructure`           | Molecule substructure search (requires SMILES)                   |
| `image`                  | Graphical representation of molecules                            |
| `biotherapeutic`         | Biotherapeutic molecules with HELM notation                      |
| `cell_line`              | Cell line information                                            |
| `tissue`                 | Tissue classification                                            |
| `organism`               | Organism classification                                          |
| `protein_classification` | Protein family classification                                    |
| `atc_class`              | WHO ATC classification for drugs                                 |
| `metabolism`             | Metabolic pathways with references                               |
| `binding_site`           | Target binding site definitions                                  |

## Filter Types

The tool supports various filter operators for precise queries:

| Filter Type                  | Description                           | Example                                               |
| ---------------------------- | ------------------------------------- | ----------------------------------------------------- |
| `exact` / `iexact`           | Exact match (case insensitive)        | `{'assay_type__exact': 'B'}`                          |
| `contains` / `icontains`     | Wild card search (case insensitive)   | `{'pref_name__contains': 'kinase'}`                   |
| `startswith` / `istartswith` | Starts with query (case insensitive)  | `{'pref_name__istartswith': 'serotonin'}`             |
| `endswith` / `iendswith`     | Ends with query (case insensitive)    | `{'pref_name__iendswith': 'nib'}`                     |
| `regex` / `iregex`           | Regular expression (case insensitive) | `{'pref_name__iregex': '(cdk1\|cdk2)'}`               |
| `gt` / `gte`                 | Greater than (or equal)               | `{'molecule_properties__full_mwt__gte': 100}`         |
| `lt` / `lte`                 | Less than (or equal)                  | `{'molecule_properties__alogp__lte': 5}`              |
| `range`                      | Within a range                        | `{'molecule_properties__full_mwt__range': '200,500'}` |
| `in`                         | Appears in list                       | `{'molecule_chembl_id__in': 'CHEMBL25,CHEMBL941'}`    |
| `isnull`                     | Field is null                         | `{'helm_notation__isnull': 'false'}`                  |

## Common Use Cases

### 1. Drug Discovery

- Find molecules with specific properties (MW, logP, etc.)
- Perform chemical similarity searches
- Identify drug targets and mechanisms

### 2. Clinical Research

- Get drug indications and contraindications
- Access safety warnings and adverse events
- Find clinical trial data

### 3. Target Validation

- Search for protein targets
- Get binding site information
- Find bioactivity data for specific targets

### 4. Chemical Analysis

- Substructure searches
- Similarity searches with Tanimoto cutoff
- Get molecular images and representations

## Pagination

ChEMBL API returns paginated results with metadata:

```json
{
  "page_meta": {
    "limit": 20,
    "next": "/chembl/api/data/activity.json?limit=20&offset=20",
    "offset": 0,
    "previous": null,
    "total_count": 13520737
  }
}
```

Use `limit` and `offset` parameters to navigate through results.

## Response Formats

- **JSON** (default): Structured data
- **XML**: XML representation
- **YAML**: YAML format
- **SVG**: Molecule images (image resource only)
- **SDF**: Structure-data file (molecule resource only)

## Important Notes

1. **Chemical Searches**: SMILES strings must be URL-encoded for GET requests
2. **ChEMBL IDs**: Use format like `CHEMBL25` for aspirin
3. **Rate Limiting**: Be mindful of API rate limits
4. **InChI Keys**: Only works for molecules already in ChEMBL database
5. **Pagination**: Default limit is 20, use offset for subsequent pages

## Related Resources

- ChEMBL Website: https://www.ebi.ac.uk/chembl/
- API Documentation: https://chembl.gitbook.io/chembl-interface-documentation/web-services
- ChEMBL Blog: https://chembl.blogspot.com/
