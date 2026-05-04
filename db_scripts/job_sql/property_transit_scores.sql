SELECT DISTINCT zpid
  FROM public.zillow_property_details
 WHERE zpid NOT IN (
           SELECT DISTINCT zpid
             FROM public.zillow_property_transit_scores
       )
   AND building_id IS NULL
 LIMIT 5