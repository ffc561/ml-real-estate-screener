SELECT DISTINCT zip_code
  FROM public.us_zip_codes
 WHERE active IS TRUE
 LIMIT 5;