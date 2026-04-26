-- This test ensures that every ZPID in our raw source tables 
-- exists in the downstream staging models.
-- If any row is returned, it means a property was dropped.

WITH raw_zpids AS (
    -- Combine all unique ZPIDs seen in either raw source
    SELECT zpid FROM {{ source('raw_zillow', 'zillow_listings_raw') }}
    UNION
    SELECT zpid FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
),

missing_from_dim_properties AS (
    SELECT r.zpid, 'dim_properties' as missing_from
    FROM raw_zpids r
    LEFT JOIN {{ ref('dim_properties') }} m ON r.zpid = m.property_zillow_id
    WHERE m.property_zillow_id IS NULL
),

missing_from_valuations AS (
    SELECT r.zpid, 'fct_property_valuations' as missing_from
    FROM raw_zpids r
    LEFT JOIN {{ ref('fct_property_valuations') }} m ON r.zpid = m.property_zillow_id
    WHERE m.property_zillow_id IS NULL
),

missing_from_financials AS (
    -- We check financials only for those in details_raw since financials come exclusively from there
    SELECT r.zpid, 'fct_property_financials' as missing_from
    FROM {{ source('raw_zillow', 'zillow_property_details_raw') }} r
    LEFT JOIN {{ ref('fct_property_financials') }} m ON r.zpid = m.property_zillow_id
    WHERE m.property_zillow_id IS NULL
)

SELECT * FROM missing_from_dim_properties
UNION ALL
SELECT * FROM missing_from_valuations
UNION ALL
SELECT * FROM missing_from_financials
