import os
import json
from datetime import datetime
from dotenv import load_dotenv
from zillow_api_scripts.zillow_extractions import ZillowAPI
from zillow_api_scripts.zillow_transformations import transform_property_search_json

load_dotenv()
ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")
ZILLOW_API_HOST = os.getenv("ZILLOW_API_HOST")

# Change these lists to DB calls in future version
zip_codes_list = [
    "33401",
    "33477",
    "33407"
]

home_types_str = "Apartments,Condos,Houses,Multi-Family,Townhomes"

zillow = ZillowAPI(ZILLOW_API_KEY, ZILLOW_API_HOST, 3, 5)

zillow_results_list = []

for zip_code in zip_codes_list:
    location_json = zillow.get_property_extended_search(zip_code, "ForSale", home_types_str)
    zillow_results_list.extend(location_json)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = "./temp_files/zillow_location_search_"+extraction_dt+".json"

with open(json_filepath, "w") as file:
    file = json.dump(zillow_results_list, file, indent = 4)

del extraction_dt

zillow_locations_df = transform_property_search_json(json_filepath)

transformation_dt = datetime.now().strftime("%Y%m%d%H%M%S")

zillow_locations_df.to_csv("temp_files/zillow_location_search_"+transformation_dt+".csv", index=False)