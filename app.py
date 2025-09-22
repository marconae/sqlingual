import sqlglot
import streamlit as st
from streamlit_ace import st_ace


def create_sql_editor(value="", key="sql_editor", height=500, readonly=False, auto_update=True):
    """Create a SQL editor with consistent styling and configuration."""
    return st_ace(
        value=value,
        language='sql',
        theme='github',
        key=key,
        height=height,
        readonly=readonly,
        auto_update=auto_update
    )

dialects = [
    "athena", "bigquery", "clickhouse", "databricks", "doris", "dremio", "drill",
    "druid", "duckdb", "dune", "exasol", "fabric", "hive", "materialize", "mysql",
    "oracle", "postgres", "presto", "prql", "redshift", "risingwave", "singlestore",
    "snowflake", "spark", "spark2", "sqlite", "starrocks", "tableau", "teradata",
    "trino", "tsql"
]

# Default query loaded on page open
with open("assets/default_query.sql", "r") as f:
    default_query = f.read()

# Initialize session state
if "sql_is_valid" not in st.session_state:
    st.session_state.sql_is_valid = True
if "current_sql" not in st.session_state:
    st.session_state.current_sql = default_query

# Page config
st.set_page_config(
    page_title="SQLingual",
    layout="wide",
    page_icon="assets/logo.png"
)

# Get current values for validation
source_dialect = st.session_state.get("source_dialect", dialects[3])
current_input = st.session_state.get("input_sql", default_query)

# Validate current SQL
sql_is_valid = True
if current_input and current_input.strip():
    try:
        sqlglot.parse(current_input, dialect=source_dialect)
        sql_is_valid = True
    except Exception:
        sql_is_valid = False

# Top row
top_c1, top_c2, top_c3 = st.columns([.1, .3, .6], vertical_alignment="center")

with top_c1:
    st.image("assets/logo.png", width=80)
with top_c2:
    st.markdown("Transpile SQL between 30 different dialects using [sqlglot](https://github.com/tobymao/sqlglot) 🚀")
with top_c3:
    ctrl_1, ctrl_2, ctrl_3, ctrl_4 = st.columns([.1, .3,.2,.3], vertical_alignment="center")

    with ctrl_1:
        st.markdown("From:")
    with ctrl_2:
        source_dialect = st.selectbox(
            "",
            label_visibility="collapsed",
            options=dialects,
            index=3,
            key="source_dialect"
        )
    with ctrl_3:
        transpile_button = st.button("Transpile to →", type="primary", disabled=not sql_is_valid)

    with ctrl_4:
        target_dialect = st.selectbox(
            "",
            label_visibility="collapsed",
            options=dialects,
            index=10,
            key="target_dialect"
        )


# Main input columns
input_col, output_col = st.columns(2, vertical_alignment="top")

with input_col:
    input_sql = create_sql_editor(
        value=default_query,
        key="input_sql"
    )

    if input_sql:
        try:
            sqlglot.parse(input_sql, dialect=source_dialect)
            st.session_state.sql_is_valid = True
        except Exception as e:
            st.error(f"Syntax error: {str(e)}", icon="❌")
            st.session_state.sql_is_valid = False
    else:
        st.session_state.sql_is_valid = False

with output_col:
    # Handle transpilation
    output_value = ""

    if transpile_button and input_sql:
        try:
            output_value = sqlglot.transpile(input_sql, read=source_dialect, write=target_dialect, pretty=True)[0]
            # Store the result in session state to persist it
            st.session_state.transpiled_sql = output_value
        except Exception as e:
            st.error(f"Error during transpilation: {str(e)}")
            st.session_state.transpiled_sql = ""

    # Get the transpiled SQL from session state if it exists
    final_output = st.session_state.get("transpiled_sql", "")

    # Output editor with dynamic key to force refresh
    output_sql = create_sql_editor(
        value=final_output,
        key=f"output_sql_{len(final_output)}",
        readonly=True
    )

st.markdown("""
<style>
.main .block-container {
    padding-top: .1rem;
    padding-bottom: .1rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)