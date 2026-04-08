-- Step 1: Identify diabetic beneficiaries
WITH diabetic_benes AS (
    SELECT DISTINCT
        bene_id
    FROM claims
    WHERE CAST(dx_code AS VARCHAR) LIKE 'E11%'
),

-- Step 2: Identify A1c test claims
a1c_claims AS (
    SELECT DISTINCT
        bene_id
    FROM claims
    WHERE CAST(hcpcs_code AS VARCHAR) IN ('83036', '83037')
),

-- Step 3: Denominator - diabetic beneficiaries attributed to each provider
denominator AS (
    SELECT
        a.attributed_provider_npi AS provider_npi,
        COUNT(DISTINCT a.bene_id) AS denominator_diabetic_benes
    FROM attribution_table a
    INNER JOIN diabetic_benes d
        ON a.bene_id = d.bene_id
    GROUP BY a.attributed_provider_npi
),

-- Step 4: Numerator - diabetic beneficiaries with ≥1 A1c test, attributed to provider
numerator AS (
    SELECT
        a.attributed_provider_npi AS provider_npi,
        COUNT(DISTINCT a.bene_id) AS numerator_diabetic_with_a1c
    FROM attribution_table a
    INNER JOIN diabetic_benes d
        ON a.bene_id = d.bene_id
    INNER JOIN a1c_claims ac
        ON a.bene_id = ac.bene_id
    GROUP BY a.attributed_provider_npi
)

-- Step 5: Combine numerator and denominator and compute rate
SELECT
    d.provider_npi,
    d.denominator_diabetic_benes,
    COALESCE(n.numerator_diabetic_with_a1c, 0) AS numerator_diabetic_with_a1c,
    CASE
        WHEN d.denominator_diabetic_benes > 0
        THEN COALESCE(n.numerator_diabetic_with_a1c, 0) * 1.0
             / d.denominator_diabetic_benes
        ELSE NULL
    END AS a1c_testing_rate
FROM denominator d
LEFT JOIN numerator n
    ON d.provider_npi = n.provider_npi
ORDER BY d.provider_npi;
