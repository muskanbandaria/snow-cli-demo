# Import python packages
import streamlit as st
import pandas as pd
import altair as alt

import pandas as pd
from common.data_utils import get_active_session
import logging

logger = logging.getLogger("todo_app")

st.markdown("# My TODOS")
st.divider()
st.markdown(
    """A simple TODO application to demonstrate how we can use Streamlit to build a CRUD application. This application gives a quick overview of Streamlit features,

* Using DataFrame to show list of TODO

* Use Form to perform the updates to TODO

The script to create Database and its data is available at https://github.com/kameshsampath/sf-git-integration-demo.git.
"""
)
st.divider()

session = get_active_session()
# TODO how to get these variables in SiS
db_name = "TODO_APP_DB"
schema = "DATA"
table = "TODOS"
table_fqn = f"{db_name}.{schema}.{table}"
categories = {
    "learning": "Learning",
    "code": "Code",
    "personal": "Personal",
    "work": "Work",
    "finance": "Finance",
    "government": "Government",
    "others": "Others",
    "family": "Personal",
}


@st.cache_data(show_spinner=True)
def get_todos():
    todos = session.table(table_fqn)
    return todos.to_pandas()


st.session_state.todos_df = get_todos()
st.session_state.edit = False

## List to show all todos
event = st.dataframe(
    st.session_state.todos_df,
    hide_index=True,
    selection_mode=["single-row"],
    on_select="rerun",
    key="todos",
    column_config={
        "TITLE": st.column_config.TextColumn(
            label="Title",
            help="Title of the Task",
            width="medium",
        ),
        "DESCRIPTION": st.column_config.TextColumn(
            label="Desc",
            width="medium",
            help="Description of the Task",
        ),
        "CATEGORY": st.column_config.TextColumn(
            label="Category",
            help="Category of the Task",
            width="small",
        ),
        "STATUS": st.column_config.CheckboxColumn(
            label="Status",
            help="Status of the Task",
            width="small",
        ),
    },
    use_container_width=True,
)

st.markdown(
    """
            ## Add/Edit Todo
            Use the following form to edit and update the TODO.
"""
)


if event.selection and event.selection.rows:
    st.write(event.selection)
    if event.selection.rows[0] is not None:
        st.session_state.edit = True
        st.session_state.todo_title = st.session_state.todos_df.iloc[
            event.selection.rows[0]
        ]["TITLE"]
        st.session_state.todo_desc = st.session_state.todos_df.iloc[
            event.selection.rows[0]
        ]["DESCRIPTION"]
        st.session_state.todo_category = st.session_state.todos_df.iloc[
            event.selection.rows[0]
        ]["CATEGORY"]
        st.session_state.todo_status = st.session_state.todos_df.iloc[
            event.selection.rows[0]
        ]["STATUS"]


with st.container():
    if st.session_state.edit:
        st.markdown("### Edit Todo")
    else:
        st.markdown("### Add Todo")
    with st.container():
        title = st.text_input(
            "Title",
            max_chars=30,
            key="todo_title",
        )
        desc = st.text_area(
            "Description",
            max_chars=280,
            key="todo_desc",
        )

        ccol1, _ = st.columns(2)
        with ccol1:
            category = st.selectbox(
                "Pick a category",
                sorted(categories),
                key="todo_category",
                format_func=lambda x: categories[x],
            )
        scol1, _ = st.columns(2)
        with scol1:
            status = st.checkbox(
                "Status",
                key="todo_status",
            )

    _, _, col2, col3, _, _ = st.columns(6)
    with col3:
        submitted = None
        if st.session_state.edit:
            st.button("Update", type="primary")
        else:
            st.button("Add", type="primary")
        if submitted:
            logger.debug("row update")
            # TODO add record to DF
    with col2:
        reset_button = st.button(
            "Clear",
            key="todo_reset",
        )
        if reset_button:
            st.session_state.todo_title = None
            st.session_state.todo_desc = None
            st.session_state.todo_category = None
            st.session_state.todo_status = False
            st.session_state.edit = False
