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

st.set_page_config(page_title="SQLingual", layout="wide")

top_c1, top_c2 = st.columns([.1,.9], vertical_alignment="center")

with top_c1:
    st.image("assets/logo.png", width=100)
with top_c2:
    st.markdown("Transpile SQL between 30 different dialects using [sqlglot](https://github.com/tobymao/sqlglot) 🚀 <br />The default example shows a typical TPC-H query in [Databricks](https://www.databricks.com/) and converts it into [Exasol](https://www.exasol.com)."
                , unsafe_allow_html=True)

st.divider()

input_col, output_col = st.columns(2, vertical_alignment="top")

with input_col:
    c1, c2, c3 = st.columns([.3, .5, .2], vertical_alignment="center")
    with c1:
        st.markdown("**Input SQL**")
    with c2:
        source_dialect = st.selectbox(
            "",
            label_visibility="collapsed",
            options=dialects,
            index=3
        )
    with c3:
        transpile_button = st.button("Transpile →", type="primary")

    input_sql = st_ace(
        value=default_query,
        language='sql',
        theme='github',
        key="input_sql",
        height=500,
        auto_update=True
    )

with output_col:
    c1, c2 = st.columns([.3,.7], vertical_alignment="center")
    with c1:
        st.markdown("**Transpiled SQL**")
    with c2:
        target_dialect = st.selectbox(
            "",
            label_visibility="collapsed",
            options=dialects,
            index=10
        )

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