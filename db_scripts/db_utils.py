import psycopg2
from psycopg2 import extras
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import re
from pathlib import Path

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_SERVICE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def camel_to_snake(name):
    """Converts camelCase JSON keys to snake_case table columns."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def extract_data(query, params=()):
    
    try:
        if params == ():
            params = (True, )
        # Establish database connection
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def upsert_zillow_data(json_payload, db_table_name, historical_upload=False, filename=""):

    # Parse JSON if it's a string
    data = json.loads(json_payload) if isinstance(json_payload, str) else json_payload

    try:

        # Establish database connection
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        records_processed = 0

        for item in data:

            columns = []
            values = []

            # Iterate through JSON properties and convert to columns/values
            for key, val in item.items():

                if val is not None:
                    col_name = camel_to_snake(key)
                    columns.append(col_name)
            
                    # Use psycopg2's Json wrapper for dicts and lists to map to JSONB correctly
                    if isinstance(val, (dict, list)):
                        values.append(extras.Json(val))
                    else:
                        values.append(val)

            # If the upsert being executed is a historical upload, the creation timestamps should be set to the original extraction date.
            if historical_upload is True:

                if db_table_name == "zillow_listings_raw":
                    file_prefix = "zillow_location_search_"
                    ts_cols = ["extracted_at"]
                elif db_table_name == "zillow_property_details_raw":
                    file_prefix = "zillow_property_details_"
                    ts_cols = ["created_at"]
                
                historical_ts = datetime.strptime(
                    Path(filename).stem.replace(file_prefix, ""),
                    "%Y%m%d%H%M%S"
                )

                for col in ts_cols:
                    columns.append(col)
                    values.append(historical_ts)

            # 1. Build INSERT column and value placeholders
            col_strings = ', '.join(columns)
            val_placeholders = ', '.join(['%s'] * len(columns))

            # 2. Build UPDATE SET statements (exclude zpid from updates)
            update_strings = ', '.join(
                [f"{col} = EXCLUDED.{col}" for col in columns if col != 'zpid']
            )

            if db_table_name == "zillow_listings_raw":
                conflict_keys = "zpid, extracted_at"
            elif db_table_name in ["zillow_property_details_raw", "zillow_property_transit_scores", "zillow_property_similar_sales", "zillow_property_comps"]:
                conflict_keys = "zpid"
            elif db_table_name == "zillow_property_building_details":
                conflict_keys = "building_id"
            elif db_table_name == "zillow_monthly_inventory":
                conflict_keys = "month_date_yyyymm, postal_code"

            # 3. Construct the UPSERT query
            # created_at defaults to current timestamp automatically on insert
            # updated_at is explicitly updated to current timestamp on conflict/update
            query = f"""
                INSERT INTO public.{db_table_name} ({col_strings})
                VALUES ({val_placeholders})
                ON CONFLICT ({conflict_keys}) DO UPDATE SET
                    {update_strings},
                    updated_at = CURRENT_TIMESTAMP;
            """

            # Execute query for the specific property
            cur.execute(query, tuple(values))
            records_processed += 1

        # Commit the transaction if everything succeeded
        conn.commit()
        print(f"Successfully processed and upserted {records_processed} records.")

    except psycopg2.OperationalError as e:
        # Catch connection failures (e.g., wrong password, DB down)
        print(f"Database Connection Error: Could not connect to the database.\nDetails: {e}")
        
    except psycopg2.Error as e:
        # Catch SQL execution errors (e.g., syntax errors, type mismatches)
        print(f"Database Query Error: Failed to execute database operation.\nDetails: {e}")
        if conn:
            print("Rolling back transaction to prevent partial inserts...")
            conn.rollback() 
            
    except Exception as e:
        # Catch any other unexpected python errors during processing
        print(f"An unexpected error occurred during database operations: {e}")
        if conn:
            print("Rolling back transaction...")
            conn.rollback()

    finally:
        # 3. Ensure connections are ALWAYS closed, regardless of success or failure
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("Database connection closed.")