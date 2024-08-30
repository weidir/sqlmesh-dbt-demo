# Import necessary libraries
import re
import time
import os
from typing import List, Union
from dotenv import dotenv_values
import snowflake.connector
from snowflake.connector.errors import ProgrammingError
import duckdb

# Import custom classes
from utils.formats import StorageFormats
from utils.envs import Environments

class SyntheticDataPipeline:
    """
    Class to create, store, and write fake data
    """

    def __init__(self, data_types: list):
        """
        Constructor for the SyntheticDataPipeline class
        :param data_types: List of TestData classes to generate data for
        """
        self.data_types = data_types
        self.data = None


    def generate(self, num_records: int):
        """
        Generalized method to create fake data
        :param data_types: Type of data to create, can take a single TestData object or a list of TestData objects
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        if isinstance(self.data_types, list):
            self.data = {}
            for dt in self.data_types:
                # Find each word in the class name, convert to lowercase, log the class being created
                name_list = re.findall('[A-Z][^A-Z]*', dt.__name__)
                name_list_lower = [name.lower() for name in name_list]
                print(f"Creating {' '.join(name_list_lower)}...")

                # Instantiate the class
                test_data = dt()

                # Get the foreign key data from the other classes
                test_data.get_fk_from_pipeline(pipeline=self)
                    
                # Generate and store the data in the class instance
                test_data.generate_data(num_records=num_records)
                self.data[dt.__name__.upper()] = test_data
        else:
            # Instantiate the class
            test_data = self.data_types()

            # Find each word in the class name, convert to lowercase, log the class being created
            name_list = re.findall('[A-Z][^A-Z]*', self.data_types.__name__)
            name_list_lower = [name.lower() for name in name_list]
            print(f"Creating {' '.join(name_list_lower)}...")

            # Generate and store the data in the class instance
            test_data.generate_data(num_records=num_records)
            self.data = [test_data]
        

    def write(self, storage_format: StorageFormats, environment: Union[Environments, List[Environments]], path: str = '', schema: str = ''):
        """
        Method to write fake data to a file or database
        :param storage_format: Storage format for the data
        :param environment: Environment to write the data to
        :param path: Path to write the data, should be a folder
        :param conn: Snowflake connection object
        :param table_name: Name of the table to write to
        :param database: Name of the database to write to
        :param schema: Name of the schema to write to
        """

        # If single database provided, convert to list
        if isinstance(environment, str):
            environment = [environment]

        # Write the data to the selected format
        if storage_format == StorageFormats.SNOWFLAKE:

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

            # Create the database and schema
            for env in environment:
                print(f"Creating database and schema for '{env}' environment if they do not exist")
                with open(f'data/sql/snowflake/create_db_schema_{env.lower()}.sql', 'r') as f:
                    sql = f.read()
                    print(f"SQL statement to create databases and schemas: \n{sql}")
                    
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
                    print(f"Results of Snowflake query: '{results[0][0]}'")

                for object, data in self.data.items():
                    results = data.write_to_snowflake(
                        conn, 
                        table_name=object, 
                        database=env, 
                        schema=schema
                    )
                    print(f"'{object}' data written to table '{object}' in '{env}' Snowflake database; success status: {results[0]}, rows inserted: {results[2]}")
                print(f"All test data written to '{env}' Snowflake database")

        elif storage_format == StorageFormats.CSV:
            path = os.path.join(path, 'csv/')
            print(f"CSV data being written to: {path}")
            for data_type, data in self.data.items():
                data.write_to_csv(os.path.join(path, f"{data_type.lower()}.csv"))
            print("Data written to CSV")

        elif storage_format == StorageFormats.DUCKDB:
            path = os.path.join(path, 'duckdb/')
            print(f"Data being written DuckDB database at: {path}")
            for env in environment:
                con = duckdb.connect(database = f"{path}/{env.lower()}.ddb", read_only = False)
                print(f"Creating database and schema for '{env}' environment if they do not exist")

                with open(f'data/sql/duckdb/create_db_schema_{env.lower()}.sql', 'r') as f:
                    sql = f.read()
                    print(f"SQL statement to create databases and schemas: \n{sql}")
                    con.sql(sql)

                for data_type, data in self.data.items():
                    data.write_to_duckdb(path_to_db=path, table_name=data_type, schema='RAW', connection=con)
                
            print("Data written to DuckDB databse")
                
        else:
            valid_format_dict = {str(format.value): format.name for format in StorageFormats}
            raise ValueError(f"Invalid data storage format, please give one of the following formats: {valid_format_dict}")