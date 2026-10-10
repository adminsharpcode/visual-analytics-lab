"""
QP1 Step 1 - build the Sales data source.

Produces a deliberately DIRTY fact table (so QP1 Step 2 cleansing has real
work to do) plus clean dimension tables, in three consumable forms:
  data/*.csv            -> folder source for Power BI
  data/SalesData.xlsx   -> single-workbook source
  sql/01_create_load.sql-> SQL Server DDL + inserts for the SQL Server step
"""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
SQL = os.path.join(BASE, "sql")
os.makedirs(DATA, exist_ok=True)
os.makedirs(SQL, exist_ok=True)

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------- DimDate
dates = pd.date_range("2023-01-01", "2025-12-31", freq="D")
dim_date = pd.DataFrame({
    "DateKey": dates.strftime("%Y%m%d").astype(int),
    "Date": dates,
    "Year": dates.year,
    "QuarterNo": dates.quarter,
    "Quarter": "Q" + dates.quarter.astype(str),
    "MonthNo": dates.month,
    "MonthName": dates.strftime("%B"),
    "MonthShort": dates.strftime("%b"),
    "YearMonth": dates.strftime("%Y-%m"),
    "WeekOfYear": dates.isocalendar().week.values,
    "DayOfMonth": dates.day,
    "DayName": dates.strftime("%A"),
    "IsWeekend": dates.dayofweek.isin([5, 6]),
})

# ---------------------------------------------------------------- DimProduct
catalogue = [
    # Category, Subcategory, Product, StandardCost, ListPrice
    ("Electronics", "Laptops", "UltraBook 14 Pro", 620, 1099),
    ("Electronics", "Laptops", "GamingBook X17", 980, 1699),
    ("Electronics", "Laptops", "EduBook 13", 310, 549),
    ("Electronics", "Mobiles", "Zenith S24", 430, 799),
    ("Electronics", "Mobiles", "Zenith A12", 145, 279),
    ("Electronics", "Audio", "AeroPods Pro", 78, 189),
    ("Electronics", "Audio", "StudioCan 700", 122, 299),
    ("Electronics", "Monitors", "ClearView 27 4K", 210, 429),
    ("Electronics", "Monitors", "ClearView 24 FHD", 96, 189),
    ("Accessories", "Peripherals", "TactKey Mechanical", 34, 89),
    ("Accessories", "Peripherals", "GlideMouse Wireless", 12, 39),
    ("Accessories", "Peripherals", "DockHub 11-in-1", 41, 99),
    ("Accessories", "Storage", "RapidSSD 1TB", 58, 139),
    ("Accessories", "Storage", "VaultHDD 4TB", 66, 149),
    ("Accessories", "Power", "VoltBank 20K", 19, 59),
    ("Furniture", "Seating", "ErgoChair Mesh", 128, 329),
    ("Furniture", "Seating", "TaskStool Basic", 44, 119),
    ("Furniture", "Desks", "RiseDesk Electric", 265, 599),
    ("Furniture", "Desks", "StudyDesk Compact", 88, 199),
    ("Software", "Productivity", "OfficeSuite Annual", 30, 119),
    ("Software", "Security", "GuardAV Annual", 14, 59),
    ("Software", "Creative", "PixelStudio Annual", 96, 239),
]
dim_product = pd.DataFrame(catalogue, columns=[
    "Category", "Subcategory", "ProductName", "StandardCost", "ListPrice"])
dim_product.insert(0, "ProductKey", range(1, len(dim_product) + 1))
dim_product["SKU"] = [
    f"{c[:3].upper()}-{s[:3].upper()}-{k:03d}"
    for c, s, k in zip(dim_product.Category, dim_product.Subcategory,
                       dim_product.ProductKey)]

# ---------------------------------------------------------------- DimTerritory
territory = pd.DataFrame([
    (1, "North", "India", "APAC"),
    (2, "South", "India", "APAC"),
    (3, "West", "India", "APAC"),
    (4, "East", "India", "APAC"),
    (5, "Central", "India", "APAC"),
], columns=["TerritoryKey", "Region", "Country", "Group"])

