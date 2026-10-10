# Applied DAX — extracted from the semantic model

Every expression below was read directly out of the applied model (`Visual1.SemanticModel/definition/tables/*.tmdl`), so it is the code actually running in the report — not a separately maintained listing.

| Object type | Count |
|---|---|
| Tables | 7 |
| Calculated columns | 6 |
| Measures | 51 |
| Calculated tables | 2 |

## Calculated columns

### DimDate

```dax
Financial Year =
    "FY " & IF ( DimDate[MonthNo] >= 4, DimDate[Year],
                    DimDate[Year] - 1 )
           & "-" & RIGHT ( IF ( DimDate[MonthNo] >= 4,
                    DimDate[Year] + 1, DimDate[Year] ), 2 )

```

### DimProduct

```dax
Price Tier =
    SWITCH ( TRUE (),
        DimProduct[ListPrice] < 100, "Budget",
        DimProduct[ListPrice] < 500, "Mid-range",
        "Premium" )

```

### FactSales

```dax
Net Unit Price =
    DIVIDE ( FactSales[SalesAmount], FactSales[OrderQuantity] )

Line Margin % =
    DIVIDE ( FactSales[SalesAmount] - FactSales[TotalCost],
             FactSales[SalesAmount] )

Order Size Band =
    SWITCH ( TRUE (),
        FactSales[OrderQuantity] <= 2, "1-2 units",
        FactSales[OrderQuantity] <= 4, "3-4 units",
        FactSales[OrderQuantity] <= 6, "5-6 units",
        "7+ units" )

Product Category =
    RELATED ( DimProduct[Category] )

```

## Measures

### 01 Sales

```dax
Total Sales =
    SUM ( FactSales[SalesAmount] )

Total Quantity =
    SUM ( FactSales[OrderQuantity] )

Order Count =
    DISTINCTCOUNT ( FactSales[SalesOrderNumber] )

Average Order Value =
    DIVIDE ( [Total Sales], [Order Count] )

Average Line Sales =
    AVERAGE ( FactSales[SalesAmount] )

Average Selling Price =
    DIVIDE ( [Total Sales], [Total Quantity] )

Customer Count =
    DISTINCTCOUNT ( FactSales[CustomerKey] )

Product Count =
    DISTINCTCOUNT ( FactSales[ProductKey] )

```

### 02 Profit

```dax
Total Cost =
    SUM ( FactSales[TotalCost] )

Total Profit =
    [Total Sales] - [Total Cost]

Profit Margin % =
    DIVIDE ( [Total Profit], [Total Sales] )

```

### 03 Ranking

```dax
Top Product by Units =
    VAR TopProduct =
        TOPN ( 1, ALL ( DimProduct[ProductName] ),
               CALCULATE ( [Total Quantity] ), DESC )
    RETURN
        CONCATENATEX ( TopProduct, DimProduct[ProductName], ", " )

Top Product Units =
    MAXX ( ALL ( DimProduct[ProductName] ),
           CALCULATE ( [Total Quantity] ) )

Top Product by Revenue =
    VAR TopProduct =
        TOPN ( 1, ALL ( DimProduct[ProductName] ),
               CALCULATE ( [Total Sales] ), DESC )
    RETURN
        CONCATENATEX ( TopProduct, DimProduct[ProductName], ", " )

Product Rank by Units =
    RANKX ( ALL ( DimProduct[ProductName] ), [Total Quantity], ,
            DESC, DENSE )

```

### 04 Category

```dax
Avg Sales per Line =
    AVERAGE ( FactSales[SalesAmount] )

Avg Sales per Order =
    DIVIDE ( [Total Sales],
             DISTINCTCOUNT ( FactSales[SalesOrderNumber] ) )

Avg Sales per Category =
    AVERAGEX ( VALUES ( DimProduct[Category] ), [Total Sales] )

Category Share % =
    DIVIDE ( [Total Sales],
             CALCULATE ( [Total Sales], ALL ( DimProduct ) ) )

```

### 05 CALCULATE

```dax
Electronics Sales =
    CALCULATE ( [Total Sales], DimProduct[Category] = "Electronics" )

Shipped Sales =
    CALCULATE ( [Total Sales], FactSales[OrderStatus] = "Shipped" )

Discounted Sales =
    CALCULATE ( [Total Sales], FactSales[DiscountPct] > 0 )

Sales All Products =
    CALCULATE ( [Total Sales], ALL ( DimProduct ) )

Pct of Total Sales =
    DIVIDE ( [Total Sales],
             CALCULATE ( [Total Sales], ALL ( DimProduct ),
                                        ALL ( DimTerritory ) ) )

Category Revenue =
    CALCULATE ( [Total Sales],
                ALLEXCEPT ( DimProduct, DimProduct[Category] ) )

Pct of Category Sales =
    DIVIDE ( [Total Sales],
             CALCULATE ( [Total Sales],
                 ALLEXCEPT ( DimProduct, DimProduct[Category] ) ) )

Pct of Selected Sales =
    DIVIDE ( [Total Sales],
             CALCULATE ( [Total Sales],
                 ALLSELECTED ( DimProduct[Category] ) ) )

Sales 2025 Override =
    CALCULATE ( [Total Sales], DimDate[Year] = 2025 )

Sales 2025 KeepFilters =
    CALCULATE ( [Total Sales],
                KEEPFILTERS ( DimDate[Year] = 2025 ) )

Laptops or Mobiles Sales =
    CALCULATE ( [Total Sales],
        FILTER ( ALL ( DimProduct[Subcategory] ),
                 DimProduct[Subcategory] = "Laptops"
              || DimProduct[Subcategory] = "Mobiles" ) )

Sales by Customer Territory =
    CALCULATE ( [Total Sales],
        USERELATIONSHIP ( DimCustomer[TerritoryKey],
                          DimTerritory[TerritoryKey] ) )

```

