let
    Source = Csv.Document(File.Contents("C:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP1_QP2\data\DimProduct.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"ProductKey", Int64.Type}, {"Category", type text},
        {"Subcategory", type text}, {"ProductName", type text},
        {"StandardCost", type number}, {"ListPrice", type number},
        {"SKU", type text}}),
    Trimmed = Table.TransformColumns(Typed, {
        {"Category", Text.Trim, type text},
        {"Subcategory", Text.Trim, type text},
        {"ProductName", Text.Trim, type text}}),
    AddedMargin = Table.AddColumn(Trimmed, "UnitMargin",
        each [ListPrice] - [StandardCost], type number)
in
    AddedMargin
