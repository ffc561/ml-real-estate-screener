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
cities_list = [
    "Atlantis, FL",
    #"Belle Glade, FL",
    #"Boca Raton, FL",
    #"Boynton Beach, FL",
    #"Briny Breezes, FL",
    #"Cloud Lake, FL",
    #"Delray Beach, FL",
    #"Glen Ridge, FL",
    #"Golf, FL"
    #"Greenacres, FL",
    #"Gulf Stream, FL",
    #"Haverhill, FL",
    #"Highland Beach, FL",
    #"Hobe Sound, FL",
    #"Hypoluxo, FL",
    #"Juno Beach, FL",
    #"Jupiter, FL",
    #"Jupiter Inlet Colony, FL",
    #"Jupiter Island, FL",
    #"Lake Clarke Shores, FL",
    #"Lake Park, FL",
    #"Lake Worth, FL",
    #"Lake Worth Beach, FL",
    #"Lantana, FL",
    #"Loxahatchee Groves, FL",
    #"Manalapan, FL",
    #"Mangonia Park, FL",
    #"North Palm Beach, FL",
    #"Ocean Ridge, FL",
    #"Pahokee, FL",
    #"Palm Beach, FL",
    #"Palm Beach Gardens, FL",
    #"Palm Beach Shores, FL",
    #"Palm Springs, FL",
    #"Palm City, FL",
    #"Riviera Beach, FL",
    #"Royal Palm Beach, FL",
    #"South Bay, FL",
    #"South Palm Beach, FL",
    "Stuart, FL",
    "Tequesta, FL",
    #"Wellington, FL",
    #"Westlake, FL",
    #"West Palm Beach, FL"
]

home_types_str = "Apartments,Condos,Houses,Multi-Family,Townhomes"

zillow = ZillowAPI(ZILLOW_API_KEY, ZILLOW_API_HOST, 3, 5)

zillow_results_list = []

for city in cities_list:
    location_json = zillow.get_property_extended_search(city, "ForSale", home_types_str)
    zillow_results_list.extend(location_json)

extraction_dt = datetime.now().strftime("%Y%m%d%H%M%S")

with open("temp_files/zillow_location_search_"+extraction_dt+".json") as file:
    file = json.dump(zillow_results_list)

del extraction_dt

zillow_locations_df = transform_property_search_json(zillow_results_list)

transformation_dt = datetime.now().strftime("%Y%m%d%H%M%S")

zillow_locations_df.to_csv("temp_files/zillow_location_search_"+transformation_dt+".csv", index=False)