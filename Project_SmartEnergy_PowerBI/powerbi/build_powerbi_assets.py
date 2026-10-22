"""
EnergyPulse BI - Power BI Dashboard Generator
Builds production-ready Power BI assets:
  1. SmartEnergy_Analytics_Dashboard.pbip (Power BI Project with PBIR + TMDL/BIM)
  2. SmartEnergy_Analytics_Dashboard.pbit (Power BI Template with DataModelSchema + Report Layout)
  3. SmartEnergy_Analytics_Dashboard.pbix (Complete Power BI Report Package)

Author: Vedant Nimkar (Lead), Jitesh Bobde, Ayush Sharma
Course: MACSE603 - Visual Analytics Lab
"""
import os
import json
import zipfile
import hashlib
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data").replace("\\", "/")
POWERBI_DIR = os.path.join(BASE_DIR, "powerbi")
ROOT_DIR = os.path.dirname(BASE_DIR)
os.makedirs(POWERBI_DIR, exist_ok=True)

MODEL_NAME = "SmartEnergy_Analytics_Model"

# Number and Currency Format Strings
CUR_INR = "\\₹#,0.00;(\\₹#,0.00);\\₹#,0.00"
NUM_INT = "#,0"
NUM_DEC = "#,0.00"
PCT_FMT = "0.0%"

def u16(text):
    """Power BI package text files require UTF-16 LE without BOM."""
    return text.encode("utf-16le")


def jdump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)

def col(name, dtype, source=None, fmt=None, summarize="none", hidden=False, sort_by=None, is_key=False):
    c = {"name": name, "dataType": dtype, "sourceColumn": source or name, "summarizeBy": summarize}
    if fmt: c["formatString"] = fmt
    if hidden: c["isHidden"] = True
    if sort_by: c["sortByColumn"] = sort_by
    if is_key: c["isKey"] = True
    return c

def calc_col(name, expr, fmt=None, summarize="none"):
    c = {"name": name, "type": "calculated", "isDataTypeInferred": True, "expression": expr, "summarizeBy": summarize}
    if fmt: c["formatString"] = fmt
    return c

def measure(name, expr, fmt=None, folder=None, desc=None):
    m = {"name": name, "expression": expr}
    if fmt: m["formatString"] = fmt
    if folder: m["displayFolder"] = folder
    if desc: m["description"] = desc
    return m

# =========================================================================
# 1. Power Query M Expressions
# =========================================================================
def make_csv_m_expr(filename, types):
    type_transforms = ", ".join([f'{{"{col_name}", {col_type}}}' for col_name, col_type in types])
    return [
        'let',
        f'    Source = Csv.Document(File.Contents("{DATA_DIR}/{filename}"), [Delimiter=",", Columns={len(types)}, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        f'    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{{type_transforms}}})',
        'in',
        '    #"Changed Type"'
    ]

