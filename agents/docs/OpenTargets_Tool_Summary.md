# Open Targets Platform GraphQL API Tool - Summary

## Overview

The Open Targets Platform GraphQL API Tool provides access to the Open Targets Platform, a comprehensive resource for finding potential drug targets and understanding target-disease associations. The platform integrates genetic, genomic, transcriptomic, and chemical data to provide evidence for target validation.

## Key Features

- **Target Discovery**: Find and validate potential drug targets
- **Disease Associations**: Get target-disease associations with evidence scores
- **Tractability Assessment**: Evaluate druggability of targets
- **Drug Information**: Access drug mechanisms, indications, and adverse events
- **Genetic Evidence**: Get genetic constraint and variant data
- **Expression Data**: Retrieve baseline expression across tissues
- **Search Functionality**: Search across all entities (targets, diseases, drugs, variants)

## Available Endpoints

| Endpoint      | Description                                   | Entity ID Format                          |
| ------------- | --------------------------------------------- | ----------------------------------------- |
| `target`      | Target annotation and associations            | Ensembl gene ID (e.g., `ENSG00000169083`) |
| `disease`     | Disease/phenotype annotation and associations | EFO ID (e.g., `EFO_0000685`)              |
| `drug`        | Drug/compound annotation and mechanisms       | ChEMBL ID (e.g., `CHEMBL1201583`)         |
| `variant`     | Variant annotation and consequences           | Variant ID (e.g., `rs7903146`)            |
| `studies`     | GWAS and other study information              | Study ID                                  |
| `credibleSet` | Credible sets from fine-mapping               | Credible set ID                           |
| `search`      | Search all entities                           | N/A (uses search query)                   |

## Query Types

### Target Endpoint

| Query Type            | Description                       | Returns                                                                       |
| --------------------- | --------------------------------- | ----------------------------------------------------------------------------- |
| `basic`               | General target information        | ID, symbol, name, biotype, genomic location, protein annotations              |
| `tractability`        | Druggability assessments          | Tractability scores for different modalities (small molecule, antibody, etc.) |
| `genetic_constraint`  | Genetic constraint data           | Constraint scores from gnomAD (pLI, LOEUF, etc.)                              |
| `expression`          | Baseline expression               | RNA and protein expression across tissues                                     |
| `associated_diseases` | Diseases associated with target   | Disease associations with evidence scores                                     |
| `known_drugs`         | Known drugs targeting this target | Drugs, indications, mechanisms, clinical phases                               |

### Disease Endpoint

| Query Type           | Description                     | Returns                                            |
| -------------------- | ------------------------------- | -------------------------------------------------- |
| `basic`              | General disease information     | ID, name, description, synonyms, therapeutic areas |
| `associated_targets` | Targets associated with disease | Target associations with evidence scores           |
| `known_drugs`        | Known drugs for this disease    | Drugs, targets, mechanisms, clinical phases        |

### Drug Endpoint

| Query Type          | Description              | Returns                                               |
| ------------------- | ------------------------ | ----------------------------------------------------- |
| `basic`             | General drug information | ID, name, type, max clinical phase, withdrawal status |
| `mechanisms`        | Mechanisms of action     | Mechanism descriptions, action types, targets         |
| `pharmacovigilance` | Adverse events           | Adverse event reports with statistical significance   |

### Search Endpoint

| Query Type | Description         | Returns                                                 |
| ---------- | ------------------- | ------------------------------------------------------- |
| `basic`    | Search all entities | Matching targets, diseases, drugs, variants with scores |

## Evidence Data Types

Open Targets integrates multiple evidence types for target-disease associations:

1. **Genetic Associations**: GWAS, rare variants, somatic mutations
2. **Literature**: Text mining from scientific publications
3. **Animal Models**: Mouse phenotype models
4. **RNA Expression**: Differential expression studies
5. **Pathways & Systems Biology**: Pathway analysis
6. **Drugs**: Known drug indications
7. **Somatic Mutations**: Cancer mutations

Each association has:

- **Overall Score**: Combined evidence score (0-1)
- **Datatype Scores**: Individual scores for each evidence type

## Tractability Assessment

Targets are assessed for tractability across different modalities:

### Small Molecule Tractability

- Clinical precedence
- Discovery precedence
- Predicted tractable (high confidence)
- Predicted tractable (medium-low confidence)

### Antibody Tractability

- Clinical precedence
- Predicted tractable (high confidence)
- Predicted tractable (medium-low confidence)

### Other Modalities

- PROTAC
- Molecular glue
- Other therapeutic modalities

## Genetic Constraint Metrics

From gnomAD database:

- **pLI**: Probability of being loss-of-function intolerant
- **LOEUF**: Loss-of-function observed/expected upper bound fraction
- **Missense Z-score**: Constraint against missense variation
- **Synonymous Z-score**: Constraint against synonymous variation

Higher constraint scores suggest the gene is essential and may be a good drug target.

## Use Cases

### 1. Target Validation

- Find genetic evidence linking target to disease
- Assess druggability with tractability scores
- Check if target is essential (genetic constraint)
- Review expression patterns

### 2. Drug Repurposing

- Find drugs with known mechanisms
- Identify shared targets across diseases
- Check adverse event profiles

### 3. Biomarker Discovery

- Find disease-associated variants
- Get credible sets from fine-mapping
- Identify genes in disease loci

### 4. Competitive Intelligence

- Find drugs in clinical trials
- Identify targets being pursued
- Track clinical phase progression

## Pagination

For queries returning multiple results (e.g., associated diseases, known drugs):

- Use `page_size` to control number of results
- Use `page_index` for pagination (0-based)
- Response includes `count` field with total results

## Custom Queries

For advanced users, the tool supports custom GraphQL queries:

```python
custom_query = """
query target($ensemblId: String!) {
    target(ensemblId: $ensemblId) {
        id
        approvedSymbol
        # Add any fields from the schema
    }
}
"""
```

Use the [GraphQL Playground](https://platform.opentargets.org/api) to explore the schema and test queries.

## Important Notes

1. **Single Entity Queries**: API is designed for single entity queries. For bulk analysis, use [data downloads](https://platform.opentargets.org/downloads) or [Google BigQuery](https://platform.opentargets.org/bigquery)

2. **Entity IDs**:

   - Targets: Use Ensembl gene IDs (ENSG...)
   - Diseases: Use EFO IDs (EFO\_...)
   - Drugs: Use ChEMBL IDs (CHEMBL...)

3. **GraphQL Benefits**:

   - Request only needed fields
   - Single query for related data
   - Strongly typed schema
   - Built-in documentation

4. **Rate Limiting**: Be respectful of API usage. For systematic queries, use data downloads.

## Related Resources

- Open Targets Platform: https://platform.opentargets.org
- GraphQL Playground: https://platform.opentargets.org/api
- Documentation: https://platform-docs.opentargets.org
- Data Downloads: https://platform.opentargets.org/downloads
- Community Forum: https://community.opentargets.org
