--!jinja
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS {{db_name}};

CREATE WAREHOUSE IF NOT EXISTS {{wh_name}};

USE WAREHOUSE {{wh_name}};

USE DATABASE {{db_name}};

CREATE SCHEMA IF NOT EXISTS {{schema_name}};

USE SCHEMA {{schema_name}};

CREATE FILE FORMAT IF NOT EXISTS  csv_ff
    SKIP_HEADER=1;

CREATE OR REPLACE TABLE TODOS (
    TITLE STRING,
    DESCRIPTION STRING,
    CATEGORY STRING,
    STATUS BOOLEAN
);

-- List files
LS @{{git_repo_name}}/branches/{{git_branch}}/;

-- Create  the stage to copy all files from git stage to current data stage
CREATE STAGE IF NOT EXISTS git_data
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Copy fies from git into local stage
COPY FILES
  INTO @git_data
  FROM @{{git_repo_name}}/branches/{{git_branch}}/todos.csv;

-- Load the CSV into the table
COPY INTO TODOS FROM @git_data/todos.csv 
  FILE_FORMAT = csv_ff;

-- check the data
SELECT * FROM TODOS;
