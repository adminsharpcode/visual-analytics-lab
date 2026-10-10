"""Builds the QP2 (Assessment 2) lab record PDF."""
from _record_lib import (AUTHOR, REG, SUBJECT, CODE_NO,
                         cover, fig, shot, read, render, reset_counters,
                         shot_status)

reset_counters()
M = []
A = M.append

A("<div class='meta'>")
A(f"<b>Name:</b> {AUTHOR} &nbsp;|&nbsp; <b>Registration No.:</b> {REG}"
  f" &nbsp;|&nbsp; <b>Subject:</b> {SUBJECT} ({CODE_NO})<br>")
A("<b>Assessment 2 covers:</b> calculated tables, columns and measures in "
  "DAX; advanced DAX with <code>CALCULATE()</code> and Time Intelligence; "
  "report design and publishing.")
A("</div>")
A("")

A("## Aim")
A("")
A("4. Create calculated tables, calculated columns and measures using Data "
  "Analysis Expressions, to answer questions such as the top sold product and "
  "the average sales of a product category.")
A("5. Use the `CALCULATE()` function to manipulate filter context, and use "
  "Time Intelligence functions on the sales data — for example total sales "
  "revenue for each product category and the year-over-year growth trend of a "
  "product category.")
A("6. Design a report with the sales data and publish it with basic "
  "visualizations.")
A("")

A("## Prerequisite")
A("")
A("Assessment 1 must be complete: the cleansed `FactSales` table of 5,013 "
  "rows loaded, the star schema built with four active relationships, and "
  "`DimDate` marked as a date table. Time Intelligence functions in Step 5 "
  "return silently incorrect results if the date table is not marked.")
A("")

# ================================================================ STEP 4
A("---")
A("")
A("# Step 4 — Calculated Tables, Columns and Measures")
A("")
A("## 4.1 Calculated columns")
A("")
A("Created via **Table tools → New column**. A calculated column is evaluated "
  "row by row at refresh time and stored in the model.")
A("")
A("```")
A("""Net Unit Price = DIVIDE ( FactSales[SalesAmount], FactSales[OrderQuantity] )

Line Margin % =
DIVIDE ( FactSales[SalesAmount] - FactSales[TotalCost],
         FactSales[SalesAmount] )

Order Size Band =
SWITCH ( TRUE (),
    FactSales[OrderQuantity] <= 2, "1-2 units",
    FactSales[OrderQuantity] <= 4, "3-4 units",
    FactSales[OrderQuantity] <= 6, "5-6 units",
    "7+ units" )

Product Category = RELATED ( DimProduct[Category] )

Price Tier =
SWITCH ( TRUE (),
    DimProduct[ListPrice] < 100, "Budget",
    DimProduct[ListPrice] < 500, "Mid-range",
    "Premium" )

Financial Year =
"FY " & IF ( DimDate[MonthNo] >= 4, DimDate[Year], DimDate[Year] - 1 )
      & "-" & RIGHT ( IF ( DimDate[MonthNo] >= 4,
                           DimDate[Year] + 1, DimDate[Year] ), 2 )""")
A("```")
A("")
A(shot("qp2_01_new_column",
       "New calculated column being authored in the DAX formula bar"))
A("")
A("## 4.2 Core measures")
A("")
A("Created via **Table tools → New measure**. A measure is evaluated at query "
  "time against the current filter context and is not stored.")
A("")
A("```")
A("""Total Sales           = SUM ( FactSales[SalesAmount] )
Total Quantity        = SUM ( FactSales[OrderQuantity] )
Total Cost            = SUM ( FactSales[TotalCost] )
Total Profit          = [Total Sales] - [Total Cost]
Profit Margin %       = DIVIDE ( [Total Profit], [Total Sales] )
Order Count           = DISTINCTCOUNT ( FactSales[SalesOrderNumber] )
Average Order Value   = DIVIDE ( [Total Sales], [Order Count] )
Average Line Sales    = AVERAGE ( FactSales[SalesAmount] )
Average Selling Price = DIVIDE ( [Total Sales], [Total Quantity] )
Customer Count        = DISTINCTCOUNT ( FactSales[CustomerKey] )""")
A("```")
A("")
A("### Observation — unfiltered model")
A("")
A("| Measure | Value |")
A("|---|---|")
A("| Total Sales | 8,955,541.25 |")
A("| Total Quantity | 22,448 |")
A("| Total Cost | 4,123,542.00 |")
A("| Total Profit | 4,831,999.25 |")
A("| Profit Margin % | 53.96% |")
A("| Order Count | 5,008 |")
A("| Average Order Value | 1,788.25 |")
A("")
A(shot("qp2_02_measures",
       "Measures listed in the Fields pane, organised into display folders"))
