#!/bin/bash

# Change to the directory where the app is located
cd /app/sqlmesh-dbt-demo

# Create a python virtual environment
python3 -m venv /app/sqlmesh-dbt-demo/.venv

# Activate the python virtual environment
source /app/sqlmesh-dbt-demo/.venv/bin/activate
echo "Virtual environment '.venv' activated. Which python: $(which python)"

# Install any needed python packages specified in requirements.txt
echo "Installing python packages..."
pip install --upgrade pip
pip install -r /app/sqlmesh-dbt-demo/requirements.txt