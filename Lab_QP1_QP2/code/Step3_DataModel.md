# QP1 Step 3 - Designing the Data Model in Power BI

Star schema: one fact table, four dimensions.

## 3.1 Model Relationships

Create these in **Model view** by dragging the field from the dimension onto
the matching field in `FactSales`.

| # | From (one side) | To (many side) | Cardinality | Cross-filter | Active |
|---|-----------------|----------------|-------------|--------------|--------|
| 1 | `DimDate[DateKey]` | `FactSales[DateKey]` | One-to-many | Single | Yes |
| 2 | `DimProduct[ProductKey]` | `FactSales[ProductKey]` | One-to-many | Single | Yes |
| 3 | `DimCustomer[CustomerKey]` | `FactSales[CustomerKey]` | One-to-many | Single | Yes |
| 4 | `DimTerritory[TerritoryKey]` | `FactSales[TerritoryKey]` | One-to-many | Single | Yes |
| 5 | `DimTerritory[TerritoryKey]` | `DimCustomer[TerritoryKey]` | One-to-many | Single | **No** (inactive - avoids ambiguity) |

> Relationship 5 must be set **inactive**. Both `FactSales` and `DimCustomer`
> carry `TerritoryKey`, which creates two paths to `DimTerritory`. Power BI
> will refuse two active paths. Keep the direct fact relationship active.

### Mark the date table

Select `DimDate` -> ribbon **Table tools** -> **Mark as date table** ->
choose the `Date` column.

This is mandatory before any Time Intelligence function in Step 5 will behave
correctly.

## 3.2 Table and Column Properties

Set these in the **Data** or **Model** view via the Properties pane.

### FactSales

| Column | Data type | Format | Summarisation | Hidden |
|--------|-----------|--------|---------------|--------|
| `SalesOrderNumber` | Text | - | Do not summarize | No |
| `OrderDate` | Date | dd mmm yyyy | Do not summarize | No |
| `DateKey` | Whole number | - | Do not summarize | **Yes** |
| `ProductKey` | Whole number | - | Do not summarize | **Yes** |
| `CustomerKey` | Whole number | - | Do not summarize | **Yes** |
| `TerritoryKey` | Whole number | - | Do not summarize | **Yes** |
| `OrderQuantity` | Whole number | #,##0 | Sum | No |
| `UnitPrice` | Decimal | Currency, 2 dp | Do not summarize | No |
| `DiscountPct` | Decimal | Percentage, 0 dp | Average | No |
| `SalesAmount` | Decimal | Currency, 2 dp | Sum | No |
| `TotalCost` | Decimal | Currency, 2 dp | Sum | No |
| `Profit` | Decimal | Currency, 2 dp | Sum | No |
| `OrderStatus` | Text | - | Do not summarize | No |

Hiding the surrogate keys is the point of this exercise: report authors should
use the descriptive dimension attributes, not raw integers.

### DimProduct

| Column | Setting |
|--------|---------|
| `ProductKey` | Hidden |
| `Category` | Sort by `Category` |
| `Subcategory` | Sort by `Subcategory` |
| `ProductName` | Default field for the table |
| `StandardCost`, `ListPrice`, `UnitMargin` | Currency, 2 dp, Do not summarize |
| `SKU` | Text, Do not summarize |

### DimDate

| Column | Setting |
|--------|---------|
| `DateKey` | Hidden |
| `Date` | Date, dd mmm yyyy |
| `MonthName` | **Sort by column** -> `MonthNo` |
| `MonthShort` | **Sort by column** -> `MonthNo` |
| `Quarter` | **Sort by column** -> `QuarterNo` |
| `DayName` | **Sort by column** -> a day-number column if added |
| `Year`, `MonthNo`, `QuarterNo`, `WeekOfYear` | Do not summarize |

> Setting **Sort by column** on `MonthName` is what stops the x-axis reading
> April, August, December... alphabetically.

### DimCustomer / DimTerritory

| Column | Setting |
|--------|---------|
| `CustomerKey`, `TerritoryKey` | Hidden |
| `CustomerName` | Default field |
| `Segment`, `Region`, `Country`, `Group` | Text, Do not summarize |

## 3.3 Hierarchies

Right-click the top field -> **Create hierarchy**, then drag the remaining
levels in order.

### Product Hierarchy  (on `DimProduct`)
```
Product Hierarchy
├── Category
├── Subcategory
└── ProductName
```

### Date Hierarchy  (on `DimDate`)
```
Date Hierarchy
├── Year
├── Quarter
├── MonthName
└── DayOfMonth
```

### Geography Hierarchy  (on `DimTerritory`)
```
Geography Hierarchy
├── Group
├── Country
└── Region
```

### Customer Hierarchy  (on `DimCustomer`)
```
Customer Hierarchy
├── Segment
└── CustomerName
```

These enable drill-down in the Step 6 visuals: click a Category column in a
chart and it expands to Subcategory, then to individual products.

## 3.4 Verification checklist

- [ ] Model view shows a star, not a snowflake or a web
- [ ] Exactly 4 active relationships + 1 inactive
- [ ] `DimDate` is marked as a date table
- [ ] All `*Key` columns hidden from report view
- [ ] `MonthName` sorts chronologically in a test bar chart
- [ ] All four hierarchies drill down correctly
