WITH price_history_details AS (
    SELECT zpid
         , jsonb_array_elements(price_history) AS price_record
         , jsonb_array_elements(price_history)->'attributeSource' AS attribute_source
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
)

SELECT zpid
     , price_record->>'date' AS as_of_date
     , price_record->>'time' AS as_of_time
     , price_record->>'event' AS event_type
     , price_record->>'price' AS price
     , price_record->>'source' AS source
     , price_record->'buyerAgent'->>'name' AS buyer_agent_name
     , price_record->'sellerAgent'->>'name' AS seller_agent_name
     , price_record->>'showCountyLink' AS show_county_link
     , attribute_source->>'infoString1' AS info_string1
     , attribute_source->>'infoString2' AS info_string2
     , attribute_source->>'infoString3' AS info_string3
     , price_record->'postingIsRental' AS is_listing_rental
     , price_record->'priceChangeRate' AS price_change_rate
     , price_record->'pricePerSquareFoot' AS price_per_square_foot
  FROM price_history_details