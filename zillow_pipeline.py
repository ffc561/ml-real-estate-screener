import os
from dotenv import load_dotenv
from zillow_api_scripts.zillow_extractions import ZillowAPI

load_dotenv()
ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")
ZILLOW_API_HOST = os.getenv("ZILLOW_API_HOST")

zillow = ZillowAPI(ZILLOW_API_KEY, ZILLOW_API_HOST, 3, 5)