SELECT TO_DATE(month_date_yyyymm::text, 'YYYYMM') AS month_date
     , postal_code
     , active_listing_count
     , active_listing_count_mm
     , new_listing_count
     , new_listing_count_mm
     , total_listing_count
     , total_listing_count_mm
     , average_listing_price
     , average_listing_price_mm
     , median_listing_price
     , median_listing_price_mm
     , price_increased_count
     , price_increased_count_mm
     , median_days_on_market
     , median_days_on_market_mm
     , created_at
     , updated_at
  FROM {{ source('raw_zillow', 'zillow_monthly_inventory') }}
