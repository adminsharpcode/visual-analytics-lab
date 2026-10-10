# Minimum DAX set for QP1 + QP2

The full library in `Step4_DAX_Calculated.txt` and `Step5_DAX_Advanced.txt` has
51 measures. The question papers only require the 14 below, plus 2 calculated
columns and 2 calculated tables.

Paste in this exact order — later items reference earlier ones.

**Desktop:** `Table tools → New measure`, paste, press Enter, repeat.
About 15 seconds each, so roughly 5 minutes for the whole set.

---

## A. Calculated columns (2)

`Table tools → New column` on **FactSales**

```
1.  Line Margin % = DIVIDE ( FactSales[SalesAmount] - FactSales[TotalCost], FactSales[SalesAmount] )
```

```
2.  Order Size Band = SWITCH ( TRUE (), FactSales[OrderQuantity] <= 2, "1-2 units", FactSales[OrderQuantity] <= 4, "3-4 units", FactSales[OrderQuantity] <= 6, "5-6 units", "7+ units" )
```

---

## B. Core measures (7) — QP2 Step 4

`Table tools → New measure` on **FactSales**

```
3.  Total Sales = SUM ( FactSales[SalesAmount] )
```
```
4.  Total Quantity = SUM ( FactSales[OrderQuantity] )
```
```
5.  Total Cost = SUM ( FactSales[TotalCost] )
```
```
6.  Total Profit = [Total Sales] - [Total Cost]
```
```
7.  Profit Margin % = DIVIDE ( [Total Profit], [Total Sales] )
```
```
8.  Order Count = DISTINCTCOUNT ( FactSales[SalesOrderNumber] )
```
```
9.  Avg Sales per Order = DIVIDE ( [Total Sales], [Order Count] )
```

**Check now, before going further.** Drop these into cards:

| Measure | Must show |
|---|---|
| Total Sales | 8,955,541.25 |
| Total Quantity | 22,448 |
| Total Cost | 4,123,542.00 |
| Total Profit | 4,831,999.25 |
| Profit Margin % | 53.96% |
| Order Count | 5,008 |
| Avg Sales per Order | 1,788.25 |

If these match, the QP1 cleansing was done correctly. If not, stop and fix
the Power Query steps first.

---

## C. Top sold product (2) — QP2 Step 4 question 1

```
10. Top Product by Units = CONCATENATEX ( TOPN ( 1, ALL ( DimProduct[ProductName] ), CALCULATE ( [Total Quantity] ), DESC ), DimProduct[ProductName], ", " )
```
```
11. Product Rank by Units = RANKX ( ALL ( DimProduct[ProductName] ), [Total Quantity], , DESC, DENSE )
```

Expected: **GlideMouse Wireless**, 3,204 units.

---

## D. CALCULATE — filter context (2) — QP2 Step 5

```
12. Category Revenue = CALCULATE ( [Total Sales], ALLEXCEPT ( DimProduct, DimProduct[Category] ) )
```
```
13. Pct of Total Sales = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( DimProduct ) ) )
```

Expected by category:

| Category | Category Revenue | Pct of Total |
|---|---|---|
| Electronics | 7,081,992.08 | 79.08% |
| Furniture | 861,784.14 | 9.62% |
| Accessories | 786,667.35 | 8.78% |
| Software | 225,097.68 | 2.51% |

---

## E. Time Intelligence (3) — QP2 Step 5

**`DimDate` must be marked as a date table first**
(`Table tools → Mark as date table → Date`). Without it these return wrong
numbers silently.

```
14. Sales YTD = TOTALYTD ( [Total Sales], DimDate[Date] )
```
```
15. Sales PY = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
```
```
16. YoY Growth % = DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )
```

Expected YoY Growth % with `Category` on rows, `Year` on columns:

| Category | 2024 | 2025 |
|---|---|---|
| Accessories | +23.13% | +16.74% |
| Electronics | +8.67% | +0.34% |
| Furniture | +32.43% | +26.74% |
| Software | −1.13% | +66.45% |
| **Overall** | **+11.46%** | **+5.59%** |

---

## F. Calculated tables (2) — QP2 Step 4

`Modeling → New table`

```
17. Product Category Summary = SUMMARIZE ( FactSales, DimProduct[Category], "Total Sales", [Total Sales], "Total Quantity", [Total Quantity], "Order Count", [Order Count], "Avg Sales per Order", [Avg Sales per Order] )
```

```
18. Top 5 Products = TOPN ( 5, SUMMARIZE ( FactSales, DimProduct[ProductName], "Units Sold", [Total Quantity], "Revenue", [Total Sales] ), [Units Sold], DESC )
```

---

## Formatting pass (1 minute)

Select the measures and set:

| Measures | Format |
|---|---|
| Total Sales, Total Cost, Total Profit, Avg Sales per Order, Category Revenue, Sales YTD, Sales PY | Currency, 2 dp |
| Profit Margin %, Pct of Total Sales, YoY Growth %, Line Margin % | Percentage, 2 dp |
| Total Quantity, Order Count, Product Rank by Units | Whole number, thousands separator |

---

## Coverage against the question papers

| Requirement | Covered by |
|---|---|
| QP2.4 calculated columns | A1, A2 |
| QP2.4 measures | B3–B9 |
| QP2.4 calculated tables | F17, F18 |
| QP2.4 "top sold product" | C10, C11 |
| QP2.4 "average sales of product category" | B9 + F17 |
| QP2.5 `CALCULATE()` filter context | D12, D13 |
| QP2.5 "total sales revenue per category" | D12 |
| QP2.5 Time Intelligence | E14, E15 |
| QP2.5 "YoY growth trend of a category" | E16 |

Everything in the papers is satisfied. The other 37 measures are optional
extras — add them only if you want the record to look fuller.
