import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Category Deep Dive", page_icon="🔍", layout="wide")

st.title("🔍 Category & Subcategory Interactive Drill-Down")
st.markdown("Visual Analytics Lab (MACSE603) &bull; Student: Vedant Nimkar (26MML0045)")

base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "..", "..", "..", "data"))
fact = pd.read_csv(os.path.join(data_dir, "FactSales_CLEAN_reference.csv"))
prod = pd.read_csv(os.path.join(data_dir, "DimProduct.csv"))
df = fact.merge(prod, on="ProductKey", how="left")

# Drill-down Selector
cat_options = df["Category"].unique().tolist()
selected_cat = st.selectbox("Select Category to Drill Down", cat_options, index=0)

sub_df = df[df["Category"] == selected_cat]

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader(f"Subcategory Sales Breakdown for '{selected_cat}'")
    subcat_grp = sub_df.groupby("Subcategory").agg(
        Revenue=("SalesAmount", "sum"),
        Units=("OrderQuantity", "sum")
    ).reset_index().sort_values("Revenue", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    bars = ax.barh(subcat_grp["Subcategory"], subcat_grp["Revenue"] / 1000, color="#10b981", edgecolor="#047857")
    ax.set_xlabel("Revenue ($ in Thousands)", color="#94a3b8")
    ax.tick_params(colors='#cbd5e1')
    for spine in ax.spines.values(): spine.set_color('#334155')
    ax.grid(axis='x', color='#1e293b', linestyle='--', alpha=0.5)
    st.pyplot(fig)

with col2:
    st.subheader(f"Top Performing SKUs in '{selected_cat}'")
    top_skus = sub_df.groupby("ProductName").agg(
        Units=("OrderQuantity", "sum"),
        Revenue=("SalesAmount", "sum")
    ).reset_index().sort_values("Revenue", ascending=False).head(8)
    top_skus["Revenue"] = top_skus["Revenue"].map("${:,.2f}".format)
    top_skus["Units"] = top_skus["Units"].map("{:,}".format)
    st.dataframe(top_skus, use_container_width=True)

st.subheader("Row-Level Transaction Inspection")
st.dataframe(
    sub_df[["SalesOrderNumber", "OrderDate", "ProductName", "Subcategory", "OrderQuantity", "UnitPrice", "SalesAmount"]].head(10),
    use_container_width=True
)
