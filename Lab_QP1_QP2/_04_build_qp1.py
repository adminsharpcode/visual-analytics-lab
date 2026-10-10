"""Builds the QP1 (Assessment 1) lab record PDF."""
import os

from _record_lib import (AUTHOR, REG, SUBJECT, CODE_NO, CODE, BASE,
                         cover, fig, shot, read, render, reset_counters,
                         shot_status)

reset_counters()
M = []
A = M.append

A("<div class='meta'>")
A(f"<b>Name:</b> {AUTHOR} &nbsp;|&nbsp; <b>Registration No.:</b> {REG}"
  f" &nbsp;|&nbsp; <b>Subject:</b> {SUBJECT} ({CODE_NO})<br>")
A("<b>Assessment 1 covers:</b> environment setup and data-source connection, "
  "data cleansing and transformation, and data-model design.")
A("</div>")
A("")

A("## Aim")
A("")
A("1. Set up the environment and connect to a data source — install Power BI "
  "Desktop, connect to SQL Server, load and preview the data.")
A("2. Apply data cleansing and transformation in Power BI, loading the "
  "resulting queries into the data model using a sales dataset.")
A("3. Design a data model — create model relationships, configure table and "
  "column properties, and create hierarchies using the sales dataset.")
A("")

A("## Software Requirements")
A("")
A("| Component | Purpose |")
A("|---|---|")
A("| Power BI Desktop | modelling, transformation and reporting |")
A("| SQL Server + SSMS | relational data source |")
A("| Power Query (M) | data cleansing and transformation |")
A("| Python (pandas) | independent verification of results |")
A("")

A("## Dataset Description")
A("")
A("A retail sales dataset in star-schema layout. The fact table was "
  "deliberately produced in an uncleansed state so that the transformation "
  "requirements operate on genuine data-quality defects rather than on "
  "already-clean data.")
A("")
A("| Table | Rows | Role |")
A("|---|---|---|")
A("| `FactSales_RAW` | 6,012 | Fact — order lines, uncleansed |")
A("| `DimProduct` | 22 | Product, subcategory, category, pricing |")
A("| `DimCustomer` | 220 | Customer name, segment, territory |")
A("| `DimTerritory` | 5 | Region, country, group |")
A("| `DimDate` | 1,096 | Calendar 2023-01-01 to 2025-12-31 |")
A("")
A("Source files: `data/*.csv`, `data/SalesData.xlsx`, and "
  "`sql/01_create_load.sql` to recreate the tables in SQL Server.")
A("")

# ================================================================ STEP 1
A("---")
A("")
A("# Step 1 — Setting Up the Environment and Connecting to the Data Source")
A("")
A("## Procedure")
A("")
A("1. Install **Power BI Desktop** and **SQL Server** with SQL Server "
  "Management Studio.")
A("2. Open `sql/01_create_load.sql` in SSMS and execute it. This creates the "
  "`VisualAnalyticsLab` database and populates all five tables.")
A("3. In Power BI Desktop select **Home → Get data → SQL Server**.")
A("4. Enter the connection details:")
A("")
A("| Field | Value |")
A("|---|---|")
A("| Server | `localhost` or `.\\SQLEXPRESS` |")
A("| Database | `VisualAnalyticsLab` |")
A("| Data connectivity mode | Import |")
A("")
A("5. In the **Navigator**, tick `FactSales`, `DimProduct`, `DimCustomer`, "
  "`DimTerritory` and `DimDate`, previewing each in the right-hand pane.")
A("6. Click **Transform Data** rather than **Load**, so the data opens "
  "directly in Power Query Editor for cleansing.")
A("")
A("> **CSV alternative.** If SQL Server is unavailable, use **Get data → "
  "Text/CSV** on the files in `data/`, or **Excel workbook** on "
  "`SalesData.xlsx`. Every later step is identical; only the `Source` line of "
  "each M query changes.")
A("")
A("### M query for the SQL Server connection")
A("")
A("```")
A("""let
    Source = Sql.Database("localhost", "VisualAnalyticsLab"),
    dbo_FactSales = Source{[Schema = "dbo", Item = "FactSales"]}[Data]
in
    dbo_FactSales""")
A("```")
A("")
A(shot("qp1_01_getdata",
       "Get data dialog with SQL Server selected"))
A(shot("qp1_02_navigator",
       "Navigator window listing the five source tables with a live preview"))