# M Query Definitions for 11 Tables
m_queries = {
    "Fact_EnergyConsumption": make_csv_m_expr("Fact_EnergyConsumption.csv", [
        ("Timestamp", "type datetime"), ("Date", "type date"), ("Hour", "Int64.Type"),
        ("FacilityID", "type text"), ("TariffID", "type text"), ("ActivePower_kWh", "type number"),
        ("ReactivePower_kVARh", "type number"), ("PowerFactor", "type number"), ("Voltage_V", "type number"),
        ("TariffBand", "type text"), ("PeakPeriodFlag", "Int64.Type"), ("SolarGeneration_kWh", "type number"),
        ("NetGridImport_kWh", "type number"), ("Cost_INR", "type number"), ("CarbonEmission_kgCO2", "type number"),
        ("AnomalyFlag", "Int64.Type"), ("AnomalyType", "type text"), ("Carbon_kgCO2", "type number"),
        ("NetImport_kWh", "type number"), ("SolarSelfConsumptionRatio", "type number")
    ]),
    "Dim_Facility": make_csv_m_expr("Dim_Facility.csv", [
        ("FacilityID", "type text"), ("FacilityName", "type text"), ("Category", "type text"),
        ("Area_SqFt", "Int64.Type"), ("Occupancy_Capacity", "Int64.Type"), ("Baseline_kW", "type number"),
        ("PeakDesign_kW", "type number"), ("EnergyStarRating", "Int64.Type"), ("SubstationZone", "type text"),
        ("Solar_kWp", "type number")
    ]),
    "Dim_Date": make_csv_m_expr("Dim_Date.csv", [
        ("Date", "type date"), ("Year", "Int64.Type"), ("Quarter", "Int64.Type"),
        ("Month", "Int64.Type"), ("MonthName", "type text"), ("WeekNum", "Int64.Type"),
        ("DayOfMonth", "Int64.Type"), ("DayOfWeek", "Int64.Type"), ("DayName", "type text"),
        ("IsWeekend", "type logical"), ("Season", "type text")
    ]),
    "Dim_Time": make_csv_m_expr("Dim_Time.csv", [
        ("Hour", "Int64.Type"), ("HourFormatted", "type text"), ("Hour12", "type text"),
        ("PeriodOfDay", "type text"), ("TariffBand", "type text"), ("PeakTariffFlag", "Int64.Type")
    ]),
    "Dim_Tariff": make_csv_m_expr("Dim_Tariff.csv", [
        ("TariffID", "type text"), ("TariffName", "type text"), ("Category", "type text"),
        ("PeakRate_INR", "type number"), ("ShoulderRate_INR", "type number"), ("OffPeakRate_INR", "type number"),
        ("DemandCharge_INR_kW", "type number"), ("CarbonFactor_kgCO2_kWh", "type number")
    ]),
    "Dim_Weather": make_csv_m_expr("Dim_Weather.csv", [
        ("Date", "type date"), ("Hour", "Int64.Type"), ("AmbientTemp_C", "type number"),
        ("Humidity_Pct", "type number"), ("SolarIrradiance_W_m2", "type number"),
        ("CoolingDegreeHours", "type number"), ("HeatingDegreeHours", "type number")
    ]),
    "Dim_Appliance": make_csv_m_expr("Dim_Appliance.csv", [
        ("ApplianceID", "type text"), ("SubmeterCategory", "type text"),
        ("Description", "type text"), ("AvgShare_Pct", "type number")
    ]),
    "Fact_DemandForecast": make_csv_m_expr("Fact_DemandForecast.csv", [
        ("Date", "type date"), ("Type", "type text"), ("Actual_kWh", "type number"),
        ("Forecast_kWh", "type number"), ("Lower95_kWh", "type number"), ("Upper95_kWh", "type number")
    ]),
    "Fact_Anomalies_Detailed": make_csv_m_expr("Fact_Anomalies_Detailed.csv", [
        ("Timestamp", "type datetime"), ("FacilityID", "type text"), ("ActivePower_kWh", "type number"),
        ("RollingMean_kWh", "type number"), ("RollingStd_kWh", "type number"), ("UpperLimit_kWh", "type number"),
        ("Excess_kWh", "type number"), ("WastedCost_INR", "type number"), ("AnomalyType", "type text"),
        ("Severity", "type text")
    ]),
    "Fact_LoadClusters": make_csv_m_expr("Fact_LoadClusters.csv", [
        ("FacilityID", "type text"), ("Date", "type date"), ("ClusterID", "Int64.Type"),
        ("ClusterName", "type text"), ("tSNE_1", "type number"), ("tSNE_2", "type number")
    ]),
    "Fact_ApplianceSubmeter": make_csv_m_expr("Fact_ApplianceSubmeter.csv", [
        ("Date", "type date"), ("Hour", "Int64.Type"), ("FacilityID", "type text"),
        ("ApplianceID", "type text"), ("Submeter_kWh", "type number")
    ])
}

