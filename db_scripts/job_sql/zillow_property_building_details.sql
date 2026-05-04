    SELECT DISTINCT building_id
      FROM public.zillow_property_details_raw
     WHERE building_id :: BIGINT NOT IN (
               SELECT DISTINCT building_id
                 FROM public.zillow_property_building_details
           )
     LIMIT 5