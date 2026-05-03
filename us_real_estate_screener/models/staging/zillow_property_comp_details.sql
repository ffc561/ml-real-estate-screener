WITH comps_raw AS (
    SELECT zpid AS target_property_zpid
         , as_of_date
         , jsonb_array_elements(comps) AS comp_record
      FROM {{ source('raw_zillow', 'zillow_property_comps') }}
)

SELECT target_property_zpid
     , as_of_date
     , (comp_record->>'zpid')::bigint AS comp_zpid
     , (comp_record->>'price')::numeric AS comp_price
     , comp_record->>'homeStatus' AS comp_home_status
     , comp_record->>'homeType' AS comp_home_type
     , (comp_record->>'bedrooms')::integer AS comp_bedrooms
     , (comp_record->>'bathrooms')::numeric AS comp_bathrooms
     , (comp_record->>'livingArea')::numeric AS comp_living_area
     , comp_record->>'livingAreaUnitsShort' AS comp_living_area_units
     , (comp_record->>'latitude')::double precision AS comp_latitude
     , (comp_record->>'longitude')::double precision AS comp_longitude
     , comp_record->'address'->>'streetAddress' AS comp_address
     , comp_record->'address'->>'city' AS comp_city
     , comp_record->'address'->>'state' AS comp_state
     , comp_record->'address'->>'zipcode' AS comp_zipcode
     , comp_record->>'hdpUrl' AS comp_zillow_url
     , comp_record->'attributionInfo'->>'mlsId' AS comp_mls_id
     , comp_record->'attributionInfo'->>'brokerName' AS comp_broker_name
  FROM comps_raw
