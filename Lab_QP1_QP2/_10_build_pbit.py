"""
Generates a Power BI Template (.pbit) containing the COMPLETE model for
QP1 and QP2:

  * 5 tables with their Power Query (M) partitions
  * all cleansing logic already applied
  * 5 relationships (one deliberately inactive)
  * 4 hierarchies
  * calculated columns
  * ~35 DAX measures (core, ranking, CALCULATE, Time Intelligence)
  * 2 calculated tables
  * DimDate marked as a date table
  * 2 named, empty report pages ready for visuals

Open the .pbit in Power BI Desktop -> it loads the data and the whole model
appears. Steps 1 to 5 of the lab are then already in place.

A .pbit is a ZIP whose text parts must be UTF-16 LE encoded.
"""
import json
import os
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
MDIR = os.path.join(BASE, "code", "ready_to_paste")
OUT = os.path.join(BASE, "VisualAnalytics_Sales_26MML0045.pbit")

MODEL_NAME = "VisualAnalyticsLab"


def m_expression(name):
    """Read a ready-to-paste M query and return it as a list of lines."""
    p = os.path.join(MDIR, f"{name}.m")
    with open(p, encoding="utf-8") as f:
        return f.read().rstrip("\n").split("\n")


CUR = "\\$#,0.00;(\\$#,0.00);\\$#,0.00"
NUM = "#,0"
DEC = "#,0.00"
PCT = "0.00%"


def col(name, dtype, source=None, fmt=None, summarize="none", hidden=False,
        sort_by=None, is_key=False):
    c = {"name": name, "dataType": dtype,
         "sourceColumn": source or name, "summarizeBy": summarize}
    if fmt:
        c["formatString"] = fmt
    if hidden:
        c["isHidden"] = True
    if sort_by:
        c["sortByColumn"] = sort_by
    if is_key:
        c["isKey"] = True
    return c


def calc_col(name, expr, fmt=None, summarize="none"):
    c = {"name": name, "type": "calculated", "isDataTypeInferred": True,
         "expression": expr, "summarizeBy": summarize}
    if fmt:
        c["formatString"] = fmt
    return c


def measure(name, expr, fmt=None, folder=None, desc=None):
    m = {"name": name, "expression": expr}
    if fmt:
        m["formatString"] = fmt
    if folder:
        m["displayFolder"] = folder
    if desc:
        m["description"] = desc
    return m


def hierarchy(name, levels):
    return {"name": name,
            "levels": [{"name": lv, "ordinal": i, "column": lv}
                       for i, lv in enumerate(levels)]}


