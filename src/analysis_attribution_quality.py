"""
Attribution and quality measure analysis for synthetic Medicare-like claims data.

This script:
- Loads cleaned claims data (or the same raw file and reuses cleaning logic)
- Attributes beneficiaries to providers based on plurality of visits
- Identifies diabetic beneficiaries
- Calculates a simple diabetes A1c testing rate by provider
- Writes outputs to the outputs/ directory
"""

import os
import pandas as pd
import numpy as np

from etl_claims import load_claims, clean_claims, OUTPUT_DIR, DATA_PATH


def define_visits(claims: pd.DataFrame) -> pd.DataFrame:
    """
    Define visits based on place_of_service and/or HCPCS codes.
    For simplicity, treat all claims with a non-null provider_npi as visits.
    In a real implementation, we might restrict to office/outpatient POS codes.
    """
    df = claims.copy()
    df = df.dropna(subset=["provider_npi", "bene_id"])
    return df


def attribute_beneficiaries(visits: pd.DataFrame) -> pd.DataFrame:
    """
    Attribute beneficiaries to providers based on plurality of visits.

    Steps:
    - Count visits per beneficiary-provider pair
    - For each beneficiary, select the provider with the highest visit count
      (ties broken deterministically by provider_npi)
    """
    visit_counts = (
        visits.groupby(["bene_id", "provider_npi"])
        .agg(visit_count=("claim_id", "nunique"))
        .reset_index()
    )

    # Rank providers within each beneficiary by visit_count (descending)
    visit_counts["rank"] = visit_counts.groupby("bene_id")["visit_count"].rank(
        method="first", ascending=False
    )

    attribution = visit_counts[visit_counts["rank"] == 1].copy()
    attribution = attribution.drop(columns=["rank"])

    return attribution


def identify_diabetic_beneficiaries(claims: pd.DataFrame) -> pd.DataFrame:
    """
    Identify diabetic beneficiaries using diagnosis codes.

    For simplicity, define diabetes as any claim with dx_code starting with 'E11'
    (Type 2 diabetes mellitus in ICD-10).
    """
    df = claims.copy()
    df["dx_code"] = df["dx_code"].astype(str)

    diabetic_claims = df[df["dx_code"].str.startswith("E11", na=False)]
    diabetic_benes = diabetic_claims[["bene_id"]].drop_duplicates()
    diabetic_benes["diabetes_flag"] = 1

    return diabetic_benes


def identify_a1c_tests(claims: pd.DataFrame) -> pd.DataFrame:
    """
    Identify A1c test claims using HCPCS codes.

    Common A1c codes include:
    - 83036: Hemoglobin; glycosylated (A1c)
    - 83037: Hemoglobin; glycosylated (A1c) by device cleared by FDA for home use
    """
    a1c_codes = {"83036", "83037"}

    df = claims.copy()
    df["hcpcs_code"] = df["hcpcs_code"].astype(str)

    a1c_claims = df[df["hcpcs_code"].isin(a1c_codes)].copy()
    return a1c_claims


def calculate_a1c_quality_measure(
    claims: pd.DataFrame,
    attribution: pd.DataFrame,
    diabetic_benes: pd.DataFrame,
    a1c_claims: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate provider-level A1c testing rate among diabetic beneficiaries.

    Denominator: diabetic beneficiaries attributed to the provider
    Numerator: those beneficiaries with at least one A1c test claim
    """

    # Merge attribution with diabetes flag
    bene_attr = attribution.merge(diabetic_benes, on="bene_id", how="left")
    bene_attr["diabetes_flag"] = bene_attr["diabetes_flag"].fillna(0)

    # Denominator: diabetic beneficiaries per provider
    denom = (
        bene_attr[bene_attr["diabetes_flag"] == 1]
        .groupby("provider_npi")
        .agg(denominator_diabetic_benes=("bene_id", "nunique"))
        .reset_index()
    )

    # Identify diabetic beneficiaries with at least one A1c test
    diabetic_a1c = (
        a1c_claims[["bene_id"]]
        .drop_duplicates()
        .merge(diabetic_benes, on="bene_id", how="inner")
    )

    # Link diabetic A1c beneficiaries to their attributed provider
    diabetic_a1c_attr = (
        diabetic_a1c.merge(attribution, on="bene_id", how="left")
        .dropna(subset=["provider_npi"])
        .drop_duplicates(subset=["bene_id", "provider_npi"])
    )

    numer = (
        diabetic_a1c_attr.groupby("provider_npi")
        .agg(numerator_diabetic_with_a1c=("bene_id", "nunique"))
        .reset_index()
    )

    # Combine numerator and denominator
    quality = denom.merge(numer, on="provider_npi", how="left")
    quality["numerator_diabetic_with_a1c"] = quality[
        "numerator_diabetic_with_a1c"
    ].fillna(0)

    # Calculate rate
    quality["a1c_testing_rate"] = (
        quality["numerator_diabetic_with_a1c"]
        / quality["denominator_diabetic_benes"]
    )

    return quality


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading and cleaning claims data...")
    claims = load_claims(DATA_PATH)
    claims_clean = clean_claims(claims)

    print("Defining visits...")
    visits = define_visits(claims_clean)

    print("Attributing beneficiaries to providers...")
    attribution = attribute_beneficiaries(visits)
    attribution_path = os.path.join(OUTPUT_DIR, "attribution_table.csv")
    attribution.to_csv(attribution_path, index=False)
    print(f"Attribution table written to: {attribution_path}")

    print("Identifying diabetic beneficiaries...")
    diabetic_benes = identify_diabetic_beneficiaries(claims_clean)

    print("Identifying A1c test claims...")
    a1c_claims = identify_a1c_tests(claims_clean)

    print("Calculating A1c quality measure by provider...")
    quality = calculate_a1c_quality_measure(
        claims_clean, attribution, diabetic_benes, a1c_claims
    )

    quality_path = os.path.join(OUTPUT_DIR, "quality_measure_provider.csv")
    quality.to_csv(quality_path, index=False)
    print(f"Quality measure results written to: {quality_path}")

    # Optional: show top providers by denominator and rate
    print("\nSample of provider-level A1c testing rates:")
    print(
        quality.sort_values("denominator_diabetic_benes", ascending=False)
        .head(10)
    )


if __name__ == "__main__":
    main()
