# Power BI Dashboard Implementation & Build Guide
**Smart Energy Consumption Visualization Dashboard**  
*Course:* MACSE603 - Visual Analytics Lab  
*Team:* Vedant Nimkar (`26MML0045`), Jitesh Bobde (`26MML0025`), Ayush Sharma (`26MML0043`)

---

## 1. Quick Start: Loading Data into Power BI Desktop
1. Open **Power BI Desktop**.
2. Click **Home > Get Data > Folder** (or **Text/CSV**).
3. Browse to the project data directory:
   `c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Project_SmartEnergy_PowerBI\data`
4. Load the 11 Star-Schema tables:
   - `Dim_Facility.csv`
   - `Dim_Tariff.csv`
   - `Dim_Appliance.csv`
   - `Dim_Time.csv`
   - `Dim_Date.csv`
   - `Dim_Weather.csv`
   - `Fact_EnergyConsumption.csv`
   - `Fact_ApplianceSubmeter.csv`
   - `Fact_DemandForecast.csv`
   - `Fact_Anomalies_Detailed.csv`
   - `Fact_LoadClusters.csv`

---

## 2. Configuring Relational Relationships (Model View)
Verify the following 1-to-Many (`1:*`) Single Cross-Filter relationships in the Model View:
- `Dim_Facility[FacilityID]` `1 ---> *` `Fact_EnergyConsumption[FacilityID]`
- `Dim_Tariff[TariffID]` `1 ---> *` `Fact_EnergyConsumption[TariffID]`
- `Dim_Date[Date]` `1 ---> *` `Fact_EnergyConsumption[Date]`
- `Dim_Time[Hour]` `1 ---> *` `Fact_EnergyConsumption[Hour]`
- `Dim_Appliance[ApplianceID]` `1 ---> *` `Fact_ApplianceSubmeter[ApplianceID]`
- `Dim_Facility[FacilityID]` `1 ---> *` `Fact_ApplianceSubmeter[FacilityID]`
- `Dim_Facility[FacilityID]` `1 ---> *` `Fact_Anomalies_Detailed[FacilityID]`
- `Dim_Facility[FacilityID]` `1 ---> *` `Fact_LoadClusters[FacilityID]`

---

## 3. Creating DAX Measures
1. Create a dedicated measure table called `_DAX_Measures`.
2. Copy and paste the DAX formulas from `DAX_Measures_Library.md`.
3. Essential measures to add first:
   - `Total Active Energy (GWh)`
   - `Total Electricity Spend (Crores INR)`
   - `Total Solar Generation (GWh)`
   - `Solar Penetration %`
   - `Campus Coincident Peak (kW)`
   - `Carbon Footprint (Tonnes CO2)`
   - `Energy MoM Growth %`
   - `Shewhart Upper Limit (kWh)`

---

## 4. Visual Layout (Page by Page)

### Page 1: Executive Overview & KPI Summary
- **Top Slicers:** Facility Selector (`Dim_Facility[FacilityName]`), Date Hierarchy Slicer (`Dim_Date[Year]`, `Month`), Tariff Band (`Dim_Time[TariffBand]`).
- **KPI Card Row:** 6 Multi-row Cards for Active Energy (GWh), Cost (Cr), Solar (GWh), Peak Demand (kW), Carbon (tCO2e), Anomalies.
- **Visual 1 (Area & Line):** Diurnal Power Flow (`Hour` on X, `Total Active Energy`, `Solar Generation`, `Net Grid Import` on Y).
- **Visual 2 (Horizontal Bar):** Top-N Facility Ranking with data bars.

### Page 2: 24x7 Load Profile Matrix
- **Matrix Visual:**
  - Rows: `Dim_Date[DayName]` (sorted by `DayOfWeek`).
  - Columns: `Dim_Time[HourFormatted]` (00:00 to 23:00).
  - Values: `[Average Active Power (kW)]`.
  - Conditional Formatting: Background color gradient (Deep Blue `#0b1a3a` to Electric Blue `#38bdf8` to Crimson `#ef4444`).

### Page 3: Machine Learning Demand Forecast
- **Line & Area Chart:**
  - X-Axis: `Fact_DemandForecast[Date]`.
  - Line 1: `Fact_DemandForecast[Actual_kWh]`.
  - Line 2: `Fact_DemandForecast[Forecast_kWh]`.
  - Shaded Area: Upper 95% and Lower 95% Confidence Bounds.

### Page 4: Automated Anomaly Detection & Control Limits
- **Line & Scatter Chart:**
  - X-Axis: `Timestamp`.
  - Line 1: `ActivePower_kWh`.
  - Line 2: `Rolling Baseline (kWh)`.
  - Shaded Area: Shewhart Upper Limit and Lower Limit band.
  - Scatter: Anomaly Breaches marked in Red.

### Page 5: Appliance Submetering & Decarbonization
- **Donut Chart:** Submeter categories (`HVAC`, `IT`, `Lighting`, `Motors`, `Auxiliary`).
- **Decomposition Tree:** Total Spend broken down by Facility -> Tariff Band -> Appliance.
