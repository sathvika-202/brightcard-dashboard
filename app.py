import pandas as pd
import streamlit as st

st.set_page_config(page_title="BrightCart Weekly Sales", layout="wide")
st.title("BrightCart Weekly Sales Dashboard")

df = pd.read_csv("clean_data.csv", parse_dates=["date"])
df["week"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")

# Store filter
stores = st.sidebar.multiselect(
    "Select stores", df["store"].unique(), default=list(df["store"].unique()))
df = df[df["store"].isin(stores)]

# Headline number
st.metric("Total sales", f"{df['sales'].sum():,.0f}")

# Weekly sales chart
st.subheader("Weekly sales by store")
weekly = df.groupby(["week", "store"])["sales"].sum().reset_index()
st.line_chart(weekly.pivot(index="week", columns="store", values="sales"))

# Top categories
st.subheader("Top categories")
top = (df.groupby("category")["sales"].sum()
         .sort_values(ascending=False).reset_index())
st.dataframe(top, use_container_width=True)