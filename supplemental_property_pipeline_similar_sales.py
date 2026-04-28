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

similar_sales_sql = """
    SELECT DISTINCT zpid
      FROM public.zillow_listings_raw
     WHERE zpid NOT IN (SELECT DISTINCT zpid FROM public.zillow_property_similar_sales)
     LIMIT 1
"""

similar_sales_zpids = [record[0] for record in extract_data(similar_sales_sql)]

similar_sales_details = []

for zpid in similar_sales_zpids:
    detail = uhmd.get_property_similar_sales(zpid)
    if detail is not None:
        record = {}
        record["zpid"] = zpid
        record["as_of_date"] = datetime.today().strftime('%Y-%m-%d')
        record["similar_sales"] = detail
        similar_sales_details.append(record)
    else:
        print(f"Transit scores not found for {zpid}.  Skipping.")
    
    time.sleep(2)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = f"./temp_files/zillow_similar_sales_{extraction_dt}.json"

with open(json_filepath, "w") as file:
    file = json.dump(similar_sales_details, file, indent = 4)

if len(similar_sales_details) != 0:
    upsert_zillow_data(similar_sales_details, "zillow_property_similar_sales")