# ---------------------------------------------------------------- DimCustomer
first = ["Aarav", "Vivaan", "Diya", "Ananya", "Kabir", "Ishaan", "Meera",
         "Riya", "Arjun", "Sara", "Rohan", "Nisha", "Dev", "Tara", "Yash",
         "Kavya", "Aditya", "Priya", "Manav", "Sneha"]
last = ["Sharma", "Patil", "Nimkar", "Bobde", "Panda", "Bose", "Mahajan",
        "Iyer", "Reddy", "Khan", "Joshi", "Nair", "Gupta", "Desai"]
n_cust = 220
dim_customer = pd.DataFrame({
    "CustomerKey": range(1, n_cust + 1),
    "FirstName": rng.choice(first, n_cust),
    "LastName": rng.choice(last, n_cust),
    "Segment": rng.choice(["Consumer", "Corporate", "Education"], n_cust,
                          p=[0.55, 0.30, 0.15]),
    "TerritoryKey": rng.choice(territory.TerritoryKey, n_cust),
})
dim_customer["CustomerName"] = (dim_customer.FirstName + " "
                                + dim_customer.LastName)

# ---------------------------------------------------------------- FactSales
N = 6000
order_dates = rng.choice(dates, N)

# skewed popularity so "top sold product" has a clear, single winner
weights = np.linspace(3.0, 1.0, len(dim_product))
weights[9] = 6.0    # GlideMouse-class cheap peripheral sells most units
weights[10] = 7.5
weights = weights / weights.sum()
prod = rng.choice(dim_product.ProductKey, N, p=weights)

fact = pd.DataFrame({
    "SalesOrderNumber": [f"SO{50000 + i}" for i in range(N)],
    "OrderDate": pd.to_datetime(order_dates),
    "ProductKey": prod,
    "CustomerKey": rng.choice(dim_customer.CustomerKey, N),
    "OrderQuantity": rng.integers(1, 9, N),
})
fact = fact.merge(dim_product[["ProductKey", "ListPrice", "StandardCost"]],
                  on="ProductKey", how="left")

# growth trend + seasonality so YoY analysis is meaningful
yr = fact.OrderDate.dt.year
month = fact.OrderDate.dt.month
growth = yr.map({2023: 1.00, 2024: 1.18, 2025: 1.31}).astype(float)
season = 1 + 0.22 * np.sin((month - 3) / 12 * 2 * np.pi)
fact["UnitPrice"] = (fact.ListPrice * growth * season
                     * rng.normal(1.0, 0.04, N)).round(2)
fact["DiscountPct"] = np.where(rng.random(N) < 0.30,
                               rng.choice([0.05, 0.10, 0.15], N), 0.0)
fact["TerritoryKey"] = fact.CustomerKey.map(
    dim_customer.set_index("CustomerKey").TerritoryKey)
fact["SalesAmount"] = (fact.UnitPrice * fact.OrderQuantity
                       * (1 - fact.DiscountPct)).round(2)
fact["TotalCost"] = (fact.StandardCost * fact.OrderQuantity).round(2)
fact = fact.drop(columns=["ListPrice", "StandardCost"])

# ---------------------------------------------------------------- dirty it up
dirty = fact.copy()

# 1) duplicate rows (12 exact duplicates)
dup_idx = rng.choice(dirty.index, 12, replace=False)
dirty = pd.concat([dirty, dirty.loc[dup_idx]], ignore_index=True)

# 2) blank / null OrderQuantity and SalesAmount
for col, k in [("OrderQuantity", 40), ("SalesAmount", 35)]:
    idx = rng.choice(dirty.index, k, replace=False)
    dirty.loc[idx, col] = np.nan

# 3) messy text in a status column with inconsistent casing + whitespace
raw_status = rng.choice(["Shipped", " shipped", "SHIPPED  ", "Pending",
                         "pending ", "Cancelled", " cancelled"], len(dirty),
                        p=[0.42, 0.10, 0.08, 0.16, 0.08, 0.10, 0.06])
dirty["OrderStatus"] = raw_status

