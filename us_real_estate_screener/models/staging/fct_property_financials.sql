WITH raw_property_details AS (
    SELECT zpid
         , monthly_hoa_fee
         , annual_homeowners_insurance
         , property_tax_rate
         , reso_facts
         , updated_at
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
)

SELECT zpid AS property_zillow_id
     , monthly_hoa_fee
     , annual_homeowners_insurance
     , (reso_facts->>'taxAnnualAmount')::numeric AS tax_annual_amount
     , (reso_facts->>'taxAssessedValue')::numeric AS tax_assessed_value
     , property_tax_rate
     , updated_at AS last_updated_at
  FROM raw_property_details
