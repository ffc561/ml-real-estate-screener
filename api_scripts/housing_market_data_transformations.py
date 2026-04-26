import pandas as pd
import numpy as np
import json
from datetime import datetime

# Work in progress. Only base JSON normalization performed at the moment.
def transform_individual_property_detail_records(json_filepath):
    with open(json_filepath) as json_data:
        loaded_json = json.load(json_data)
        property_details_df = pd.json_normalize(loaded_json)

    property_details_df.set_index("zpid", inplace=True)
    property_details_df['extracted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return property_details_df

def unnest_property_details(json_filepath, record_path):

    with open(json_filepath) as json_data:
         loaded_json = json.load(json_data)
         details_df = pd.json_normalize(loaded_json, record_path = record_path)
    
    try:
        return details_df
    except KeyError:
        print("Column could not be exploded.  Check column name and try again.")

# Work in progress. Only base JSON normalization and basic transformations performed at the moment.
def transform_property_search_json(json_filepath):

    with open(json_filepath) as json_data:
        data = json.load(json_data)
        full_location_df = pd.DataFrame()

        for line in data:
            if line != {} and line != []:
                try:
                    location_df = pd.json_normalize(line['props'])
                    full_location_df = pd.concat([full_location_df, location_df])
                except KeyError:
                    print(f"Empty result.  Skipping.")
        
        final_cols = [
            "zpid",
            "address",
            "unit",
            "latitude",
            "longitude",
            "bedrooms",
            "bathrooms",
            "livingArea",
            "lotAreaValue",
            "lotAreaUnit",
            "price",
            "rentZestimate",
            "zestimate",
            "has3DModel",
            "hasVideo",
            "hasImage",
            "propertyType",
            "listingStatus",
            "listingSubType.is_FSBA",
            "listingSubType.is_openHouse",
            "detailUrl",
            "daysOnZillow",
            "country",
            "currency"
        ]

        final_df = full_location_df[final_cols]

        final_df['extracted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return final_df
