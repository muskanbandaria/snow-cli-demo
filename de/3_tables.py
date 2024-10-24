import os
from snowflake.core import Root
from snowflake.snowpark.session import Session
from snowflake.core.table import Table, TableColumn


session = Session.builder.getOrCreate()
root = Root(session)

db_name = os.getenv("TODO_APP_DB", "TODO_APP_DB")
data_schema = os.getenv("TODOS_DATA_SCHEMA", "DATA")

todo_table = Table(
    name="todos",
    columns=[
        TableColumn(
            name="title",
            datatype="string",
            nullable=False,
        ),
        TableColumn(
            name="description",
            datatype="string",
            nullable=True,
        ),
        TableColumn(
            name="category",
            datatype="string",
            nullable=True,
        ),
        TableColumn(
            name="status",
            datatype="boolean",
            default="FALSE",
        ),
    ],
    comment="All TODOS data are stored in this",
)
root.databases[db_name].schemas[data_schema].tables["todos"].create_or_alter(todo_table)
