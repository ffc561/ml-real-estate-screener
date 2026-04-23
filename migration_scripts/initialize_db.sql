-- This db script creates the db objects required to house the raw Zillow data
DROP TABLE IF EXISTS public.zillow_listings_raw;

CREATE TABLE IF NOT EXISTS public.zillow_listings_raw (
    zpid INT PRIMARY KEY,
    address VARCHAR(2000),
    unit VARCHAR(250),
    latitude NUMERIC(10, 5),
    longitude NUMERIC(10, 5),
    num_bedrooms INT,
    num_bathrooms INT,
    living_area NUMERIC(12, 1),
    lot_area_value NUMERIC(12, 1),
    lot_area_unit VARCHAR(10),
    price NUMERIC(12, 2),
    rent_zestimate NUMERIC(12, 2),
    zestimate NUMERIC(12, 2),
    has_3d_model BOOLEAN,
    has_video BOOLEAN,
    has_image BOOLEAN,
    property_type VARCHAR(50),
    listing_status VARCHAR(50),
    listing_subtype JSONB,
    detail_url VARCHAR(255),
    days_on_zillow INT,
    country VARCHAR(3),
    currency VARCHAR(3),
    extracted_at TIMESTAMP
);