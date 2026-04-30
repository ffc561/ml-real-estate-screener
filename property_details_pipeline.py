import pandas as pd
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv
from db_scripts.db_utils import extract_data, upsert_zillow_data
from api_scripts.housing_market_data_extractions import UhmdApi

load_dotenv()
uhmd = UhmdApi(api_key = os.getenv("UHMD_API_KEY"), api_host = os.getenv("UHMD_API_HOST"), max_retries = 10, retry_delay = 60)

zpids_query = f"""
SELECT DISTINCT zpid
  FROM public.zillow_listings_raw
 WHERE zpid NOT IN (SELECT DISTINCT zpid FROM public.zillow_property_details_raw)
 LIMIT 502
"""

zpids_list = [record[0] for record in extract_data(zpids_query)]

property_details_list = []

print(f"Number of properties to extract data on: {len(zpids_list)}")

for zpid in zpids_list:

    print(f"Property ID: {zpid}")
    detail = uhmd.get_property_details_by_zpid(zpid)

    if detail is not None:
        if "zpid" in detail and detail["zpid"] is not None:
            property_details_list.append(detail)
        else:
            print(f"Invalid record for {zpid}. Skipping")
            print(detail)
    else:
        print(f"No result found for {zpid}.  Skipping")

    time.sleep(1)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = f"./temp_files/zillow_property_details_{extraction_dt}.json"

with open(json_filepath, "w") as file:
    file = json.dump(property_details_list, file, indent = 4)

upsert_zillow_data(property_details_list, "zillow_property_details_raw")