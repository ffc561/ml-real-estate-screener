WITH nearby_school_records AS (
    SELECT zpid
         , jsonb_array_elements(schools) as nearby_school_record
      FROM {{ source('raw_zillow', 'zillow_property_details_raw') }}
)

SELECT zpid
     , nearby_school_record->>'link' AS school_link
     , nearby_school_record->>'name' AS school_name
     , nearby_school_record->>'size' AS school_size
     , nearby_school_record->>'type' AS school_type
     , nearby_school_record->>'level' AS school_level
     , nearby_school_record->>'grades' AS school_grades
     , nearby_school_record->>'rating' AS school_rating
     , nearby_school_record->>'assigned' AS school_assigned
     , nearby_school_record->>'distance' AS property_distance_to_school
     , nearby_school_record->>'isAssigned' AS is_school_assigned
     , nearby_school_record->>'totalCount' AS total_count
     , nearby_school_record->>'studentsPerTeacher' AS students_per_teacher
  FROM nearby_school_records