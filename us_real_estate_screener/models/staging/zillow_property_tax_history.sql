WITH tax_history_details AS (
    SELECT zpid
         , jsonb_array_elements(tax_history) AS tax_record
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
)

SELECT zpid
     , TO_TIMESTAMP((tax_record->>'time') :: BIGINT / 1000) :: DATE AS as_of_time
     , (tax_record->>'value') :: NUMERIC(18, 2) AS tax_appraisal_value
     , (tax_record->>'taxPaid') :: NUMERIC(12, 2) AS tax_paid
     , ((tax_record->>'taxPaid') :: NUMERIC / (tax_record->>'value') :: NUMERIC) :: NUMERIC(24,10) AS effective_tax_rate
     , (tax_record->>'taxIncreaseRate') :: NUMERIC(24, 10) AS tax_increase_rate
     , (tax_record->>'valueIncreaseRate') :: NUMERIC(24, 10) AS value_increase_rate
  FROM tax_history_details