# 4) currency stored as text with symbols on some rows
dirty["UnitPriceText"] = dirty.UnitPrice.map(lambda v: f"Rs. {v:,.2f}")

# 5) dates as text in mixed formats
def messy_date(d, i):
    if i % 7 == 0:
        return d.strftime("%d-%m-%Y")
    if i % 11 == 0:
        return d.strftime("%d/%m/%Y")
    return d.strftime("%Y-%m-%d")


dirty["OrderDateText"] = [messy_date(d, i)
                          for i, d in enumerate(dirty.OrderDate)]

# 6) a fully blank throwaway column Power BI will import
dirty["Notes"] = ""

# 7) negative quantity outliers (data-entry errors)
neg_idx = rng.choice(dirty.index, 8, replace=False)
dirty.loc[neg_idx, "OrderQuantity"] = -dirty.loc[neg_idx, "OrderQuantity"]

dirty_out = dirty[[
    "SalesOrderNumber", "OrderDateText", "ProductKey", "CustomerKey",
    "TerritoryKey", "OrderQuantity", "UnitPriceText", "DiscountPct",
    "SalesAmount", "TotalCost", "OrderStatus", "Notes"]]

# ---------------------------------------------------------------- write CSV
dim_date.to_csv(os.path.join(DATA, "DimDate.csv"), index=False)
dim_product.to_csv(os.path.join(DATA, "DimProduct.csv"), index=False)
dim_customer.drop(columns=["FirstName", "LastName"]).to_csv(
    os.path.join(DATA, "DimCustomer.csv"), index=False)
territory.to_csv(os.path.join(DATA, "DimTerritory.csv"), index=False)
dirty_out.to_csv(os.path.join(DATA, "FactSales_RAW.csv"), index=False)
fact.to_csv(os.path.join(DATA, "FactSales_CLEAN_reference.csv"), index=False)

# ---------------------------------------------------------------- write XLSX
xlsx = os.path.join(DATA, "SalesData.xlsx")
with pd.ExcelWriter(xlsx, engine="openpyxl") as xw:
    dirty_out.to_excel(xw, sheet_name="FactSales_RAW", index=False)
    dim_product.to_excel(xw, sheet_name="DimProduct", index=False)
    dim_customer.drop(columns=["FirstName", "LastName"]).to_excel(
        xw, sheet_name="DimCustomer", index=False)
    territory.to_excel(xw, sheet_name="DimTerritory", index=False)
    dim_date.to_excel(xw, sheet_name="DimDate", index=False)

# ---------------------------------------------------------------- SQL script
def sql_lit(v):
    if pd.isna(v):
        return "NULL"
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    if isinstance(v, (bool, np.bool_)):
        return "1" if v else "0"
    return str(v)


def insert_block(df, table, chunk=200):
    cols = ", ".join(f"[{c}]" for c in df.columns)
    out = []
    for start in range(0, len(df), chunk):
        part = df.iloc[start:start + chunk]
        vals = ",\n".join(
            "(" + ", ".join(sql_lit(v) for v in row) + ")"
            for row in part.itertuples(index=False, name=None))
        out.append(f"INSERT INTO {table} ({cols}) VALUES\n{vals};\n")
    return "\n".join(out)


