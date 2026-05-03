WITH all_zpids AS (
    SELECT zpid FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
    UNION
    SELECT zpid FROM {{ source('raw_zillow', 'zillow_listings_raw') }}
)

SELECT az.zpid AS property_zillow_id
     , lpd.address as full_address
     , COALESCE(rpd.home_type, lpd.property_type) AS property_type
     , bd.building_type
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
     , rpd.year_built
     , rpd.attribution_info->>'mlsId' AS mls_id
     , rpd.bedrooms AS bedroom_count
     , rpd.bathrooms AS total_bathroom_count
     , (rpd.reso_facts->>'bathroomsFull')::integer AS bathrooms_full_count
     , (rpd.reso_facts->>'bathroomsHalf')::integer AS bathrooms_half_count
     , COALESCE(rpd.living_area, lpd.living_area) AS living_area_sqft
     
     -- Lot Area Feature Engineering
     , CASE 
         WHEN rpd.reso_facts->>'lotSize' LIKE '%Acres%' 
           THEN REPLACE(REPLACE(rpd.reso_facts->>'lotSize', ' Acres', ''), ',', '')::numeric * 43560
         WHEN rpd.reso_facts->>'lotSize' LIKE '%sqft%' 
           THEN REPLACE(REPLACE(rpd.reso_facts->>'lotSize', ' sqft', ''), ',', '')::numeric
         ELSE lpd.lot_area_value 
       END AS lot_area_sqft
     
     -- Structural Details
     , rpd.reso_facts->>'architecturalStyle' AS architectural_style
     , COALESCE(bd.building_name, rpd.reso_facts->>'buildingName') AS building_name
     , (rpd.reso_facts->>'stories')::numeric AS stories_count
     , (rpd.reso_facts->>'parkingCapacity')::numeric AS parking_capacity
     , (rpd.reso_facts->>'garageParkingCapacity')::numeric AS garage_parking_capacity
     , (rpd.reso_facts->>'coveredParkingCapacity')::numeric AS covered_parking_capacity
     , rpd.reso_facts->>'levels' AS levels_description
     , rpd.reso_facts->>'basement' AS basement_description
     , rpd.reso_facts->>'roofType' AS roof_type
     , rpd.reso_facts->>'foundationDetails' AS foundation_details
     , rpd.reso_facts->>'constructionMaterials' AS construction_materials
     , rpd.reso_facts->>'exteriorFeatures' AS exterior_features
     , rpd.reso_facts->>'flooring' AS flooring_types
     , rpd.reso_facts->>'interiorFeatures' AS interior_features
     , rpd.reso_facts->>'appliances' AS appliances_list
     , rpd.reso_facts->>'cooling' AS cooling_systems
     , rpd.reso_facts->>'heating' AS heating_systems
     , (rpd.reso_facts->>'fireplaces')::numeric AS fireplace_count
     , rpd.reso_facts->>'sewer' AS sewer_description
     , rpd.reso_facts->>'waterSource' AS water_source
     , rpd.reso_facts->>'zoning' AS zoning_code
     , rpd.reso_facts->>'parcelNumber' AS parcel_number
     , rpd.reso_facts->>'subdivisionName' AS subdivision_name
     , rpd.reso_facts->>'propertyCondition' AS property_condition
     , rpd.reso_facts->>'listingTerms' AS listing_terms

     -- ML One-Hot Encoded Features (Property Types)
     , CASE WHEN COALESCE(rpd.home_type, lpd.property_type) = 'SINGLE_FAMILY' THEN 1 ELSE 0 END AS is_single_family
     , CASE WHEN COALESCE(rpd.home_type, lpd.property_type) = 'CONDO' THEN 1 ELSE 0 END AS is_condo
     , CASE WHEN COALESCE(rpd.home_type, lpd.property_type) = 'TOWNHOUSE' THEN 1 ELSE 0 END AS is_townhouse
     , CASE WHEN COALESCE(rpd.home_type, lpd.property_type) = 'MULTI_FAMILY' THEN 1 ELSE 0 END AS is_multi_family
     , CASE WHEN COALESCE(rpd.home_type, lpd.property_type) = 'APARTMENT' THEN 1 ELSE 0 END AS is_apartment

     -- ML One-Hot Encoded Features (Architectural Styles)
     , CASE WHEN rpd.reso_facts->>'architecturalStyle' ILIKE '%Ranch%' THEN 1 ELSE 0 END AS is_architectural_style_ranch
     , CASE WHEN rpd.reso_facts->>'architecturalStyle' ILIKE '%Colonial%' THEN 1 ELSE 0 END AS is_architectural_style_colonial
     , CASE WHEN rpd.reso_facts->>'architecturalStyle' ILIKE '%Mediterranean%' THEN 1 ELSE 0 END AS is_architectural_style_mediterranean
     , CASE WHEN rpd.reso_facts->>'architecturalStyle' ILIKE '%Traditional%' THEN 1 ELSE 0 END AS is_architectural_style_traditional
     , CASE WHEN rpd.reso_facts->>'architecturalStyle' ILIKE '%Contemporary%' THEN 1 ELSE 0 END AS is_architectural_style_contemporary

     -- ML One-Hot Encoded Features (Construction Materials)
     , CASE WHEN rpd.reso_facts->>'constructionMaterials' ILIKE '%Block%' THEN 1 ELSE 0 END AS is_construction_material_block
     , CASE WHEN rpd.reso_facts->>'constructionMaterials' ILIKE '%Concrete%' THEN 1 ELSE 0 END AS is_construction_material_concrete
     , CASE WHEN rpd.reso_facts->>'constructionMaterials' ILIKE '%Stucco%' THEN 1 ELSE 0 END AS is_construction_material_stucco
     , CASE WHEN rpd.reso_facts->>'constructionMaterials' ILIKE '%Masonry%' THEN 1 ELSE 0 END AS is_construction_material_masonry

     -- ML Binary Features (Amenity & Structural Flags)
     , COALESCE((rpd.reso_facts->>'hasGarage')::boolean, false) AS has_garage
     , COALESCE((rpd.reso_facts->>'hasAttachedGarage')::boolean, false) AS has_attached_garage
     , COALESCE((rpd.reso_facts->>'hasCooling')::boolean, false) AS has_cooling
     , COALESCE((rpd.reso_facts->>'hasHeating')::boolean, false) AS has_heating
     , COALESCE((rpd.reso_facts->>'hasFireplace')::boolean, false) AS has_fireplace
     , COALESCE((rpd.reso_facts->>'hasSpa')::boolean, false) AS has_spa
     , COALESCE((rpd.reso_facts->>'hasView')::boolean, false) AS has_view
     , COALESCE((rpd.reso_facts->>'hasWaterfrontView')::boolean, false) AS has_waterfront_view
     , COALESCE((rpd.reso_facts->>'hasAssociation')::boolean, false) AS has_association
     , COALESCE((rpd.reso_facts->>'isNewConstruction')::boolean, false) AS is_new_construction
     , COALESCE((rpd.reso_facts->>'isSeniorCommunity')::boolean, bd.is_senior_housing, false) AS is_senior_community
     , COALESCE((rpd.reso_facts->>'hasHomeWarranty')::boolean, false) AS has_home_warranty
     , COALESCE(bd.is_low_income, false) AS is_low_income_building
     , COALESCE(bd.is_student_housing, false) AS is_student_housing_building
     
     -- Location Scores (useful for ML)
     , (bd.walk_score->>'walkscore')::integer AS walk_score
     , (bd.transit_score->>'transit_score')::integer AS transit_score
     , (bd.bike_score->>'bikescore')::integer AS bike_score

     -- Amenity Counts (useful for ML)
     , jsonb_array_length(CASE WHEN jsonb_typeof(rpd.reso_facts->'rooms') = 'array' THEN rpd.reso_facts->'rooms' ELSE '[]'::jsonb END) AS rooms_count
     , jsonb_array_length(CASE WHEN jsonb_typeof(rpd.reso_facts->'appliances') = 'array' THEN rpd.reso_facts->'appliances' ELSE '[]'::jsonb END) AS appliances_count
     , jsonb_array_length(CASE WHEN jsonb_typeof(rpd.reso_facts->'interiorFeatures') = 'array' THEN rpd.reso_facts->'interiorFeatures' ELSE '[]'::jsonb END) AS interior_features_count
     , jsonb_array_length(CASE WHEN jsonb_typeof(rpd.reso_facts->'communityFeatures') = 'array' THEN rpd.reso_facts->'communityFeatures' ELSE '[]'::jsonb END) AS community_features_count
     , jsonb_array_length(CASE WHEN jsonb_typeof(rpd.reso_facts->'lotFeatures') = 'array' THEN rpd.reso_facts->'lotFeatures' ELSE '[]'::jsonb END) AS lot_features_count

     -- Market Activity Dates
     , CASE 
         WHEN rpd.reso_facts->>'onMarketDate' IS NOT NULL 
         THEN TO_TIMESTAMP((rpd.reso_facts->>'onMarketDate')::bigint / 1000)::DATE 
         ELSE NULL 
       END AS on_market_date

     -- Descriptions and Metadata
     , rpd.description AS structural_description
     , lpd.last_extracted_at
     , rpd.created_at
     , rpd.updated_at
  FROM all_zpids AS az
       LEFT JOIN {{ ref('latest_zillow_listings') }} AS lpd
       ON az.zpid = lpd.zpid
       LEFT JOIN {{ source('raw_zillow', 'zillow_property_details_raw') }} AS rpd
       ON az.zpid = rpd.zpid
       LEFT JOIN {{ source('raw_zillow', 'zillow_property_building_details') }} AS bd
       ON rpd.building_id::bigint = bd.building_id
