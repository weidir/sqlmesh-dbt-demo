# Tech Demo: SQLMesh and dbt Example Data Project

<img src="assets/images/sqlmesh_dbt_icons.png" width=300 height=100 />

## Table of contents:
- [Background and context](#background-and-context)
- [Setup steps](#setup-steps-for-this-demo)
- [Running this application](#running-this-application)
- [Structure of the repo](#structure-of-the-repo)

## Background and context
### What this application is:
This is a basic demonstration of a <b> proposed tech stack and development pattern </b> used to build data products using modern DataOps techniques. It is meant to serve as an <b> example of good data engineering patterns </b> when building <b> data products </b>.

The basic stack of the application includes:
- <b>dbt</b>: for executing SQL code to transform and build data objects
- <b>Snowflake</b>: connection to Snowflake database for storing and processing data
- <b>SQLMesh</b>: DataOps framework for executing SQL pipelines, building data environments
- <b>python</b>: for creating test data if necessary

### What this application does:
1. <i>(optional)</i> Generates basic, synthetic test data that mimics the kinds of data typically found in consumer enterprises (e.g., CPG)
2. Execute basic dbt transformations using SQLMesh for DataOps on this test data that mimic the kinds of transformations typical for this kind of data
3. Builds an example data product

## Setup steps for this demo
1. Make sure you have the correct software packages installed
    - <b>python</b> (v3.9 or newer)
    - <b>dbt</b> (v1.8 or newer preferred)
    - <b>git</b> (v2 or newer preferred)
    - <i>(optional)</i> <b>SQLMesh</b> (v0.110.0 or newer preferred)
    - <i>(optional)</i> <b>make</b> for lifestyle enhancements, easy recipes for development, building, testing code
    - <i>(optional)</i> <b>Docker</b> to run application in linux container
2. First, clone the repository to your local machine to begin working. This is done with the ```git clone <https_url>``` command. The HTTPS URL for the git repo where this repo is stored should be available on the git hosting website where this application's code is hosted (e.g., GitHub, GitLab, Bitbucket).
3. (Optional but recommended) Create a python virtual environment with the command: ```python3 -m venv /path/to/new/virtual/environment``` (on Windows this command is ```python -m venv c:\path\to\myenv```); once complete, activate the virtual environment with the command ```source <venv>/bin/activate``` using bash or zsh (on Linux or MacOS), or on Windows ```<venv>\Scripts\activate.bat``` using 'cmd.exe' or ```<venv>\Scripts\Activate.ps1``` using PowerShell. Check which version of python is being used with the ```which python``` (on MacOS and Linux) or ```where python``` on Windows.
4. Install all necessary python packages using the command: ```python3 -m pip install -r requirements.txt```
5. If choosing to authenticate with Snowflake using username and password stored in local environment files, create a '.env' file in the root directory of the application and store the following: 
```
USER = '<Snowflake username>'
PASSWORD = '<Snowflake password>'
ACCOUNT = '<org name>-<account name>'
WAREHOUSE = '<warehouse name>'
```
Note: there are other ways of authenticating, please follow the standards prescribed by your organization/client. If choosing another method, you will have to set up your environment accordingly using [this guide](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect).

6. Initialize the dbt project by navigating to the 'dbt_src' directory and running the ```dbt init``` command. This will prompt you through multiple setup steps, including:
* 'Which database would you like to use?' -> select option for snowflake
* account: <snowflake_orgname>-<snowflake_account_name> # NOTE: when signed into Snowflake in your web browser your org and account names can be found here: 'https://app.snowflake.com/<org_name>/<account_name>/'
* user: <snowflake_username>
* Desired authentication type option (enter a number): [1] password [2] keypair [3] sso
    * (Depending on authentication method, dbt will prompt for password, keypair, or sso info)
* role: <snowflake_dev_role>
* warehouse: <snowflake_warehouse>
* database: <snowflake_database> # (should probably be either DEV or PROD)
* schema: <snowflake_schema> # (e.g., PUBLIC)
* threads [1]: (leaving set to 1 is fine)

These setup steps will create 'profiles.yml' file and '.user.yml' files in your home directory (```~/.dbt/profiles.yml```). Make sure your 'profiles.yml' looks like this before proceding:
```
dbt_src:
  target: <snowflake_database> (dev or prod)
  outputs:
    <snowflake_database>:
      account: <snowflake_orgname-snowflake_account_name>
      database: <snowflake_database>
      password: <snowflake_user_password>
      role: <snowflake_role_name>
      schema: PUBLIC # default
      threads: 1 # default
      type: snowflake
      user: <snowflake_user_name>
      warehouse: <snowflake_warehouse_name>
```
NOTE: you can optionally choose to move the 'profiles.yml' and '.user.yml' files to your dbt project directory as well so they are easier to make edits to

7. Initialize SQLMesh application by running the ```sqlmesh init -t dbt``` command in the 'dbt_src' directory. This will create a 'config.py' file if it does not exist already. The '-t dbt' option given to the init command creates a SQLMesh application using a dbt template, so SQLMesh can run essentially on top of dbt.

8. <i>(optional)</i> If running this application in a container, run the following commands in the application root directory:
```
docker build -t "<image_name>" .
docker run -di --name <container_name> <image_name>
```
Note: (1) The "-di" argument in the docker run command means to run the container in detached and interactive and interactive mode, see [this documentation](https://docs.docker.com/reference/cli/docker/container/run/) for more details (2) There are also convenient make recipes for these commands, ```make build``` and ```make run_docker``` respectively.

## Running this application
### Running with SQLMesh (recommended)
1. The entire application can be <b>run in just one command</b> using SQLMesh: ```make plan```. This make recipe is an abstraction for the ```sqlmesh plan``` command, that uses the SQLMesh framework to:
    * <b>Interpret dbt resources</b> like models and schemas
    * <b>Read and assess all dbt models</b> that have been defined
    * <b>Materialize the models</b> according to specifications in the dbt_project.yml file
    * <b>Backfill data</b> upon any updates to the models, including both:
        * <i>Non-breaking changes</i> like adding new columns
        * <i>Breaking changes</i> like changing a column name, the SQL that computes that column, etc.
2. If changes to any models/objects have been made since the last SQLMesh plan, SQLMesh will ask you if you would like to backfill any tables with the updates. If you want to backfill, simply type ```y``` and hit enter in the command line.
3. SQLMesh provides a web-based UI for managing projects that provides helpful resources including an IDE, a dynamic DAG visualization, environment toggle, easy debugging messages, model/object metadata cataloging. 
    * Simply run the ```make ui``` command to start up the web server
    * Once the server is running, navigate to the localhost url provided to see and interact the application

### Running with dbt
1. Similarly to sqlmesh, the entire pipeline can be run in just one command using dbt: ```make run```. This make recipe is an abstraction for the ```dbt run``` command. Running this command will:
    * <b>Read and assess all dbt models</b> that have been defined
    * <b>Materialize the models</b> according to specifications in the dbt_project.yml file

### (optional) Generating test data
1. For this demo, we will generate synthetic data to perform transformations on. This can be done using the ```make generate``` command in the CLI.
    * You will be <b>prompted to make several inputs</b>, including
        * Which environment to create data for (dev, prod, or both)
        * How many fake records to create
        * Where to persist the data to (e.g., Snowflake, CSV)
    * By default, synthetic data will be <b>written to Snowflake</b>, the "DEV" database and "RAW" schema more specifically
    * By default, schemas will be created for sqlmesh/dbt to materializ models into, including "BRONZE", "SILVER", and "GOLD"

## Structure of the repo
We've included summaries of the critical parts of the application structure:
```
|__ dbt_src: folder containing all dbt/SQLMesh resources, including models and macros
    |__ models: folder to hold all model definitions/transformations and schemas
        |__ bronze: 'bronze' data layer models, typically conforming raw data to correct data schemas
        |__ silver: 'silver' data layer models, typically handling basic data issues and preparing bronze data for consumption
        |__ gold: 'gold' data layer models, typically calculating metrics and modeling data into data products
    |__ macros: folder to contain all dbt macros
        |__ generate_schema_name.sql: defines a macro to adjust the schema naming convention of dbt
    |-- dbt_project.yml: dbt project definition file containing configuration of dbt project
    |-- profiles.yml: contains dbt profile and connection configurations
    |-- config.py: SQLMesh configuration file
|__ data: folder containing scripts related to generating synthetic test data for use in this application
    |-- create_data.py: script to create test data
    |-- drop_data.py: script to delete test data
    |__ src: folder holding test data generation classes and methods
        |-- testdataclasses.py: contains definitions of all test data classes, methods to generate fake data
        |-- testdata.py: contains definition of abstract test data class, methods to generate and write fake data
        |-- pipeline.py: contains definition of test data pipeline, methods for generating and writing batches of fake data
        |-- model.yml: defines dependencies and foreign keys between test classes
    |__ utils: folder containing utility classes
        |-- envs.py: enum class enumerating environments to write to (dev and prod)
        |-- formats.py: enum class enumerating storage formats supports (e.g., snowflake, CSV)
        |-- progressbar.py: class to help visualize test data creation progress
    |__ sql: folder containing all SQL code
        |-- create_db_schema_dev.sql: SQL code that creates DEV database and schemas
        |-- create_db_schema_prod.sql: SQL code that creates PROD database and schemas
        |-- drop_schema_table_dev.sql: SQL code that drops DEV schemas and tables (including raw data)
        |-- drop_schema_table_nonraw_dev.sql: SQL code that drops DEV schemas and tables excluding RAW schema
        |-- drop_schema_table_nonraw_prod.sql: SQL code that drops PROD schemas and tables excluding RAW schema
        |-- drop_schema_table_prod.sql: SQL code that drops PROD schemas and tables (including raw data)
|__ docker:
    |-- dockerfile: defines Docker container for running application in container
    |-- dockerfile.dockerignore: defines what files and folders to ignore when dockerizing the application
    |-- python_statup.sh: shell script initializing python environment in the container
|-- makefile: defines 'make' recipes to improve quality of life for developers
|-- requirements.txt: defines all the python modules required to run the application
|-- (local) .env: [TO BE CREATED BY EACH DEVELOPER] environment file containing sensitive Snowflake connection parameters
    
```