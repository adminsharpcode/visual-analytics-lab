let
    Source = Csv.Document(File.Contents("C:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP1_QP2\data\DimCustomer.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"CustomerKey", Int64.Type}, {"Segment", type text},
        {"TerritoryKey", Int64.Type}, {"CustomerName", type text}})
in
    Typed
