import pandas as pd
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv
from housing_market_data_api_scripts.housing_market_data_extractions import UhmdApi
from housing_market_data_api_scripts.housing_market_data_transformations import transform_individual_property_detail_records, explode_nested_property_details

load_dotenv()
UHMD_API_KEY = os.getenv("UHMD_API_KEY")
UHMD_API_HOST = os.getenv("UHMD_API_HOST")
uhmd = UhmdApi(api_key = UHMD_API_KEY, api_host = UHMD_API_HOST, max_retries = 10, retry_delay = 60)

# Get list of properties that require a detail lookup
# NOTE: Replace this with database query once db support is built out
temp_filepath = './temp_files/zillow_location_search_20251229122008.csv'
properties_df = pd.read_csv(temp_filepath)

zpids_list = properties_df['zpid'].unique().tolist()

del properties_df

property_details_list = []

#Temporarily limited to first 100 ids for testing
print(f"Number of properties to extract data on: {len(zpids_list)}")

for zpid in zpids_list[100:225]:
    print(f"Property ID: {zpid}")
    detail = uhmd.get_property_details_by_zpid(zpid)
    time.sleep(5)
    if detail is not None:
        property_details_list.append(detail)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = "./temp_files/zillow_property_details_"+extraction_dt+".json"

with open(json_filepath, "w") as file:
    file = json.dump(property_details_list, file, indent = 4)

del extraction_dt

transformation_dt = datetime.now().strftime("%Y%m%d%H%M%S")

zillow_property_details_df = transform_individual_property_detail_records(json_filepath)
zillow_property_details_df.to_csv("temp_files/zillow_property_details_"+transformation_dt+".csv", index = False)

zillow_property_tax_history_df = explode_nested_property_details(json_filepath, "taxHistory")
zillow_property_tax_history_df.to_csv("temp_files/zillow_property_tax_history_"+transformation_dt+".csv", index = False)

zillow_property_price_history_df = explode_nested_property_details(json_filepath, "priceHistory")
zillow_property_price_history_df.to_csv("temp_files/zillow_property_price_history_"+transformation_dt+".csv", index = False)