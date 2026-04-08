## Project Overview

This project implements an end‑to‑end healthcare claims analytics workflow using synthetic Medicare‑like data. It includes data generation, ETL processing, provider‑level summarization, beneficiary attribution, and calculation of a diabetes A1c quality measure. The workflow is fully reproducible and organized to support transparent, modular analysis.

---

## Final Product Workflow (508‑Friendly)

This workflow summarizes the end-to-end analytics pipeline, from synthetic claims input through ETL, attribution, and quality measurement. It is designed to be fully accessible and screen‑reader friendly.

FINAL PRODUCT WORKFLOW

1. Synthetic Claims Input  
   - File: data/synthetic_claims.csv  
   - Medicare-like structure (bene_id, provider_npi, dx_code, hcpcs_code, allowed_amount, date_of_service)

        |
        v

2. ETL Pipeline (Python or SQL)  
   - Clean and standardize fields  
   - Parse dates and numeric amounts  
   - Remove invalid or zero-allowed claims  
   - Output: outputs/provider_summary.csv

        |
        v

3. Provider Summary  
   - total_claims  
   - unique_bene_count  
   - total_allowed  
   - avg_allowed  
   - paid_to_allowed_ratio

        |
        v

4. Attribution Logic  
   - Plurality-of-visits model  
   - Tie-break by provider NPI  
   - Output: outputs/attribution_table.csv

        |
        v

5. Quality Measure Logic (Diabetes A1c)  
   - Identify diabetic beneficiaries (dx_code starts with E11)  
   - Identify A1c tests (HCPCS 83036, 83037)  
   - Compute numerator and denominator  
   - Output: outputs/quality_measure_provider.csv

        |
        v

6. Final Outputs (Analytics-Ready Tables)  
   - provider_summary.csv  
   - attribution_table.csv  
   - quality_measure_provider.csv  

**Alt-text:** This diagram shows a linear workflow for an end-to-end healthcare claims analytics pipeline. The workflow begins with a synthetic claims input file. The data flows into an ETL pipeline that cleans and standardizes the claims. The next step produces a provider summary with metrics such as total claims and total allowed amounts. The workflow then applies attribution logic to assign beneficiaries to providers using a plurality-of-visits model. After attribution, the workflow calculates a diabetes A1c quality measure by identifying diabetic beneficiaries and A1c test claims. The final outputs include three CSV files: provider_summary.csv, attribution_table.csv, and quality_measure_provider.csv.

---


## Folder Structure
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

#How to Run This Project
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

## SQL Component

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


## Additional documentation

- [Assumptions](docs/assumptions.md)
- [Technical Appendix](docs/technical_appendix.md)
- [Portfolio Summary](docs/portfolio_summary.md)
- [Future Enhancements](docs/future_enhancements.md)


---

