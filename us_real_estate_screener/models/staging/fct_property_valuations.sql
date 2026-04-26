WITH raw_property_details AS (
    SELECT *
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
),

raw_listings AS (
    SELECT *
      FROM {{ source('raw_zillow', 'zillow_listings_raw') }}
),

latest_listings AS (
    SELECT *
      FROM {{ ref('latest_zillow_listings') }}
),

all_zpids AS (
    SELECT zpid FROM raw_property_details
    UNION
    SELECT zpid FROM raw_listings
)

SELECT az.zpid AS property_zillow_id
     , COALESCE(rpd.price, lpd.price) AS current_price
     , COALESCE(rpd.price_change, lpd.latest_price_change) AS latest_price_change
     , rpd.zestimate
     , rpd.rent_zestimate
     , (rpd.reso_facts->>'pricePerSquareFoot')::numeric AS price_per_square_foot
     , rpd.page_view_count
     , rpd.favorite_count
     , COALESCE(rpd.time_on_zillow, lpd.days_on_zillow::text) AS time_on_zillow
     , rpd.home_status
     , CASE
           WHEN rpd.date_posted = '' THEN NULL
           ELSE rpd.date_posted::DATE
       END AS date_posted
     , CASE
           WHEN rpd.date_sold = '' THEN NULL
           ELSE rpd.date_sold::DATE
       END AS date_sold
     , rpd.updated_at AS last_updated_at
  FROM all_zpids AS az
       LEFT JOIN latest_listings AS lpd ON az.zpid = lpd.zpid
       LEFT JOIN raw_property_details AS rpd ON az.zpid = rpd.zpid