A("")
A("## Observation — data as loaded")
A("")
A(fig("fig01_raw_preview.png",
      "Raw <code>FactSales</code> as loaded from the source. Dates arrive as "
      "text in three different formats, unit price is text carrying a currency "
      "prefix and thousands separators, <code>Notes</code> is entirely blank, "
      "and several quantities are missing."))
A(shot("qp1_03_raw_preview",
       "Raw FactSales preview in Power BI before any transformation"))
A("")

# ================================================================ STEP 2
A("---")
A("")
A("# Step 2 — Data Cleansing and Transformation")
A("")
A("## Data-quality defects identified")
A("")
A("| Defect | Occurrences | Treatment applied |")
A("|---|---|---|")
A("| Exact duplicate rows | 12 | `Table.Distinct` |")
A("| Null `OrderQuantity` | 40 | rows removed |")
A("| Null `SalesAmount` | 35 | recomputed as price × qty × (1 − discount) |")
A("| Negative `OrderQuantity` | 8 | rows removed as data-entry errors |")
A("| Blank `Notes` column | 1 column | column removed |")
A("| Mixed date formats | 3 formats | parsed into a true `date` type |")
A("| Currency stored as text | all rows | `\"Rs. 1,234.00\"` → `1234.00` |")
A("| Untrimmed, inconsistent status text | many | "
  "`Text.Proper(Text.Trim())` |")
A("| Cancelled orders | 949 | excluded from sales analysis |")
A("")
A(fig("fig02_data_issues.png",
      "Data-quality issues detected in the raw source, counted directly from "
      "the loaded data."))
A("")
A("## Applied steps and resulting row count")
A("")
A("| # | Applied step | Rows remaining |")
A("|---|---|---|")
A("| 0 | Source loaded | 6,012 |")
A("| 1 | Removed blank `Notes` column | 6,012 |")
A("| 2 | Removed duplicates | 6,010 |")
A("| 3 | Removed null quantity | 5,970 |")
A("| 4 | Removed negative quantity | 5,962 |")
A("| 5 | Excluded cancelled orders | **5,013** |")
A("")
A(fig("fig03_cleansing_funnel.png",
      "Row count after each applied step. 6,012 raw rows reduce to 5,013 "
      "analysable rows, a 16.6% reduction attributable entirely to "
      "data-quality defects."))
A("")
A("## Power Query M — FactSales cleansing query")
A("")
A("Paste into **Home → Transform data → Advanced Editor**, replacing "
  "`<PATH>` with the `data` folder path.")
A("")
A("```")
m = read(os.path.join(CODE, "Step2_PowerQuery_M.txt"))
A(m[m.index("let\n    // 1. CONNECT"):m.index("EXPECTED RESULT")].rstrip())
A("```")
A("")
A("The dimension queries and the SQL Server variant are in "
  "`code/Step2_PowerQuery_M.txt`.")
A("")
A(shot("qp1_04_pq_editor",
       "Power Query Editor showing all five queries in the Queries pane"))
A(shot("qp1_05_applied_steps",
       "Applied Steps pane listing every transformation in order"))
A(shot("qp1_06_advanced_ed",
       "Advanced Editor displaying the complete M script"))
A("")
A("## Result of cleansing")
A("")
A(fig("fig04_clean_preview.png",
      "Cleansed <code>FactSales</code>. Dates are real date values, currency "
      "is numeric, order status is normalised to two values, and a derived "
      "<code>Profit</code> column has been added."))
A(shot("qp1_07_clean_preview",
       "Cleansed FactSales in Power Query showing 5,013 rows"))
A("")
A("<div class='ok'><b>Verification.</b> The identical cleansing logic was "
  "replicated in pandas over the same source file, producing 5,013 rows and "
  "the distinct status values <code>Pending</code> and <code>Shipped</code>. "
  "See <code>expected_results/EXPECTED_RESULTS.txt</code>.</div>")
A("")

# ================================================================ STEP 3
A("---")
A("")
A("# Step 3 — Designing the Data Model")
A("")
A("## 3.1 Model relationships")
A("")
A("Created in **Model view** by dragging each dimension key onto the matching "
  "column in `FactSales`.")
A("")
A("| # | One side | Many side | Cardinality | Cross-filter | Active |")
A("|---|---|---|---|---|---|")
A("| 1 | `DimDate[DateKey]` | `FactSales[DateKey]` | 1:* | Single | Yes |")
A("| 2 | `DimProduct[ProductKey]` | `FactSales[ProductKey]` | 1:* | Single | "
  "Yes |")
A("| 3 | `DimCustomer[CustomerKey]` | `FactSales[CustomerKey]` | 1:* | Single "
  "| Yes |")
