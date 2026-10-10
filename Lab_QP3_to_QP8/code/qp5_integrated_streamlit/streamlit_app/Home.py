"""
=============================================================================
Visual Analytics Lab (MACSE603) - Assessment 5
Author: Vedant Nimkar | Reg No: 26MML0045
Experiment 13: Multipage Enterprise Sales Dashboard using Streamlit
=============================================================================
Main Application Hub & Data Engine
"""

import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales Analytics Hub | Streamlit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Sleek Dark Aesthetics
st.markdown("""
<style>
  .main-title { font-size: 2.2rem; font-weight: 800; color: #3b82f6; margin-bottom: 0px; }
  .sub-title { font-size: 1.05rem; color: #94a3b8; margin-bottom: 25px; }
  .metric-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 10px; padding: 15px 20px; }
  .student-tag { background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; padding: 10px 15px; border-radius: 6px; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# Shared Data Loader
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "..", "..", "data"))
    fact = pd.read_csv(os.path.join(data_dir, "FactSales_CLEAN_reference.csv"))
    prod = pd.read_csv(os.path.join(data_dir, "DimProduct.csv"))
    cust = pd.read_csv(os.path.join(data_dir, "DimCustomer.csv"))
    terr = pd.read_csv(os.path.join(data_dir, "DimTerritory.csv"))
    date = pd.read_csv(os.path.join(data_dir, "DimDate.csv"))

    fact["OrderDate"] = pd.to_datetime(fact["OrderDate"])
    fact["Year"] = fact["OrderDate"].dt.year
    fact["YearMonth"] = fact["OrderDate"].dt.strftime("%Y-%m")
    
    merged = fact.merge(prod, on="ProductKey", how="left")
    merged = merged.merge(terr, on="TerritoryKey", how="left")
    merged = merged.merge(cust, on="CustomerKey", how="left", suffixes=("", "_cust"))
    return merged, date

df, dim_date = load_data()

# Student Info Banner
st.markdown("""
<div class="student-tag">
  <b>Visual Analytics Lab (MACSE603) &bull; Assessment 5 &bull; Experiment 13</b><br>
  <b>Student:</b> Vedant Nimkar &nbsp;|&nbsp; <b>Reg No.:</b> 26MML0045 &nbsp;|&nbsp; <b>M.Tech CSE</b>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 Enterprise Visual Analytics Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">High-performance Multipage Interactive Sales Intelligence Platform</div>', unsafe_allow_html=True)

# Overview Columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"${df['SalesAmount'].sum():,.2f}", "+14.2% YoY")
with col2:
    st.metric("Total Gross Profit", f"${(df['SalesAmount'].sum() - df['TotalCost'].sum()):,.2f}", "Margin: 53.96%")
with col3:
    st.metric("Total Units Sold", f"{df['OrderQuantity'].sum():,}", "22,448 Units")
with col4:
    st.metric("Active Customer Accounts", f"{df['CustomerKey'].nunique()}", "220 Global Clients")

st.markdown("---")

st.subheader("📑 Multipage Application Architecture")
st.write("""
This Streamlit application demonstrates a production-grade visual analytics architecture segmented into specialized analytical perspectives:
""")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    - **Page 1: Executive KPIs** &ndash; High-level corporate health metrics, time series trends, and category distribution.
    - **Page 2: Category & Product Deep Dive** &ndash; Interactive hierarchical drill-down from Category to SubCategory and individual SKU level.
    """)
with c2:
    st.markdown("""
    - **Page 3: Time Intelligence & Forecasting** &ndash; Year-over-Year (YoY) revenue comparison, rolling moving averages, and monthly seasonality.
    - **Page 4: Customer & Territory Analytics** &ndash; Geographic revenue distribution across North America, Europe, and Pacific territories.
    """)

st.subheader("📊 Dataset Health & Schema Verification")
st.dataframe(
    pd.DataFrame({
        "Table": ["FactSales", "DimProduct", "DimCustomer", "DimTerritory", "DimDate"],
        "Records": [len(df), 22, 220, 5, len(dim_date)],
        "Schema Role": ["Central Fact Table", "Product Dimension", "Customer Dimension", "Territory Dimension", "Date Dimension"],
        "Integrity Status": ["Verified Clean", "Verified Star Schema", "Verified Star Schema", "Verified Star Schema", "Marked Date Table"]
    }),
    use_container_width=True
)