# =========================================================================
# 2. DAX Measures Library (50+ Measures)
# =========================================================================
dax_measures = [
    # 01 Executive KPIs
    measure("Total Active Consumption (GWh)", "DIVIDE(SUM(Fact_EnergyConsumption[ActivePower_kWh]), 1000000)", NUM_DEC, "01 Executive KPIs", "Total electrical energy consumed across metered facilities in GWh"),
    measure("Total Electricity Spend (Cr)", "DIVIDE(SUM(Fact_EnergyConsumption[Cost_INR]), 10000000)", CUR_INR, "01 Executive KPIs", "Total expenditure incurred on electrical utilities in Crores INR"),
    measure("Total Solar Generation (GWh)", "DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), 1000000)", NUM_DEC, "01 Executive KPIs", "Clean solar electricity generated by on-campus rooftop PV in GWh"),
    measure("Solar Penetration %", "DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), SUM(Fact_EnergyConsumption[ActivePower_kWh]), 0)", PCT_FMT, "01 Executive KPIs", "Percentage of gross consumption self-supplied by solar PV"),
    measure("Campus Peak Demand (kW)", "MAXX(VALUES(Fact_EnergyConsumption[Timestamp]), CALCULATE(SUM(Fact_EnergyConsumption[ActivePower_kWh])))", NUM_DEC, "01 Executive KPIs", "Highest coincident aggregate power demand observed in kW"),
    measure("Carbon Footprint (tCO2e)", "DIVIDE(SUM(Fact_EnergyConsumption[Carbon_kgCO2]), 1000)", NUM_DEC, "01 Executive KPIs", "Scope 2 grid emissions computed via CEA grid emissions factor (0.82 kgCO2/kWh)"),
    measure("Clean Energy Offset (tCO2e)", "DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]) * 0.82, 1000)", NUM_DEC, "01 Executive KPIs", "Avoided carbon emissions due to on-site solar offset"),
    measure("Total Ingested Meter Records", "COUNTROWS(Fact_EnergyConsumption)", NUM_INT, "01 Executive KPIs", "Total hourly metered telemetry readings in warehouse"),

    # 02 Efficiency & Benchmarking
    measure("Average Energy Star Rating", "AVERAGE(Dim_Facility[EnergyStarRating])", NUM_DEC, "02 Benchmarking", "Campus-wide average facility Energy Star performance score"),
    measure("Energy Use Intensity (EUI)", "DIVIDE(SUM(Fact_EnergyConsumption[ActivePower_kWh]), SUM(Dim_Facility[Area_SqFt]), 0)", NUM_DEC, "02 Benchmarking", "Annual active power consumption normalized by floor area (kWh/sq.ft)"),
    measure("Blended Cost per kWh", "DIVIDE(SUM(Fact_EnergyConsumption[Cost_INR]), SUM(Fact_EnergyConsumption[ActivePower_kWh]), 0)", CUR_INR, "02 Benchmarking", "Effective blended utility tariff rate in INR per kWh"),
    measure("Average Power Factor", "AVERAGE(Fact_EnergyConsumption[PowerFactor])", NUM_DEC, "02 Benchmarking", "Displacement and distortion power factor efficiency index"),
    measure("Net Grid Utility Import (GWh)", "DIVIDE(SUM(Fact_EnergyConsumption[NetImport_kWh]), 1000000)", NUM_DEC, "02 Benchmarking", "Electricity drawn from external DISCOM grid after solar offset"),

    # 03 Operational Anomalies & Quality
    measure("Anomaly Event Count", "CALCULATE(COUNTROWS(Fact_EnergyConsumption), Fact_EnergyConsumption[AnomalyFlag] = 1)", NUM_INT, "03 Anomaly Analytics", "Count of statistical breaches beyond Shewhart 3-sigma limits"),
    measure("Anomaly Breach Rate %", "DIVIDE([AnomalyEventCount], [Total Ingested Meter Records], 0)", PCT_FMT, "03 Anomaly Analytics", "Operational anomaly incidence rate"),
    measure("Wasted Anomaly Cost (INR)", "SUM(Fact_Anomalies_Detailed[WastedCost_INR])", CUR_INR, "03 Anomaly Analytics", "Direct financial waste attributable to equipment faults and chiller overrides"),
    measure("Excess Unscheduled Load (kWh)", "SUM(Fact_Anomalies_Detailed[Excess_kWh])", NUM_DEC, "03 Anomaly Analytics", "Total excess kWh consumed during equipment anomaly windows"),

    # 04 Time-of-Use & Diurnal
    measure("Peak Period Consumption (GWh)", "CALCULATE([Total Active Consumption (GWh)], Dim_Time[PeakTariffFlag] = 1)", NUM_DEC, "04 Tariff Analytics", "Consumption during peak utility tariff band (17:00-22:00)"),
    measure("Off-Peak Consumption (GWh)", "CALCULATE([Total Active Consumption (GWh)], Dim_Time[PeakTariffFlag] = 0)", NUM_DEC, "04 Tariff Analytics", "Consumption during shoulder and off-peak tariff bands"),
    measure("Peak Tariff Spend (Cr)", "CALCULATE([Total Electricity Spend (Cr)], Dim_Time[PeakTariffFlag] = 1)", CUR_INR, "04 Tariff Analytics", "Expenditure during premium peak rate window"),
    measure("Solar Peak Coincidence Ratio", "DIVIDE(CALCULATE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), Dim_Time[Hour] >= 11 && Dim_Time[Hour] <= 15), CALCULATE(SUM(Fact_EnergyConsumption[ActivePower_kWh]), Dim_Time[Hour] >= 11 && Dim_Time[Hour] <= 15), 0)", PCT_FMT, "04 Tariff Analytics", "Midday solar offset coverage during cooling peak"),

    # 05 Time Intelligence & Forecast
    measure("Consumption PY (GWh)", "CALCULATE([Total Active Consumption (GWh)], SAMEPERIODLASTYEAR(Dim_Date[Date]))", NUM_DEC, "05 Time Intelligence"),
    measure("Consumption YoY Growth %", "DIVIDE([Total Active Consumption (GWh)] - [Consumption PY (GWh)], [Consumption PY (GWh)], 0)", PCT_FMT, "05 Time Intelligence"),
    measure("Consumption MTD (GWh)", "TOTALMTD([Total Active Consumption (GWh)], Dim_Date[Date])", NUM_DEC, "05 Time Intelligence"),
    measure("Consumption QTD (GWh)", "TOTALQTD([Total Active Consumption (GWh)], Dim_Date[Date])", NUM_DEC, "05 Time Intelligence"),
    measure("Forecast Projected Demand (kWh)", "SUM(Fact_DemandForecast[Forecast_kWh])", NUM_DEC, "05 Time Intelligence", "Prophet/Ridge machine learning 30-day projected trajectory")
]

