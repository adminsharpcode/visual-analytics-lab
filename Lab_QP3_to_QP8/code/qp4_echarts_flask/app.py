"""
=============================================================================
Visual Analytics Lab (MACSE603) - Assessment 4 & 5
Author: Vedant Nimkar | Reg No: 26MML0045
Experiment 11: Flask Backend API for Enterprise Sales Analytics
=============================================================================
Exposes REST endpoints connecting to Excel and relational star schema
datasets using pandas DataFrames. Supports dynamic filtering, drilldown,
and CORS for interactive frontend visualization (Apache ECharts).
"""

import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data"))
EXCEL_PATH = os.path.join(DATA_DIR, "SalesData.xlsx")
CLEAN_CSV = os.path.join(DATA_DIR, "FactSales_CLEAN_reference.csv")
SQLITE_DB = os.path.join(DATA_DIR, "SalesAnalytics.db")


def init_database_and_load_data():
    """
    Loads data from Excel/CSV into a consolidated analytical pandas DataFrame
    and also syncs into a local SQLite database to fulfill SQL source requirement.
    """
    # 1. Load Dimension Tables
    dim_product = pd.read_csv(os.path.join(DATA_DIR, "DimProduct.csv"))
    dim_customer = pd.read_csv(os.path.join(DATA_DIR, "DimCustomer.csv"))
    dim_territory = pd.read_csv(os.path.join(DATA_DIR, "DimTerritory.csv"))
    dim_date = pd.read_csv(os.path.join(DATA_DIR, "DimDate.csv"))

    # 2. Load Fact Table
    if os.path.exists(CLEAN_CSV):
        fact = pd.read_csv(CLEAN_CSV)
    elif os.path.exists(EXCEL_PATH):
        fact = pd.read_excel(EXCEL_PATH, sheet_name="FactSales_RAW")
        # Cleansing pipeline if raw is loaded
        fact = fact.dropna(subset=["OrderQuantity", "UnitPriceText"]).copy()
        fact["UnitPrice"] = fact["UnitPriceText"].astype(str).str.replace("$", "").str.replace(",", "").astype(float)
        fact["SalesAmount"] = fact["OrderQuantity"] * fact["UnitPrice"] * (1 - fact["DiscountPct"].fillna(0))
        fact["TotalCost"] = fact["SalesAmount"] * 0.46
    else:
        raise FileNotFoundError("Sales dataset not found in data directory.")

    fact["OrderDate"] = pd.to_datetime(fact["OrderDate"])
    fact["Year"] = fact["OrderDate"].dt.year
    fact["YearMonth"] = fact["OrderDate"].dt.strftime("%Y-%m")
    fact["MonthName"] = fact["OrderDate"].dt.strftime("%b")

    # 3. Create Consolidated Star-Schema Merge
    merged = fact.merge(dim_product, on="ProductKey", how="left")
    dim_cust_clean = dim_customer.drop(columns=["TerritoryKey"], errors="ignore")
    merged = merged.merge(dim_cust_clean, on="CustomerKey", how="left")
    merged = merged.merge(dim_territory, on="TerritoryKey", how="left")

    # 4. Save into SQLite for relational SQL demonstration
    conn = sqlite3.connect(SQLITE_DB)
    dim_product.to_sql("DimProduct", conn, if_exists="replace", index=False)
    dim_customer.to_sql("DimCustomer", conn, if_exists="replace", index=False)
    dim_territory.to_sql("DimTerritory", conn, if_exists="replace", index=False)
    dim_date.to_sql("DimDate", conn, if_exists="replace", index=False)
    fact.to_sql("FactSales", conn, if_exists="replace", index=False)
    conn.close()

    return merged


# Global cached dataframe for fast query processing
DF_SALES = init_database_and_load_data()


def filter_sales(df, request_args):
    """Apply category, territory, and year filters from URL query parameters."""
    filtered = df.copy()
    cat = request_args.get("category")
    if cat and cat.lower() != "all":
        filtered = filtered[filtered["Category"].str.lower() == cat.lower()]

    terr = request_args.get("territory")
    if terr and terr.lower() != "all":
        filtered = filtered[filtered["Region"].str.lower() == terr.lower()]

    yr = request_args.get("year")
    if yr and yr.lower() != "all":
        try:
            filtered = filtered[filtered["Year"] == int(yr)]
        except ValueError:
            pass

    return filtered


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Visual Analytics Flask API",
        "student": "Vedant Nimkar (26MML0045)",
        "records_loaded": len(DF_SALES),
        "data_sources": ["SalesData.xlsx", "SQLite (SalesAnalytics.db)", "CSV Star-Schema"]
    })


@app.route("/api/kpis", methods=["GET"])
def get_kpis():
    """Summary metrics: Revenue, Cost, Profit, Profit Margin %, Units, Orders, AOV."""
    df = filter_sales(DF_SALES, request.args)
    tot_sales = float(df["SalesAmount"].sum())
    tot_cost = float(df["TotalCost"].sum())
    tot_profit = tot_sales - tot_cost
    margin_pct = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0.0
    tot_units = int(df["OrderQuantity"].sum())
    orders = int(df["SalesOrderNumber"].nunique())
    aov = (tot_sales / orders) if orders > 0 else 0.0

    return jsonify({
        "total_revenue": round(tot_sales, 2),
        "total_cost": round(tot_cost, 2),
        "total_profit": round(tot_profit, 2),
        "profit_margin_pct": round(margin_pct, 2),
        "total_units_sold": tot_units,
        "total_orders": orders,
        "average_order_value": round(aov, 2),
        "active_customers": int(df["CustomerKey"].nunique())
    })


