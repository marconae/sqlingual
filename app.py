import streamlit as st
import sqlglot
from streamlit_ace import st_ace

dialects = [
    "athena", "bigquery", "clickhouse", "databricks", "doris", "dremio", "drill",
    "druid", "duckdb", "dune", "exasol", "fabric", "hive", "materialize", "mysql",
    "oracle", "postgres", "presto", "prql", "redshift", "risingwave", "singlestore",
    "snowflake", "spark", "spark2", "sqlite", "starrocks", "tableau", "teradata",
    "trino", "tsql"
]

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

# Validate SQL before creating UI elements
source_dialect = st.session_state.get("source_dialect", dialects[3])
current_input = st.session_state.get("input_sql", default_query)

if current_input:
    try:
        sqlglot.parse(current_input, dialect=source_dialect)
        st.session_state.sql_is_valid = True
    except Exception:
        st.session_state.sql_is_valid = False
else:
    st.session_state.sql_is_valid = False

# Top row
top_c1, top_c2, top_c3 = st.columns([.1, .3, .6], vertical_alignment="center")

with top_c1:
    st.image("assets/logo.png", width=80)
with top_c2:
    st.markdown("Transpile SQL between 30 different dialects using [sqlglot](https://github.com/tobymao/sqlglot) 🚀")
with top_c3:
    ctrl_1, ctrl_2, ctrl_3 = st.columns(3, vertical_alignment="center")

    with ctrl_1:
        source_dialect = st.selectbox(
            "",
            label_visibility="collapsed",
            options=dialects,
            index=3,
            key="source_dialect"
        )
    with ctrl_2:
        transpile_button = st.button("Transpile →", type="primary", disabled=not st.session_state.sql_is_valid)

    with ctrl_3:
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
    input_sql = st_ace(
        value=default_query,
        language='sql',
        theme='github',
        key="input_sql",
        height=500,
        auto_update=True
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
    if transpile_button and input_sql:
        try:
            transpiled = sqlglot.transpile(input_sql, read=source_dialect, write=target_dialect, pretty=True)[0]
            output_sql = st_ace(
                value=transpiled,
                language='sql',
                theme='github',
                key="output_sql",
                height=500,
                readonly=True,
                auto_update=True
            )
        except Exception as e:
            st.error(f"Error during transpilation: {str(e)}")
            output_sql = st_ace(
                value="",
                language='sql',
                theme='github',
                key="output_sql_error",
                height=500,
                readonly=True,
                auto_update=True
            )
    else:
        output_sql = st_ace(
            value="",
            language='sql',
            theme='github',
            key="output_sql_empty",
            height=500,
            readonly=True,
            auto_update=True
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