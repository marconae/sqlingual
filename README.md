# SQLingual

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sqlingual.streamlit.app/)

**Translate SQL between 30+ dialects 🚀** - try it here: 👉 [sqlingual.streamlit.app](https://sqlingual.streamlit.app/)

## What can you use it for?

- Migrating from one database to the next, eg. from Databricks to Exasol
- Comparing different SQL dialects syntactically side-by-side

## Features

- **Transpile across 30+ SQL dialects** with [sqlglot](https://github.com/tobymao/sqlglot)  
- **Interactive SQL editor** powered by [streamlit-ace](https://github.com/okld/streamlit-ace)  
- **Live syntax validation** with immediate error feedback

## Run Locally

```bash
git clone https://github.com/marconae/sqlingual.git
cd sqlingual
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack

- [Streamlit](https://streamlit.io/) – web app framework  
- [sqlglot](https://github.com/tobymao/sqlglot) – SQL parser, transpiler & optimizer  
- [streamlit-ace](https://github.com/okld/streamlit-ace) – ACE editor component  
- Python 3.10+

##  Acknowledgements
- Huge thanks to [@tobymao](https://github.com/tobymao) for creating sqlglot
- [streamlit](https://streamlit.io) community for the ecosystem ❤️