# ============================================================ FactSales
fact_measures = [
    # ---- core -----------------------------------------------------------
    measure("Total Sales", "SUM ( FactSales[SalesAmount] )", CUR, "01 Sales"),
    measure("Total Quantity", "SUM ( FactSales[OrderQuantity] )", NUM,
            "01 Sales"),
    measure("Total Cost", "SUM ( FactSales[TotalCost] )", CUR, "02 Profit"),
    measure("Total Profit", "[Total Sales] - [Total Cost]", CUR, "02 Profit"),
    measure("Profit Margin %", "DIVIDE ( [Total Profit], [Total Sales] )",
            PCT, "02 Profit"),
    measure("Order Count", "DISTINCTCOUNT ( FactSales[SalesOrderNumber] )",
            NUM, "01 Sales"),
    measure("Average Order Value", "DIVIDE ( [Total Sales], [Order Count] )",
            CUR, "01 Sales"),
    measure("Average Line Sales", "AVERAGE ( FactSales[SalesAmount] )", CUR,
            "01 Sales"),
    measure("Average Selling Price",
            "DIVIDE ( [Total Sales], [Total Quantity] )", CUR, "01 Sales"),
    measure("Customer Count", "DISTINCTCOUNT ( FactSales[CustomerKey] )", NUM,
            "01 Sales"),
    measure("Product Count", "DISTINCTCOUNT ( FactSales[ProductKey] )", NUM,
            "01 Sales"),

    # ---- Step 4 : top sold product --------------------------------------
    measure("Top Product by Units",
            "VAR TopProduct =\n"
            "    TOPN ( 1, ALL ( DimProduct[ProductName] ),\n"
            "           CALCULATE ( [Total Quantity] ), DESC )\n"
            "RETURN\n"
            "    CONCATENATEX ( TopProduct, DimProduct[ProductName], \", \" )",
            None, "03 Ranking"),
    measure("Top Product Units",
            "MAXX ( ALL ( DimProduct[ProductName] ),\n"
            "       CALCULATE ( [Total Quantity] ) )", NUM, "03 Ranking"),
    measure("Top Product by Revenue",
            "VAR TopProduct =\n"
            "    TOPN ( 1, ALL ( DimProduct[ProductName] ),\n"
            "           CALCULATE ( [Total Sales] ), DESC )\n"
            "RETURN\n"
            "    CONCATENATEX ( TopProduct, DimProduct[ProductName], \", \" )",
            None, "03 Ranking"),
    measure("Product Rank by Units",
            "RANKX ( ALL ( DimProduct[ProductName] ), [Total Quantity], ,\n"
            "        DESC, DENSE )", NUM, "03 Ranking"),

    # ---- Step 4 : category averages -------------------------------------
    measure("Avg Sales per Line", "AVERAGE ( FactSales[SalesAmount] )", CUR,
            "04 Category"),
    measure("Avg Sales per Order",
            "DIVIDE ( [Total Sales],\n"
            "         DISTINCTCOUNT ( FactSales[SalesOrderNumber] ) )", CUR,
            "04 Category"),
    measure("Avg Sales per Category",
            "AVERAGEX ( VALUES ( DimProduct[Category] ), [Total Sales] )",
            CUR, "04 Category"),
    measure("Category Share %",
            "DIVIDE ( [Total Sales],\n"
            "         CALCULATE ( [Total Sales], ALL ( DimProduct ) ) )",
            PCT, "04 Category"),

    # ---- Step 5 : CALCULATE ---------------------------------------------
    measure("Electronics Sales",
            "CALCULATE ( [Total Sales], DimProduct[Category] = "
            "\"Electronics\" )", CUR, "05 CALCULATE"),
    measure("Shipped Sales",
            "CALCULATE ( [Total Sales], FactSales[OrderStatus] = "
            "\"Shipped\" )", CUR, "05 CALCULATE"),
    measure("Discounted Sales",
            "CALCULATE ( [Total Sales], FactSales[DiscountPct] > 0 )", CUR,
            "05 CALCULATE"),
    measure("Sales All Products",
            "CALCULATE ( [Total Sales], ALL ( DimProduct ) )", CUR,
            "05 CALCULATE"),
    measure("Pct of Total Sales",
            "DIVIDE ( [Total Sales],\n"
            "         CALCULATE ( [Total Sales], ALL ( DimProduct ),\n"
            "                                    ALL ( DimTerritory ) ) )",
            PCT, "05 CALCULATE"),
    measure("Category Revenue",
            "CALCULATE ( [Total Sales],\n"
            "            ALLEXCEPT ( DimProduct, DimProduct[Category] ) )",
            CUR, "05 CALCULATE"),
    measure("Pct of Category Sales",
            "DIVIDE ( [Total Sales],\n"
            "         CALCULATE ( [Total Sales],\n"
            "             ALLEXCEPT ( DimProduct, DimProduct[Category] ) ) )",
            PCT, "05 CALCULATE"),
    measure("Pct of Selected Sales",
            "DIVIDE ( [Total Sales],\n"
            "         CALCULATE ( [Total Sales],\n"
            "             ALLSELECTED ( DimProduct[Category] ) ) )", PCT,
            "05 CALCULATE"),
    measure("Sales 2025 Override",
            "CALCULATE ( [Total Sales], DimDate[Year] = 2025 )", CUR,
            "05 CALCULATE"),
    measure("Sales 2025 KeepFilters",
            "CALCULATE ( [Total Sales],\n"
            "            KEEPFILTERS ( DimDate[Year] = 2025 ) )", CUR,
            "05 CALCULATE"),
    measure("Laptops or Mobiles Sales",
            "CALCULATE ( [Total Sales],\n"
            "    FILTER ( ALL ( DimProduct[Subcategory] ),\n"
            "             DimProduct[Subcategory] = \"Laptops\"\n"
            "          || DimProduct[Subcategory] = \"Mobiles\" ) )", CUR,
            "05 CALCULATE"),
    measure("Sales by Customer Territory",
            "CALCULATE ( [Total Sales],\n"
            "    USERELATIONSHIP ( DimCustomer[TerritoryKey],\n"
            "                      DimTerritory[TerritoryKey] ) )", CUR,
            "05 CALCULATE"),

    # ---- Step 5 : Time Intelligence -------------------------------------
    measure("Sales YTD", "TOTALYTD ( [Total Sales], DimDate[Date] )", CUR,
            "06 Time"),
    measure("Sales QTD", "TOTALQTD ( [Total Sales], DimDate[Date] )", CUR,
            "06 Time"),
    measure("Sales MTD", "TOTALMTD ( [Total Sales], DimDate[Date] )", CUR,
            "06 Time"),
    measure("Sales FYTD",
            "TOTALYTD ( [Total Sales], DimDate[Date], \"31/03\" )", CUR,
            "06 Time"),
    measure("Sales PY",
            "CALCULATE ( [Total Sales],\n"
            "            SAMEPERIODLASTYEAR ( DimDate[Date] ) )", CUR,
            "06 Time"),
    measure("Sales PM",
            "CALCULATE ( [Total Sales],\n"
            "            DATEADD ( DimDate[Date], -1, MONTH ) )", CUR,
            "06 Time"),
    measure("Sales PQ",
            "CALCULATE ( [Total Sales],\n"
            "            DATEADD ( DimDate[Date], -1, QUARTER ) )", CUR,
            "06 Time"),
    measure("Sales PY YTD",
            "CALCULATE ( [Sales YTD],\n"
            "            SAMEPERIODLASTYEAR ( DimDate[Date] ) )", CUR,
            "06 Time"),
    measure("YoY Growth",
            "VAR Cur = [Total Sales]\n"
            "VAR Prev = [Sales PY]\n"
            "RETURN\n"
            "    IF ( NOT ISBLANK ( Prev ), Cur - Prev )", CUR, "06 Time"),
    measure("YoY Growth %",
            "DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )", PCT,
            "06 Time"),
    measure("MoM Growth %",
            "DIVIDE ( [Total Sales] - [Sales PM], [Sales PM] )", PCT,
            "06 Time"),
    measure("YoY Trend",
            "VAR G = [YoY Growth %]\n"
            "RETURN\n"
            "    SWITCH ( TRUE (),\n"
            "        ISBLANK ( G ), \"No prior year\",\n"
            "        G > 0.10,      \"Strong growth\",\n"
            "        G > 0,         \"Growing\",\n"
            "        G > -0.10,     \"Slight decline\",\n"
            "        \"Sharp decline\" )", None, "06 Time"),
    measure("Sales Rolling 3M",
            "CALCULATE ( [Total Sales],\n"
            "    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ),\n"
            "                    -3, MONTH ) )", CUR, "06 Time"),
    measure("Sales Rolling 12M",
            "CALCULATE ( [Total Sales],\n"
            "    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ),\n"
            "                    -12, MONTH ) )", CUR, "06 Time"),
    measure("Sales Cumulative",
            "CALCULATE ( [Total Sales],\n"
            "    FILTER ( ALLSELECTED ( DimDate[Date] ),\n"
            "             DimDate[Date] <= MAX ( DimDate[Date] ) ) )", CUR,
            "06 Time"),
    measure("Sales 3M Moving Avg",
            "AVERAGEX (\n"
            "    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ),\n"
            "                    -3, MONTH ),\n"
            "    CALCULATE ( [Total Sales] ) )", CUR, "06 Time"),
    measure("Category Revenue PY",
            "CALCULATE ( [Total Sales],\n"
            "    ALLEXCEPT ( DimProduct, DimProduct[Category] ),\n"
            "    SAMEPERIODLASTYEAR ( DimDate[Date] ) )", CUR, "06 Time"),
    measure("Electronics YoY %",
            "VAR Cur =\n"
            "    CALCULATE ( [Total Sales],\n"
            "                DimProduct[Category] = \"Electronics\" )\n"
            "VAR Prev =\n"
            "    CALCULATE ( [Total Sales],\n"
            "                DimProduct[Category] = \"Electronics\",\n"
            "                SAMEPERIODLASTYEAR ( DimDate[Date] ) )\n"
            "RETURN\n"
            "    DIVIDE ( Cur - Prev, Prev )", PCT, "06 Time"),
    measure("Best Month Sales",
            "MAXX ( VALUES ( DimDate[YearMonth] ),\n"
            "       CALCULATE ( [Total Sales] ) )", CUR, "06 Time"),
    measure("Best Month Name",
            "VAR T = TOPN ( 1, VALUES ( DimDate[YearMonth] ),\n"
            "               CALCULATE ( [Total Sales] ), DESC )\n"
            "RETURN\n"
            "    CONCATENATEX ( T, DimDate[YearMonth], \", \" )", None,
            "06 Time"),
]