@app.route("/api/sales/monthly", methods=["GET"])
def get_monthly_trend():
    """Monthly aggregated time-series for Line Chart."""
    df = filter_sales(DF_SALES, request.args)
    monthly = df.groupby("YearMonth").agg(
        revenue=("SalesAmount", "sum"),
        cost=("TotalCost", "sum"),
        units=("OrderQuantity", "sum")
    ).reset_index().sort_values("YearMonth")

    monthly["profit"] = monthly["revenue"] - monthly["cost"]

    return jsonify({
        "months": monthly["YearMonth"].tolist(),
        "revenue": [round(x, 2) for x in monthly["revenue"].tolist()],
        "profit": [round(x, 2) for x in monthly["profit"].tolist()],
        "units": monthly["units"].tolist()
    })


@app.route("/api/sales/by-category", methods=["GET"])
def get_sales_by_category():
    """Category breakdown for Bar Chart."""
    df = filter_sales(DF_SALES, request.args)
    cat_grp = df.groupby("Category").agg(
        revenue=("SalesAmount", "sum"),
        profit=("SalesAmount", lambda s: s.sum() - df.loc[s.index, "TotalCost"].sum()),
        units=("OrderQuantity", "sum")
    ).reset_index().sort_values("revenue", ascending=False)

    total_rev = cat_grp["revenue"].sum()
    cat_grp["share_pct"] = (cat_grp["revenue"] / total_rev * 100) if total_rev > 0 else 0

    return jsonify({
        "categories": cat_grp["Category"].tolist(),
        "revenue": [round(x, 2) for x in cat_grp["revenue"].tolist()],
        "profit": [round(x, 2) for x in cat_grp["profit"].tolist()],
        "units": cat_grp["units"].tolist(),
        "share_pct": [round(x, 1) for x in cat_grp["share_pct"].tolist()]
    })


@app.route("/api/sales/by-territory", methods=["GET"])
def get_sales_by_territory():
    """Territory distribution for Donut / Pie Chart."""
    df = filter_sales(DF_SALES, request.args)
    terr_grp = df.groupby(["Region", "Country"]).agg(
        revenue=("SalesAmount", "sum")
    ).reset_index().sort_values("revenue", ascending=False)

    data = []
    for _, row in terr_grp.iterrows():
        data.append({
            "name": f"{row['Region']} ({row['Country']})",
            "value": round(float(row["revenue"]), 2)
        })

    return jsonify(data)


@app.route("/api/products/top", methods=["GET"])
def get_top_products():
    """Top N products ranking table and scatter chart data."""
    df = filter_sales(DF_SALES, request.args)
    limit = int(request.args.get("limit", 10))

    prod_grp = df.groupby(["ProductName", "Category", "Subcategory"]).agg(
        revenue=("SalesAmount", "sum"),
        cost=("TotalCost", "sum"),
        units=("OrderQuantity", "sum")
    ).reset_index()

    prod_grp["profit"] = prod_grp["revenue"] - prod_grp["cost"]
    prod_grp["margin_pct"] = (prod_grp["profit"] / prod_grp["revenue"] * 100).round(1)
    top_df = prod_grp.sort_values("revenue", ascending=False).head(limit)

    return jsonify([
        {
            "product_name": r["ProductName"],
            "category": r["Category"],
            "subcategory": r["Subcategory"],
            "revenue": round(r["revenue"], 2),
            "profit": round(r["profit"], 2),
            "units": int(r["units"]),
            "margin_pct": float(r["margin_pct"])
        }
        for _, r in top_df.iterrows()
    ])


@app.route("/api/products/drilldown", methods=["GET"])
def get_drilldown():
    """Drilldown into subcategories and products for a given category."""
    cat = request.args.get("category", "Bikes")
    df = DF_SALES[DF_SALES["Category"].str.lower() == cat.lower()]
    
    subcat_grp = df.groupby("Subcategory").agg(
        revenue=("SalesAmount", "sum"),
        units=("OrderQuantity", "sum")
    ).reset_index().sort_values("revenue", ascending=False)

    return jsonify({
        "category": cat,
        "subcategories": subcat_grp["Subcategory"].tolist(),
        "revenue": [round(x, 2) for x in subcat_grp["revenue"].tolist()],
        "units": subcat_grp["units"].tolist()
    })


@app.route("/api/filters/options", methods=["GET"])
def get_filter_options():
    """Returns available categories, territories, and fiscal years."""
    return jsonify({
        "categories": sorted(DF_SALES["Category"].dropna().unique().tolist()),
        "territories": sorted(DF_SALES["Region"].dropna().unique().tolist()),
        "years": sorted(DF_SALES["Year"].dropna().unique().tolist())
    })


if __name__ == "__main__":
    print(f"[*] Visual Analytics Backend running on http://127.0.0.1:5000")
    print(f"[*] Serving dataset: {len(DF_SALES)} verified rows")
    app.run(host="0.0.0.0", port=5000, debug=False)
