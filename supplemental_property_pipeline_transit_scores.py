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

transit_scores_sql = """
    SELECT DISTINCT zpid
      FROM public.zillow_property_details
     WHERE zpid NOT IN (SELECT DISTINCT zpid FROM public.zillow_property_transit_scores)
       AND building_id IS NULL
     LIMIT 5
"""

transit_score_zpids = [record[0] for record in extract_data(transit_scores_sql)]

transit_score_details = []

for zpid in transit_score_zpids:
    detail = uhmd.get_transit_scores_by_zpid(zpid)
    if detail is not None:
        detail["zpid"] = zpid
        transit_score_details.append(detail)
    else:
        print(f"Transit scores not found for {zpid}.  Skipping.")
    
    time.sleep(2)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = f"./temp_files/zillow_transit_scores_{extraction_dt}.json"

with open(json_filepath, "w") as file:
    file = json.dump(transit_score_details, file, indent = 4)

if len(transit_score_details) != 0:
    upsert_zillow_data(transit_score_details, "zillow_property_transit_scores")