fact = {
    "name": "FactSales",
    "columns": [
        col("SalesOrderNumber", "string"),
        col("OrderDate", "dateTime", fmt="dd mmm yyyy"),
        col("DateKey", "int64", hidden=True),
        col("ProductKey", "int64", hidden=True),
        col("CustomerKey", "int64", hidden=True),
        col("TerritoryKey", "int64", hidden=True),
        col("OrderQuantity", "int64", fmt=NUM, summarize="sum"),
        col("UnitPrice", "double", fmt=CUR),
        col("DiscountPct", "double", fmt=PCT, summarize="average"),
        col("SalesAmount", "double", fmt=CUR, summarize="sum"),
        col("TotalCost", "double", fmt=CUR, summarize="sum"),
        col("Profit", "double", fmt=CUR, summarize="sum"),
        col("OrderStatus", "string"),
        calc_col("Net Unit Price",
                 "DIVIDE ( FactSales[SalesAmount], "
                 "FactSales[OrderQuantity] )", CUR),
        calc_col("Line Margin %",
                 "DIVIDE ( FactSales[SalesAmount] - FactSales[TotalCost],\n"
                 "         FactSales[SalesAmount] )", PCT),
        calc_col("Order Size Band",
                 "SWITCH ( TRUE (),\n"
                 "    FactSales[OrderQuantity] <= 2, \"1-2 units\",\n"
                 "    FactSales[OrderQuantity] <= 4, \"3-4 units\",\n"
                 "    FactSales[OrderQuantity] <= 6, \"5-6 units\",\n"
                 "    \"7+ units\" )"),
        calc_col("Product Category", "RELATED ( DimProduct[Category] )"),
    ],
    "partitions": [{
        "name": "FactSales",
        "mode": "import",
        "source": {"type": "m", "expression": m_expression("FactSales")},
    }],
    "measures": fact_measures,
}

