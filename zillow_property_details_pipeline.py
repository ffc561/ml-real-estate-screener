import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from zillow_api_scripts.zillow_extractions import ZillowAPI
from zillow_api_scripts.zillow_transformations import transform_individual_property_json

load_dotenv()
ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")
ZILLOW_API_HOST = os.getenv("ZILLOW_API_HOST")
zillow = ZillowAPI(zillow_api_key = ZILLOW_API_KEY, zillow_api_host = ZILLOW_API_HOST, max_retries = 3, retry_delay = 5)

# Get list of properties that require a detail lookup
# NOTE: Replace this with database query once db support is built out
temp_filepath = './temp_files/zillow_location_search_20250413233704.csv'
properties_df = pd.read_csv(temp_filepath)

zpids_list = properties_df['zpid'].unique().tolist()

del properties_df

property_details_list = []

#Temporarily limited to first 100 ids for testing
for zpid in zpids_list[:99]:
    detail = zillow.get_property_details_by_zpid(zpid)
    property_details_list.append(detail)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

json_filepath = "./temp_files/zillow_property_details_"+extraction_dt+".json"

with open(json_filepath, "w") as file:
    file = json.dump(property_details_list, file, indent = 4)

del extraction_dt

transformation_dt = datetime.now().strftime("%Y%m%d%H%M%S")

zillow_locations_df = transform_individual_property_json(json_filepath)
zillow_locations_df.to_csv("temp_files/zillow_property_details_"+transformation_dt+".csv", index = False)