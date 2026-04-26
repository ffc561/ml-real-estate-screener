WITH nearby_home_records AS (
    SELECT zpid
         , jsonb_array_elements(nearby_homes) AS nearby_home_record
         , jsonb_array_elements(nearby_homes)->'address' AS nearby_home_address
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
)

SELECT zpid
     , nearby_home_record->>'price' AS price
     , nearby_home_record->>'homeType' AS home_type
     , nearby_home_record->>'propertyTypeDimension' AS property_type_dimension
     , nearby_home_record->>'homeStatus' AS home_status
     , nearby_home_record->>'hdpUrl' AS hdp_url
     , nearby_home_address->>'streetAddress' AS street_address
     , nearby_home_address->>'city' AS city
     , nearby_home_address->>'state' AS state
     , nearby_home_address->>'zipcode' AS zipcode
     , nearby_home_record->>'bedrooms' AS bedrooms
     , nearby_home_record->>'bathrooms' AS bathrooms
     , nearby_home_record->>'latitude' AS latitude
     , nearby_home_record->>'longitude' AS longitude
     , nearby_home_record->>'livingArea' AS living_area
     , nearby_home_record->>'livingAreaValue' AS living_area_value
     , nearby_home_record->>'livingAreaUnits' AS living_area_units
     , nearby_home_record->>'livingAreaUnitsShort' AS living_area_units_short
     , nearby_home_record->>'lotAreaValue' AS lot_area_value
     , nearby_home_record->>'lotAreaUnits' AS lot_area_units
     , nearby_home_record->'listing_sub_type' AS listing_sub_type
     , nearby_home_record->'attributionInfo'->>'mlsId' AS mls_id
     , nearby_home_record
  FROM nearby_home_records