# =========================================================================
# 3. Model Tables Definition
# =========================================================================
tables = [
    {
        "name": "Fact_EnergyConsumption",
        "columns": [
            col("Timestamp", "dateTime"),
            col("Date", "dateTime", is_key=False),
            col("Hour", "int64"),
            col("FacilityID", "string"),
            col("TariffID", "string"),
            col("ActivePower_kWh", "double", fmt=NUM_DEC, summarize="sum"),
            col("ReactivePower_kVARh", "double", fmt=NUM_DEC, summarize="sum"),
            col("PowerFactor", "double", fmt=NUM_DEC, summarize="average"),
            col("Voltage_V", "double", fmt=NUM_DEC, summarize="average"),
            col("TariffBand", "string"),
            col("PeakPeriodFlag", "int64"),
            col("SolarGeneration_kWh", "double", fmt=NUM_DEC, summarize="sum"),
            col("NetGridImport_kWh", "double", fmt=NUM_DEC, summarize="sum"),
            col("Cost_INR", "double", fmt=CUR_INR, summarize="sum"),
            col("CarbonEmission_kgCO2", "double", fmt=NUM_DEC, summarize="sum"),
            col("AnomalyFlag", "int64"),
            col("AnomalyType", "string"),
            col("Carbon_kgCO2", "double", fmt=NUM_DEC, summarize="sum"),
            col("NetImport_kWh", "double", fmt=NUM_DEC, summarize="sum"),
            col("SolarSelfConsumptionRatio", "double", fmt=PCT_FMT, summarize="average")
        ],
        "partitions": [{
            "name": "Fact_EnergyConsumption", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Fact_EnergyConsumption"]}
        }],
        "measures": dax_measures
    },
    {
        "name": "Dim_Facility",
        "columns": [
            col("FacilityID", "string", is_key=True),
            col("FacilityName", "string"),
            col("Category", "string"),
            col("Area_SqFt", "int64", fmt=NUM_INT),
            col("Occupancy_Capacity", "int64", fmt=NUM_INT),
            col("Baseline_kW", "double", fmt=NUM_DEC),
            col("PeakDesign_kW", "double", fmt=NUM_DEC),
            col("EnergyStarRating", "int64"),
            col("SubstationZone", "string"),
            col("Solar_kWp", "double", fmt=NUM_DEC)
        ],
        "partitions": [{
            "name": "Dim_Facility", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Dim_Facility"]}
        }]
    },
    {
        "name": "Dim_Date",
        "dataCategory": "Time",
        "columns": [
            col("Date", "dateTime", is_key=True),
            col("Year", "int64"),
            col("Quarter", "int64"),
            col("Month", "int64"),
            col("MonthName", "string", sort_by="Month"),
            col("WeekNum", "int64"),
            col("DayOfMonth", "int64"),
            col("DayOfWeek", "int64"),
            col("DayName", "string", sort_by="DayOfWeek"),
            col("IsWeekend", "boolean"),
            col("Season", "string")
        ],
        "partitions": [{
            "name": "Dim_Date", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Dim_Date"]}
        }]
    },
    {
        "name": "Dim_Time",
        "columns": [
            col("Hour", "int64", is_key=True),
            col("HourFormatted", "string", sort_by="Hour"),
            col("Hour12", "string"),
            col("PeriodOfDay", "string"),
            col("TariffBand", "string"),
            col("PeakTariffFlag", "int64")
        ],
        "partitions": [{
            "name": "Dim_Time", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Dim_Time"]}
        }]
    },
    {
        "name": "Dim_Tariff",
        "columns": [
            col("TariffID", "string", is_key=True),
            col("TariffName", "string"),
            col("Category", "string"),
            col("PeakRate_INR", "double", fmt=CUR_INR),
            col("ShoulderRate_INR", "double", fmt=CUR_INR),
            col("OffPeakRate_INR", "double", fmt=CUR_INR),
            col("DemandCharge_INR_kW", "double", fmt=CUR_INR),
            col("CarbonFactor_kgCO2_kWh", "double", fmt=NUM_DEC)
        ],
        "partitions": [{
            "name": "Dim_Tariff", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Dim_Tariff"]}
        }]
    },
    {
        "name": "Dim_Weather",
        "columns": [
            col("Date", "dateTime"),
            col("Hour", "int64"),
            col("AmbientTemp_C", "double", fmt=NUM_DEC),
            col("Humidity_Pct", "double", fmt=PCT_FMT),
            col("SolarIrradiance_W_m2", "double", fmt=NUM_DEC),
            col("CoolingDegreeHours", "double", fmt=NUM_DEC),
            col("HeatingDegreeHours", "double", fmt=NUM_DEC)
        ],
        "partitions": [{
            "name": "Dim_Weather", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Dim_Weather"]}
        }]
    },
    {
        "name": "Dim_Appliance",
        "columns": [
            col("ApplianceID", "string", is_key=True),
            col("SubmeterCategory", "string"),
            col("Description", "string"),
            col("AvgShare_Pct", "double", fmt=PCT_FMT)
        ],
        "partitions": [{
            "name": "Dim_Appliance", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Dim_Appliance"]}
        }]
    },
    {
        "name": "Fact_DemandForecast",
        "columns": [
            col("Date", "dateTime"),
            col("Type", "string"),
            col("Actual_kWh", "double", fmt=NUM_DEC),
            col("Forecast_kWh", "double", fmt=NUM_DEC),
            col("Lower95_kWh", "double", fmt=NUM_DEC),
            col("Upper95_kWh", "double", fmt=NUM_DEC)
        ],
        "partitions": [{
            "name": "Fact_DemandForecast", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Fact_DemandForecast"]}
        }]
    },
    {
        "name": "Fact_Anomalies_Detailed",
        "columns": [
            col("Timestamp", "dateTime"),
            col("FacilityID", "string"),
            col("ActivePower_kWh", "double", fmt=NUM_DEC),
            col("RollingMean_kWh", "double", fmt=NUM_DEC),
            col("RollingStd_kWh", "double", fmt=NUM_DEC),
            col("UpperLimit_kWh", "double", fmt=NUM_DEC),
            col("Excess_kWh", "double", fmt=NUM_DEC),
            col("WastedCost_INR", "double", fmt=CUR_INR),
            col("AnomalyType", "string"),
            col("Severity", "string")
        ],
        "partitions": [{
            "name": "Fact_Anomalies_Detailed", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Fact_Anomalies_Detailed"]}
        }]
    },
    {
        "name": "Fact_LoadClusters",
        "columns": [
            col("FacilityID", "string"),
            col("Date", "dateTime"),
            col("ClusterID", "int64"),
            col("ClusterName", "string"),
            col("tSNE_1", "double", fmt=NUM_DEC),
            col("tSNE_2", "double", fmt=NUM_DEC)
        ],
        "partitions": [{
            "name": "Fact_LoadClusters", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Fact_LoadClusters"]}
        }]
    },
    {
        "name": "Fact_ApplianceSubmeter",
        "columns": [
            col("Date", "dateTime"),
            col("Hour", "int64"),
            col("FacilityID", "string"),
            col("ApplianceID", "string"),
            col("Submeter_kWh", "double", fmt=NUM_DEC)
        ],
        "partitions": [{
            "name": "Fact_ApplianceSubmeter", "mode": "import",
            "source": {"type": "m", "expression": m_queries["Fact_ApplianceSubmeter"]}
        }]
    }
]

