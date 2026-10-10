# Applied model structure — extracted from the semantic model

## Relationships

| Name | From (many) | To (one) | Active |
|---|---|---|---|
| `rel_Date_Fact` | `FactSales.DateKey` | `DimDate.DateKey` | Yes |
| `rel_Product_Fact` | `FactSales.ProductKey` | `DimProduct.ProductKey` | Yes |
| `rel_Customer_Fact` | `FactSales.CustomerKey` | `DimCustomer.CustomerKey` | Yes |
| `rel_Territory_Fact` | `FactSales.TerritoryKey` | `DimTerritory.TerritoryKey` | Yes |
| `rel_Territory_Customer` | `DimCustomer.TerritoryKey` | `DimTerritory.TerritoryKey` | **No** |

5 relationships, 1 inactive.

## Date table

`DimDate` carries `dataCategory: Time`, confirming it is marked as the model date table. This is required for the Time Intelligence functions used in Assessment 2.

## Hierarchies

| Table | Hierarchy | Levels |
|---|---|---|
| `DimCustomer` | Customer Hierarchy | Segment → CustomerName |
| `DimDate` | Date Hierarchy | Year → Quarter → MonthName → DayOfMonth |
| `DimProduct` | Product Hierarchy | Category → Subcategory → ProductName |
| `DimTerritory` | Geography Hierarchy | Group → Country → Region |

## Column properties

Only the properties configured in Step 3 are listed: hidden surrogate keys, formatting, summarisation and sort-by-column.

### DimCustomer

| Column | Type | Format | Summarise | Hidden | Sort by |
|---|---|---|---|---|---|
| `CustomerKey` | int64 |  | none | Yes |  |
| `TerritoryKey` | int64 |  | none | Yes |  |

### DimDate

| Column | Type | Format | Summarise | Hidden | Sort by |
|---|---|---|---|---|---|
| `DateKey` | int64 |  | none | Yes |  |
| `Date` | dateTime | dd mmm yyyy | none |  |  |
| `QuarterNo` | int64 |  | none | Yes |  |
| `Quarter` | string |  | none |  | QuarterNo |
| `MonthNo` | int64 |  | none | Yes |  |
| `MonthName` | string |  | none |  | MonthNo |
| `MonthShort` | string |  | none |  | MonthNo |

### DimProduct

| Column | Type | Format | Summarise | Hidden | Sort by |
|---|---|---|---|---|---|
| `ProductKey` | int64 |  | none | Yes |  |
| `StandardCost` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | none |  |  |
| `ListPrice` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | none |  |  |
| `UnitMargin` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | none |  |  |

### DimTerritory

| Column | Type | Format | Summarise | Hidden | Sort by |
|---|---|---|---|---|---|
| `TerritoryKey` | int64 |  | none | Yes |  |

### FactSales

| Column | Type | Format | Summarise | Hidden | Sort by |
|---|---|---|---|---|---|
| `OrderDate` | dateTime | dd mmm yyyy | none |  |  |
| `DateKey` | int64 |  | none | Yes |  |
| `ProductKey` | int64 |  | none | Yes |  |
| `CustomerKey` | int64 |  | none | Yes |  |
| `TerritoryKey` | int64 |  | none | Yes |  |
| `OrderQuantity` | int64 | #,0 | sum |  |  |
| `UnitPrice` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | none |  |  |
| `DiscountPct` | double | 0.00% | average |  |  |
| `SalesAmount` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | sum |  |  |
| `TotalCost` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | sum |  |  |
| `Profit` | double | \$#,0.00;(\$#,0.00);\$#,0.00 | sum |  |  |
