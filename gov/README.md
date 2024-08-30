# Metadata Management for Data Governance

<img src="https://private-user-images.githubusercontent.com/40225091/290879885-e794ced8-7220-4393-8efc-3faf93bfb503.svg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjIwMTE0MTksIm5iZiI6MTcyMjAxMTExOSwicGF0aCI6Ii80MDIyNTA5MS8yOTA4Nzk4ODUtZTc5NGNlZDgtNzIyMC00MzkzLThlZmMtM2ZhZjkzYmZiNTAzLnN2Zz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA3MjYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNzI2VDE2MjUxOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQwNzU4OTY4NjFjMWE0ZTc0YjRmNWQ2ODc2OTM1NjBkMTg5NzE3ZDY1NWY4ZjYzYWI5OTc2NjhhMTc0OWM2M2EmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.caQcjNKac8opvBqZDYNV9vL-YIGVxuLpNIMNBX6qLg8" width=300 height=auto />

## Background and context
This application uses the open source tool OpenMetadata to ingest and manage metadata in Snowflake (and other sources in the future). OpenMetadata:
- Scans data sources and add metadata to the catalog
- Provides a UI for users to manually edit and add metadata
- Tracks lineage metadata
- Monitors data quality metrics

## Setup steps
1. To run OpenMetadata locally, the easiest method is to use Docker. Detailed instructions can be found [here](https://docs.open-metadata.org/v1.4.x/quick-start/local-docker-deployment). Make sure you have the necessary software installed:
    * Docker (recent version preferred)
    * OpenMetadata python packages (listed in the 'requirements-gov.txt' file)
2. Create a '.env' file in the 'gov/' directory that looks like this:
```
GOV_ROLE = <role_name> # Snowflake role name for OpenMetadata (e.g., 'OPEN_METADATA_ROLE')
GOV_USER = <user_name> # Snowflake user name for OpenMetadata (e.g., 'OPEN_METADATA_USER')
GOV_PASSWORD = <password> # Password for Snowflake OpenMetadata user
GOV_DATABASE = <database_name> # The name of the database where your data resides (for this demo, use 'PROD')
GOV_WAREHOUSE = <warehouse_name> The name of the database where your data resides (for this demo, use 'COMPUTE_WH')
```
3. Run the ```make init_open_metadata``` command from the root directory of the application. This command will do three things:
    1. Install the OpenMetadata ingestion python packages by running ```python3 -m pip install -r gov/requirements-gov.txt``` from the application root directory
    2. Run the 'create_gov_role_user_access.py' script that generates Snowflake SQL code to create a Snowflake role, user, and permissions for OpenMetadata
    3. Executes the 'initialize.sh' script with starts up the OpenMetadata container locally and automatically ingests metadata from Snowflake