# ============================================================ DimProduct
dim_product = {
    "name": "DimProduct",
    "columns": [
        col("ProductKey", "int64", hidden=True),
        col("Category", "string"),
        col("Subcategory", "string"),
        col("ProductName", "string"),
        col("StandardCost", "double", fmt=CUR),
        col("ListPrice", "double", fmt=CUR),
        col("SKU", "string"),
        col("UnitMargin", "double", fmt=CUR),
        calc_col("Price Tier",
                 "SWITCH ( TRUE (),\n"
                 "    DimProduct[ListPrice] < 100, \"Budget\",\n"
                 "    DimProduct[ListPrice] < 500, \"Mid-range\",\n"
                 "    \"Premium\" )"),
    ],
    "partitions": [{
        "name": "DimProduct", "mode": "import",
        "source": {"type": "m", "expression": m_expression("DimProduct")},
    }],
    "hierarchies": [hierarchy("Product Hierarchy",
                              ["Category", "Subcategory", "ProductName"])],
}

# ============================================================ DimCustomer
dim_customer = {
    "name": "DimCustomer",
    "columns": [
        col("CustomerKey", "int64", hidden=True),
        col("Segment", "string"),
        col("TerritoryKey", "int64", hidden=True),
        col("CustomerName", "string"),
    ],
    "partitions": [{
        "name": "DimCustomer", "mode": "import",
        "source": {"type": "m", "expression": m_expression("DimCustomer")},
    }],
    "hierarchies": [hierarchy("Customer Hierarchy",
                              ["Segment", "CustomerName"])],
}

