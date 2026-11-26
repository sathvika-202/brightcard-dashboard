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
from openai import OpenAI

st.divider()
st.subheader("Ask a question about your sales")
question = st.text_input("Example: Which store sold the most in the week of Oct 12?")

if question:
    data_summary = (df.groupby(["week", "store", "category"])["sales"]
                      .sum().reset_index().to_csv(index=False))

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[
            {"role": "system",
             "content": ("You are a sales analyst for BrightCart. Answer ONLY using "
                         "the data provided. If the answer is not in the data, say "
                         "you don't have that information. Keep answers short.")},
            {"role": "user",
             "content": f"Sales data (CSV):\n{data_summary}\n\nQuestion: {question}"},
        ],
    )
    st.write(response.choices[0].message.content)