A(shot("qp2_03_core_kpis",
       "Card visuals showing the core measure values"))
A("")
A("## 4.3 Question 1 — top sold product")
A("")
A("```")
A("""Top Product by Units =
VAR TopProduct =
    TOPN ( 1, ALL ( DimProduct[ProductName] ),
           CALCULATE ( [Total Quantity] ), DESC )
RETURN CONCATENATEX ( TopProduct, DimProduct[ProductName], ", " )

Top Product Units =
MAXX ( ALL ( DimProduct[ProductName] ), CALCULATE ( [Total Quantity] ) )

Top Product by Revenue =
VAR TopProduct =
    TOPN ( 1, ALL ( DimProduct[ProductName] ),
           CALCULATE ( [Total Sales] ), DESC )
RETURN CONCATENATEX ( TopProduct, DimProduct[ProductName], ", " )

Product Rank by Units =
RANKX ( ALL ( DimProduct[ProductName] ), [Total Quantity], , DESC, DENSE )""")
A("```")
A("")
A("`ALL()` is required inside `TOPN` so that the ranking is evaluated across "
  "every product rather than only the product on the current row.")
A("")
A("### Observation")
A("")
A("| Product | Units sold | Revenue |")
A("|---|---|---|")
A("| **GlideMouse Wireless** | **3,204** | 141,847.22 |")
A("| TactKey Mechanical | 2,501 | 249,113.16 |")
A("| GamingBook X17 | 1,344 | **2,534,432.17** |")
A("| Zenith A12 | 1,219 | 383,030.70 |")
A("| EduBook 13 | 1,210 | 746,661.45 |")
A("")
A("The two rankings disagree, which is the analytically interesting result. "
  "`GlideMouse Wireless` leads on volume at 3,204 units but contributes only "
  "141,847.22 in revenue, whereas `GamingBook X17` sells 58% fewer units yet "
  "generates almost eighteen times the revenue. A dashboard that reported only "
  "unit volume would misdirect attention entirely.")
A("")
A(fig("fig07_top_products.png",
      "Top ten products by units sold, with the leading product highlighted."))
A(shot("qp2_04_top_product",
       "Top sold product result shown in a card and table visual"))
A("")
A("## 4.4 Question 2 — average sales of product category")
A("")
A("```")
A("""Avg Sales per Line = AVERAGE ( FactSales[SalesAmount] )

Avg Sales per Order =
DIVIDE ( [Total Sales], DISTINCTCOUNT ( FactSales[SalesOrderNumber] ) )

Avg Sales per Category =
AVERAGEX ( VALUES ( DimProduct[Category] ), [Total Sales] )

Category Share % =
DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( DimProduct ) ) )""")
A("```")
A("")
A("### Observation")
A("")
A("| Category | Total Sales | Orders | Units | Avg Sales per Order | Share % |")
A("|---|---|---|---|---|---|")
A("| Electronics | 7,081,992.08 | 2,172 | 9,758 | 3,260.59 | 79.08% |")
A("| Furniture | 861,784.14 | 519 | 2,422 | 1,660.47 | 9.62% |")
A("| Accessories | 786,667.35 | 1,996 | 8,818 | 394.12 | 8.78% |")
A("| Software | 225,097.68 | 321 | 1,450 | 701.24 | 2.51% |")
A("")
A("`Avg Sales per Category` across all four categories = **2,238,885.31**.")
A("")
A("Accessories ranks second on order count (1,996, almost matching "
  "Electronics at 2,172) yet last but one on total sales, because its average "
  "order value is 394.12 against Electronics at 3,260.59 — roughly eight "
  "times lower. High transaction volume is therefore not a proxy for revenue "
  "contribution.")
A("")
A(fig("fig08_category_avg.png",
      "Total sales and average sales per order by category, showing that "
      "order count and order value rank the categories differently."))
