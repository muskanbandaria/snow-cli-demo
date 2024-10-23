import os
from snowflake.core import Root
from snowflake.snowpark.session import Session
from snowflake.core.schema import Schema


session = Session.builder.getOrCreate()
root = Root(session)

db_name = os.getenv("TODO_APP_DB", "TODO_APP_DB")


app_schema = os.getenv("TODO_APP_SCHEMA", "APPS")
data_schema = os.getenv("TODOS_DATA_SCHEMA", "DATA")

for name in [app_schema, data_schema]:
    new_schema = Schema(name)
    root.databases[db_name].schemas[name].create_or_alter(new_schema)
