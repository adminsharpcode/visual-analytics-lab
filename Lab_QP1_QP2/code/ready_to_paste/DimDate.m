let
    Source = Csv.Document(File.Contents("C:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP1_QP2\data\DimDate.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"DateKey", Int64.Type}, {"Date", type date}, {"Year", Int64.Type},
        {"QuarterNo", Int64.Type}, {"Quarter", type text},
        {"MonthNo", Int64.Type}, {"MonthName", type text},
        {"MonthShort", type text}, {"YearMonth", type text},
        {"WeekOfYear", Int64.Type}, {"DayOfMonth", Int64.Type},
        {"DayName", type text}, {"IsWeekend", type logical}})
in
    Typed