lines = [
    "/* =========================================================",
    "   Visual Analytics Lab - QP1 Step 1",
    "   Creates the VisualAnalyticsLab database and Sales tables",
    "   Run in SQL Server Management Studio or: sqlcmd -S . -i this.sql",
    "   ========================================================= */",
    "IF DB_ID('VisualAnalyticsLab') IS NULL",
    "    CREATE DATABASE VisualAnalyticsLab;",
    "GO",
    "USE VisualAnalyticsLab;",
    "GO",
    "IF OBJECT_ID('dbo.FactSales','U')   IS NOT NULL DROP TABLE dbo.FactSales;",
    "IF OBJECT_ID('dbo.DimProduct','U')  IS NOT NULL DROP TABLE dbo.DimProduct;",
    "IF OBJECT_ID('dbo.DimCustomer','U') IS NOT NULL DROP TABLE dbo.DimCustomer;",
    "IF OBJECT_ID('dbo.DimTerritory','U')IS NOT NULL DROP TABLE dbo.DimTerritory;",
    "IF OBJECT_ID('dbo.DimDate','U')     IS NOT NULL DROP TABLE dbo.DimDate;",
    "GO",
    "",
    "CREATE TABLE dbo.DimTerritory (",
    "    TerritoryKey INT PRIMARY KEY, Region NVARCHAR(50),",
    "    Country NVARCHAR(50), [Group] NVARCHAR(50));",
    "",
    "CREATE TABLE dbo.DimProduct (",
    "    ProductKey INT PRIMARY KEY, Category NVARCHAR(50),",
    "    Subcategory NVARCHAR(50), ProductName NVARCHAR(100),",
    "    StandardCost DECIMAL(10,2), ListPrice DECIMAL(10,2),",
    "    SKU NVARCHAR(30));",
    "",
    "CREATE TABLE dbo.DimCustomer (",
    "    CustomerKey INT PRIMARY KEY, Segment NVARCHAR(30),",
    "    TerritoryKey INT, CustomerName NVARCHAR(100));",
    "",
    "CREATE TABLE dbo.DimDate (",
    "    DateKey INT PRIMARY KEY, [Date] DATE, [Year] INT, QuarterNo INT,",
    "    [Quarter] NVARCHAR(4), MonthNo INT, MonthName NVARCHAR(20),",
    "    MonthShort NVARCHAR(5), YearMonth NVARCHAR(10), WeekOfYear INT,",
    "    DayOfMonth INT, DayName NVARCHAR(15), IsWeekend BIT);",
    "",
    "/* Fact table is intentionally loaded RAW (text dates, text currency,",
    "   nulls, duplicates) so that Power Query cleansing has real work. */",
    "CREATE TABLE dbo.FactSales (",
    "    SalesOrderNumber NVARCHAR(20), OrderDateText NVARCHAR(20),",
    "    ProductKey INT, CustomerKey INT, TerritoryKey INT,",
    "    OrderQuantity INT NULL, UnitPriceText NVARCHAR(30),",
    "    DiscountPct DECIMAL(5,2), SalesAmount DECIMAL(12,2) NULL,",
    "    TotalCost DECIMAL(12,2), OrderStatus NVARCHAR(30),",
    "    Notes NVARCHAR(50) NULL);",
    "GO",
    "",
]
lines.append(insert_block(territory, "dbo.DimTerritory"))
lines.append(insert_block(dim_product, "dbo.DimProduct"))
lines.append(insert_block(
    dim_customer.drop(columns=["FirstName", "LastName"]), "dbo.DimCustomer"))
d2 = dim_date.copy()
d2["Date"] = d2["Date"].dt.strftime("%Y-%m-%d")
lines.append(insert_block(d2, "dbo.DimDate"))
f2 = dirty_out.copy()
f2["OrderQuantity"] = f2["OrderQuantity"].astype("object").where(
    f2["OrderQuantity"].notna(), None)
lines.append(insert_block(f2, "dbo.FactSales"))
lines.append("GO\nSELECT COUNT(*) AS FactRows FROM dbo.FactSales;\n")

with open(os.path.join(SQL, "01_create_load.sql"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ---------------------------------------------------------------- report
print("Data source created")
print(f"  DimDate       {len(dim_date):>6} rows")
print(f"  DimProduct    {len(dim_product):>6} rows")
print(f"  DimCustomer   {len(dim_customer):>6} rows")
print(f"  DimTerritory  {len(territory):>6} rows")
print(f"  FactSales RAW {len(dirty_out):>6} rows  "
      f"(incl. 12 duplicates, {int(dirty_out.OrderQuantity.isna().sum())} "
      f"null qty, {int(dirty_out.SalesAmount.isna().sum())} null amount, "
      f"8 negative qty)")
print(f"  clean reference {len(fact):>4} rows")
print("  ->", DATA)
print("  ->", os.path.join(SQL, "01_create_load.sql"))