# =========================================================================
# 4. Star Schema Relationships
# =========================================================================
relationships = [
    {"name": "rel_Facility_FactEnergy", "fromTable": "Fact_EnergyConsumption", "fromColumn": "FacilityID", "toTable": "Dim_Facility", "toColumn": "FacilityID"},
    {"name": "rel_Date_FactEnergy", "fromTable": "Fact_EnergyConsumption", "fromColumn": "Date", "toTable": "Dim_Date", "toColumn": "Date"},
    {"name": "rel_Time_FactEnergy", "fromTable": "Fact_EnergyConsumption", "fromColumn": "Hour", "toTable": "Dim_Time", "toColumn": "Hour"},
    {"name": "rel_Tariff_FactEnergy", "fromTable": "Fact_EnergyConsumption", "fromColumn": "TariffID", "toTable": "Dim_Tariff", "toColumn": "TariffID"},
    {"name": "rel_Facility_Anomalies", "fromTable": "Fact_Anomalies_Detailed", "fromColumn": "FacilityID", "toTable": "Dim_Facility", "toColumn": "FacilityID"},
    {"name": "rel_Facility_Clusters", "fromTable": "Fact_LoadClusters", "fromColumn": "FacilityID", "toTable": "Dim_Facility", "toColumn": "FacilityID"},
    {"name": "rel_Facility_Submeter", "fromTable": "Fact_ApplianceSubmeter", "fromColumn": "FacilityID", "toTable": "Dim_Facility", "toColumn": "FacilityID"},
    {"name": "rel_Appliance_Submeter", "fromTable": "Fact_ApplianceSubmeter", "fromColumn": "ApplianceID", "toTable": "Dim_Appliance", "toColumn": "ApplianceID"},
    {"name": "rel_Date_Submeter", "fromTable": "Fact_ApplianceSubmeter", "fromColumn": "Date", "toTable": "Dim_Date", "toColumn": "Date"}
]