A("| 4 | `DimTerritory[TerritoryKey]` | `FactSales[TerritoryKey]` | 1:* | "
  "Single | Yes |")
A("| 5 | `DimTerritory[TerritoryKey]` | `DimCustomer[TerritoryKey]` | 1:* | "
  "Single | **No** |")
A("")
A("Relationship 5 is deliberately left **inactive**. Both `FactSales` and "
  "`DimCustomer` carry `TerritoryKey`, which creates two routes to "
  "`DimTerritory`; Power BI permits only one active path between two tables. "
  "The direct fact relationship is kept active, and the inactive one is "
  "invoked on demand with `USERELATIONSHIP` in Assessment 2.")
A("")
A("### Marking the date table")
A("")
A("Select `DimDate` → **Table tools → Mark as date table** → choose the "
  "`Date` column. This is a prerequisite for the Time Intelligence functions "
  "used in Assessment 2; without it those functions return silently "
  "incorrect results.")
A("")
A(fig("fig05_star_schema.png",
      "Star schema: a single fact table surrounded by four conformed "
      "dimensions. The inactive Customer→Territory relationship is shown "
      "dashed."))
A(shot("qp1_08_model_view",
       "Model view showing the completed star schema"))
A(shot("qp1_09_relationship",
       "Edit relationship dialog confirming cardinality and cross-filter "
       "direction"))
A("")
A("## 3.2 Table and column properties")
A("")
A("### FactSales")
A("")
A("| Column | Data type | Format | Summarisation | Hidden |")
A("|---|---|---|---|---|")
A("| `SalesOrderNumber` | Text | — | Do not summarize | No |")
A("| `OrderDate` | Date | dd mmm yyyy | Do not summarize | No |")
A("| `DateKey` | Whole number | — | Do not summarize | Yes |")
A("| `ProductKey` | Whole number | — | Do not summarize | Yes |")
A("| `CustomerKey` | Whole number | — | Do not summarize | Yes |")
A("| `TerritoryKey` | Whole number | — | Do not summarize | Yes |")
A("| `OrderQuantity` | Whole number | #,##0 | Sum | No |")
A("| `UnitPrice` | Decimal | Currency 2 dp | Do not summarize | No |")
A("| `DiscountPct` | Decimal | Percentage | Average | No |")
A("| `SalesAmount` | Decimal | Currency 2 dp | Sum | No |")
A("| `TotalCost` | Decimal | Currency 2 dp | Sum | No |")
A("| `Profit` | Decimal | Currency 2 dp | Sum | No |")
A("| `OrderStatus` | Text | — | Do not summarize | No |")
A("")
A("Hiding the surrogate keys is the substantive point of this exercise: "
  "report authors are forced to use descriptive dimension attributes rather "
  "than meaningless integers, and the keys can no longer be accidentally "
  "aggregated.")
A("")
A("### DimDate — sort-by-column settings")
A("")
A("| Column | Sort by | Reason |")
A("|---|---|---|")
A("| `MonthName` | `MonthNo` | otherwise the axis reads April, August, "
  "December alphabetically |")
A("| `MonthShort` | `MonthNo` | same |")
A("| `Quarter` | `QuarterNo` | chronological quarter order |")
A("")
A("### DimProduct / DimCustomer / DimTerritory")
A("")
A("| Setting | Applied to |")
A("|---|---|")
A("| Hidden | `ProductKey`, `CustomerKey`, `TerritoryKey` |")
A("| Currency 2 dp, Do not summarize | `StandardCost`, `ListPrice`, "
  "`UnitMargin` |")
A("| Do not summarize | `Category`, `Subcategory`, `Segment`, `Region` |")
A("")
A(shot("qp1_10_properties",
       "Column properties pane showing format, summarisation and hidden "
       "settings"))
A(shot("qp1_11_sort_by",
       "Sort by column applied to MonthName so the axis is chronological"))
A("")
A("## 3.3 Hierarchies")
A("")
A("Created by right-clicking the top-level field → **Create hierarchy**, then "
  "dragging the remaining levels in order.")
A("")
A("| Hierarchy | Levels |")
A("|---|---|")
A("| Product Hierarchy | Category → Subcategory → ProductName |")
A("| Date Hierarchy | Year → Quarter → MonthName → DayOfMonth |")
A("| Geography Hierarchy | Group → Country → Region |")
A("| Customer Hierarchy | Segment → CustomerName |")
A("")
A(fig("fig06_hierarchies.png",
      "The four hierarchies created to support drill-down in the report "
      "visuals."))
