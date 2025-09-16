import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Streamlit Page Configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Interactive Sales Dashboard")

# Sidebar Options
st.sidebar.header("Controls")

data_source = st.sidebar.radio("Select Data Source", ["Excel", "SQL"])

# API endpoint based on selection
if data_source == "Excel":
    url = "http://127.0.0.1:5000/api/xlsx"
else:
    url = "http://127.0.0.1:5000/api/sql"

# Fetch Data
try:
    response = requests.get(url)

    # Check if response is valid JSON
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            st.error("❌ The response is not in JSON format.")
            st.code(response.text, language="text")
            st.stop()

        # Convert JSON to DataFrame
        df = pd.DataFrame(data)

        # Fix: Convert numeric columns
        if "Total" in df.columns:
            df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

        # KPIs
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)

        if "Total" in df.columns:
            with col1:
                st.metric("Total Sales", f"${df['Total'].sum():,.2f}")
            with col2:
                st.metric("Average Sale", f"${df['Total'].mean():,.2f}")
            with col3:
                st.metric("Transactions", f"{len(df)}")
        else:
            st.info("⚠ No 'Total' column found in data")

        # Filters
        st.sidebar.subheader("Filters")

        if "Gender" in df.columns:
            gender_filter = st.sidebar.multiselect(
                "Select Gender",
                df["Gender"].unique(),
                default=df["Gender"].unique()
            )
            df = df[df["Gender"].isin(gender_filter)]

        if "Product line" in df.columns:
            product_filter = st.sidebar.multiselect(
                "Select Product Line",
                df["Product line"].unique(),
                default=df["Product line"].unique()
            )
            df = df[df["Product line"].isin(product_filter)]

        # Visualizations
        st.subheader("Visualizations")
        col1, col2 = st.columns(2)

        with col1:
            if "Gender" in df.columns and "Total" in df.columns:
                fig1 = px.bar(df, x="Gender", y="Total", color="Gender", title="Sales by Gender")
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            if "Product line" in df.columns and "Total" in df.columns:
                fig2 = px.pie(df, names="Product line", values="Total", title="Sales by Product Line")
                st.plotly_chart(fig2, use_container_width=True)

        # Time Series Analysis
        st.subheader("Time Series Analysis")
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df_time = df.groupby("Date")["Total"].sum().reset_index()
            fig3 = px.line(df_time, x="Date", y="Total", title="Sales Over Time")
            st.plotly_chart(fig3, use_container_width=True)

        # Raw Data
        with st.expander("📂 View Raw Data"):
            st.dataframe(df)

    else:
        st.error(f"❌ Failed to fetch data. Status code: {response.status_code}")
        st.code(response.text, language="text")

except requests.exceptions.RequestException as e:
    st.error(f"Connection error: {e}")
