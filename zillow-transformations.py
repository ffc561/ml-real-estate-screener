import pandas as pd
import polars as pl
import numpy as np
import json
from datetime import datetime

pd.set_option('display.max_columns', 10000)

# Work in progress. Only base JSON normalization performed at the moment.
def transform_individual_property_json(json_filepath):
    with open(json_filepath) as json_data:
        return pd.json_normalize(json.load(json_data))

# Work in progress. Only base JSON normalization and basic transformations performed at the moment.
def transform_property_search_json(json_filepath):

    with open(json_filepath) as json_data:
        data = json.load(json_data)
        full_location_df = pd.DataFrame()

        for line in data:
            location_df = pd.json_normalize(line['props'])
            print(location_df.shape)
            full_location_df = pd.concat([full_location_df, location_df])
        
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
