-- This db script creates the db objects required to house the raw Zillow data
DROP TABLE IF EXISTS public.zillow_listings_raw;

CREATE TABLE IF NOT EXISTS public.zillow_listings_raw (
    zpid BIGINT NOT NULL,
    address VARCHAR(2000),
    unit VARCHAR(250),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    bedrooms INT,
    bathrooms NUMERIC, --Allow decimals for half bathrooms
    living_area NUMERIC(12, 1),
    lot_area_value NUMERIC(12, 1),
    lot_area_unit VARCHAR(10),
    price NUMERIC(12, 2),
    price_change NUMERIC(12, 2),
    rent_zestimate NUMERIC(12, 2),
    zestimate NUMERIC(12, 2),
    has3_d_model BOOLEAN,
    has_video BOOLEAN,
    has_image BOOLEAN,
    property_type VARCHAR(50),
    listing_status VARCHAR(50),
    listing_sub_type JSONB,
    detail_url VARCHAR(1000),
    days_on_zillow INT,
    country VARCHAR(3),
    currency VARCHAR(3),
    broker_name VARCHAR(1000),
    carousel_photos JSONB,
    coming_soon_on_market_date BIGINT,
    contingent_listing_type VARCHAR(50),
    date_price_changed BIGINT,
    img_src VARCHAR(1000),
    new_construction_type VARCHAR(255),
    extracted_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS public.zillow_property_details_raw;

CREATE TABLE IF NOT EXISTS public.zillow_property_details_raw (
    zpid BIGINT PRIMARY KEY,
    address JSONB,
    annual_homeowners_insurance NUMERIC,
    attribution_info JSONB,
    bathrooms NUMERIC,
    bedrooms INTEGER,
    broker_id VARCHAR(50),
    brokerage_name VARCHAR(1000),
    building VARCHAR(1000),
    building_id VARCHAR(50),
    building_permits JSONB,
    city VARCHAR(100),
    city_id INTEGER,
    climate JSONB,
    coming_soon_on_market_date BIGINT,
    contact_recipients JSONB,
    contingent_listing_type VARCHAR(255),
    country VARCHAR(100),
    county VARCHAR(100),
    county_fips VARCHAR(50),
    county_id INTEGER,
    currency VARCHAR(10),
    date_posted VARCHAR(50),
    date_sold VARCHAR(50),
    description TEXT,
    estimated_sales_range JSONB,
    favorite_count INTEGER,
    home_facts JSONB,
    home_insights JSONB,
    home_status VARCHAR(100),
    home_type VARCHAR(100),
    img_src TEXT,
    is_listed_by_owner BOOLEAN,
    is_showcase_listing BOOLEAN,
    latitude DOUBLE PRECISION,
    listed_by JSONB,
    listing_provider VARCHAR(1000),
    listing_sub_type JSONB,
    living_area NUMERIC,
    living_area_units VARCHAR(50),
    living_area_value NUMERIC,
    longitude DOUBLE PRECISION,
    mlsid VARCHAR(100),
    monthly_hoa_fee NUMERIC,
    mortgage_rates JSONB,
    mortgage_zhl_rates JSONB,
    nearby_homes JSONB,
    neighborhood_map_thumb JSONB,
    neighborhood_region JSONB,
    open_house_schedule JSONB,
    page_view_count INTEGER,
    photo_count INTEGER,
    price NUMERIC,
    price_change NUMERIC,
    price_change_date BIGINT,
    price_change_date_string VARCHAR(50),
    price_history JSONB,
    property_tax_rate NUMERIC,
    property_type_dimension VARCHAR(100),
    provider_listing_id VARCHAR(255),
    rent_zestimate NUMERIC,
    reso_facts JSONB,
    schools JSONB,
    solar_potential JSONB,
    state VARCHAR(50),
    state_id INTEGER,
    street_address VARCHAR(2000),
    tax_history JSONB,
    time_on_zillow VARCHAR(100),
    time_zone VARCHAR(100),
    url TEXT,
    year_built INTEGER,
    zestimate NUMERIC,
    zestimate_high_percent VARCHAR(50),
    zestimate_low_percent VARCHAR(50),
    zipcode VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS public.zip_codes;

CREATE TABLE IF NOT EXISTS public.zip_codes (
    zipcode VARCHAR(20) PRIMARY KEY,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    primary_city VARCHAR(100),
    state_province_code VARCHAR(2),
    state_name VARCHAR(100),
    population BIGINT,
    density NUMERIC,
    county_fips VARCHAR(5),
    county_name VARCHAR(50),
    county_weights JSONB,
    county_names_all VARCHAR(50),
    county_fips_all VARCHAR(50),
    timezone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_listings
ON zillow_listings_raw (zpid, extracted_at);

CREATE UNIQUE INDEX idx_property_details
ON zillow_property_details_raw (zpid);

DROP TABLE IF EXISTS public.zillow_property_transit_score;

CREATE TABLE IF NOT EXISTS public.zillow_property_transit_scores (
    zpid BIGINT PRIMARY KEY,
    transit_score JSONB,
    bike_score JSONB,
    walk_score JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_property_transit_scores
ON zillow_property_transit_scores (zpid);

DROP TABLE IF EXISTS public.zillow_property_building_details;

CREATE TABLE IF NOT EXISTS public.zillow_property_building_details (
    building_id BIGINT PRIMARY KEY,
    -- Standard text and string fields
    address TEXT,
    bdp_url TEXT,
    building_name TEXT,
    building_phone_number TEXT,
    building_type TEXT,
    county TEXT,
    description TEXT,
    lot_id TEXT,
    neighborhood TEXT,
    -- Numeric and geographic fields
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    photo_count INTEGER,
    -- Boolean flags
    is_low_income BOOLEAN,
    is_senior_housing BOOLEAN,
    is_student_housing BOOLEAN,
    -- Complex objects and arrays stored as JSONB for efficient querying
    amenity_details JSONB,
    amenity_summary JSONB,
    assigned_schools JSONB,
    bike_score JSONB,
    building_attributes JSONB,
    floor_plans JSONB,
    housing_connector JSONB,
    photos JSONB,
    special_offers JSONB,
    transit_score JSONB,
    ungrouped_units JSONB,
    walk_score JSONB,
    -- Audit timestamps (Optional but recommended)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_buildings
ON zillow_property_building_details (building_id);

DROP TABLE IF EXISTS public.zillow_propery_comps;

CREATE TABLE IF NOT EXISTS public.zillow_property_comps (
    -- Core Property Identifiers and Attributes
    comp_zpid BIGINT,
    price NUMERIC,
    currency TEXT,
    bedrooms INTEGER,
    bathrooms NUMERIC,
    
    -- Area and Sizing
    living_area NUMERIC,
    living_area_value NUMERIC,
    living_area_units TEXT,
    living_area_units_short TEXT,
    lot_size NUMERIC,
    lot_area_value NUMERIC,
    lot_area_units TEXT,
    
    -- Location Coordinates and Basic Info
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    state TEXT,
    
    -- Property Status and Categorization
    home_status TEXT,
    home_type TEXT,
    hdp_url TEXT,
    hdp_type_dimension TEXT,
    property_type_dimension TEXT,
    listing_type_dimension TEXT,
    provider_listing_id TEXT,
    new_construction_type TEXT,
    
    -- Boolean Flags
    is_showcase_listing BOOLEAN,
    is_premier_builder BOOLEAN,
    
    -- Complex Nested Objects and Arrays (Stored as JSONB)
    mini_card_photos JSONB,
    listing_metadata JSONB,
    address JSONB,
    parent_region JSONB,
    formatted_chip JSONB,
    listing_sub_type JSONB,
    attribution_info JSONB,
    
    -- Audit Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

    -- Unique constraint to facilitate Python ON CONFLICT upsert logic
    CONSTRAINT uq_building_id UNIQUE (zpid, created_at)
);

DROP TABLE IF EXISTS public.zillow_monthly_inventory;

CREATE TABLE IF NOT EXISTS public.zillow_monthly_inventory (    
    -- Core Dimensions
    month_date_yyyymm INTEGER NOT NULL,
    postal_code TEXT NOT NULL,
    
    -- Listing Counts
    active_listing_count INTEGER,
    active_listing_count_mm NUMERIC,
    new_listing_count INTEGER,
    new_listing_count_mm NUMERIC,
    total_listing_count INTEGER,
    total_listing_count_mm NUMERIC,
    
    -- Pricing Metrics
    average_listing_price NUMERIC,
    average_listing_price_mm NUMERIC,
    median_listing_price NUMERIC,
    median_listing_price_mm NUMERIC,
    price_increased_count INTEGER,
    price_increased_count_mm NUMERIC,
    
    -- Days on Market
    median_days_on_market INTEGER,
    median_days_on_market_mm NUMERIC,
    
    -- Audit Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique constraint to facilitate Python ON CONFLICT upsert logic
    CONSTRAINT uq_monthly_inventory_period_zip UNIQUE (month_date_yyyymm, postal_code)
);

DROP TABLE IF EXISTS public.zillow_property_comps;

CREATE TABLE IF NOT EXISTS public.zillow_property_comps (    
    -- Core Dimensions
    zpid BIGINT PRIMARY KEY,
    as_of_date DATE,
    comps JSONB,
    
    -- Audit Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique constraint to facilitate Python ON CONFLICT upsert logic
    CONSTRAINT uq_zpid_pc UNIQUE (zpid)
);

DROP TABLE IF EXISTS public.elt_job_parameters;

CREATE TABLE IF NOT EXISTS public.elt_job_parameters (
    job_type VARCHAR(255),
    data_source VARCHAR(255),
    input_id VARCHAR(255),
    payload_compilation_method VARCHAR(255),
    empty_record_handling_method VARCHAR(255)
);

INSERT INTO public.elt_job_parameters (job_type, data_source, input_id, payload_compilation_method) 
VALUES ('zillow_listings_raw', 'uhmd', 'zip_code', 'extend', 'skip'),
       ('zillow_property_details', 'uhmd', 'zpid', 'append', 'stub'),
       ('zillow_property_comps', 'uhmd', 'zpid', 'append', 'stub'),
       ('zillow_property_building_details', 'uhmd', 'building_id', 'append', 'stub'),
       ('zillow_property_transit_scores', 'uhmd', 'zpid', 'append', 'stub'),
       ('zillow_monthly_inventory', 'uhmd', 'zip_code', 'extend', 'skip');

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO auto_job;