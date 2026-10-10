import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Time Intelligence", page_icon="⏱️", layout="wide")

st.title("⏱️ Time Intelligence & YoY Analytics")
st.markdown("Visual Analytics Lab (MACSE603) &bull; Student: Vedant Nimkar (26MML0045)")

base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "..", "..", "..", "data"))
fact = pd.read_csv(os.path.join(data_dir, "FactSales_CLEAN_reference.csv"))
fact["OrderDate"] = pd.to_datetime(fact["OrderDate"])
fact["Year"] = fact["OrderDate"].dt.year
fact["Month"] = fact["OrderDate"].dt.month
fact["MonthName"] = fact["OrderDate"].dt.strftime("%b")

# Yearly Pivot
pivot = fact.pivot_table(index="Month", columns="Year", values="SalesAmount", aggfunc="sum").fillna(0)
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
pivot.index = [month_names[m-1] for m in pivot.index]

st.subheader("Monthly Revenue Comparison by Calendar Year")
fig, ax = plt.subplots(figsize=(11, 4.5))
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')

colors = {2023: '#64748b', 2024: '#3b82f6', 2025: '#10b981'}
for yr in pivot.columns:
    ax.plot(pivot.index, pivot[yr] / 1000, marker='o', linewidth=2.5, label=f"CY {yr}", color=colors.get(yr, '#8b5cf6'))

ax.set_ylabel("Revenue ($ in Thousands)", color="#94a3b8")
ax.tick_params(colors='#cbd5e1')
for spine in ax.spines.values(): spine.set_color('#334155')
ax.grid(color='#1e293b', linestyle='--', alpha=0.5)
ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#f8fafc')
st.pyplot(fig)

st.subheader("Year-over-Year (YoY) Growth Matrix")
yearly_totals = fact.groupby("Year")["SalesAmount"].sum().reset_index()
yearly_totals["YoY Growth $"] = yearly_totals["SalesAmount"].diff()
yearly_totals["YoY Growth %"] = (yearly_totals["SalesAmount"].pct_change() * 100).round(2)
yearly_totals["Revenue"] = yearly_totals["SalesAmount"].map("${:,.2f}".format)
st.dataframe(yearly_totals[["Year", "Revenue", "YoY Growth $", "YoY Growth %"]], use_container_width=True)