A(shot("qp2_05_category_avg",
       "Average sales by product category in a table visual"))
A("")
A("## 4.5 Calculated tables")
A("")
A("Created via **Modeling → New table**. A calculated table is materialised "
  "at refresh.")
A("")
A("```")
A("""Product Category Summary =
SUMMARIZE ( FactSales, DimProduct[Category],
    "Total Sales",         [Total Sales],
    "Total Quantity",      [Total Quantity],
    "Order Count",         [Order Count],
    "Avg Sales per Order", [Avg Sales per Order],
    "Total Profit",        [Total Profit],
    "Profit Margin %",     [Profit Margin %] )

Top 5 Products =
TOPN ( 5,
    SUMMARIZE ( FactSales, DimProduct[ProductName], DimProduct[Category],
        "Units Sold", [Total Quantity], "Revenue", [Total Sales] ),
    [Units Sold], DESC )

Date Table DAX =
ADDCOLUMNS ( CALENDAR ( DATE(2023,1,1), DATE(2025,12,31) ),
    "Year",      YEAR ( [Date] ),
    "MonthNo",   MONTH ( [Date] ),
    "MonthName", FORMAT ( [Date], "MMMM" ),
    "Quarter",   "Q" & QUARTER ( [Date] ),
    "YearMonth", FORMAT ( [Date], "YYYY-MM" ) )

Category Year Performance =
SUMMARIZE ( FactSales, DimProduct[Category], DimDate[Year],
            "Sales", [Total Sales] )

Discount Scenario = GENERATESERIES ( 0, 0.25, 0.05 )""")
A("```")
A("")
A("`Product Category Summary` returns exactly four rows matching the table in "
  "section 4.4.")
A("")
A(shot("qp2_06_calc_table",
       "Product Category Summary calculated table in Data view"))
A("")

# ================================================================ STEP 5
A("---")
A("")
A("# Step 5 — Advanced DAX: CALCULATE and Time Intelligence")
A("")
A("## 5.1 Manipulating filter context with CALCULATE()")
A("")
A("`CALCULATE` evaluates an expression under a modified filter context. It is "
  "the only DAX function that can change filter context.")
A("")
A("| Technique | Function | Effect on context |")
A("|---|---|---|")
A("| Add a filter | `Category = \"Electronics\"` | narrows the context |")
A("| Remove all filters | `ALL(DimProduct)` | grand-total denominator |")
A("| Keep one filter | `ALLEXCEPT(DimProduct, Category)` | share within own "
  "category |")
A("| Respect slicers | `ALLSELECTED(Category)` | share of user selection |")
A("| Intersect, not replace | `KEEPFILTERS(Year = 2025)` | preserves an "
  "existing Year slicer |")
A("| Switch relationship | `USERELATIONSHIP(...)` | activates the inactive "
  "path from Assessment 1 |")
A("")
A("```")
A("""Electronics Sales =
CALCULATE ( [Total Sales], DimProduct[Category] = "Electronics" )

Pct of Total Sales =
DIVIDE ( [Total Sales],
         CALCULATE ( [Total Sales], ALL ( DimProduct ),
                                    ALL ( DimTerritory ) ) )

Pct of Category Sales =
DIVIDE ( [Total Sales],
         CALCULATE ( [Total Sales],
                     ALLEXCEPT ( DimProduct, DimProduct[Category] ) ) )

Sales 2025 Override    = CALCULATE ( [Total Sales], DimDate[Year] = 2025 )
Sales 2025 KeepFilters =
CALCULATE ( [Total Sales], KEEPFILTERS ( DimDate[Year] = 2025 ) )

Laptops or Mobiles Sales =
CALCULATE ( [Total Sales],
    FILTER ( ALL ( DimProduct[Subcategory] ),
             DimProduct[Subcategory] = "Laptops"
          || DimProduct[Subcategory] = "Mobiles" ) )

Sales by Customer Territory =
CALCULATE ( [Total Sales],
    USERELATIONSHIP ( DimCustomer[TerritoryKey],
                      DimTerritory[TerritoryKey] ) )""")
A("```")
A("")
A("`Sales 2025 Override` and `Sales 2025 KeepFilters` differ materially: a "
  "direct predicate **replaces** any existing filter on that column, so with "
  "a Year slicer set to 2023 the override still returns 2025. `KEEPFILTERS` "
  "**intersects** instead, returning blank because 2023 and 2025 do not "
  "overlap.")
