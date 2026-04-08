Project Overview

This project implements an end‑to‑end healthcare claims analytics workflow using synthetic Medicare‑like data. It includes data generation, ETL processing, provider‑level summarization, beneficiary attribution, and calculation of a diabetes A1c quality measure. The workflow is fully reproducible and organized to support transparent, modular analysis.

Folder Structure
Code
project-root/
│
├── data/
│   └── synthetic_claims.csv
├── outputs/
│   ├── provider_summary.csv
│   ├── attribution_table.csv
│   └── quality_measure_provider.csv
├── src/
│   ├── generate_synthetic_claims.py
│   ├── etl_claims.py
│   └── analysis_attribution_quality.py
├── sql/
│   ├── provider_summary_example.sql
│   ├── attribution_logic.sql
│   └── a1c_quality_measure.sql
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

### SQL Component

In addition to the Python-based workflow, this repository includes SQL scripts that mirror the core analytics logic. These examples demonstrate how the same ETL, attribution, and quality measure steps can be implemented in SQL-based data warehouse environments (e.g., Snowflake, Databricks SQL, SQL Server).

- `sql/provider_summary_example.sql` — Provider-level payment and utilization summary.
- `sql/attribution_logic.sql` — Beneficiary attribution to providers using plurality-of-visits logic.
- `sql/a1c_quality_measure.sql` — Provider-level diabetes A1c testing rate calculation.


- `sql/provider_summary_example.sql` — SQL version of the provider-level claims summarization workflow
| Component                    | Python Implementation                                      | SQL Implementation                                           |
|-----------------------------|------------------------------------------------------------|-------------------------------------------------------------|
| Data source                 | `pandas.read_csv("data/synthetic_claims.csv")`            | `SELECT * FROM claims`                                      |
| ETL / cleaning              | `clean_claims()` function (types, dates, filters)         | `CAST`, `WHERE`, and basic validation in `SELECT`/`WHERE`   |
| Provider summary            | `summarize_provider_payments()` with `groupby().agg()`    | `GROUP BY provider_npi, specialty, state` with aggregates   |
| Visit definition            | Filter non-null `provider_npi` / E/M HCPCS in DataFrame   | `WHERE provider_npi IS NOT NULL` and HCPCS filters          |
| Attribution logic           | `attribute_beneficiaries()` with `groupby` + `rank()`     | `ROW_NUMBER() OVER (PARTITION BY bene_id ORDER BY ...)`     |
| Diabetes identification     | `dx_code.str.startswith("E11")`                           | `WHERE CAST(dx_code AS VARCHAR) LIKE 'E11%'`                |
| A1c test identification     | `hcpcs_code.isin({"83036","83037"})`                      | `WHERE hcpcs_code IN ('83036','83037')`                     |
| Quality measure calculation | Merge/join DataFrames, compute rate in Python             | CTEs + `JOIN`s + calculated rate in final `SELECT`          |
| Outputs                     | CSVs in `outputs/` via `to_csv()`                         | Views or tables via `CREATE TABLE AS` / `INSERT INTO`       |


### Additional documentation

- [Assumptions](docs/assumptions.md)
- [Technical Appendix](docs/technical_appendix.md)
- [Portfolio Summary](docs/portfolio_summary.md)
- [Future Enhancements](docs/future_enhancements.md)


---