# ============================================================ DimTerritory
dim_territory = {
    "name": "DimTerritory",
    "columns": [
        col("TerritoryKey", "int64", hidden=True),
        col("Region", "string"),
        col("Country", "string"),
        col("Group", "string"),
    ],
    "partitions": [{
        "name": "DimTerritory", "mode": "import",
        "source": {"type": "m", "expression": m_expression("DimTerritory")},
    }],
    "hierarchies": [hierarchy("Geography Hierarchy",
                              ["Group", "Country", "Region"])],
}

# ============================================================ DimDate
dim_date = {
    "name": "DimDate",
    "dataCategory": "Time",
    "columns": [
        col("DateKey", "int64", hidden=True),
        col("Date", "dateTime", fmt="dd mmm yyyy", is_key=True),
        col("Year", "int64"),
        col("QuarterNo", "int64", hidden=True),
        col("Quarter", "string", sort_by="QuarterNo"),
        col("MonthNo", "int64", hidden=True),
        col("MonthName", "string", sort_by="MonthNo"),
        col("MonthShort", "string", sort_by="MonthNo"),
        col("YearMonth", "string"),
        col("WeekOfYear", "int64"),
        col("DayOfMonth", "int64"),
        col("DayName", "string"),
        col("IsWeekend", "boolean"),
        calc_col("Financial Year",
                 "\"FY \" & IF ( DimDate[MonthNo] >= 4, DimDate[Year],\n"
                 "                DimDate[Year] - 1 )\n"
                 "       & \"-\" & RIGHT ( IF ( DimDate[MonthNo] >= 4,\n"
                 "                DimDate[Year] + 1, DimDate[Year] ), 2 )"),
    ],
    "partitions": [{
        "name": "DimDate", "mode": "import",
        "source": {"type": "m", "expression": m_expression("DimDate")},
    }],
    "hierarchies": [hierarchy("Date Hierarchy",
                              ["Year", "Quarter", "MonthName",
                               "DayOfMonth"])],
}

# ============================================================ calc tables
cat_summary = {
    "name": "Product Category Summary",
    "columns": [
        {"name": "Category", "dataType": "string",
         "sourceColumn": "[Category]", "type": "calculatedTableColumn",
         "isNameInferred": True, "summarizeBy": "none"},
        {"name": "Total Sales", "dataType": "double",
         "sourceColumn": "[Total Sales]", "type": "calculatedTableColumn",
         "isNameInferred": True, "formatString": CUR,
         "summarizeBy": "sum"},
        {"name": "Total Quantity", "dataType": "int64",
         "sourceColumn": "[Total Quantity]", "type": "calculatedTableColumn",
         "isNameInferred": True, "formatString": NUM, "summarizeBy": "sum"},
        {"name": "Order Count", "dataType": "int64",
         "sourceColumn": "[Order Count]", "type": "calculatedTableColumn",
         "isNameInferred": True, "formatString": NUM, "summarizeBy": "sum"},
        {"name": "Avg Sales per Order", "dataType": "double",
         "sourceColumn": "[Avg Sales per Order]",
         "type": "calculatedTableColumn", "isNameInferred": True,
         "formatString": CUR, "summarizeBy": "none"},
    ],
    "partitions": [{
        "name": "Product Category Summary", "mode": "import",
        "source": {"type": "calculated",
                   "expression":
                       "SUMMARIZE (\n"
                       "    FactSales,\n"
                       "    DimProduct[Category],\n"
                       "    \"Total Sales\",         [Total Sales],\n"
                       "    \"Total Quantity\",      [Total Quantity],\n"
                       "    \"Order Count\",         [Order Count],\n"
                       "    \"Avg Sales per Order\", [Avg Sales per Order]\n"
                       ")"},
    }],
}

