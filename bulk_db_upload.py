from db_scripts.db_utils import upsert_zillow_data
import json
from pathlib import Path

def upload_historical_data(db_table_name, file_list):

    ALLOWED_DB_TABLES = [
        "zillow_listings_raw",
        "zillow_property_details_raw"
    ]

    if db_table_name not in ALLOWED_DB_TABLES:
        print(f"Historical upload process not supported for {db_table_name}")   

    else:

        for file in file_list:

            print(file)
            file_path = f"./temp_files/{file}"

            with open(file_path, "r") as f:
                data = json.load(f)

            if isinstance(data, dict):
                data = [data]

            if db_table_name == "zillow_listings_raw":
                records = []
                for record in data:
                    if record != []:
                        if record["totalResultCount"] != 0:
                            records.extend(record["props"])

            elif db_table_name == "zillow_property_details_raw":
                records = data

            upsert_zillow_data(records, db_table_name, True, file)

if __name__ == "__main__":

    hist_directory = Path("./temp_files/")

    zillow_listings_files = []
    zillow_properties_files = []

    for item in hist_directory.iterdir():

        if item.is_file():

            if "zillow_location_search_" in item.name:
                zillow_listings_files.append(item.name)

            elif "zillow_property_details_" in item.name:
                zillow_properties_files.append(item.name)

    upload_historical_data("zillow_listings_raw", zillow_listings_files)
    upload_historical_data("zillow_property_details_raw", zillow_properties_files)