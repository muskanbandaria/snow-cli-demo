import os
from snowflake.core import Root
from snowflake.core.warehouse import Warehouse
from snowflake.snowpark.session import Session


session = Session.builder.getOrCreate()
root = Root(session)

name = os.getenv("TODO_APP_WH", "TODO_APP_WH")

todos_wh = Warehouse(name)
todos_wh.warehouse_size = "SMALL"
todos_wh.auto_suspend = 120
todos_wh.initially_suspended = "true"

root.warehouses[todos_wh].create_or_alter(todos_wh)
