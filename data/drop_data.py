#####################################################################
### Description: This script drops synthetic data for the project ###
### Formats supported currently:                                  ###
###   - CSV                                                       ###
###   - Snowflake                                                 ###
###   - DuckDB                                                    ###
### This script is mapped to the 'drop' make command.             ###
#####################################################################

# Import required packages
import os
import shutil
import snowflake.connector
from dotenv import dotenv_values

# Import the required custom classes
from utils.formats import StorageFormats
from utils.envs import Environments 

# Path to drop data locally
path = os.path.join(os.getcwd(), 'data/data/')

# Create dictionary of supported formats
valid_format_dict = {str(format.value): format.name for format in StorageFormats}
valid_environment_dict = {str(env.value): env.name for env in Environments}
valid_data_category_dict = {'1': 'NON-RAW', '2': 'RAW', '3': 'BOTH'}


def main() -> None:

    # Choose the environment to generate test data for
    environment_input = input(f"Enter the environment to drop synthetic data for [1] {valid_environment_dict}: ")
    environment_input = environment_input if environment_input else "1"
    try:
        environment = [valid_environment_dict[environment_input]]
        environment = ["DEV", "PROD"] if environment == "BOTH" else environment
    except KeyError:
        print(f"Invalid value given for environment. Accepted values are: {valid_environment_dict.keys()} \nUsing 'DEV' by default...")
        environment = ["DEV"]
    print(f"Environment(s) selected: {environment}")

    # Choose if raw data, non-raw data, or both will be dropped
    data_category_input = input(f"Enter what kind of data will be dropped [1] {valid_data_category_dict} ")
    try:
        data_category = valid_data_category_dict[data_category_input]
    except KeyError:
        print(f"Invalid value given for data category. Accepted values are: {valid_environment_dict.keys()} \nUsing 'NON-RAW' by default...")
        data_category = "NON-RAW"
    print(f"Data categories selected: {data_category}")

    # Let the user choose the storage format to use
    format_input = input(f"Choose a data format to use to create synthetic data [1] {valid_format_dict} ")
    format_input = format_input if format_input else "1"
    try:
        format_select = valid_format_dict[format_input]
    except KeyError:
        print(f"Invalid value given for format. Accepted values are: {valid_format_dict.keys()} \nUsing 'DUCKDB' by default...")
        format_select = "DUCKDB"
    storage_format = StorageFormats[format_select]
    print(f"Synthetic data format: '{storage_format}'")

    # Write the data to the selected format
    if storage_format == StorageFormats.SNOWFLAKE:

        # Import configuration parameters
        env = dotenv_values('.env')
        USER = env.get("USER")
        PASSWORD = env.get("PASSWORD")
        ACCOUNT = env.get("ACCOUNT")
        WAREHOUSE = env.get("WAREHOUSE")

        # Determine if raw data is being droppped
        raw_flg = False if "NON" in data_category.upper() else True # args.raw_flg == "true"
        print(f"Dropping test data from environment: {environment}")
        print(f"Dropping raw data: {raw_flg}")
        
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
            warehouse=WAREHOUSE,
        )
        print("Connected to Snowflake")

        # Create the database and schema
        print(f"Dropping schemas and tables from {environment} environment(s) if they do exist")
        for env_name in environment:
            file_name = f"data/sql/snowflake/drop_schema_table_{env_name.lower()}.sql" if raw_flg else f"data/sql/snowflake/drop_schema_table_nonraw_{env_name.lower()}.sql"
            print(f"Reading SQL statement from file: '{file_name}'")
            with open(file_name, 'r') as f:
                sql = f.read()
                print(f"SQL statement to create database and schemas: \n{sql}")
                conn.cursor().execute(sql, num_statements=sql.count(';'))
    
    elif storage_format == StorageFormats.CSV:
        for env in environment:
            env_path = os.path.join(path, 'csv', env.lower())
            try:
                shutil.rmtree(env_path)
            except FileNotFoundError as fne:
                print(f"No folder found to drop. {fne}")
            except Exception as e:
                print(f"Exception thrown while trying to delete CSV data")
                raise e
            print(f"'{env_path}' folder removed")

    elif storage_format == StorageFormats.DUCKDB:
        duckdb_path = os.path.join(path, 'duckdb/')
        if "DEV" in environment and "PROD" in environment:
            try:
                shutil.rmtree(duckdb_path)
                print(f"DEV and PROD {data_category.upper()} DuckDB data removed at: '{duckdb_path}')")
            except FileNotFoundError as fne:
                print(f"No folder/database found to drop. {fne}")
            except Exception as e:
                print(f"Exception thrown while trying to delete DuckDB data")
                raise e
        else:
            try:
                os.remove(os.path.join(duckdb_path, f"{environment[0].lower()}.ddb"))
                print(f"{environment[0]} {data_category.upper()} DuckDB data removed at: '{duckdb_path}')")
            except FileNotFoundError as fne:
                print(f"No database found to drop. {fne}")
            except Exception as e:
                print(f"Exception thrown while trying to delete DuckDB data")
                raise e


# Run this code when script is executed
if __name__ == '__main__':
    main()
