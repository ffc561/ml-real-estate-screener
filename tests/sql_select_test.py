from ..db_scripts.db_utils import extract_data
import pandas as pd

query = """
SELECT DISTINCT zpid
  FROM public.zillow_listings_raw
 WHERE zpid NOT IN (SELECT DISTINCT zpid FROM public.zillow_property_details_raw)
"""

data = extract_data(query)
unique_zpids = [record[0] for record in data]
print(len(unique_zpids))
