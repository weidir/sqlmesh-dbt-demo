from enum import Enum

# Define the supported data stores
class StorageFormats(Enum):
    SNOWFLAKE = 1
    DUCKDB = 2
    CSV = 3
