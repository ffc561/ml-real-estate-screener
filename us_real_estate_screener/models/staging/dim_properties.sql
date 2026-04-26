WITH raw_property_details AS (
    SELECT *
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
),

listing_property_dimensions AS (
    SELECT zpid
         , address
         , property_type
         , bedrooms
         , bathrooms
         , latitude
         , longitude
         , living_area
         , lot_area_value
         , lot_area_unit
         , detail_url
         , last_extracted_at
      FROM {{ ref('latest_zillow_listings') }}
)

SELECT lpd.zpid AS property_zillow_id
     , lpd.address as full_address
     , COALESCE(rpd.home_type, lpd.property_type) AS property_type
     , COALESCE(rpd.latitude, lpd.latitude) AS latitude
     , COALESCE(rpd.longitude, lpd.longitude) AS longitude
     , rpd.address->>'streetAddress' AS parsed_street_address
     , rpd.address->>'city' AS parsed_city
     , rpd.address->>'state' AS parsed_state
     , rpd.address->>'zipcode' AS parsed_postal_code
     , rpd.address->>'community' AS parsed_community
     , rpd.address->>'subdivision' AS parsed_subdivision
     , rpd.address->>'neighborhood' AS parsed_neighborhood
     , rpd.neighborhood_region->>'name' AS parsed_neighborhood_region
     , rpd.county
     , rpd.country
     , CASE
           WHEN rpd.date_posted = ''
               THEN NULL
           ELSE rpd.date_posted :: DATE
       END AS date_posted
     , CASE
           WHEN rpd.date_sold = ''
               THEN NULL
           ELSE rpd.date_sold :: DATE
       END AS date_sold
     , rpd.year_built
     , rpd.attribution_info->>'mlsId' AS mls_id
     , rpd.bathrooms AS bathroom_count
     , rpd.bedrooms AS bedroom_count
     , rpd.description AS zillow_property_description
     , rpd.property_tax_rate
     , lpd.last_extracted_at
     , rpd.created_at
     , rpd.updated_at
  FROM listing_property_dimensions AS lpd
       LEFT JOIN raw_property_details AS rpd
       ON lpd.zpid = rpd.zpid