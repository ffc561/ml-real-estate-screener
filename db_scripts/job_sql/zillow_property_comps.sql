SELECT DISTINCT zpid
  FROM public.zillow_property_details_raw 
 WHERE zpid NOT IN (
           SELECT DISTINCT zpid
             FROM public.zillow_property_comps
       )
   AND home_status = 'FOR_SALE'
 LIMIT 5