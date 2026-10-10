let
    // 1. CONNECT ------------------------------------------------------------
    Source = Csv.Document(
        File.Contents("C:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP1_QP2\data\FactSales_RAW.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // 2. REMOVE the always-blank column -------------------------------------
    RemovedBlankCol = Table.RemoveColumns(Promoted, {"Notes"}),

    // 3. REMOVE duplicate rows ----------------------------------------------
    RemovedDuplicates = Table.Distinct(RemovedBlankCol),

    // 4. PARSE the mixed-format text date into a real date -------------------
    //    Source has yyyy-MM-dd, dd-MM-yyyy and dd/MM/yyyy mixed together.
    AddedOrderDate = Table.AddColumn(RemovedDuplicates, "OrderDate",
        each let t = Text.Replace([OrderDateText], "/", "-"),
                 p = Text.Split(t, "-")
             in  if Text.Length(p{0}) = 4
                 then #date(Number.FromText(p{0}), Number.FromText(p{1}),
                            Number.FromText(p{2}))
                 else #date(Number.FromText(p{2}), Number.FromText(p{1}),
                            Number.FromText(p{0})),
        type date),

    // 5. STRIP the currency text into a decimal ------------------------------
    AddedUnitPrice = Table.AddColumn(AddedOrderDate, "UnitPrice",
        each Number.FromText(
            Text.Trim(Text.Replace(Text.Replace([UnitPriceText], "Rs.", ""),
                                   ",", ""))),
        type number),

    // 6. CLEAN the messy status text (trim + consistent casing) --------------
    CleanedStatus = Table.TransformColumns(AddedUnitPrice,
        {{"OrderStatus", each Text.Proper(Text.Trim(_)), type text}}),

    // 7. SET data types ------------------------------------------------------
    Typed = Table.TransformColumnTypes(CleanedStatus, {
        {"SalesOrderNumber", type text},
        {"ProductKey", Int64.Type},
        {"CustomerKey", Int64.Type},
        {"TerritoryKey", Int64.Type},
        {"OrderQuantity", Int64.Type},
        {"DiscountPct", type number},
        {"SalesAmount", type number},
        {"TotalCost", type number}}),

    // 8. REMOVE rows with a missing quantity ---------------------------------
    RemovedNullQty = Table.SelectRows(Typed,
        each [OrderQuantity] <> null),

    // 9. REMOVE negative-quantity data-entry errors --------------------------
    RemovedNegative = Table.SelectRows(RemovedNullQty,
        each [OrderQuantity] > 0),

    // 10. FILL the missing SalesAmount from price x qty x (1 - discount) -----
    FixedSalesAmount = Table.ReplaceValue(RemovedNegative,
        each [SalesAmount],
        each if [SalesAmount] = null
             then Number.Round([UnitPrice] * [OrderQuantity]
                               * (1 - [DiscountPct]), 2)
             else [SalesAmount],
        Replacer.ReplaceValue, {"SalesAmount"}),

    // 11. EXCLUDE cancelled orders from the sales analysis --------------------
    RemovedCancelled = Table.SelectRows(FixedSalesAmount,
        each [OrderStatus] <> "Cancelled"),

    // 12. ADD a Profit column ------------------------------------------------
    AddedProfit = Table.AddColumn(RemovedCancelled, "Profit",
        each [SalesAmount] - [TotalCost], type number),

    // 13. ADD the DateKey used to join DimDate -------------------------------
    AddedDateKey = Table.AddColumn(AddedProfit, "DateKey",
        each Date.Year([OrderDate]) * 10000
           + Date.Month([OrderDate]) * 100
           + Date.Day([OrderDate]), Int64.Type),

    // 14. DROP the now-redundant raw text columns ----------------------------
    RemovedRawText = Table.RemoveColumns(AddedDateKey,
        {"OrderDateText", "UnitPriceText"}),

    // 15. REORDER for readability --------------------------------------------
    Reordered = Table.ReorderColumns(RemovedRawText, {
        "SalesOrderNumber", "OrderDate", "DateKey", "ProductKey",
        "CustomerKey", "TerritoryKey", "OrderQuantity", "UnitPrice",
        "DiscountPct", "SalesAmount", "TotalCost", "Profit", "OrderStatus"})
in
    Reordered
