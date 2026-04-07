Project Overview

This project implements an end‑to‑end healthcare claims analytics workflow using synthetic Medicare‑like data. It includes data generation, ETL processing, provider‑level summarization, beneficiary attribution, and calculation of a diabetes A1c quality measure. The workflow is fully reproducible and organized to support transparent, modular analysis.

Folder Structure
Code
project-root/
│
├── data/
│   └── synthetic_claims.csv
│
├── outputs/
│   ├── provider_summary.csv
│   ├── attribution_table.csv
│   └── quality_measure_provider.csv
│
├── src/
│   ├── generate_synthetic_claims.py
│   ├── etl_claims.py
│   └── analysis_attribution_quality.py
│
└── README.md
Prerequisites
Python 3.8+

Required packages:

Code
pip install pandas numpy

How to Run This Project
1. Generate Synthetic Claims Data
Creates a 1,000‑row synthetic Medicare‑like claims dataset.

Code
python src/generate_synthetic_claims.py
Output:

Code
data/synthetic_claims.csv
2. Run the ETL Pipeline
Cleans the dataset and produces provider‑level payment and utilization metrics.

Code
python src/etl_claims.py
Output:

Code
outputs/provider_summary.csv
3. Run Attribution and Quality Measures
Assigns beneficiaries to providers and calculates A1c testing rates.

Code
python src/analysis_attribution_quality.py
Outputs:

Code
outputs/attribution_table.csv
outputs/quality_measure_provider.csv
Workflow Diagram
Code
                ┌──────────────────────────┐
                │  generate_synthetic_     │
                │     _claims.py           │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │   data/synthetic_        │
                │       _claims.csv        │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │      etl_claims.py       │
                │  - clean claims          │
                │  - standardize fields    │
                │  - summarize providers   │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │ outputs/provider_        │
                │     _summary.csv         │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │ analysis_attribution_    │
                │     _quality.py          │
                │  - define visits         │
                │  - attribute bene → NPI  │
                │  - identify diabetics    │
                │  - check A1c testing     │
                └────────────┬─────────────┘
                             │
           ┌─────────────────┴──────────────────┐
           ▼                                    ▼
┌──────────────────────────┐        ┌──────────────────────────┐
│ outputs/attribution_     │        │ outputs/quality_measure_ │
│        _table.csv        │        │       _provider.csv      │
└──────────────────────────┘        └──────────────────────────┘

> Note: The dataset is synthetic and contains no real PHI.

## Additional documentation

- [Assumptions](docs/assumptions.md)
- [Technical Appendix](docs/technical_appendix.md)
- [Portfolio Summary](docs/portfolio_summary.md)
- [Future Enhancements](docs/future_enhancements.md)


---

