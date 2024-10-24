import os

from snowflake.core import Root
from snowflake.core.database import Database
from snowflake.snowpark.session import Session


session = Session.builder.getOrCreate()
root = Root(session)

# Create Database to hold todo database
db_name = os.getenv("TODO_APP_DB", "TODO_APP_DB")
db = Database(
    name=db_name,
    comment="Database to hold the TODOs and its related objects",
)

root.databases[db_name].create_or_alter(db)
