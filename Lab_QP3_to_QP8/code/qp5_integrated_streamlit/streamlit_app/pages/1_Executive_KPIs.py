import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Executive KPIs", page_icon="📈", layout="wide")

st.title("📈 Executive Sales KPIs & Overview")
st.markdown("Visual Analytics Lab (MACSE603) &bull; Student: Vedant Nimkar (26MML0045)")

base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "..", "..", "..", "data"))
fact = pd.read_csv(os.path.join(data_dir, "FactSales_CLEAN_reference.csv"))
prod = pd.read_csv(os.path.join(data_dir, "DimProduct.csv"))
terr = pd.read_csv(os.path.join(data_dir, "DimTerritory.csv"))

fact["OrderDate"] = pd.to_datetime(fact["OrderDate"])
fact["YearMonth"] = fact["OrderDate"].dt.strftime("%Y-%m")
df = fact.merge(prod, on="ProductKey", how="left").merge(terr, on="TerritoryKey", how="left")

# Sidebar Slicers
st.sidebar.header("Interactive Filters")
sel_cat = st.sidebar.multiselect("Filter Categories", options=df["Category"].unique(), default=df["Category"].unique())
sel_region = st.sidebar.multiselect("Filter Regions", options=df["Region"].unique(), default=df["Region"].unique())

filtered = df[(df["Category"].isin(sel_cat)) & (df["Region"].isin(sel_region))]

# Metrics Row
c1, c2, c3, c4 = st.columns(4)
rev = filtered["SalesAmount"].sum()
cost = filtered["TotalCost"].sum()
profit = rev - cost
margin = (profit / rev * 100) if rev > 0 else 0

c1.metric("Selected Revenue", f"${rev:,.2f}")
c2.metric("Selected Profit", f"${profit:,.2f}")
c3.metric("Profit Margin %", f"{margin:.2f}%")
c4.metric("Orders Processed", f"{filtered['SalesOrderNumber'].nunique():,}")

st.markdown("---")

# Visual Charts
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Monthly Revenue vs Gross Profit")
    monthly = filtered.groupby("YearMonth").agg(
        Revenue=("SalesAmount", "sum"),
        Profit=("SalesAmount", lambda s: s.sum() - filtered.loc[s.index, "TotalCost"].sum())
    ).reset_index()

    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.plot(monthly["YearMonth"], monthly["Revenue"], color="#3b82f6", linewidth=2.5, label="Revenue")
    ax.plot(monthly["YearMonth"], monthly["Profit"], color="#10b981", linewidth=2.5, label="Profit")
    ax.tick_params(colors='#94a3b8', labelsize=8)
    plt.xticks(rotation=45)
    for spine in ax.spines.values(): spine.set_color('#334155')
    ax.grid(color='#1e293b', linestyle='--', alpha=0.6)
    ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#f8fafc')
    st.pyplot(fig)

with col_right:
    st.subheader("Regional Territory Share")
    reg_grp = filtered.groupby("Region")["SalesAmount"].sum()
    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    fig2.patch.set_facecolor('#0f172a')
    ax2.set_facecolor('#0f172a')
    wedges, texts, autotexts = ax2.pie(
        reg_grp, labels=reg_grp.index, autopct='%1.1f%%',
        colors=['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'],
        wedgeprops=dict(width=0.45, edgecolor='#0f172a', linewidth=2)
    )
    for t in texts: t.set_color('#cbd5e1')
    for at in autotexts: at.set_color('#ffffff'); at.set_weight('bold')
    st.pyplot(fig2)
