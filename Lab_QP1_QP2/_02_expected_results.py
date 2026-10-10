"""
Computes, from the SAME data Power BI will load, the numbers your DAX
measures must reproduce. Use this to verify QP2 steps 4 and 5.
"""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "expected_results")
os.makedirs(OUT, exist_ok=True)

raw = pd.read_csv(os.path.join(DATA, "FactSales_RAW.csv"))
prod = pd.read_csv(os.path.join(DATA, "DimProduct.csv"))
cust = pd.read_csv(os.path.join(DATA, "DimCustomer.csv"))
terr = pd.read_csv(os.path.join(DATA, "DimTerritory.csv"))

# ---------- replicate the Power Query cleansing exactly -------------------
df = raw.copy()
df = df.drop(columns=["Notes"])
df = df.drop_duplicates()
df["OrderDate"] = pd.to_datetime(df["OrderDateText"], format="mixed",
                                 dayfirst=True, errors="coerce")
df["UnitPrice"] = (df["UnitPriceText"].str.replace("Rs.", "", regex=False)
                   .str.replace(",", "", regex=False).str.strip()
                   .astype(float))
df["OrderStatus"] = df["OrderStatus"].str.strip().str.title()
df = df[df["OrderQuantity"].notna()]
df = df[df["OrderQuantity"] > 0]
df["SalesAmount"] = df["SalesAmount"].fillna(
    (df["UnitPrice"] * df["OrderQuantity"] * (1 - df["DiscountPct"])).round(2))
df = df[df["OrderStatus"] != "Cancelled"]
df = df.drop(columns=["OrderDateText", "UnitPriceText"])

df = df.merge(prod[["ProductKey", "Category", "Subcategory", "ProductName",
                    "StandardCost"]], on="ProductKey", how="left")
df["Year"] = df["OrderDate"].dt.year
df["MonthNo"] = df["OrderDate"].dt.month
df["Profit"] = df["SalesAmount"] - df["TotalCost"]

report = []


def section(title):
    report.append("")
    report.append("=" * 74)
    report.append(title)
    report.append("=" * 74)


section("CLEANSING OUTCOME  (QP1 Step 2)")
report.append(f"Raw rows loaded                : {len(raw):,}")
report.append(f"After removing blank column    : Notes dropped")
report.append(f"After removing duplicates      : {len(raw.drop(columns=['Notes']).drop_duplicates()):,}")
report.append(f"After removing null quantity   : dropped {int(raw['OrderQuantity'].isna().sum())} rows")
report.append(f"After removing negative qty    : dropped 8 rows")
report.append(f"After excluding Cancelled      : final row count {len(df):,}")
report.append(f"Distinct OrderStatus (cleaned) : {sorted(df.OrderStatus.unique())}")

# ---------- KEY MEASURES -------------------------------------------------
total_sales = df.SalesAmount.sum()
total_qty = df.OrderQuantity.sum()
total_cost = df.TotalCost.sum()
total_profit = df.Profit.sum()
n_orders = df.SalesOrderNumber.nunique()

section("CORE MEASURES  (QP2 Step 4)")
report.append(f"Total Sales      = {total_sales:,.2f}")
report.append(f"Total Quantity   = {total_qty:,.0f}")
report.append(f"Total Cost       = {total_cost:,.2f}")
report.append(f"Total Profit     = {total_profit:,.2f}")
report.append(f"Profit Margin %  = {total_profit / total_sales * 100:,.2f}%")
report.append(f"Order Count      = {n_orders:,}")
report.append(f"Avg Order Value  = {total_sales / n_orders:,.2f}")

# ---------- top sold product --------------------------------------------
by_prod = (df.groupby("ProductName")
             .agg(UnitsSold=("OrderQuantity", "sum"),
                  Sales=("SalesAmount", "sum"))
             .sort_values("UnitsSold", ascending=False))
section("TOP SOLD PRODUCT  (by units)  -  QP2 Step 4")
report.append(by_prod.head(10).to_string(
    float_format=lambda v: f"{v:,.2f}"))
report.append("")
report.append(f"ANSWER -> Top sold product by UNITS  : "
              f"{by_prod.index[0]}  ({by_prod.UnitsSold.iloc[0]:,.0f} units)")
