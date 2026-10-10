let
    Source = Csv.Document(File.Contents("C:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP1_QP2\data\DimTerritory.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"TerritoryKey", Int64.Type}, {"Region", type text},
        {"Country", type text}, {"Group", type text}})
in
    Typed
