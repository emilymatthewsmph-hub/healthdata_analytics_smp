import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
N_ROWS = 1000
OUTPUT_PATH = "data/synthetic_claims.csv"

np.random.seed(42)
random.seed(42)

# -----------------------------
# Synthetic value pools
# -----------------------------
providers = [
    ("1111111111", "INTERNAL_MEDICINE", "TX"),
    ("2222222222", "FAMILY_PRACTICE", "GA"),
    ("3333333333", "ENDOCRINOLOGY", "FL"),
    ("4444444444", "FAMILY_PRACTICE", "TX"),
    ("5555555555", "INTERNAL_MEDICINE", "CA"),
    ("6666666666", "ENDOCRINOLOGY", "WA"),
    ("7777777777", "FAMILY_PRACTICE", "CO"),
    ("8888888888", "INTERNAL_MEDICINE", "NY"),
    ("9999999999", "FAMILY_PRACTICE", "IL"),
]

hcpcs_pool = ["99213", "99214", "83036", "83037"]
dx_pool = ["E119", "E669", "I109", "M545", "J189"]  # diabetes, obesity, hypertension, back pain, pneumonia
pos_pool = ["11", "22"]  # office, outpatient hospital

# -----------------------------
# Helper functions
# -----------------------------
def random_date(start="2024-01-01", end="2024-04-30"):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    delta = end_dt - start_dt
    return start_dt + timedelta(days=random.randint(0, delta.days))

# -----------------------------
# Generate rows
# -----------------------------
rows = []

for i in range(1, N_ROWS + 1):
    claim_id = f"C{i:04d}"
    bene_id = f"B{random.randint(1, 200):03d}"  # ~200 beneficiaries
    provider_npi, specialty, state = random.choice(providers)
    date_of_service = random_date().strftime("%Y-%m-%d")
    hcpcs_code = random.choice(hcpcs_pool)
    dx_code = random.choice(dx_pool)
    place_of_service = random.choice(pos_pool)

    # Allowed & paid amounts
    if hcpcs_code in ["83036", "83037"]:  # A1c tests
        allowed = round(np.random.uniform(18, 30), 2)
    else:
        allowed = round(np.random.uniform(70, 140), 2)

    paid = round(allowed * np.random.uniform(0.75, 0.95), 2)

    rows.append([
        claim_id, bene_id, provider_npi, date_of_service,
        hcpcs_code, dx_code, place_of_service, specialty,
        state, allowed, paid
    ])

# -----------------------------
# Create DataFrame and save
# -----------------------------
cols = [
    "claim_id", "bene_id", "provider_npi", "date_of_service",
    "hcpcs_code", "dx_code", "place_of_service", "specialty",
    "state", "allowed_amount", "paid_amount"
]

df = pd.DataFrame(rows, columns=cols)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Generated {N_ROWS} synthetic claims at: {OUTPUT_PATH}")