A("")
A(shot("qp2_07_calculate",
       "CALCULATE measure and its result, contrasted with the base measure"))
A("")
A("## 5.2 Total sales revenue for each product category")
A("")
A("```")
A("""Category Revenue =
CALCULATE ( [Total Sales], ALLEXCEPT ( DimProduct, DimProduct[Category] ) )

Category Revenue Table =
SUMMARIZE ( FactSales, DimProduct[Category], "Revenue", [Total Sales] )""")
A("```")
A("")
A("| Category | 2023 | 2024 | 2025 | Total |")
A("|---|---|---|---|---|")
A("| Electronics | 2,229,091.18 | 2,422,281.89 | 2,430,619.01 | 7,081,992.08 |")
A("| Furniture | 215,300.29 | 285,115.53 | 361,368.32 | 861,784.14 |")
A("| Accessories | 214,422.23 | 264,027.21 | 308,217.91 | 786,667.35 |")
A("| Software | 61,936.51 | 61,233.78 | 101,927.39 | 225,097.68 |")
A("| **Total** | **2,720,750.21** | **3,032,658.41** | **3,202,132.63** | "
  "**8,955,541.25** |")
A("")
A("## 5.3 Time Intelligence")
A("")
A("```")
A("""Sales YTD = TOTALYTD ( [Total Sales], DimDate[Date] )
Sales QTD = TOTALQTD ( [Total Sales], DimDate[Date] )
Sales MTD = TOTALMTD ( [Total Sales], DimDate[Date] )

-- Indian financial year, April start
Sales FYTD = TOTALYTD ( [Total Sales], DimDate[Date], "31/03" )

Sales PY = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
Sales PM = CALCULATE ( [Total Sales], DATEADD ( DimDate[Date], -1, MONTH ) )

Sales Rolling 3M =
CALCULATE ( [Total Sales],
    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ), -3, MONTH ) )

Sales Cumulative =
CALCULATE ( [Total Sales],
    FILTER ( ALLSELECTED ( DimDate[Date] ),
             DimDate[Date] <= MAX ( DimDate[Date] ) ) )

Sales 3M Moving Avg =
AVERAGEX (
    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ), -3, MONTH ),
    CALCULATE ( [Total Sales] ) )""")
A("```")
A("")
A(fig("fig10_ytd.png",
      "<code>TOTALYTD</code> behaviour. The cumulative line resets at each "
      "year boundary, confirming <code>DimDate</code> is correctly marked as "
      "a date table."))
A(shot("qp2_08_time_intel",
       "Time Intelligence measures (Sales YTD, Sales PY) in a table visual"))
A("")
A("## 5.4 Year-over-year growth trend of a product category")
A("")
A("```")
A("""YoY Growth = 
VAR Cur = [Total Sales]
VAR Prev = [Sales PY]
RETURN IF ( NOT ISBLANK ( Prev ), Cur - Prev )

YoY Growth % = DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )

YoY Trend =
VAR G = [YoY Growth %]
RETURN SWITCH ( TRUE (),
    ISBLANK ( G ), "No prior year",
    G > 0.10,      "Strong growth",
    G > 0,         "Growing",
    G > -0.10,     "Slight decline",
    "Sharp decline" )

Electronics YoY % =
VAR Cur  = CALCULATE ( [Total Sales], DimProduct[Category] = "Electronics" )
VAR Prev = CALCULATE ( [Total Sales], DimProduct[Category] = "Electronics",
                       SAMEPERIODLASTYEAR ( DimDate[Date] ) )
RETURN DIVIDE ( Cur - Prev, Prev )""")
A("```")
A("")
A("### Observation")
A("")
A("| Category | 2024 vs 2023 | 2025 vs 2024 | Trend |")
A("|---|---|---|---|")
A("| Accessories | +23.13% | +16.74% | Strong growth |")
A("| Electronics | +8.67% | +0.34% | Growing, now plateaued |")
A("| Furniture | +32.43% | +26.74% | Strong growth |")
A("| Software | −1.13% | +66.45% | Recovered sharply |")
A("| **Overall** | **+11.46%** | **+5.59%** | Growing |")
A("")
A("The headline figures conceal the important detail. Overall growth halved "
  "from +11.46% to +5.59%, and the cause is visible only at category level: "
  "Electronics, which is 79% of revenue, effectively stopped growing at "
  "+0.34%. Furniture and Accessories continued to grow strongly but are too "
  "small to compensate. Software reversed from −1.13% to +66.45%, though from "
  "a low base of 2.51% of revenue. This is precisely the divergence that Time "
  "Intelligence measures exist to surface.")