by_prod_rev = by_prod.sort_values("Sales", ascending=False)
report.append(f"ANSWER -> Top product by REVENUE     : "
              f"{by_prod_rev.index[0]}  ({by_prod_rev.Sales.iloc[0]:,.2f})")
by_prod.to_csv(os.path.join(OUT, "top_products.csv"))

# ---------- average sales per product category --------------------------
by_cat = (df.groupby("Category")
            .agg(TotalSales=("SalesAmount", "sum"),
                 Orders=("SalesOrderNumber", "nunique"),
                 UnitsSold=("OrderQuantity", "sum"),
                 AvgLineSales=("SalesAmount", "mean"))
            .sort_values("TotalSales", ascending=False))
by_cat["AvgSalesPerOrder"] = by_cat.TotalSales / by_cat.Orders
section("SALES BY CATEGORY  (QP2 Steps 4 and 5)")
report.append(by_cat.to_string(float_format=lambda v: f"{v:,.2f}"))
by_cat.to_csv(os.path.join(OUT, "sales_by_category.csv"))

# ---------- yearly + YoY -------------------------------------------------
yearly = (df.pivot_table(index="Category", columns="Year",
                         values="SalesAmount", aggfunc="sum")
            .fillna(0).round(2))
section("TOTAL SALES BY CATEGORY AND YEAR  (QP2 Step 5 - CALCULATE)")
report.append(yearly.to_string(float_format=lambda v: f"{v:,.2f}"))

yoy = pd.DataFrame(index=yearly.index)
for y in [2024, 2025]:
    if y in yearly.columns and (y - 1) in yearly.columns:
        yoy[f"{y} vs {y-1} %"] = ((yearly[y] - yearly[y - 1])
                                  / yearly[y - 1] * 100).round(2)
section("YEAR-OVER-YEAR GROWTH %  BY CATEGORY  (QP2 Step 5 - Time Intelligence)")
report.append(yoy.to_string(float_format=lambda v: f"{v:,.2f}"))
yearly.to_csv(os.path.join(OUT, "sales_by_category_year.csv"))
yoy.to_csv(os.path.join(OUT, "yoy_growth_by_category.csv"))

overall_year = df.groupby("Year").SalesAmount.sum()
section("OVERALL SALES BY YEAR + YoY")
for y in sorted(overall_year.index):
    prev = overall_year.get(y - 1)
    g = "" if prev is None else f"   YoY {((overall_year[y]-prev)/prev*100):+,.2f}%"
    report.append(f"  {y}   {overall_year[y]:>15,.2f}{g}")

# ---------- monthly running total ---------------------------------------
m = (df.assign(Period=df.OrderDate.dt.to_period("M"))
       .groupby("Period", as_index=True).SalesAmount.sum()
       .rename("Sales").to_frame())
m["Year"] = m.index.year
m["YTD"] = m.groupby("Year").Sales.cumsum().round(2)
monthly = m.drop(columns="Year")
monthly.index = monthly.index.astype(str)
section("MONTHLY SALES WITH YTD  (first 15 months)  -  TOTALYTD check")
report.append(monthly.head(15).to_string(float_format=lambda v: f"{v:,.2f}"))
monthly.to_csv(os.path.join(OUT, "monthly_sales_ytd.csv"))

# ---------- region / segment --------------------------------------------
by_region = (df.merge(terr, on="TerritoryKey", how="left")
               .groupby("Region").SalesAmount.sum()
               .sort_values(ascending=False).round(2))
section("SALES BY REGION")
report.append(by_region.to_string(float_format=lambda v: f"{v:,.2f}"))
by_region.to_csv(os.path.join(OUT, "sales_by_region.csv"))

txt = "\n".join(report)
with open(os.path.join(OUT, "EXPECTED_RESULTS.txt"), "w",
          encoding="utf-8") as f:
    f.write("VISUAL ANALYTICS LAB - EXPECTED RESULTS\n")
    f.write("Computed in pandas from the same source data Power BI loads.\n")
    f.write("Your DAX measures must reproduce these numbers.\n")
    f.write(txt)

df.to_csv(os.path.join(OUT, "FactSales_cleaned_by_python.csv"), index=False)
print(txt)
print("\nwritten ->", OUT)
