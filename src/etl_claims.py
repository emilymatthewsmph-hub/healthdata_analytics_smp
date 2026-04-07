"""
ETL and payment/utilization analysis for synthetic Medicare-like claims data.

This script:
- Loads synthetic claims from CSV
- Cleans and standardizes key fields
- Produces provider-level payment and utilization summaries
- Writes outputs to the outputs/ directory
"""

import os
import pandas as pd
import numpy as np


DATA_PATH = os.path.join("data", "synthetic_claims.csv")
OUTPUT_DIR = "outputs"


def load_claims(path: str) -> pd.DataFrame:
    """Load raw claims data from CSV."""
    claims = pd.read_csv(path)
    return claims


def clean_claims(claims: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize claims data."""
    df = claims.copy()

    # Standardize column names (lowercase)
    df.columns = [c.strip().lower() for c in df.columns]

    # Parse dates
    if "date_of_service" in df.columns:
        df["date_of_service"] = pd.to_datetime(df["date_of_service"], errors="coerce")

    # Enforce numeric types for payment fields
    for col in ["allowed_amount", "paid_amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Basic data quality filters
    required_cols = ["claim_id", "bene_id", "provider_npi", "allowed_amount"]
    df = df.dropna(subset=[c for c in required_cols if c in df.columns])

    # Optional: remove negative or zero allowed amounts
    df = df[df["allowed_amount"] > 0]

    return df


def summarize_provider_payments(claims: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate claims to provider level to compute payment and utilization metrics.
    """
    group_cols = ["provider_npi"]
    if "specialty" in claims.columns:
        group_cols.append("specialty")
    if "state" in claims.columns:
        group_cols.append("state")

    summary = (
        claims.groupby(group_cols)
        .agg(
            total_claims=("claim_id", "nunique"),
            total_beneficiaries=("bene_id", "nunique"),
            total_allowed=("allowed_amount", "sum"),
            avg_allowed=("allowed_amount", "mean"),
            total_paid=("paid_amount", "sum") if "paid_amount" in claims.columns else ("allowed_amount", "sum"),
        )
        .reset_index()
    )

    # Compute paid-to-allowed ratio if both fields exist
    if "paid_amount" in claims.columns:
        summary["paid_to_allowed_ratio"] = summary["total_paid"] / summary["total_allowed"]

    return summary


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading claims data...")
    claims = load_claims(DATA_PATH)

    print("Cleaning claims data...")
    claims_clean = clean_claims(claims)

    print("Summarizing provider payments and utilization...")
    provider_summary = summarize_provider_payments(claims_clean)

    output_path = os.path.join(OUTPUT_DIR, "provider_summary.csv")
    provider_summary.to_csv(output_path, index=False)

    print(f"Provider summary written to: {output_path}")

    # Optional: show top 10 providers by total allowed
    top10 = provider_summary.sort_values("total_allowed", ascending=False).head(10)
    print("\nTop 10 providers by total allowed amount:")
    print(top10)


if __name__ == "__main__":
    main()
