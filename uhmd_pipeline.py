import os
import json
from datetime import datetime
from dotenv import load_dotenv
import time
from api_scripts.housing_market_data_extractions import UhmdApi
from db_scripts.db_utils import extract_data, upsert_zillow_data

load_dotenv()

def run_uhmd_api_pipeline(job_type, api_max_retries=10, api_retry_delay=30):

    AVAILABLE_JOB_TYPES = [
        "property_location_search",
        "property_details",
        "property_comps",
        "property_transit_scores",
        "property_building_details",
        "zillow_monthly_inventory"
    ]

    if job_type not in AVAILABLE_JOB_TYPES:

        print("Job type not supported.  Exiting.")

    else:

        uhmd = UhmdApi(
            api_key=os.getenv("UHMD_API_KEY"),
            api_host=os.getenv("UHMD_API_HOST"),
            max_retries=api_max_retries,
            retry_delay=api_retry_delay
        )

        if job_type == "property_location_search":
            pass
        elif job_type == "property_details":
            pass
        elif job_type == "property_comps":
            pass
        elif job_type == "property_transit_scores":
            pass
        elif job_type == "property_building_details":
            pass
        elif job_type == "zillow_monthly_inventory":
            pass