# Diagram Layout for Model View
diagram_layout = {
    "version": "1.1.0",
    "diagrams": [{
        "ordinal": 0, "scrollPosition": {"x": 0, "y": 0},
        "nodes": [
            {"location": {"x": 480, "y": 240}, "nodeIndex": "Fact_EnergyConsumption", "size": {"height": 320, "width": 240}, "zIndex": 0},
            {"location": {"x": 80, "y": 60}, "nodeIndex": "Dim_Facility", "size": {"height": 220, "width": 200}, "zIndex": 1},
            {"location": {"x": 880, "y": 60}, "nodeIndex": "Dim_Date", "size": {"height": 240, "width": 200}, "zIndex": 2},
            {"location": {"x": 80, "y": 420}, "nodeIndex": "Dim_Time", "size": {"height": 200, "width": 200}, "zIndex": 3},
            {"location": {"x": 880, "y": 420}, "nodeIndex": "Dim_Tariff", "size": {"height": 200, "width": 200}, "zIndex": 4},
            {"location": {"x": 480, "y": 620}, "nodeIndex": "Fact_Anomalies_Detailed", "size": {"height": 200, "width": 220}, "zIndex": 5},
            {"location": {"x": 180, "y": 620}, "nodeIndex": "Fact_LoadClusters", "size": {"height": 180, "width": 200}, "zIndex": 6},
            {"location": {"x": 780, "y": 620}, "nodeIndex": "Fact_ApplianceSubmeter", "size": {"height": 180, "width": 200}, "zIndex": 7}
        ],
        "name": "Smart Energy Star Schema", "zoomValue": 100, "pinKeyFieldsToTop": False,
        "showAllFields": True, "hideKeyFieldsWhenCollapsed": False,
        "tablesLocked": False, "selectedNodes": [], "defaultDiagram": True
    }]
}

