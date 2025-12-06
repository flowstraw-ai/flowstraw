import sqlite3
import pandas as pd
import streamlit as st

# 🔴 IMPORTANT: change this if your DB file name is different
DB_PATH = "flowstraw.db"   # e.g. "app.db" or "data/flowstraw.db"

st.set_page_config(page_title="FlowStraw Analytics", layout="wide")

st.title("📊 FlowStraw Analytics Dashboard")
st.write("Analyze curated data loaded through the FlowStraw ingestion engine.")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# --- List tables dynamically ---
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
table_list = tables["name"].tolist()

if not table_list:
    st.error("No tables found in the database. Check DB_PATH or your ingestion step.")
else:
    selected_table = st.selectbox("Choose a table to explore:", table_list)

    if selected_table:
        st.subheader(f"Table Preview: {selected_table}")

        # Preview first 200 rows
        df = pd.read_sql(f"SELECT * FROM {selected_table} LIMIT 200;", conn)
        st.dataframe(df, use_container_width=True)

        # Basic summary
        st.subheader("Column-level Summary")
        with st.expander("Show summary statistics"):
            st.write(df.describe(include="all"))

        # Numeric column chart
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if numeric_cols:
            st.subheader("Numeric Column Distribution")
            col_choice = st.selectbox("Select a numeric column:", numeric_cols)
            if col_choice:
                st.bar_chart(df[col_choice])
        else:
            st.info("No numeric columns detected for charting in this table.")

        # Optional: simple custom query section
        st.subheader("Run a custom SQL query")
        default_query = f"SELECT * FROM {selected_table} LIMIT 20;"
        user_query = st.text_area("SQL", value=default_query, height=120)

        if st.button("Run query"):
            try:
                result_df = pd.read_sql(user_query, conn)
                st.dataframe(result_df, use_container_width=True)
                st.success(f"Returned {len(result_df)} rows.")
            except Exception as e:
                st.error(f"Error running query: {e}")

# Close connection when done
conn.close()
