import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# Connexion PostgreSQL

from sqlalchemy import create_engine
engine = create_engine(
    "postgresql+psycopg2://user:Aishahbb22@localhost:5432/dashboard_streamlit_superstore",
    connect_args={"options": "-c client_encoding=utf8"}
)

query = "SELECT * FROM orders"

df = pd.read_sql(query, engine)

# Dashboard Title


st.title("Superstore Sales Dashboard")


# Filter


region = st.sidebar.selectbox(
    "Select Region",
    df["region"].unique()
)

df_filtered = df[df["region"] == region]


# KPIs


total_sales = df_filtered["sales"].sum()
total_profit = df_filtered["profit"].sum()

profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")


# Sales by Region Chart


sales_region = df_filtered.groupby("region")["sales"].sum().reset_index()

fig, ax = plt.subplots()

sns.barplot(data=sales_region, x="region", y="sales", ax=ax)

ax.set_title("Sales by Region")

st.pyplot(fig)


# Show Data


st.subheader("Filtered Data")

st.write(df_filtered)