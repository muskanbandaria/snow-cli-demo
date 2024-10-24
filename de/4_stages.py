import os

from snowflake.core import Root
from snowflake.snowpark.session import Session
from snowflake.core.stage import Stage, StageEncryption, StageDirectoryTable
from snowflake.core import CreateMode

session = Session.builder.getOrCreate()
root = Root(session)

db_name = os.getenv("TODO_APP_DB", "TODO_APP_DB")
data_schema = os.getenv("TODOS_DATA_SCHEMA", "DATA")

git_data = Stage(
    name="git_data",
    directory_table=StageDirectoryTable(enable=True),
    encryption=StageEncryption(
        type="SNOWFLAKE_SSE",
    ),
)

stages = root.databases[db_name].schemas[data_schema].stages
stages.create(git_data, mode=CreateMode.if_not_exists)
