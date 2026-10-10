import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Analytics", page_icon="👥", layout="wide")

st.title("👥 Customer & Segment Analytics")
st.markdown("Visual Analytics Lab (MACSE603) &bull; Student: Vedant Nimkar (26MML0045)")

base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "..", "..", "..", "data"))
fact = pd.read_csv(os.path.join(data_dir, "FactSales_CLEAN_reference.csv"))
cust = pd.read_csv(os.path.join(data_dir, "DimCustomer.csv"))
df = fact.merge(cust, on="CustomerKey", how="left")

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Revenue by Customer Segment")
    seg_grp = df.groupby("Segment")["SalesAmount"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.pie(
        seg_grp["SalesAmount"], labels=seg_grp["Segment"], autopct='%1.1f%%',
        colors=['#3b82f6', '#10b981', '#f59e0b'],
        textprops=dict(color='#cbd5e1')
    )
    st.pyplot(fig)

with col2:
    st.subheader("Top 10 High-Value Customer Accounts")
    top_cust = df.groupby(["CustomerName", "Segment"]).agg(
        Orders=("SalesOrderNumber", "nunique"),
        TotalSpend=("SalesAmount", "sum")
    ).reset_index().sort_values("TotalSpend", ascending=False).head(10)
    top_cust["TotalSpend"] = top_cust["TotalSpend"].map("${:,.2f}".format)
    st.dataframe(top_cust, use_container_width=True)
