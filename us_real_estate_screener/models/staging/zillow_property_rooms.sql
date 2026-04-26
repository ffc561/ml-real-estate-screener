SELECT zpid
     , jsonb_array_elements(reso_facts->'rooms')->'area' AS area
     , jsonb_array_elements(reso_facts->'rooms')->'level' AS "level"
     , jsonb_array_elements(reso_facts->'rooms')->'features' AS features
     , jsonb_array_elements(reso_facts->'rooms')->'roomArea' AS room_area
     , jsonb_array_elements(reso_facts->'rooms')->'roomType' AS room_type
     , jsonb_array_elements(reso_facts->'rooms')->'roomLevel' AS room_level
     , jsonb_array_elements(reso_facts->'rooms')->'roomWidth' AS room_width
     , jsonb_array_elements(reso_facts->'rooms')->'dimensions' AS dimensions
     , jsonb_array_elements(reso_facts->'rooms')->'roomLength' AS room_length
     , jsonb_array_elements(reso_facts->'rooms')->'description' AS "description"
     , jsonb_array_elements(reso_facts->'rooms')->'roomFeatures' AS room_features
     , jsonb_array_elements(reso_facts->'rooms')->'roomAreaUnits' AS room_area_units
     , jsonb_array_elements(reso_facts->'rooms')->'roomAreaSource' AS room_area_source
     , jsonb_array_elements(reso_facts->'rooms')->'roomDimensions' AS room_dimensions
     , jsonb_array_elements(reso_facts->'rooms')->'roomDescription' AS room_description
     , jsonb_array_elements(reso_facts->'rooms')->'roomLengthWidthUnits' AS room_length_width_units
     , jsonb_array_elements(reso_facts->'rooms')->'roomLengthWidthSource' AS room_length_width_source
  FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}