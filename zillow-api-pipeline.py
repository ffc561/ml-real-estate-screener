import os
from dotenv import load_dotenv

load_dotenv()
ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")
ZILLOW_API_HOST = os.getenv("ZILLOW_API_HOST")