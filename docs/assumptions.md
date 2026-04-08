This document outlines the assumptions used throughout the synthetic data generation, ETL processing, attribution logic, and quality measure calculations. These assumptions support transparency, reproducibility, and audit readiness.

Data Assumptions
All data is fully synthetic and contains no PHI.

Beneficiary IDs, provider NPIs, and claim IDs are randomly generated.

Dates of service fall within a single calendar year.

Procedure codes represent simplified E/M and lab services.

Allowed amounts follow approximate Medicare‑like distributions using log‑normal sampling.

Diagnosis codes are simplified and used only for cohort identification.

ETL Assumptions
Claims with missing or invalid dates are excluded.

Allowed amounts are treated as the primary financial metric.

Duplicate claims (same beneficiary, provider, date, and code) are removed.

Provider specialty is not used for attribution in this version.

Visit indicators are derived from E/M‑type HCPCS codes.

Attribution Assumptions
Attribution is based on plurality of visits (provider with the most visits).

A “visit” is defined as any claim with an E/M‑type HCPCS code.

Ties in visit counts default to the earliest provider by NPI.

Attribution is performed at the beneficiary‑year level.

Attribution does not incorporate geography, specialty, or risk adjustment.

Quality Measure Assumptions
Diabetes identification is based on diagnosis codes appearing on any claim.

A1c testing is identified using HCPCS/CPT codes for A1c lab tests.

Denominator = attributed diabetic beneficiaries.

Numerator = diabetic beneficiaries with ≥1 A1c test.

Measure is calculated at the provider level.

No risk adjustment or exclusions are applied.

SQL A1C quality measure assumptions
Diabetes: dx_code starts with 'E11'

A1c: hcpcs_code in ('83036', '83037')
