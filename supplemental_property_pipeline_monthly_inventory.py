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

zip_codes_list = [
    "33407",
    "33415"
]

inventory_details = []

for zip_code in zip_codes_list:
    print(f"ZIP Code: {zip_code}")
    detail = uhmd.get_monthly_inventory(zip_code)
    if detail is not None:
        inventory_details.extend(detail)

print(inventory_details)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = f"./temp_files/zillow_monthly_inventory_{extraction_dt}.json"

with open(json_filepath, "w") as file:
    file = json.dump(inventory_details, file, indent = 4)

upsert_zillow_data(inventory_details, "zillow_monthly_inventory")