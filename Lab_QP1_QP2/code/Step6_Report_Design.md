# QP2 Step 6 - Design and Publish a Report in Power BI

Two report pages, then publish to the Power BI Service.

## 6.1 Page 1 — Sales Overview

### KPI cards (top row)

| Card | Measure | Format |
|------|---------|--------|
| Total Sales | `[Total Sales]` | Currency, 2 dp |
| Total Quantity | `[Total Quantity]` | Whole number |
| Total Profit | `[Total Profit]` | Currency, 2 dp |
| Profit Margin % | `[Profit Margin %]` | Percentage, 2 dp |
| YoY Growth % | `[YoY Growth %]` | Percentage, 2 dp |

### Visuals

| Visual | Type | Axis / Legend | Values |
|--------|------|---------------|--------|
| Sales trend | Line chart | Axis `DimDate[Date Hierarchy]` | `[Total Sales]`, `[Sales PY]` |
| Sales by category | Stacked column | Axis `DimProduct[Category]`, Legend `DimDate[Year]` | `[Total Sales]` |
| Top 10 products | Bar chart | Axis `DimProduct[ProductName]` | `[Total Quantity]` |
| Sales by region | Map or donut | Location `DimTerritory[Region]` | `[Total Sales]` |
| Category detail | Table | `Category`, `Subcategory` | `[Total Sales]`, `[Avg Sales per Order]`, `[Category Share %]` |

Apply **Top N** filter = 10 on the Top 10 products visual, ranked by
`[Total Quantity]` descending.

### Slicers (left panel)

- `DimDate[Year]` — dropdown
- `DimProduct[Category]` — list, multi-select
- `DimTerritory[Region]` — list
- `DimCustomer[Segment]` — dropdown
- `FactSales[OrderStatus]` — list

## 6.2 Page 2 — Category & Time Analysis

| Visual | Type | Configuration |
|--------|------|---------------|
| YoY matrix | Matrix | Rows `Category`, Columns `DimDate[Year]`, Values `[Total Sales]`, `[Sales PY]`, `[YoY Growth %]` |
| Cumulative sales | Area chart | Axis `DimDate[YearMonth]`, Values `[Sales Cumulative]` |
| Rolling average | Line chart | Axis `DimDate[Date]`, Values `[Total Sales]`, `[Sales 3M Moving Avg]` |
| Monthly YTD | Line and clustered column | Axis `MonthName`, Column `[Total Sales]`, Line `[Sales YTD]` |
| Growth by subcategory | Bar chart | Axis `Subcategory`, Values `[YoY Growth %]` |

Add conditional formatting on the YoY matrix: `[YoY Growth %]` background
green above 0, red below 0.

## 6.3 Formatting

- Canvas 16:9, page background `#F7F9FC`
- One accent colour throughout (`#3366CC`)
- Title text box on each page: `Sales Analysis — Vedant Nimkar (26MML0045)`
- Enable **Drill down** on the category column chart via `Product Hierarchy`
- Add **Edit interactions** so slicers filter, not highlight
- Set **Sort by** `[Total Sales]` descending on all category visuals

## 6.4 Publish

1. **File > Save** as `VisualAnalytics_Sales_26MML0045.pbix`
2. **Home > Publish**
3. Sign in with the college Microsoft 365 account
4. Select destination workspace → **My workspace**
5. Wait for *Success!* then click **Open in Power BI**

### Post-publish tasks

| Task | Where |
|------|-------|
| Set scheduled refresh | Workspace → Dataset → Settings → Scheduled refresh |
| Configure gateway (only if SQL Server source) | Settings → Gateway connection |
| Pin KPI cards to a dashboard | Report → hover visual → Pin icon |
| Share / export | Report → Share, or File → Export to PDF |

### Screenshot checklist for the record

- [ ] Publish dialog showing workspace selection
- [ ] *Success!* confirmation with the report link
- [ ] Report rendered in the browser at app.powerbi.com
- [ ] Dataset settings page showing scheduled refresh configured

## 6.5 Expected values on Page 1 (unfiltered)

| KPI | Value |
|-----|-------|
| Total Sales | 8,955,541.25 |
| Total Quantity | 22,448 |
| Total Profit | 4,831,999.25 |
| Profit Margin % | 53.96% |
| Order Count | 5,008 |

If your cards match these, the whole pipeline from Step 2 through Step 5 is
correct.
