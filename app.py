import base64

import streamlit as st
import streamlit.components.v1 as components
from sqlglot import parse, dialects, transpile
from streamlit_ace import st_ace


# Render the SQL editor
def sql_editor(value="", key="sql_editor", height=500, readonly=False, auto_update=True):
    return st_ace(
        value=value,
        language='sql',
        theme='eclipse',
        key=key,
        height=height,
        readonly=readonly,
        auto_update=auto_update
    )


# Available dialects of sqlglot
@st.cache_data
def get_dialects():
    return sorted([dialect.lower() for dialect in dialects.DIALECTS])


DIALECTS = get_dialects()


# Default query loaded on page open
@st.cache_data
def load_sql_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


DEFAULT_QUERY = load_sql_file("assets/default_query.sql")


# Validate
def validate_sql(input_str, dialect):
    if not input_str or not input_str.strip():
        st.session_state.sql_is_valid = True
        st.session_state.validation_error = None
        return

    try:
        parse(input_str, dialect=dialect)
        st.session_state.sql_is_valid = True
        st.session_state.validation_error = None
    except Exception as err:
        st.session_state.sql_is_valid = False
        st.session_state.validation_error = str(err)


# Initialize session state
if "input_sql" not in st.session_state:
    st.session_state.input_sql = DEFAULT_QUERY
if "editor_rev" not in st.session_state:
    st.session_state.editor_rev = 0
if "sql_is_valid" not in st.session_state:
    st.session_state.sql_is_valid = True
if "validation_error" not in st.session_state:
    st.session_state.validation_error = None
if "transpiled_sql" not in st.session_state:
    st.session_state.transpiled_sql = ""
if "swap_counter" not in st.session_state:
    st.session_state.swap_counter = 0

# Swap handler
if st.session_state.get("swap_requested", False):
    swap_input = st.session_state.get("input_sql", DEFAULT_QUERY)
    swap_output = st.session_state.get("transpiled_sql", "")
    swap_src_dialect = st.session_state.source_dialect
    swap_target_dialect = st.session_state.target_dialect

    st.session_state.input_sql = swap_output
    st.session_state.transpiled_sql = swap_input
    st.session_state.source_dialect = swap_target_dialect
    st.session_state.target_dialect = swap_src_dialect

    st.session_state.swap_counter += 1
    st.session_state.swap_requested = False

    st.session_state.editor_rev += 1
    st.rerun()

# Page config
st.set_page_config(
    page_title="SQLingual",
    layout="wide",
    page_icon="assets/logo.png"
)

# Top row
top_c1, top_c2, top_c3 = st.columns([.1, .3, .6], vertical_alignment="center")

with top_c1:
    st.image("assets/logo.png", width=80)
with top_c2:
    st.markdown("Translate SQL between 30 different dialects 🚀")
with top_c3:
    # Controls row
    ctrl_1, ctrl_2, ctrl_3, ctrl_4 = st.columns([1, 6, 2, 6], vertical_alignment="center")

    with ctrl_1:
        st.markdown("From:")

    with ctrl_2:
        source_dialect = st.selectbox(
            "Source Dialect",
            label_visibility="collapsed",
            options=DIALECTS,
            index=3,
            key="source_dialect"
        )

    with ctrl_3:
        transpile_btn_slot = st.empty()

    with ctrl_4:
        target_dialect = st.selectbox(
            "Target Dialect",
            label_visibility="collapsed",
            options=DIALECTS,
            index=10,
            key="target_dialect"
        )

# Main input columns
input_col, swap_col, output_col = st.columns([12, 1, 12], vertical_alignment="top")

with input_col:
    editor_val = sql_editor(
        value=st.session_state.get("input_sql"),
        key=f"input_sql_editor_{st.session_state.editor_rev}",  # re-mount trigger
    )

    if editor_val is not None and editor_val != st.session_state.input_sql:
        st.session_state.input_sql = editor_val

# Validate input_sql, once it is updated
validate_sql(st.session_state.get("input_sql", ""), st.session_state.source_dialect)

# Create transpile button *after* validation, in the reserved slot
with ctrl_3:
    transpile_button = transpile_btn_slot.button(
        "transpile →",
        type="primary",
        help=f"Transpile query from '{source_dialect}' to '{target_dialect}'",
        key="transpile_button",   # stable key for consistency
        disabled=not st.session_state.sql_is_valid,
    )

with input_col:
    if st.session_state.validation_error:
        st.error(f"Syntax error: {st.session_state.validation_error}", icon="❌")

with swap_col:
    swap_button = st.button("⇄", help="Swap input and output queries", key="swap_button")

    if swap_button:
        st.session_state.swap_requested = True
        st.rerun()

with output_col:
    if transpile_button and st.session_state.get("input_sql"):
        try:
            st.session_state.transpiled_sql = transpile(
                st.session_state.input_sql,
                read=st.session_state.source_dialect,
                write=st.session_state.target_dialect,
                pretty=True,
            )[0]
        except Exception as parse_error:
            st.error(f"Error during transpilation: {str(parse_error)}")
            st.session_state.transpiled_sql = ""

    final_output = st.session_state.get("transpiled_sql", "")
    output_sql = sql_editor(
        value=final_output,
        key=f"output_sql_{len(final_output)}",
        readonly=True,
    )

# Footer

st.markdown(f"""
<small>SQLingual supports the following dialects: {', '.join(dialects.DIALECTS)}.</small>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.main .block-container {
    padding-top: .1rem;
    padding-bottom: .1rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)