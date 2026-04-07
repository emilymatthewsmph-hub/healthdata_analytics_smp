Technical Appendix
This appendix provides detailed documentation of the workflow, including data generation, ETL logic, attribution methodology, and quality measure calculations.

A. Synthetic Data Generation
The synthetic dataset is generated using randomized but realistic patterns:

Beneficiary demographics: Random IDs, age ranges, and genders

Provider NPIs: Random 10‑digit identifiers

Claim dates: Uniform distribution across a calendar year

HCPCS codes: Sampled from E/M and lab categories

Allowed amounts: Generated using log‑normal distributions to mimic Medicare payment patterns

Diagnosis codes: Sampled from common chronic condition categories

A fixed random seed ensures reproducibility.

B. ETL Processing Steps
Load raw synthetic claims

Standardize column names and formats

Convert dates to datetime

Remove invalid or missing values

Derive visit indicators based on HCPCS codes

Aggregate provider‑level metrics:

Total allowed amount

Number of claims

Number of unique beneficiaries

Number of visits

Output: provider_summary.csv

C. Attribution Logic
Attribution follows a plurality‑of‑visits model:

Group claims by beneficiary

Count visits per provider

Select provider with the highest visit count

Resolve ties deterministically using NPI ordering

Output beneficiary → provider mapping

Output: attribution_table.csv

D. Quality Measure Logic
The diabetes A1c testing measure includes:

Identify diabetic beneficiaries using diagnosis codes

Identify A1c test claims using HCPCS/CPT codes

Join attribution, diabetes, and A1c test tables

Calculate provider‑level:

Denominator (diabetic beneficiaries)

Numerator (beneficiaries with ≥1 A1c test)

Rate (numerator ÷ denominator)

Output: quality_measure_provider.csv

E. Output Files
provider_summary.csv

attribution_table.csv

quality_measure_provider.csv