A("")
A(fig("fig09_yoy.png",
      "Category revenue by year produced with <code>CALCULATE</code>, and "
      "year-over-year growth percentage produced with "
      "<code>SAMEPERIODLASTYEAR</code>."))
A(shot("qp2_09_yoy_matrix",
       "Matrix visual with Total Sales, Sales PY and YoY Growth %, with "
       "conditional formatting applied"))
A("")

# ================================================================ STEP 6
A("---")
A("")
A("# Step 6 — Designing and Publishing the Report")
A("")
A("## 6.1 Page 1 — Sales Overview")
A("")
A("| Element | Visual type | Configuration |")
A("|---|---|---|")
A("| KPI row | Cards | Total Sales, Total Quantity, Total Profit, Profit "
  "Margin %, YoY Growth % |")
A("| Sales trend | Line chart | Axis `Date Hierarchy`; values `[Total Sales]`, "
  "`[Sales PY]` |")
A("| Category performance | Stacked column | Axis `Category`, legend `Year` |")
A("| Top 10 products | Bar chart | Top-N filter 10 by `[Total Quantity]` |")
A("| Regional split | Map or donut | Location `Region` |")
A("| Category detail | Table | `Category`, `Subcategory`, `[Total Sales]`, "
  "`[Avg Sales per Order]`, `[Category Share %]` |")
A("| Slicers | Year, Category, Region, Segment, OrderStatus | left panel |")
A("")
A("## 6.2 Page 2 — Category and Time Analysis")
A("")
A("| Element | Visual type | Configuration |")
A("|---|---|---|")
A("| YoY matrix | Matrix | Rows `Category`, columns `Year`, values "
  "`[Total Sales]`, `[Sales PY]`, `[YoY Growth %]` |")
A("| Cumulative sales | Area chart | Axis `YearMonth`, value "
  "`[Sales Cumulative]` |")
A("| Rolling average | Line chart | `[Total Sales]` vs "
  "`[Sales 3M Moving Avg]` |")
A("| Monthly YTD | Line and clustered column | column `[Total Sales]`, line "
  "`[Sales YTD]` |")
A("| Growth by subcategory | Bar chart | Axis `Subcategory`, value "
  "`[YoY Growth %]` |")
A("")
A("Conditional formatting is applied to `[YoY Growth %]` on the matrix: green "
  "background above zero, red below.")
A("")
A(fig("fig11_report_mockup.png",
      "Intended layout of the Page 1 report canvas. This is an illustration "
      "of the design, not a Power BI capture."))
A(shot("qp2_10_report_p1", "Report Page 1 — Sales Overview in Power BI"))
A(shot("qp2_11_report_p2",
       "Report Page 2 — Category and Time Analysis in Power BI"))
A("")
A("## 6.3 Formatting applied")
A("")
A("| Setting | Value |")
A("|---|---|")
A("| Canvas | 16:9, background `#F7F9FC` |")
A("| Accent colour | `#3366CC` throughout |")
A("| Page title | `Sales Analysis — Vedant Nimkar (26MML0045)` |")
A("| Drill-down | enabled via `Product Hierarchy` on category visuals |")
A("| Interactions | slicers set to filter rather than highlight |")
A("| Sort order | `[Total Sales]` descending on all category visuals |")
A("")
A("## 6.4 Publishing procedure")
A("")
A("1. **File → Save As** → `VisualAnalytics_Sales_26MML0045.pbix`")
A("2. **Home → Publish**")
A("3. Sign in with the institutional Microsoft 365 account")
A("4. Select destination workspace → **My workspace**")
A("5. On the *Success!* confirmation, follow the link to open the report in "
  "the browser")
