-- Snowflake SQL statement to create a new role, user and grant access to the required database, schemas, tables and views

-- Create New Role
CREATE ROLE IF NOT EXISTS $GOV_ROLE;

-- Create New User
CREATE USER IF NOT EXISTS $GOV_USER DEFAULT_ROLE=$GOV_ROLE PASSWORD='$GOV_PASSWORD';

-- Grant role to user
GRANT ROLE $GOV_ROLE TO USER $GOV_USER;

-- Grant USAGE Privilege on Warehouse to New Role
GRANT USAGE ON WAREHOUSE $GOV_WAREHOUSE TO ROLE $GOV_ROLE;

-- Grant USAGE Privilege on Database to New Role
GRANT USAGE ON DATABASE $GOV_DATABASE TO ROLE $GOV_ROLE;

-- Use the selected database for the rest of the script
USE DATABASE $GOV_DATABASE;

-- Grant USAGE Privilege on required Schemas to New Role
$GRANT_SCHEMA_USAGE_STMTS

-- Grant SELECT Privilege on required tables & views to New Role
$GRANT_SELECT_STMTS

-- Give the new role the ability to import metadata from SNOWFLAKE database
GRANT IMPORTED PRIVILEGES ON ALL SCHEMAS IN DATABASE SNOWFLAKE TO ROLE $GOV_ROLE;