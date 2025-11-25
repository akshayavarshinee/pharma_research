# Open Targets Drug Indication Tool - Summary

## Overview

The Open Targets Drug Indication Tool provides access to drug-disease indication data from the Open Targets Platform. This tool helps identify approved and investigational indications for drugs, including clinical trial phases and supporting references.

## Key Features

- **Drug Indications**: Find all indications for a specific drug
- **Disease Drugs**: Find all drugs for a specific disease
- **Clinical Phase Filtering**: Filter by minimum clinical trial phase
- **Approved Indications**: Get only approved (phase 4) indications
- **Reference Sources**: Access supporting evidence and references
- **Mechanism of Action**: Get drug mechanisms for disease indications

## Data Schema

### Drug Indication Fields

| Field                               | Type    | Description                                   |
| ----------------------------------- | ------- | --------------------------------------------- |
| `id`                                | Text    | Open Targets molecule identifier (ChEMBL ID)  |
| `name`                              | Text    | Drug name                                     |
| `drugType`                          | Text    | Type of drug (small molecule, antibody, etc.) |
| `maximumClinicalTrialPhase`         | Float   | Highest phase reached across all indications  |
| `indications`                       | Array   | List of disease indications                   |
| `indications.disease.id`            | Text    | Disease identifier (EFO ID)                   |
| `indications.disease.name`          | Text    | Disease name                                  |
| `indications.maxPhaseForIndication` | Float   | Highest phase for this specific indication    |
| `indications.references`            | Array   | Supporting references                         |
| `indications.references.source`     | Text    | Reference source name                         |
| `indications.references.ids`        | Array   | Reference IDs                                 |
| `approvedIndications`               | Array   | List of approved disease IDs                  |
| `indicationCount`                   | Integer | Total number of indications                   |

## Clinical Trial Phases

| Phase | Description                         |
| ----- | ----------------------------------- |
| 0     | Preclinical / Discovery             |
| 1     | Phase 1 - Safety and dosage         |
| 2     | Phase 2 - Efficacy and side effects |
| 3     | Phase 3 - Efficacy confirmation     |
| 4     | Approved / Phase 4 - Post-marketing |

## Query Parameters

### Drug-Based Queries

- **drug_id**: ChEMBL ID (e.g., `CHEMBL25` for aspirin)
- **disease_id**: Optional EFO ID to filter specific indication
- **min_phase**: Minimum clinical trial phase (0-4)
- **approved_only**: Boolean to get only approved indications
- **limit**: Maximum number of results

### Disease-Based Queries

- **disease_id**: EFO ID (e.g., `EFO_0000685` for rheumatoid arthritis)
- **drug_id**: Optional ChEMBL ID to filter specific drug
- **min_phase**: Minimum clinical trial phase (0-4)
- **approved_only**: Boolean to get only approved drugs
- **limit**: Maximum number of results

## Common Use Cases

### 1. Drug Development

- Find all indications for a drug candidate
- Check clinical trial phases
- Identify approved vs investigational uses

### 2. Drug Repurposing

- Find drugs approved for similar diseases
- Identify drugs in clinical trials for target disease
- Check mechanism of action for repurposing potential

### 3. Competitive Intelligence

- Track drugs in development for specific diseases
- Monitor clinical trial progress
- Identify approved competitors

### 4. Regulatory Research

- Get approved indications for drugs
- Access supporting references
- Check withdrawal status

### 5. Market Analysis

- Count drugs per disease area
- Identify unmet medical needs
- Track approval trends

## Response Structure

### Drug Query Response

```json
{
  "drug": {
    "id": "CHEMBL25",
    "name": "ASPIRIN",
    "drugType": "Small molecule",
    "maximumClinicalTrialPhase": 4
  },
  "indications": [
    {
      "disease": {
        "id": "EFO_0000612",
        "name": "myocardial infarction"
      },
      "maxPhaseForIndication": 4,
      "references": [
        {
          "source": "FDA",
          "ids": ["NDA011"]
        }
      ]
    }
  ],
  "indicationCount": 15,
  "approvedIndications": ["EFO_0000612", "EFO_0000508"],
  "approvedIndicationCount": 2
}
```

### Disease Query Response

```json
{
  "disease": {
    "id": "EFO_0000685",
    "name": "rheumatoid arthritis"
  },
  "drugs": [
    {
      "drug": {
        "id": "CHEMBL1201583",
        "name": "ADALIMUMAB",
        "drugType": "Antibody"
      },
      "phase": 4,
      "status": "Approved",
      "mechanismOfAction": "Tumor necrosis factor inhibitor",
      "references": [...]
    }
  ],
  "drugCount": 25,
  "approvedDrugs": ["CHEMBL1201583", "CHEMBL1201572"],
  "approvedDrugCount": 15
}
```

## Reference Sources

Common reference sources in the data:

- **FDA**: US Food and Drug Administration
- **EMA**: European Medicines Agency
- **ATC**: Anatomical Therapeutic Chemical Classification
- **DailyMed**: FDA drug labels
- **ClinicalTrials.gov**: Clinical trial registry
- **ChEMBL**: Bioactivity database

## Filtering Examples

### By Clinical Phase

```python
# Get drugs in late-stage trials (phase 3+)
min_phase=3

# Get only approved drugs
approved_only=True  # Equivalent to min_phase=4
```

### By Disease

```python
# Find if aspirin is approved for myocardial infarction
drug_id='CHEMBL25',
disease_id='EFO_0000612'
```

### By Drug Type

Drug types in the data:

- Small molecule
- Antibody
- Protein
- Oligosaccharide
- Oligonucleotide
- Enzyme
- Unknown

## Important Notes

1. **Data Source**: This tool uses the Open Targets Platform GraphQL API, which provides the same data as the Parquet files but with easier querying

2. **Entity IDs**:

   - Drugs use ChEMBL IDs (format: `CHEMBL` + numbers)
   - Diseases use EFO IDs (format: `EFO_` + numbers)

3. **Phase Interpretation**:

   - Phase 4 = Approved for this indication
   - Phase 0-3 = Investigational for this indication
   - Maximum phase may differ per indication

4. **Multiple Indications**: A drug can have different phases for different indications

5. **References**: Each indication may have multiple supporting references from different sources

## Limitations

- Single drug or disease queries (not bulk queries)
- For systematic analysis, use Open Targets data downloads
- Clinical phase data may not reflect most recent trials
- Some drugs may have off-label uses not captured

## Related Resources

- Open Targets Platform: https://platform.opentargets.org
- Data Downloads: https://platform.opentargets.org/downloads/data
- ChEMBL Database: https://www.ebi.ac.uk/chembl/
- EFO Ontology: https://www.ebi.ac.uk/efo/
