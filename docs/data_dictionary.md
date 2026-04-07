Data Dictionary
This data dictionary describes the key fields used in the synthetic claims dataset and all downstream outputs. It supports transparency, reproducibility, and audit readiness.

1. Synthetic Claims Data (data/synthetic_claims.csv)
claim_id  
Unique identifier for each claim record.

bene_id  
Synthetic beneficiary identifier.

provider_npi  
Synthetic provider National Provider Identifier.

date_of_service  
Date the service was rendered (YYYY‑MM‑DD).

hcpcs_code  
Procedure code representing E/M or lab services.

diagnosis_code  
Primary diagnosis code associated with the claim.

allowed_amount  
Allowed payment amount for the claim.

place_of_service  
Code indicating the setting of care (e.g., office, outpatient).

2. Provider Summary (outputs/provider_summary.csv)
provider_npi  
Synthetic provider identifier.

total_allowed_amount  
Sum of allowed amounts for all claims for the provider.

claim_count  
Number of claims associated with the provider.

unique_bene_count  
Number of unique beneficiaries seen by the provider.

visit_count  
Number of visits (claims meeting the visit definition) for the provider.

3. Attribution Table (outputs/attribution_table.csv)
bene_id  
Synthetic beneficiary identifier.

attributed_provider_npi  
Provider NPI to whom the beneficiary is attributed based on plurality of visits.

visit_count_attributed_provider  
Number of visits the beneficiary had with the attributed provider.

4. Quality Measure Results (outputs/quality_measure_provider.csv)
provider_npi  
Synthetic provider identifier.

diabetic_bene_count  
Number of attributed beneficiaries identified as having diabetes (denominator).

diabetic_bene_with_a1c_count  
Number of diabetic beneficiaries with ≥1 A1c test (numerator).

a1c_testing_rate  
Proportion of diabetic beneficiaries with ≥1 A1c test (numerator ÷ denominator).