top5 = {
    "name": "Top 5 Products",
    "columns": [
        {"name": "ProductName", "dataType": "string",
         "sourceColumn": "[ProductName]", "type": "calculatedTableColumn",
         "isNameInferred": True, "summarizeBy": "none"},
        {"name": "Category", "dataType": "string",
         "sourceColumn": "[Category]", "type": "calculatedTableColumn",
         "isNameInferred": True, "summarizeBy": "none"},
        {"name": "Units Sold", "dataType": "int64",
         "sourceColumn": "[Units Sold]", "type": "calculatedTableColumn",
         "isNameInferred": True, "formatString": NUM, "summarizeBy": "sum"},
        {"name": "Revenue", "dataType": "double",
         "sourceColumn": "[Revenue]", "type": "calculatedTableColumn",
         "isNameInferred": True, "formatString": CUR, "summarizeBy": "sum"},
    ],
    "partitions": [{
        "name": "Top 5 Products", "mode": "import",
        "source": {"type": "calculated",
                   "expression":
                       "TOPN (\n"
                       "    5,\n"
                       "    SUMMARIZE (\n"
                       "        FactSales,\n"
                       "        DimProduct[ProductName],\n"
                       "        DimProduct[Category],\n"
                       "        \"Units Sold\", [Total Quantity],\n"
                       "        \"Revenue\",    [Total Sales]\n"
                       "    ),\n"
                       "    [Units Sold], DESC\n"
                       ")"},
    }],
}

# ============================================================ relationships
rels = [
    {"name": "rel_Date_Fact", "fromTable": "FactSales",
     "fromColumn": "DateKey", "toTable": "DimDate", "toColumn": "DateKey"},
    {"name": "rel_Product_Fact", "fromTable": "FactSales",
     "fromColumn": "ProductKey", "toTable": "DimProduct",
     "toColumn": "ProductKey"},
    {"name": "rel_Customer_Fact", "fromTable": "FactSales",
     "fromColumn": "CustomerKey", "toTable": "DimCustomer",
     "toColumn": "CustomerKey"},
    {"name": "rel_Territory_Fact", "fromTable": "FactSales",
     "fromColumn": "TerritoryKey", "toTable": "DimTerritory",
     "toColumn": "TerritoryKey"},
    # inactive: avoids the ambiguous second path to DimTerritory
    {"name": "rel_Territory_Customer", "fromTable": "DimCustomer",
     "fromColumn": "TerritoryKey", "toTable": "DimTerritory",
     "toColumn": "TerritoryKey", "isActive": False},
]

model = {
    "name": MODEL_NAME,
    "compatibilityLevel": 1550,
    "model": {
        "culture": "en-US",
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True,
        },
        "tables": [fact, dim_product, dim_customer, dim_territory, dim_date,
                   cat_summary, top5],
        "relationships": rels,
        "annotations": [
            {"name": "PBI_QueryOrder",
             "value": json.dumps(["FactSales", "DimProduct", "DimCustomer",
                                  "DimTerritory", "DimDate"])},
        ],
    },
}

# ============================================================ report layout
def page(name, ordinal):
    return {
        "name": f"page{ordinal}",
        "displayName": name,
        "displayOption": 1,
        "width": 1280,
        "height": 720,
        "ordinal": ordinal,
        "visualContainers": [],
        "config": json.dumps({
            "layouts": [{"id": 0, "position": {
                "x": 0, "y": 0, "z": 0, "width": 1280, "height": 720}}],
        }),
        "filters": "[]",
    }


layout = {
    "id": 0,
    "resourcePackages": [],
    "sections": [page("1 Sales Overview", 0),
                 page("2 Category and Time Analysis", 1)],
    "config": json.dumps({
        "version": "5.43",
        "themeCollection": {"baseTheme": {"name": "CY24SU10"}},
        "activeSectionIndex": 0,
        "defaultDrillFilterOtherVisuals": True,
        "settings": {"useStylableVisualContainerHeader": True},
    }),
    "layoutOptimization": 0,
    "publicCustomVisuals": [],
    "filters": "[]",
}

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="utf-8"?>\r\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
    'content-types">'
    '<Default Extension="json" ContentType="" />'
    '<Override PartName="/Version" ContentType="" />'
    '<Override PartName="/Settings" ContentType="" />'
    '<Override PartName="/Report/Layout" ContentType="" />'
    '<Override PartName="/DataModelSchema" ContentType="" />'
    '<Override PartName="/DiagramLayout" ContentType="" />'
    '<Override PartName="/Metadata" ContentType="" />'
    '<Override PartName="/SecurityBindings" ContentType="" />'
    '</Types>'
)

metadata = {"Version": 3, "AutoCreatedRelationships": [],
            "FileDescription": "Visual Analytics Lab - QP1 and QP2 model"}