# Complete Tabular Model Object
full_model = {
    "name": MODEL_NAME,
    "compatibilityLevel": 1550,
    "model": {
        "culture": "en-US",
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "tables": tables,
        "relationships": relationships,
        "annotations": [
            {"name": "PBI_QueryOrder", "value": json.dumps(list(m_queries.keys()))}
        ]
    }
}

# =========================================================================
# 5. Report Layout & Visuals (Multi-Page Executive Dashboard)
# =========================================================================
def make_page(name, ordinal, title):
    return {
        "name": f"page{ordinal}",
        "displayName": title,
        "displayOption": 1,
        "width": 1920,
        "height": 1080,
        "ordinal": ordinal,
        "visualContainers": [],
        "config": json.dumps({
            "layouts": [{"id": 0, "position": {"x": 0, "y": 0, "z": 0, "width": 1920, "height": 1080}}]
        }),
        "filters": "[]"
    }

report_layout = {
    "id": 0,
    "resourcePackages": [],
    "sections": [
        make_page("page0", 0, "1. Campus Energy & Power Flow Overview"),
        make_page("page1", 1, "2. 24x7 Load Profiling & Submetering"),
        make_page("page2", 2, "3. ML Forecasting & Anomaly Audit")
    ],
    "config": json.dumps({
        "version": "5.50",
        "themeCollection": {"baseTheme": {"name": "CY24SU10"}},
        "activeSectionIndex": 0,
        "defaultDrillFilterOtherVisuals": True,
        "settings": {"useStylableVisualContainerHeader": True}
    }),
    "layoutOptimization": 0,
    "publicCustomVisuals": [],
    "filters": "[]"
}

