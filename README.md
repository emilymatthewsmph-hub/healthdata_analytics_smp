
Medicare-like claims ETL, payment analysis, attribution, and quality measure coding sample
## Medicare-like Claims ETL, Payment Analysis, and Attribution Logic

This repository contains a self-contained coding sample that demonstrates:
- ETL and cleaning of Medicare-like synthetic claims data
- Payment and utilization analysis at the provider level
- Patient attribution to primary providers based on visit plurality
- Implementation of a simple quality measure (diabetes A1c testing rate)

---

## Data

The analysis uses a synthetic claims file with the following expected columns:

- `claim_id`: Unique claim identifier
- `bene_id`: Beneficiary (patient) identifier
- `provider_npi`: Rendering or attributed provider NPI
- `date_of_service`: Date of service (YYYY-MM-DD)
- `hcpcs_code`: Procedure/HCPCS code
- `dx_code`: Primary diagnosis code (ICD-10-like)
- `place_of_service`: Place of service code
- `specialty`: Provider specialty (e.g., INTERNAL_MEDICINE, FAMILY_PRACTICE)
- `state`: Provider state
- `allowed_amount`: Allowed amount for the claim
- `paid_amount`: Paid amount for the claim

> Note: The dataset is synthetic and contains no real PHI.

---

## Environment

- Python 3.9+
- Recommended packages:
  - pandas
  - numpy

Install dependencies:

```bash
pip install pandas numpy
