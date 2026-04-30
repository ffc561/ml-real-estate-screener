import os
import json
from datetime import datetime
from dotenv import load_dotenv
import time
from api_scripts.housing_market_data_extractions import UhmdApi
from db_scripts.db_utils import extract_data, upsert_zillow_data

load_dotenv()
UHMD_API_KEY = os.getenv("UHMD_API_KEY")
UHMD_API_HOST = os.getenv("UHMD_API_HOST")

uhmd = UhmdApi(api_key = UHMD_API_KEY, api_host = UHMD_API_HOST, max_retries = 10, retry_delay = 30)

property_comps_sql = """
    SELECT DISTINCT zpid
      FROM public.zillow_listings_raw
     WHERE zpid NOT IN (SELECT DISTINCT zpid FROM public.zillow_property_comps)
     LIMIT 100
"""

comps_zpids = [record[0] for record in extract_data(property_comps_sql)]

comps_details = []

for zpid in comps_zpids:
    detail = uhmd.get_property_comps(zpid)
    if detail is not None:
        record = {}
        record["zpid"] = zpid
        record["as_of_date"] = datetime.today().strftime('%Y-%m-%d')
        record["comps"] = detail["comps"]
        comps_details.append(record)
    else:
        print(f"Transit scores not found for {zpid}.  Skipping.")
    
    time.sleep(2)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = f"./temp_files/zillow_property_comps_{extraction_dt}.json"

with open(json_filepath, "w") as file:
    file = json.dump(comps_details, file, indent = 4)

if len(comps_details) != 0:
    upsert_zillow_data(comps_details, "zillow_property_comps")