A("")
A("### Post-publish configuration")
A("")
A("| Task | Location |")
A("|---|---|")
A("| Scheduled refresh | Workspace → Dataset → Settings → Scheduled refresh |")
A("| Gateway connection | required only for the SQL Server source |")
A("| Pin visuals to dashboard | hover a visual → Pin icon |")
A("| Export | File → Export to PDF |")
A("")
A(shot("qp2_12_publish",
       "Publish dialog with the destination workspace selected"))
A(shot("qp2_13_success",
       "Success confirmation showing the published report link"))
A(shot("qp2_14_service",
       "Published report rendered at app.powerbi.com"))
A("")

# ================================================================ RESULT
A("---")
A("")
A("# Result")
A("")
A("All three objectives of Assessment 2 were completed.")
A("")
A("**Step 4.** Six calculated columns, ten core measures and five calculated "
  "tables were authored in DAX. `TOPN` with `ALL` identified `GlideMouse "
  "Wireless` as the top product by units at 3,204, while ranking by revenue "
  "returned `GamingBook X17` at 2,534,432.17 — demonstrating that volume and "
  "value produce different leaders. Category averages showed Accessories "
  "generating an average order value of 394.12 against Electronics at "
  "3,260.59 despite comparable order counts.")
A("")
A("**Step 5.** `CALCULATE` was used with `ALL`, `ALLEXCEPT`, `ALLSELECTED`, "
  "`KEEPFILTERS`, `FILTER` and `USERELATIONSHIP` to add, remove, retain and "
  "intersect filters and to activate the inactive relationship from "
  "Assessment 1. Time Intelligence functions produced year-to-date, "
  "prior-year, rolling three-month, cumulative and moving-average measures. "
  "Category year-over-year growth ranged from −1.13% to +66.45% against an "
  "overall +5.59%, revealing that Electronics had plateaued at +0.34% while "
  "contributing 79% of revenue.")
A("")
A("**Step 6.** A two-page report was designed with KPI cards, trend, "
  "category, ranking and regional visuals, drill-down hierarchies, five "
  "slicers and a conditionally formatted year-over-year matrix, then published "
  "to the Power BI Service.")
A("")
A("Every measure value was cross-checked against an independent pandas "
  "computation over the same source data, recorded in "
  "`expected_results/EXPECTED_RESULTS.txt`.")
A("")
A("## Deliverables")
A("")
A("| Path | Contents |")
A("|---|---|")
A("| `code/Step4_DAX_Calculated.txt` | calculated columns, measures, tables |")
A("| `code/Step5_DAX_Advanced.txt` | CALCULATE and Time Intelligence |")
A("| `code/Step6_Report_Design.md` | report layout and publish steps |")
A("| `expected_results/` | verification values and derived tables |")
A("| `figures/` | figures reproduced in this record |")
A("| `screenshots/` | Power BI Desktop captures |")
A("")

# ================================================================ APPENDIX
import os as _os
from _record_lib import BASE as _B

_dax = _os.path.join(_B, "code", "APPLIED_DAX.md")
if _os.path.exists(_dax):
    A("---")
    A("")
    A("# Appendix — Complete Applied DAX")
    A("")
    A("The listing below was extracted programmatically from the applied "
      "semantic model (`Visual1.SemanticModel/definition/tables/*.tmdl`). It "
      "is therefore the exact code running in the report, not a separately "
      "maintained transcription.")
    A("")
    _txt = read(_dax).split("\n")
    # drop the source file's own H1 and its intro paragraph
    _start = 0
    for _i, _ln in enumerate(_txt):
        if _ln.startswith("| Object type"):
            _start = _i
            break
    A("\n".join(_txt[_start:]))
    A("")

n = shot_status("qp2_")
A(f"<div class='note'><b>Figures and screenshots.</b> Figures 1 to 4 are "
  f"rendered directly from the actual dataset and are therefore genuine "
  f"results. Figure 5 is an illustration of the report layout. The "
  f"{n} screenshots are Power BI Desktop captures from the working file. The "
  f"DAX appendix was extracted from the applied semantic model, so it is "
  f"verifiably the code running in the report.</div>")

md = "\n".join(M)
cv = cover("Assessment 2",
           "DAX Calculations, Advanced Filter Context and Report Publishing",
           "Power BI Desktop &middot; DAX &middot; Power BI Service")
print("Building QP2 record...")
render(md, cv, f"VisualAnalyticsLab_QP2_{REG}")
print(f"   screenshots present: {n} / 14")
