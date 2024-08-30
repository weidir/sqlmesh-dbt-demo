#!/bin/bash

# Run this script using the 'make start_open_meta' recipe

# Set variable for docker container folder
CONTAINER_FOLDER=gov/openmetadata-docker/
DOCKER_FILE=docker-compose-postgres.yml

# Create the directory for the metadata container
echo "Checking if directory '$CONTAINER_FOLDER' exists for metadata container"
if [ ! -d $CONTAINER_FOLDER ]; then
    echo "Directory did not exist, creating directory '$CONTAINER_FOLDER' for metadata container"
  mkdir -p $CONTAINER_FOLDER
else
    echo "Directory '$CONTAINER_FOLDER' already exists"
fi

# Download the docker-compose file
echo "Checking if docker-compose file exists as '$CONTAINER_FOLDER/$DOCKER_FILE' directory"
if [ ! -f $CONTAINER_FOLDER/$DOCKER_FILE ]; then
  echo "File does not exist yet, downloading docker-compose file to the '$CONTAINER_FOLDER' directory"
  curl -sL -o gov/openmetadata-docker/docker-compose-postgres.yml https://github.com/open-metadata/OpenMetadata/releases/download/1.4.1-release/docker-compose-postgres.yml
else
    echo "Docker-compose file already exists in the '$CONTAINER_FOLDER' directory"
fi

# Start the metadata container
echo "Checking if the OpenMetadata container is running"
if [ "$( docker container inspect -f '{{.State.Status}}' openmetadata_ingestion )" = "running" ]; then
    echo "Metadata container already running"
else
    echo "Metadata container is not running, starting metadata container"
    docker compose -f $CONTAINER_FOLDER/$DOCKER_FILE up --detach
fi

# Add Snowflake connection
echo "Adding Snowflake connection to the metadata server"
metadata ingest -c $CONTAINER_FOLDER/snowflake-ingest.yaml
echo "Snowflake connection added to the metadata server"

# Add Snowflake lineage
echo "Adding Snowflake lineage to the metadata server"
metadata ingest -c $CONTAINER_FOLDER/snowflake-lineage.yaml
echo "Snowflake lineage added to the metadata server"

# TODO: debug the dbt integration
# Error: metadata.ingestion.ometa.client.APIError: Principal: CatalogPrincipal{name='ryan_weidinger'} operations [ViewBasic]
# # Add dbt local connection
# echo "Adding dbt integration to the metadata server"
# metadata ingest -c $CONTAINER_FOLDER/dbt-ingest.yaml
# echo "dbt integration added to the metadata server"