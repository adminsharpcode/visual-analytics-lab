# Power Query (M) Cleansing & Ingestion Scripts
## Smart Energy Consumption Visualization Dashboard
**Course:** MACSE603 - Visual Analytics Lab  
**Team:** Vedant Nimkar (26MML0045) | Jitesh Bobde (26MML0025) | Ayush Sharma (26MML0043)  

---

### 1. Ingestion Pipeline Overview

The data ingestion pipeline connects to raw CSV telemetry streams extracted from smart meters, IoT gateways (ESP32 via MQTT), building management systems (BMS), and billing databases. Power Query applies the following cleansing operations:
1. **Source Connection & Dynamic Path Resolution:** Uses parameterised source paths for portability.
2. **Type Enforcement & Standardisation:** Explicitly enforces `DateTime.Type`, `Int64.Type`, `type number`, and `type text`.
3. **Data Quality Validations:** Filters negative power values, treats missing records via forward interpolation or rolling means, and standardises unit scales (kWh, kW, kVARh, V).
4. **Enrichment Columns:** Calculates derived fields such as Net Grid Import, Carbon Footprint, and Tariff Band classifications.

---

### 2. M Query: `Fact_EnergyConsumption`

```powerquery
let
    // Step 1: Connect to CSV Source
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Fact_EnergyConsumption.csv"),
        [Delimiter=",", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    
    // Step 2: Promote Headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // Step 3: Change Column Data Types
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"Timestamp", type datetime},
        {"Date", type date},
        {"Hour", Int64.Type},
        {"FacilityID", type text},
        {"TariffID", type text},
        {"ActivePower_kWh", type number},
        {"ReactivePower_kVARh", type number},
        {"PowerFactor", type number},
        {"Voltage_V", type number},
        {"TariffBand", type text},
        {"PeakPeriodFlag", Int64.Type},
        {"SolarGeneration_kWh", type number},
        {"NetGridImport_kWh", type number},
        {"Cost_INR", type number},
        {"CarbonEmission_kgCO2", type number},
        {"AnomalyFlag", Int64.Type},
        {"AnomalyType", type text}
    }),
    
    // Step 4: Quality Gate - Ensure non-negative active power
    #"Filtered Valid Telemetry" = Table.SelectRows(#"Changed Types", each [ActivePower_kWh] >= 0),
    
    // Step 5: Replace null solar generation with zero
    #"Replaced Null Solar" = Table.ReplaceValue(#"Filtered Valid Telemetry", null, 0, Replacer.ReplaceValue, {"SolarGeneration_kWh"}),
    
    // Step 6: Add Apparent Power (kVAh) = sqrt(kW^2 + kVAR^2)
    #"Added Apparent Power" = Table.AddColumn(#"Replaced Null Solar", "ApparentPower_kVAh", each Number.Round(Number.Sqrt(Number.Power([ActivePower_kWh], 2) + Number.Power([ReactivePower_kVARh], 2)), 2), type number)
in
    #"Added Apparent Power"
```

---

### 3. M Query: `Dim_Facility`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Dim_Facility.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"FacilityID", type text},
        {"FacilityName", type text},
        {"Category", type text},
        {"Area_SqFt", Int64.Type},
        {"Occupancy_Capacity", Int64.Type},
        {"Baseline_kW", type number},
        {"PeakDesign_kW", type number},
        {"EnergyStarRating", Int64.Type},
        {"SubstationZone", type text},
        {"Solar_kWp", type number}
    }),
    // Add Building Size Tier
    #"Added Size Tier" = Table.AddColumn(#"Changed Types", "SizeTier", each 
        if [Area_SqFt] >= 150000 then "Large Campus Facility"
        else if [Area_SqFt] >= 80000 then "Medium Facility"
        else "Specialized Wing", type text)
in
    #"Added Size Tier"
```

---

### 4. M Query: `Dim_Date`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Dim_Date.csv"),
        [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"Date", type date},
        {"Year", Int64.Type},
        {"Quarter", type text},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"WeekNum", Int64.Type},
        {"DayOfMonth", Int64.Type},
        {"DayOfWeek", Int64.Type},
        {"DayName", type text},
        {"IsWeekend", Int64.Type},
        {"Season", type text}
    }),
    // Add YearMonth Sort Key (e.g. 202501)
    #"Added YearMonthKey" = Table.AddColumn(#"Changed Types", "YearMonthKey", each [Year] * 100 + [Month], Int64.Type)
in
    #"Added YearMonthKey"
```

---

### 5. M Query: `Dim_Time`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Dim_Time.csv"),
        [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"Hour", Int64.Type},
        {"HourFormatted", type text},
        {"Hour12", type text},
        {"PeriodOfDay", type text},
        {"TariffBand", type text},
        {"PeakTariffFlag", Int64.Type}
    })
in
    #"Changed Types"
```

---

### 6. M Query: `Dim_Tariff`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Dim_Tariff.csv"),
        [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"TariffID", type text},
        {"TariffName", type text},
        {"Category", type text},
        {"PeakRate_INR", type number},
        {"ShoulderRate_INR", type number},
        {"OffPeakRate_INR", type number},
        {"DemandCharge_INR_kW", type number},
        {"CarbonFactor_kgCO2_kWh", type number}
    })
in
    #"Changed Types"
```

---

### 7. M Query: `Dim_Weather`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Dim_Weather.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"Date", type date},
        {"Hour", Int64.Type},
        {"AmbientTemp_C", type number},
        {"Humidity_Pct", type number},
        {"SolarIrradiance_W_m2", type number},
        {"CoolingDegreeHours", type number},
        {"HeatingDegreeHours", type number}
    })
in
    #"Changed Types"
```

---

### 8. M Query: `Fact_DemandForecast`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Fact_DemandForecast.csv"),
        [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"Date", type date},
        {"Forecast_kWh", type number},
        {"Lower_95_CI", type number},
        {"Upper_95_CI", type number},
        {"IsHistorical", Int64.Type}
    })
in
    #"Changed Types"
```

---

### 9. M Query: `Fact_LoadClusters`

```powerquery
let
    Source = Csv.Document(
        File.Contents(#"DataFolderPath" & "Fact_LoadClusters.csv"),
        [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"FacilityID", type text},
        {"Date", type date},
        {"ClusterID", Int64.Type},
        {"ClusterArchetype", type text},
        {"tSNE_Dim1", type number},
        {"tSNE_Dim2", type number}
    })
in
    #"Changed Types"
```
