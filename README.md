# ML Real Estate Screener

This project is a real estate data engineering pipeline designed to extract, load, and transform property data from Zillow for market analysis and machine learning applications.

## Project Overview

- **Extraction**: Python-based pipelines (`property_location_search_pipeline.py`, `property_details_pipeline.py`) extract real estate listings and granular property details using the [US Housing Market Data API](https://rapidapi.com/unoflow-unoflow-default/api/us-housing-market-data).
- **Storage**: Raw data is stored in a PostgreSQL database using `JSONB` for flexible schema handling of complex property attributes.
- **Transformation**: A dbt project (`us_real_estate_screener`) transforms raw data into a structured Dimensional Model:
  - `dim_properties`: Static structural attributes of properties.
  - `fct_property_valuations`: Dynamic market pricing and popularity metrics.
  - `fct_property_financials`: Ongoing costs like HOA fees, taxes, and insurance.
- **Quality Assurance**: Automated dbt tests ensure data integrity and record preservation across the pipeline.

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- PostgreSQL 17+
- dbt (dbt-core and dbt-postgres)

### 2. Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DB_SERVICE=ml_real_estate_app
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# API Configuration (US Housing Market Data API via RapidAPI)
UHMD_API_KEY=your_rapidapi_key
UHMD_API_HOST=us-housing-market-data.p.rapidapi.com
```

### 3. Local PostgreSQL Setup
1. Create a database named `ml_real_estate_app`.
2. Run the initialization script to create the raw schema:
   ```bash
   psql -d ml_real_estate_app -f migration_scripts/initialize_db.sql
   ```

### 4. Python Environment Setup
Install the required Python packages:
```bash
pip install psycopg2-binary python-dotenv requests
```

### 5. dbt Project Setup
1. Configure your dbt profile. Add the following to your `~/.dbt/profiles.yml`:
   ```yaml
   us_real_estate_screener:
     outputs:
       dev:
         type: postgres
         host: localhost
         user: your_postgres_user
         password: your_postgres_password
         port: 5432
         dbname: ml_real_estate_app
         schema: public
         threads: 1
     target: dev
   ```
2. Navigate to the dbt directory:
   ```bash
   cd us_real_estate_screener
   ```
3. Install dependencies and run the models:
   ```bash
   dbt deps
   dbt run
   dbt test
   ```

## Running the Pipelines
- **Search for listings**: `python3 property_location_search_pipeline.py`
- **Get property details**: `python3 property_details_pipeline.py`
- **Bulk Upload**: `python3 bulk_db_upload.py` (for processing JSON files in `temp_files`)
