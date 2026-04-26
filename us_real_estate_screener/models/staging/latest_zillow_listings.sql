WITH listing_ranks AS (
    SELECT zpid
         , extracted_at
         , ROW_NUMBER() OVER (PARTITION BY zpid ORDER BY extracted_at DESC) AS listing_rank
      FROM {{ source('raw_zillow', 'zillow_listings_raw') }}
)

SELECT zlr.zpid
     , zlr.address
     , zlr.property_type
     , zlr.bedrooms
     , zlr.bathrooms
     , zlr.latitude
     , zlr.longitude
     , zlr.living_area
     , zlr.lot_area_value
     , zlr.lot_area_unit
     , zlr.detail_url
     , zlr.price
     , zlr.price_change as latest_price_change
     , zlr.days_on_zillow
     , zlr.extracted_at AS last_extracted_at
  FROM {{ source('raw_zillow', 'zillow_listings_raw') }} AS zlr
       JOIN listing_ranks AS ls
       ON zlr.zpid = ls.zpid
          AND zlr.extracted_at = ls.extracted_at
          AND 1 = ls.listing_rank