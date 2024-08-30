# Import required libraries
import time
from dotenv import dotenv_values
import snowflake.connector
from snowflake.connector.errors import ProgrammingError

# List of schemas for role and user to be granted permissions to 
SCHEMAS = ['RAW', 'BRONZE', 'SILVER', 'GOLD']

# Run this code when script is executed
if __name__ == "__main__":

    # Import configuration parameters
    env = dotenv_values('.env')
    USER = env.get("USER")
    PASSWORD = env.get("PASSWORD")
    ACCOUNT = env.get("ACCOUNT")
    WAREHOUSE = env.get("WAREHOUSE")

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
    )
    print("Connected to Snowflake")

    # Import configuration parameters
    gov_env = dotenv_values('gov/.env')
    GOV_ROLE = gov_env.get('GOV_ROLE')
    GOV_USER = gov_env.get('GOV_USER')
    GOV_PASSWORD = gov_env.get('GOV_PASSWORD')
    GOV_DATABASE = gov_env.get('GOV_DATABASE')
    GOV_WAREHOUSE = gov_env.get('GOV_WAREHOUSE')

    print(f"Creating role '{GOV_ROLE}' and user '{GOV_USER}' for OpenMetadata to use")
    with open(f'gov/create_gov_role_user_access.sql', 'r') as f:
        sql = f.read()

        # Insert configuration parameters into SQL statement (with password excluded)
        sql = sql.replace('$GOV_ROLE', GOV_ROLE)
        sql = sql.replace('$GOV_USER', GOV_USER)
        sql = sql.replace('$GOV_DATABASE', GOV_DATABASE)
        sql = sql.replace('$GOV_WAREHOUSE', GOV_WAREHOUSE)
        
        # Generate GRANT SCHEMA USAGE statements based on schemas in list
        GRANT_SCHEMA_USAGE_STMTS = '\n'.join([f"GRANT USAGE ON SCHEMA {schema} TO ROLE {GOV_ROLE};" for schema in SCHEMAS])
        sql = sql.replace('$GRANT_SCHEMA_USAGE_STMTS', GRANT_SCHEMA_USAGE_STMTS)

        # Generate GRANT TABLE SELECT statements based on schemas in list
        GRANT_TBL_SELECT_STMTS = '\n'.join([f"GRANT SELECT ON ALL TABLES IN SCHEMA {schema} TO ROLE {GOV_ROLE};" for schema in SCHEMAS])
        GRANT_EXT_TBL_SELECT_STMTS = '\n'.join([f"GRANT SELECT ON ALL EXTERNAL TABLES IN SCHEMA {schema} TO ROLE {GOV_ROLE};" for schema in SCHEMAS])
        GRANT_VIEW_SELECT_STMTS = '\n'.join([f"GRANT SELECT ON ALL VIEWS IN SCHEMA {schema} TO ROLE {GOV_ROLE};" for schema in SCHEMAS])
        GRANT_DYN_TBL_SELECT_STMTS = '\n'.join([f"GRANT SELECT ON ALL DYNAMIC TABLES IN SCHEMA {schema} TO ROLE {GOV_ROLE};" for schema in SCHEMAS])
        GRANT_SELECT_STMTS = f"{GRANT_TBL_SELECT_STMTS}\n{GRANT_EXT_TBL_SELECT_STMTS}\n{GRANT_VIEW_SELECT_STMTS}\n{GRANT_DYN_TBL_SELECT_STMTS}"
        sql = sql.replace('$GRANT_SELECT_STMTS', GRANT_SELECT_STMTS)
        print(f"SQL statement to create databases and schemas (password exluded): \n{sql}")

        # Insert password into SQL statement
        sql = sql.replace('$GOV_PASSWORD', GOV_PASSWORD)

    # Execute SQL statement
    cur = conn.cursor()
    try:
        cur.execute(sql, num_statements=sql.count(';'))
        query_id = cur.sfqid
        while conn.is_still_running(conn.get_query_status_throw_if_error(query_id)):
            time.sleep(1)
    except ProgrammingError as err:
        print(f'Programming Error: {err}')

    # Get the results from a query.
    cur.get_results_from_sfqid(query_id)
    results = cur.fetchall()
    print(f'Results of Snowflake query: \n{results[0]}')

    print(f"OpenMetadata Snowflake role '{GOV_ROLE}' and user '{GOV_USER}' created with access to '{GOV_DATABASE}' database and schemas: {', '.join(SCHEMAS)}")