### 06 Time

```dax
Sales YTD =
    TOTALYTD ( [Total Sales], DimDate[Date] )

Sales QTD =
    TOTALQTD ( [Total Sales], DimDate[Date] )

Sales MTD =
    TOTALMTD ( [Total Sales], DimDate[Date] )

Sales FYTD =
    TOTALYTD ( [Total Sales], DimDate[Date], "31/03" )

Sales PY =
    CALCULATE ( [Total Sales],
                SAMEPERIODLASTYEAR ( DimDate[Date] ) )

Sales PM =
    CALCULATE ( [Total Sales],
                DATEADD ( DimDate[Date], -1, MONTH ) )

Sales PQ =
    CALCULATE ( [Total Sales],
                DATEADD ( DimDate[Date], -1, QUARTER ) )

Sales PY YTD =
    CALCULATE ( [Sales YTD],
                SAMEPERIODLASTYEAR ( DimDate[Date] ) )

YoY Growth =
    VAR Cur = [Total Sales]
    VAR Prev = [Sales PY]
    RETURN
        IF ( NOT ISBLANK ( Prev ), Cur - Prev )

YoY Growth % =
    DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )

MoM Growth % =
    DIVIDE ( [Total Sales] - [Sales PM], [Sales PM] )

YoY Trend =
    VAR G = [YoY Growth %]
    RETURN
        SWITCH ( TRUE (),
            ISBLANK ( G ), "No prior year",
            G > 0.10,      "Strong growth",
            G > 0,         "Growing",
            G > -0.10,     "Slight decline",
            "Sharp decline" )

Sales Rolling 3M =
    CALCULATE ( [Total Sales],
        DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ),
                        -3, MONTH ) )

Sales Rolling 12M =
    CALCULATE ( [Total Sales],
        DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ),
                        -12, MONTH ) )

Sales Cumulative =
    CALCULATE ( [Total Sales],
        FILTER ( ALLSELECTED ( DimDate[Date] ),
                 DimDate[Date] <= MAX ( DimDate[Date] ) ) )

Sales 3M Moving Avg =
    AVERAGEX (
        DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ),
                        -3, MONTH ),
        CALCULATE ( [Total Sales] ) )

Category Revenue PY =
    CALCULATE ( [Total Sales],
        ALLEXCEPT ( DimProduct, DimProduct[Category] ),
        SAMEPERIODLASTYEAR ( DimDate[Date] ) )

Electronics YoY % =
    VAR Cur =
        CALCULATE ( [Total Sales],
                    DimProduct[Category] = "Electronics" )
    VAR Prev =
        CALCULATE ( [Total Sales],
                    DimProduct[Category] = "Electronics",
                    SAMEPERIODLASTYEAR ( DimDate[Date] ) )
    RETURN
        DIVIDE ( Cur - Prev, Prev )

Best Month Sales =
    MAXX ( VALUES ( DimDate[YearMonth] ),
           CALCULATE ( [Total Sales] ) )

Best Month Name =
    VAR T = TOPN ( 1, VALUES ( DimDate[YearMonth] ),
                   CALCULATE ( [Total Sales] ), DESC )
    RETURN
        CONCATENATEX ( T, DimDate[YearMonth], ", " )

```

## Calculated tables

### Product Category Summary

```dax
Product Category Summary =
    SUMMARIZE (
        FactSales,
        DimProduct[Category],
        "Total Sales",         [Total Sales],
        "Total Quantity",      [Total Quantity],
        "Order Count",         [Order Count],
        "Avg Sales per Order", [Avg Sales per Order]
    )
```

### Top 5 Products

```dax
Top 5 Products =
    TOPN (
        5,
        SUMMARIZE (
            FactSales,
            DimProduct[ProductName],
            DimProduct[Category],
            "Units Sold", [Total Quantity],
            "Revenue",    [Total Sales]
        ),
        [Units Sold], DESC
    )
```

## Relationships

| Name | From | To | Active |
|---|---|---|---|
| `rel_Date_Fact` | `FactSales.DateKey` | `DimDate.DateKey` | Yes |
| `rel_Product_Fact` | `FactSales.ProductKey` | `DimProduct.ProductKey` | Yes |
| `rel_Customer_Fact` | `FactSales.CustomerKey` | `DimCustomer.CustomerKey` | Yes |
| `rel_Territory_Fact` | `FactSales.TerritoryKey` | `DimTerritory.TerritoryKey` | Yes |
| `rel_Territory_Customer` | `DimCustomer.TerritoryKey` | `DimTerritory.TerritoryKey` | No |
