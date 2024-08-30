# Import the required classes
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import pandas as pd
import duckdb
import yaml
from snowflake.connector.pandas_tools import write_pandas

# Import custom classes
from src.pipeline import SyntheticDataPipeline

class SyntheticData(ABC):
    """
    Abstract class to create, store, and write test data
    """

    def __init__(self):
        self.data = None
        self.foreign_data = None

    @abstractmethod
    def generate_data(self, num_records: int) -> List[Dict]:
        pass

    def __name__(self):
        return self.__class__.__name__

    def get_fk_from_pipeline(
            self, 
            pipeline: SyntheticDataPipeline,
    ):
        # Load the foreign keys from the model.yml file
        foreign_keys_dict = yaml.safe_load(open("data/src/model.yml", "r"))

        try:
            # Get the dependencies for the class
            name = self.__name__()
            dependencies = foreign_keys_dict['classes'][name]['dependencies']
            if dependencies:
                print(f"Dependencies for {name}: {', '.join(dependencies)}")
            else:
                print(f"No dependencies found for {name}.")

            if dependencies:
                # Store the foreign key data
                self.foreign_data = {}
                for dependency in dependencies:
                    self.foreign_data[dependency] = pipeline.data[dependency.upper()]

        except KeyError as ke:
            print(f"No dependencies found for {self.__name__()}.")
            pass
        except Exception as e:
            raise e

        
    def data_to_df(self) -> pd.DataFrame:
        try:
            return pd.DataFrame(self.data)
        except AttributeError as ae:
            raise AttributeError(f"{ae}. \nMust create test data before writing to CSV")
        except Exception as e:
            raise e
    

    def write_to_csv(self, path: str = ''):
        
        # Create the folder path if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Convert data to DataFrame
        data_df = pd.DataFrame(self.data)

        # Write data to CSV
        try:
            data_df.to_csv(path, index=False)
        except Exception as e:
            print("Exception while writing data to CSV")
            raise e
    

    def write_to_duckdb(
            self,
            path_to_db: str,
            table_name: str,
            schema: str,
            connection: duckdb.DuckDBPyConnection,
    ):
        
        # Create the folder path if it doesn't exist
        if not os.path.exists(path_to_db):
            os.makedirs(path_to_db)
        
        # Convert data to DataFrame
        data_df = pd.DataFrame(self.data)

        # Create schema and tables
        connection.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        connection.sql(f"CREATE OR REPLACE TABLE {schema}.{table_name} AS SELECT * FROM data_df")
        connection.sql(f"TRUNCATE {schema}.{table_name}")
        connection.sql(f"INSERT INTO {schema}.{table_name} SELECT * FROM data_df")


    def write_to_snowflake(
            self, 
            conn, 
            table_name: str, 
            database: str, 
            schema: str
    ) -> Tuple[bool, int, int, List[Tuple[str, str, int, int, int, int, str, int, int, str]]]:
        """
        Method to write data to Snowflake
        Args:
            conn: Snowflake connection object
            table_name: Name of the table to write to
            database: Name of the database to write to
            schema: Name of the schema to write to
        Returns:
            Tuple containing the results of the write operation with the following structure:
            (
                bool: success is True if the function successfully wrote the data to the table.
                int: num_chunks is the number of chunks of data that the function copied.
                int: num_rows is the number of rows that the function inserted.
                list: output is the output of the COPY INTO <table> command with the following structure:
                [
                    (FILE, STATUS, ROWS_PARSED, ROWS_LOADED, ERROR_LIMIT, ERRORS_SEEN, FIRST_ERROR, FIRST_ERROR_LINE, FIRST_ERROR_CHARACTER, FIRST_ERROR_COLUMN_NAME),
                ]
            )
        """
        
        # Convert data to DataFrame
        data_df = pd.DataFrame(self.data)
        
        # Write data to Snowflake
        try:
            results = write_pandas(
                conn=conn, 
                df=data_df, 
                table_name=table_name,
                database=database,
                schema=schema,
                auto_create_table=True,
                overwrite=True,
            )
            return results
        except Exception as e:
            print("Exception while writing data to Snowflake")
            raise e
