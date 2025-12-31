import os
import json
from datetime import datetime
from dotenv import load_dotenv
import time
from housing_market_data_api_scripts.housing_market_data_extractions import UhmdApi
from housing_market_data_api_scripts.housing_market_data_transformations import transform_property_search_json

load_dotenv()
UHMD_API_KEY = os.getenv("UHMD_API_KEY")
UHMD_API_HOST = os.getenv("UHMD_API_HOST")

# Change these lists to DB calls in future version
zip_codes_list = [
    "33401",
    "33402",
    "33403",
    "33404",
    "33405",
    "33406",
    #"33407",
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

home_types_str = "Apartments,Condos,Houses,Multi-Family,Townhomes"

zillow = UhmdApi(api_key = UHMD_API_KEY, api_host = UHMD_API_HOST, max_retries = 10, retry_delay = 30)

zillow_results_list = []

for zip_code in zip_codes_list:
    print(f"ZIP Code: {zip_code}")
    location_json = zillow.get_property_extended_search(zip_code, "ForSale", home_types_str)
    print(location_json)
    if (location_json is not None) & (location_json != []):
        zillow_results_list.extend(location_json)
    time.sleep(5)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = "./temp_files/zillow_location_search_"+extraction_dt+".json"

with open(json_filepath, "w") as file:
    file = json.dump(zillow_results_list, file, indent = 4)

del extraction_dt

zillow_locations_df = transform_property_search_json(json_filepath)

transformation_dt = datetime.now().strftime("%Y%m%d%H%M%S")

zillow_locations_df.to_csv("temp_files/zillow_location_search_"+transformation_dt+".csv", index=False)