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

building_ids_sql = """
    SELECT DISTINCT building_id
      FROM public.zillow_property_details_raw
     WHERE building_id :: BIGINT NOT IN (SELECT DISTINCT building_id FROM public.zillow_property_building_details)
     LIMIT 5
"""

building_ids = [record[0] for record in extract_data(building_ids_sql)]

building_details = []

for building_id in building_ids:
    detail = uhmd.get_building_details(building_id)
    if detail is not None:
        detail["building_id"] = building_id
        building_details.append(detail)
    else:
        print(f"Building deatils not found for {building_id}.  Skipping.")
    
    time.sleep(2)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = f"./temp_files/zillow_building_details_{extraction_dt}.json"

with open(json_filepath, "w") as file:
    file = json.dump(building_details, file, indent = 4)

if len(building_details) != 0:
    upsert_zillow_data(building_details, "zillow_property_building_details")