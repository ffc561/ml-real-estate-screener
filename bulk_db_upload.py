from db_scripts.db_utils import insert_zillow_listings_data
import os
import json

historical_listings_files = [
    "zillow_location_search_20250321003842",
    "zillow_location_search_20250321003952",
    "zillow_location_search_20250417002000",
    "zillow_location_search_20250417003402",
    "zillow_location_search_20251229122008",
    "zillow_location_search_20251230102041",
    "zillow_location_search_20260120212304",
    "zillow_location_search_20260217011412",
    "zillow_location_search_20260217025029",
    "zillow_location_search_20260217195522",
    "zillow_location_search_20260220205838",
    "zillow_location_search_20260305225110",
    "zillow_location_search_20260307135946",
    "zillow_location_search_20260420224058",
    "zillow_location_search_20260422192557"
]

for file in historical_listings_files:
    filename = f"./temp_files/{file}.json"
    with open(filename, "r") as f:
        data = json.load(f)
    property_records = []
    for payload in data:
        if payload != []:
            if payload["totalResultCount"] != 0:
                property_records.extend(payload["props"])
    insert_zillow_listings_data(property_records, True, file)