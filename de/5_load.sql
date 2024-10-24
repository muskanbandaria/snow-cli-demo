--!jinja

USE WAREHOUSE {{wh_name}};

USE DATABASE {{db_name}};

USE SCHEMA {{schema_name}};

CREATE FILE FORMAT IF NOT EXISTS  csv_ff
    SKIP_HEADER=1;

-- referesh repository content
ALTER GIT REPOSITORY {{git_repo_name}} FETCH;

-- Copy fies from git into local stage
COPY FILES
  INTO @git_data
  FROM @{{git_repo_name}}/branches/{{git_branch}}/data/todos.csv;

-- Load the CSV into the table
COPY INTO TODOS FROM @git_data/todos.csv 
  FILE_FORMAT = csv_ff;

-- check the data
SELECT * FROM TODOS;
