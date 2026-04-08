-- Step 1: Count visits per beneficiary-provider pair
WITH visit_counts AS (
    SELECT
        bene_id,
        provider_npi,
        COUNT(DISTINCT claim_id) AS visit_count
    FROM claims
    WHERE provider_npi IS NOT NULL
      AND bene_id IS NOT NULL
    GROUP BY bene_id, provider_npi
),

-- Step 2: Rank providers within each beneficiary by visit_count (ties by provider_npi)
ranked_visits AS (
    SELECT
        bene_id,
        provider_npi,
        visit_count,
        ROW_NUMBER() OVER (
            PARTITION BY bene_id
            ORDER BY visit_count DESC, provider_npi ASC
        ) AS rn
    FROM visit_counts
)

-- Step 3: Keep only the top-ranked provider per beneficiary
SELECT
    bene_id,
    provider_npi AS attributed_provider_npi,
    visit_count AS visit_count_attributed_provider
FROM ranked_visits
WHERE rn = 1;