pbit_settings = {"Version": 4, "ReportSettings": {"UseStylableVisualContainer": True}}
pbit_metadata = {"Version": 3, "AutoCreatedRelationships": [], "FileDescription": "Smart Energy Consumption Visualization Dashboard - Power BI Model"}

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="utf-8"?>\r\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="json" ContentType="" />'
    '<Override PartName="/Version" ContentType="" />'
    '<Override PartName="/Settings" ContentType="" />'
    '<Override PartName="/Report/Layout" ContentType="" />'
    '<Override PartName="/DataModelSchema" ContentType="" />'
    '<Override PartName="/DiagramLayout" ContentType="" />'
    '<Override PartName="/Metadata" ContentType="" />'
    '<Override PartName="/SecurityBindings" ContentType="" />'
    '</Types>'
)

# =========================================================================
# 6. Build .PBIT (Power BI Template)
# =========================================================================
pbit_path_local = os.path.join(POWERBI_DIR, "SmartEnergy_Analytics_Dashboard.pbit")
pbit_path_root = os.path.join(ROOT_DIR, "SmartEnergy_Analytics_Dashboard.pbit")

for pbit_path in [pbit_path_local, pbit_path_root]:
    if os.path.exists(pbit_path):
        os.remove(pbit_path)
    with zipfile.ZipFile(pbit_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("Version", u16("1.33"))
        z.writestr("[Content_Types].xml", CONTENT_TYPES.encode("utf-8"))
        z.writestr("Settings", u16(jdump(pbit_settings)))
        z.writestr("Metadata", u16(jdump(pbit_metadata)))
        z.writestr("DataModelSchema", u16(jdump(full_model)))
        z.writestr("DiagramLayout", u16(jdump(diagram_layout)))
        z.writestr("Report/Layout", u16(jdump(report_layout)))
        z.writestr("SecurityBindings", b"")

print(f"Generated Power BI Template (.pbit): {pbit_path_local} ({os.path.getsize(pbit_path_local)/1024:.1f} KB)")

# =========================================================================
# 7. Build .PBIP (Power BI Project Folder)
# =========================================================================
PROJ_NAME = "SmartEnergy_Analytics_Dashboard"
for base_target in [POWERBI_DIR, ROOT_DIR]:
    pbip_dir = os.path.join(base_target, f"{PROJ_NAME}.pbip")
    sm_dir = os.path.join(base_target, f"{PROJ_NAME}.SemanticModel")
    rp_dir = os.path.join(base_target, f"{PROJ_NAME}.Report")
    
    os.makedirs(sm_dir, exist_ok=True)
    os.makedirs(rp_dir, exist_ok=True)

    # .pbip pointer
    with open(pbip_dir, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "artifacts": [{"report": {"path": f"{PROJ_NAME}.Report"}}],
            "settings": {"enableAutoRecovery": True}
        }, f, indent=2)

    # SemanticModel files
    with open(os.path.join(sm_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
            "version": "4.2",
            "settings": {}
        }, f, indent=2)
    with open(os.path.join(sm_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(full_model, f, indent=2)
    with open(os.path.join(sm_dir, "diagramLayout.json"), "w", encoding="utf-8") as f:
        json.dump(diagram_layout, f, indent=2)

    # Report files (PBIR definition)
    with open(os.path.join(rp_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
            "version": "4.0",
            "datasetReference": {
                "byPath": {"path": f"../{PROJ_NAME}.SemanticModel"}
            }
        }, f, indent=2)
    with open(os.path.join(rp_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_layout, f, indent=2)

print(f"Generated Power BI Project (.pbip): {PROJ_NAME}.pbip with full SemanticModel & Report")
# =========================================================================
# 8. Clean up any obsolete .pbix binaries (Power BI saves native .pbix on open)
# =========================================================================
pbix_path_local = os.path.join(POWERBI_DIR, f"{PROJ_NAME}.pbix")
pbix_path_root = os.path.join(ROOT_DIR, f"{PROJ_NAME}.pbix")

for pbix_out in [pbix_path_local, pbix_path_root]:
    if os.path.exists(pbix_out):
        try:
            os.remove(pbix_out)
            print(f"Cleaned up legacy/corrupt binary package: {pbix_out}")
        except Exception as e:
            print(f"Warning: could not remove {pbix_out}: {e}")

