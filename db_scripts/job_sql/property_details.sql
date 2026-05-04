SELECT DISTINCT zpid
  FROM public.zillow_listings_raw
 WHERE zpid NOT IN (SELECT DISTINCT zpid FROM public.zillow_property_details_raw)
 LIMIT 502