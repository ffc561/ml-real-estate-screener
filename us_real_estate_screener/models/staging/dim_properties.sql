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
     , rpd.year_built
     , rpd.attribution_info->>'mlsId' AS mls_id
     , rpd.bathrooms AS bathroom_count
     , rpd.bedrooms AS bedroom_count
     , COALESCE(rpd.living_area, lpd.living_area) AS living_area_sqft
     , lpd.lot_area_value
     , lpd.lot_area_unit
     -- Structural Details from reso_facts
     , rpd.reso_facts->>'architecturalStyle' AS architectural_style
     , rpd.reso_facts->>'buildingName' AS building_name
     , (rpd.reso_facts->>'stories')::numeric AS stories_count
     , (rpd.reso_facts->>'parkingCapacity')::numeric AS parking_capacity
     , (rpd.reso_facts->>'isNewConstruction')::boolean AS is_new_construction
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
     -- Descriptions and Metadata
     , rpd.description AS structural_description
     , lpd.last_extracted_at
     , rpd.created_at
     , rpd.updated_at
  FROM all_zpids AS az
       LEFT JOIN latest_listings AS lpd ON az.zpid = lpd.zpid
       LEFT JOIN raw_property_details AS rpd ON az.zpid = rpd.zpid
