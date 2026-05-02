import os
import json
from datetime import datetime
from dotenv import load_dotenv
from api_scripts.housing_market_data_extractions import UhmdApi
from db_scripts.db_utils import extract_data, upsert_zillow_data

load_dotenv()
UHMD_API_KEY = os.getenv("UHMD_API_KEY")
UHMD_API_HOST = os.getenv("UHMD_API_HOST")

uhmd = UhmdApi(api_key = UHMD_API_KEY, api_host = UHMD_API_HOST, max_retries = 10, retry_delay = 30)

zip_codes_list = [
    "33401",
    "33402",
    "33403",
    "33404",
    "33405",
    "33406",
    "33407",
    "33408",
    "33409",
    "33410",
    "33411",
    "33412",
    "33413",
    "33414",
    "33415",
    "33416",
    "33417",
    "33426",
    "33428",
    "33431",
    "33432",
    "33433",
    "33434",
    "33435",
    "33436",
    "33437",
    "33438",
    "33444",
    "33445",
    "33446",
    "33458",
    "33460",
    "33461",
    "33462",
    "33463",
    "33467",
    "33469",
    "33470",
    "33472",
    "33473",
    "33475",
    "33477",
    "33478",
    "33480",
    "33483",
    "33484",
    "33486",
    "33487",
    "33496"
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