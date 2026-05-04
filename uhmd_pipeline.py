import os
import json
from datetime import datetime
from dotenv import load_dotenv
import time
from api_scripts.housing_market_data_extractions import UhmdApi
from db_scripts.db_utils import extract_data, upsert_zillow_data
from psycopg2 import sql

load_dotenv()

def run_uhmd_api_pipeline(job_type, api_max_retries=10, api_retry_delay=30):

    job_type_sql = sql.SQL(
        "SELECT * FROM public.elt_job_parameters WHERE job_type = %s"
    )

    job_type_params_data = extract_data(
        job_type_sql,
        (job_type,)
    )[0]

    print(job_type_params_data)

    if len(job_type_params_data) == 0:

        print("Job type not supported.  Exiting.")

    else:

        jt_params = {
            "job_type_name" : job_type_params_data[0],
            "data_source" : job_type_params_data[1],
            "id_col" : job_type_params_data[2],
            "compilation_type" : job_type_params_data[3]
        }

        print(jt_params)

        uhmd = UhmdApi(
            api_key=os.getenv("UHMD_API_KEY"),
            api_host=os.getenv("UHMD_API_HOST"),
            max_retries=api_max_retries,
            retry_delay=api_retry_delay
        )

        with open(f"db_scripts/job_sql/{job_type}.sql", "r") as f:
            input_sql = f.read()
        
        input_ids = [
            record[0] for record in extract_data(input_sql)
        ]

        api_records = []

        none_values = [None, [], [[]]]

        for id in input_ids:

            if job_type == "zillow_listings_raw":
                home_type_str = "Apartments,Condos,Houses,Multi-Family,Townhomes"
                detail = uhmd.get_property_extended_search(query_location=id, status_type="ForSale", home_type=home_type_str)
            elif job_type == "zillow_property_details":
                detail = uhmd.get_property_details_by_zpid(property_zpid=id)
            elif job_type == "zillow_property_comps":
                detail = uhmd.get_property_comps(zpid=id)
            elif job_type == "zillow_property_building_details":
                detail = uhmd.get_building_details(building_id=id)
            elif job_type == "zillow_monthly_inventory":
                detail = uhmd.get_monthly_inventory(zipcode=id)
            elif job_type == "zillow_property_transit_scores":
                detail = uhmd.get_transit_scores_by_zpid(property_zpid=id)
            
            if detail in none_values:

                print("API call returned no results")

                if job_type not in ["zillow_listings_raw", "zillow_monthly_inventory"]:

                    print("Creating stub record")
                    record = {}
                    record[jt_params["id_col"]] = id

                    if job_type == "zillow_property_comps":
                        record["as_of_date"] = datetime.today().strftime("%Y-%m-%d")
                        record["comps"] = []

                    if jt_params["compilation_type"] == "append":
                        api_records.append(record)
                    elif jt_params["compilation_type"] == "extend":
                        api_records.extend(record)

                else:

                    print("Skipping")

            else:

                if job_type == "zillow_listings_raw":
                    if detail["totalResultCount"] != 0:
                        record = detail["props"]
                    else:
                        print("No properties found for this zip code.  Skipping.")
                        continue
                elif job_type == "zillow_property_comps":
                    record = {}
                    record[jt_params["id_col"]] = id
                    record["as_of_date"] = datetime.today().strftime("%Y-%m-%d")
                    record["comps"] = detail["comps"]
                else:
                    record = detail
                    record[jt_params["id_col"]] = id
                
                if jt_params["compilation_type"] == "append":
                    api_records.append(record)
                elif jt_params["compilation_type"] == "extend":
                    api_records.extend(record)

        extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")
        json_filepath = f"./temp_files/{job_type}_{extraction_dt}.json"

        with open(json_filepath, "w") as file:
            file = json.dump(api_records, file, indent = 4)

        print(api_records)

        #upsert_zillow_data(api_records, job_type)
        
if __name__ == "__main__":
    job_type = input("Enter job type to run: ")
    run_uhmd_api_pipeline(job_type)