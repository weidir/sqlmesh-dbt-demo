################################################################################
### Description: This script initializes synthetic data for the project      ###
### It will create a file or database and table, and load data into it.      ###
### Formats supported currently:                                             ###
###   - CSV                                                                  ###
###   - Snowflake                                                            ###
###   - DuckDB                                                               ###
### This script is mapped to the 'generate' make command.                    ###
################################################################################

# Import the required libraries
import os
from datetime import datetime

# Import the required custom classes
from utils.formats import StorageFormats
from utils.envs import Environments
from src.synthdataclasses import (
    CustomerSynthData, 
    OrdersSynthData, 
    ProductSynthData, 
    StoreSynthData, 
    LoyaltySynthData, 
    CampaignSynthData
)
from src.pipeline import SyntheticDataPipeline

# Path to write data locally
path = os.path.join(os.getcwd(), 'data/data/')

# Define the types of synthetic data to generate
data_types = [CustomerSynthData, ProductSynthData, StoreSynthData, CampaignSynthData, LoyaltySynthData, OrdersSynthData,]

# Create dictionary of supported formats
valid_format_dict = {str(format.value): format.name for format in StorageFormats}
valid_environment_dict = {str(env.value): env.name for env in Environments}

def main() -> None:

    # Capture start time
    start_tmstp = datetime.now()

    # Let the user choose the storage format to use
    format_input = input(f"Choose a data format to use to create synthetic data [1] {valid_format_dict} ")
    format_input = format_input if format_input else "1"
    try:
        format_select = valid_format_dict[format_input]
    except KeyError:
        print(f"Invalid value given for format. Accepted values are: {valid_format_dict.keys()} \nUsing 'SNOWFLAKE' by default...")
        format_select = "SNOWFLAKE"
    storage_format = StorageFormats[format_select]
    print(f"Synthetic data format: '{storage_format}'")

    # Choose the environment to generate synthetic data for
    environment_input = input(f"Enter the environment to generate synthetic data for [1] {valid_environment_dict}: ")
    environment_input = environment_input if environment_input else "1"
    try:
        environment = valid_environment_dict[environment_input]
        if environment == "BOTH":
            environment = ["DEV", "PROD"]
    except KeyError:
        print(f"Invalid value given for environment. Accepted values are: {valid_environment_dict.keys()} \nUsing 'DEV' by default...")
        environment = "DEV"
    print(f"Environment(s) selected: {environment}")

    # Choose the number of records to generate
    num_records = input("Enter the number of records to generate [1000]: ")
    num_records = int(num_records) if num_records else 1000
    if num_records < 1:
        print(f"Number of records must be at least 1, value given: {num_records:,}. Using 1000 by default...")
        num_records = 1000
    print(f"Number of records to generate: {num_records:,}")

    # Create a synthetic data pipeline and generate synthetic data
    synth_data_pipeline = SyntheticDataPipeline(data_types=data_types)
    synth_data_pipeline.generate(num_records=num_records)

    # Write the synthetic data to the selected format and database(s))
    synth_data_pipeline.write(environment=environment, schema="RAW", storage_format=storage_format, path=path)

    # Capture how long the script took to run
    duration = datetime.now() - start_tmstp
    duration_str = f"{duration.seconds // 60} minutes, {duration.seconds % 60} seconds" if duration.seconds > 60 else f"{duration.seconds} seconds"
    print(f"Synthetic data generation and writing complete. Time taken: {duration_str}")


# Run this code when script is executed
if __name__ == "__main__":
    main()