A(shot("qp1_12_hierarchies",
       "Fields pane showing the four completed hierarchies"))
A("")
A("## 3.4 Verification checklist")
A("")
A("| Check | Expected |")
A("|---|---|")
A("| Model shape | star, not snowflake |")
A("| Active relationships | 4 |")
A("| Inactive relationships | 1 |")
A("| `DimDate` marked as date table | yes |")
A("| Surrogate keys hidden | all `*Key` columns |")
A("| `MonthName` axis order | chronological |")
A("| Hierarchies drilling correctly | all four |")
A("")

# ================================================================ RESULT
A("---")
A("")
A("# Result")
A("")
A("All three objectives of Assessment 1 were completed.")
A("")
A("**Step 1.** The environment was configured and the sales dataset connected "
  "in Import mode, with all five tables previewed in the Navigator before "
  "being opened in Power Query Editor.")
A("")
A("**Step 2.** Fifteen applied steps reduced 6,012 raw rows to 5,013 "
  "analysable rows. Twelve duplicates, 40 null quantities and 8 negative "
  "quantities were removed, 949 cancelled orders excluded, 35 missing sales "
  "amounts recomputed, three mixed date formats parsed into a single date "
  "type, text currency converted to numeric, and order status normalised.")
A("")
A("**Step 3.** A star schema was built with four active relationships and one "
  "deliberately inactive relationship to avoid an ambiguous filter path. "
  "`DimDate` was marked as a date table, surrogate keys were hidden, formats "
  "and summarisation were configured, sort-by-column was applied so that "
  "month names order chronologically, and four hierarchies were created for "
  "drill-down.")
A("")
A("The cleansing outcome was independently verified against a pandas "
  "reimplementation over the same source data.")
A("")
A("## Deliverables")
A("")
A("| Path | Contents |")
A("|---|---|")
A("| `data/` | CSV files and `SalesData.xlsx` |")
A("| `sql/01_create_load.sql` | SQL Server DDL and data load |")
A("| `code/Step2_PowerQuery_M.txt` | all five Power Query M queries |")
A("| `code/Step3_DataModel.md` | relationships, properties, hierarchies |")
A("| `expected_results/EXPECTED_RESULTS.txt` | verification values |")
A("| `figures/` | figures reproduced in this record |")
A("| `screenshots/` | Power BI Desktop captures |")
A("")

# ================================================================ APPENDIX
import os as _os
from _record_lib import BASE as _B

_m = _os.path.join(_B, "code", "APPLIED_M.md")
if _os.path.exists(_m):
    A("---")
    A("")
    A("# Appendix A — Complete Applied Power Query (M)")
    A("")
    A("Extracted programmatically from the applied semantic model "
      "(`Visual1.SemanticModel/definition/tables/*.tmdl`). Each listing is "
      "the actual `partition = m` source executing on refresh, not a "
      "separately maintained transcription.")
    A("")
    _t = read(_m).split("\n")
    _i = next((k for k, l in enumerate(_t) if l.startswith("## ")), 0)
    A("\n".join(_t[_i:]))
    A("")

_mod = _os.path.join(_B, "code", "APPLIED_MODEL.md")
if _os.path.exists(_mod):
    A("---")
    A("")
    A("# Appendix B — Applied Model Structure")
    A("")
    A("Relationships, hierarchies and column properties as they exist in the "
      "applied model, confirming the Step 3 configuration.")
    A("")
    _t = read(_mod).split("\n")
    _i = next((k for k, l in enumerate(_t) if l.startswith("## ")), 0)
    A("\n".join(_t[_i:]))
    A("")

n = shot_status("qp1_")
A(f"<div class='note'><b>Figures and screenshots.</b> Figures 1 to 4 are "
  f"rendered directly from the actual dataset and are therefore genuine "
  f"results. Figures 5 and 6 are diagrams of the model design. The "
  f"{n} screenshots are Power BI Desktop captures from the working file. All "
  f"code in the appendices was extracted from the applied semantic model, so "
  f"it is verifiably the logic running in the report.</div>")

md = "\n".join(M)
cv = cover("Assessment 1",
           "Environment Setup, Data Cleansing and Data Modelling",
           "Power BI Desktop &middot; SQL Server &middot; Power Query (M)")
print("Building QP1 record...")
render(md, cv, f"VisualAnalyticsLab_QP1_{REG}")
print(f"   screenshots present: {n} / 12")
