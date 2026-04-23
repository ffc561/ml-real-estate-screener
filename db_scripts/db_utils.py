import psycopg2
from psycopg2 import extras
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_SERVICE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def insert_zillow_listings_data(json_payload, historical_upload=False, filename=""):
    # Parse JSON if it's a string
    data = json.loads(json_payload) if isinstance(json_payload, str) else json_payload
    
    # Ensure data is a list of dictionaries
    if isinstance(data, dict):
        data = [data]

    # Prepare the query
    insert_query = """
    INSERT INTO public.zillow_listings_raw (
        zpid, address, unit, latitude, longitude, num_bedrooms, num_bathrooms, 
        living_area, lot_area_value, lot_area_unit, price, rent_zestimate, 
        zestimate, has_3d_model, has_video, has_image, property_type, 
        listing_status, listing_subtype, detail_url, 
        days_on_zillow, country, currency, extracted_at
    ) VALUES %s
    ON CONFLICT (zpid) DO UPDATE SET
        price = EXCLUDED.price,
        zestimate = EXCLUDED.zestimate,
        listing_status = EXCLUDED.listing_status,
        extracted_at = EXCLUDED.extracted_at;
    """

    # Transform list of dicts to list of tuples for psycopg2
    # Ensure keys match your table column names
    if historical_upload is True:
        extract_ts = datetime.strptime(filename.replace("zillow_location_search_", ""), "%Y%m%d%H%M%S")
    else:
        extract_ts = datetime.now()

    values = [
        (
            item['zpid'], item.get('address'), item.get('unit'), 
            item['latitude'], item['longitude'], item['bedrooms'], 
            item['bathrooms'], item['livingArea'], item['lotAreaValue'], 
            item['lotAreaUnit'], item['price'], item['rentZestimate'], 
            item['zestimate'], item['has3DModel'], item['hasVideo'], 
            item['hasImage'], item.get('propertyType'), item['listingStatus'], 
            json.dumps(item['listingSubType']), item['detailUrl'], 
            item['daysOnZillow'], item['country'], item['currency'], 
            extract_ts
        ) for item in data if item != [[]] and item != []
    ]

    print(values)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Execute batch insert
        extras.execute_values(cur, insert_query, values)
        
        conn.commit()
        print(f"Successfully inserted/updated {len(values)} records.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()