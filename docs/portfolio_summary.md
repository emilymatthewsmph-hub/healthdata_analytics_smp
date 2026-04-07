Portfolio Summary
This project implements a complete healthcare claims analytics workflow using synthetic Medicare‑like data. The workflow includes synthetic data generation, ETL processing, provider‑level summarization, beneficiary attribution, and calculation of a diabetes A1c quality measure. The design emphasizes reproducibility, transparency, and modularity, aligning with common expectations in federal health analytics environments.

The ETL component standardizes and cleans claims data, derives visit indicators, and produces provider‑level payment and utilization metrics. Attribution assigns beneficiaries to providers based on plurality of visits, a method frequently used in value‑based care programs and population health analytics. The quality measure component identifies diabetic beneficiaries and evaluates whether they received an A1c test, producing provider‑level performance metrics that mirror typical quality reporting workflows.

Outputs are stored in the outputs/ directory and include provider summaries, attribution tables, and quality measure results. The project demonstrates the ability to design and execute an end‑to‑end analytics workflow that is clear, auditable, and aligned with federal program requirements.

This project highlights skills in:

Claims ETL and data cleaning

Provider attribution logic

Quality measure calculation

Synthetic data generation

Reproducible analytics workflows

Python‑based data engineering