settings = {"Version": 4, "ReportSettings": {"UseStylableVisualContainer": True}}
diagram = {
    "version": "1.1.0",
    "diagrams": [{
        "ordinal": 0, "scrollPosition": {"x": 0, "y": 0},
        "nodes": [
            {"location": {"x": 430, "y": 220}, "nodeIndex": "FactSales",
             "size": {"height": 240, "width": 220}, "zIndex": 0},
            {"location": {"x": 60, "y": 40}, "nodeIndex": "DimDate",
             "size": {"height": 220, "width": 200}, "zIndex": 1},
            {"location": {"x": 830, "y": 40}, "nodeIndex": "DimProduct",
             "size": {"height": 220, "width": 200}, "zIndex": 2},
            {"location": {"x": 60, "y": 430}, "nodeIndex": "DimCustomer",
             "size": {"height": 180, "width": 200}, "zIndex": 3},
            {"location": {"x": 830, "y": 430}, "nodeIndex": "DimTerritory",
             "size": {"height": 180, "width": 200}, "zIndex": 4},
        ],
        "name": "All tables", "zoomValue": 100, "pinKeyFieldsToTop": False,
        "showAllFields": True, "hideKeyFieldsWhenCollapsed": False,
        "tablesLocked": False, "selectedNodes": [], "defaultDiagram": True,
    }],
}


def u16(text):
    """PBIT text parts are UTF-16 LE with BOM."""
    return b"\xff\xfe" + text.encode("utf-16-le")


def jdump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)


# ==================================================================== PBIT
if os.path.exists(OUT):
    os.remove(OUT)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    # part order matters to Power BI's package reader
    z.writestr("Version", u16("1.28"))
    z.writestr("[Content_Types].xml", CONTENT_TYPES.encode("utf-8"))
    z.writestr("Settings", u16(jdump(settings)))
    z.writestr("Metadata", u16(jdump(metadata)))
    z.writestr("DataModelSchema", u16(jdump(model)))
    z.writestr("DiagramLayout", u16(jdump(diagram)))
    z.writestr("Report/Layout", u16(jdump(layout)))
    z.writestr("SecurityBindings", b"")

# ==================================================================== PBIP
# Power BI Project format: plain UTF-8, far less fragile than .pbit.
PROJ = os.path.join(BASE, "pbip")
NAME = "VisualAnalytics_Sales_26MML0045"
SM = os.path.join(PROJ, f"{NAME}.SemanticModel")
RP = os.path.join(PROJ, f"{NAME}.Report")
os.makedirs(SM, exist_ok=True)
os.makedirs(RP, exist_ok=True)


def w(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        f.write(jdump(obj) if not isinstance(obj, str) else obj)


w(os.path.join(PROJ, f"{NAME}.pbip"), {
    "version": "1.0",
    "artifacts": [{"report": {"path": f"{NAME}.Report"}}],
    "settings": {"enableAutoRecovery": True},
})

w(os.path.join(SM, "definition.pbism"), {"version": "1.0", "settings": {}})
w(os.path.join(SM, "model.bim"), model)
w(os.path.join(SM, "diagramLayout.json"), diagram)

w(os.path.join(RP, "definition.pbir"), {
    "version": "1.0",
    "datasetReference": {
        "byPath": {"path": f"../{NAME}.SemanticModel"},
        "byConnection": None,
    },
})
w(os.path.join(RP, "report.json"), layout)

# ==================================================================== report
n_meas = len(fact_measures)
n_calc = sum(1 for t in (fact, dim_product, dim_date)
             for c in t["columns"] if c.get("type") == "calculated")

print(f"Model contents")
print(f"  tables         : 7 (5 imported + 2 calculated)")
print(f"  relationships  : {len(rels)} (1 inactive)")
print(f"  hierarchies    : 4")
print(f"  calc columns   : {n_calc}")
print(f"  measures       : {n_meas}")
print(f"  report pages   : 2")
print()
print(f"OPTION A (preferred) - Power BI Project")
print(f"  {os.path.join('pbip', NAME + '.pbip')}")
print(f"  Open this .pbip in Power BI Desktop. Plain UTF-8, most reliable.")
print()
print(f"OPTION B - Power BI Template")
print(f"  {os.path.basename(OUT)} ({os.path.getsize(OUT)/1024:.0f} KB)")
print(f"  Fixed: part named 'Version' (was 'version.txt'), "
      f"SecurityBindings added.")
