"""
Full Native Power BI Project (.pbip) & Report Builder
Builds TMDL semantic model + PBIR multi-page visual layout.
Works natively in Microsoft Power BI Desktop (August 2026 / 2.157+).
"""
import os
import json
import uuid
import hashlib
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data").replace("\\", "/")
POWERBI_DIR = os.path.join(BASE_DIR, "powerbi")
ROOT_DIR = os.path.dirname(BASE_DIR)

SCH_REPORT = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
V_SCHEMA = f"{SCH_REPORT}/visualContainer/2.12.0/schema.json"
P_SCHEMA = f"{SCH_REPORT}/page/2.1.0/schema.json"
PS_SCHEMA = f"{SCH_REPORT}/pagesMetadata/1.1.0/schema.json"

_ids = set()
def vid(seed):
    h = hashlib.sha1(seed.encode()).hexdigest()[:20]
    while h in _ids:
        h = hashlib.sha1((seed + "x").encode()).hexdigest()[:20]
    _ids.add(h)
    return h

def measure_ref(entity, prop):
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop
    }

def column_ref(entity, prop):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop
    }

def sum_ref(entity, prop):
    return {
        "field": {
            "Aggregation": {
                "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
                "Function": 0
            }
        },
        "queryRef": f"Sum({entity}.{prop})",
        "nativeQueryRef": f"Sum of {prop}"
    }

def make_visual(seed, vtype, x, y, w, h, roles, z=0):
    qs = {r: {"projections": p} for r, p in roles.items() if p}
    return {
        "$schema": V_SCHEMA,
        "name": vid(seed),
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z * 1000},
        "visual": {
            "visualType": vtype,
            "query": {"queryState": qs},
            "drillFilterOtherVisuals": True
        }
    }

def build_solution():
    print("Starting Power BI PBIP Generation...")
    
    # Target directories
    targets = [
        (ROOT_DIR, "SmartEnergy_Analytics_Dashboard"),
        (POWERBI_DIR, "SmartEnergy_Analytics_Dashboard")
    ]
    
    for base_folder, proj_name in targets:
        pbip_file = os.path.join(base_folder, f"{proj_name}.pbip")
        sm_dir = os.path.join(base_folder, f"{proj_name}.SemanticModel")
        rp_dir = os.path.join(base_folder, f"{proj_name}.Report")
        
        # Clean existing
        if os.path.exists(sm_dir): shutil.rmtree(sm_dir)
        if os.path.exists(rp_dir): shutil.rmtree(rp_dir)
        
        sm_def = os.path.join(sm_dir, "definition")
        sm_tables = os.path.join(sm_def, "tables")
        sm_cultures = os.path.join(sm_def, "cultures")
        os.makedirs(sm_tables, exist_ok=True)
        os.makedirs(sm_cultures, exist_ok=True)
        
        rp_def = os.path.join(rp_dir, "definition")
        rp_pages = os.path.join(rp_def, "pages")
        os.makedirs(rp_pages, exist_ok=True)
        
        # 1. PBIP file
        with open(pbip_file, "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
                "version": "1.0",
                "artifacts": [{"report": {"path": f"{proj_name}.Report"}}],
                "settings": {"enableAutoRecovery": True}
            }, f, indent=2)
            
        # 2. SemanticModel .platform & pbism
        with open(os.path.join(sm_dir, ".platform"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                "metadata": {"type": "SemanticModel", "displayName": proj_name},
                "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}
            }, f, indent=2)
            
        with open(os.path.join(sm_dir, "definition.pbism"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
                "version": "4.2",
                "settings": {}
            }, f, indent=2)

        # 3. TMDL: database.tmdl
        with open(os.path.join(sm_def, "database.tmdl"), "w", encoding="utf-8") as f:
            f.write("database\n\tcompatibilityLevel: 1606\n\n")

        # 4. TMDL: cultures/en-US.tmdl
        with open(os.path.join(sm_cultures, "en-US.tmdl"), "w", encoding="utf-8") as f:
            f.write("cultureInfo en-US\n\n")

        # 5. TMDL: model.tmdl
        table_names = [
            "Fact_EnergyConsumption", "Dim_Facility", "Dim_Date", "Dim_Time",
            "Dim_Tariff", "Dim_Weather", "Dim_Appliance", "Fact_DemandForecast",
            "Fact_Anomalies_Detailed", "Fact_LoadClusters", "Fact_ApplianceSubmeter"
        ]
        
        model_tmdl = [
            "model Model",
            "\tculture: en-US",
            "\tdefaultPowerBIDataSourceVersion: powerBI_V3",
            "\tsourceQueryCulture: en-IN",
            "\tvalueFilterBehavior: independent",
            "\tdataAccessOptions",
            "\t\tlegacyRedirects",
            "\t\treturnErrorValuesAsNull",
            "",
            "annotation __PBI_TimeIntelligenceEnabled = 0",
            'annotation PBI_ProTooling = ["TMDLView_Desktop","DevMode"]',
            f'annotation PBI_QueryOrder = {json.dumps(table_names)}',
            ""
        ]
        for t in table_names:
            model_tmdl.append(f"ref table {t}")
        model_tmdl.append("\nref cultureInfo en-US\n")
        
        with open(os.path.join(sm_def, "model.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(model_tmdl))

        # 6. TMDL: relationships.tmdl
        rels_tmdl = [
            "relationship rel_Facility_FactEnergy",
            "\tfromColumn: Fact_EnergyConsumption.FacilityID",
            "\ttoColumn: Dim_Facility.FacilityID",
            "",
            "relationship rel_Date_FactEnergy",
            "\tfromColumn: Fact_EnergyConsumption.Date",
            "\ttoColumn: Dim_Date.Date",
            "",
            "relationship rel_Time_FactEnergy",
            "\tfromColumn: Fact_EnergyConsumption.Hour",
            "\ttoColumn: Dim_Time.Hour",
            "",
            "relationship rel_Tariff_FactEnergy",
            "\tfromColumn: Fact_EnergyConsumption.TariffID",
            "\ttoColumn: Dim_Tariff.TariffID",
            "",
            "relationship rel_Facility_Anomalies",
            "\tfromColumn: Fact_Anomalies_Detailed.FacilityID",
            "\ttoColumn: Dim_Facility.FacilityID",
            "",
            "relationship rel_Facility_Clusters",
            "\tfromColumn: Fact_LoadClusters.FacilityID",
            "\ttoColumn: Dim_Facility.FacilityID",
            "",
            "relationship rel_Facility_Submeter",
            "\tfromColumn: Fact_ApplianceSubmeter.FacilityID",
            "\ttoColumn: Dim_Facility.FacilityID",
            "",
            "relationship rel_Appliance_Submeter",
            "\tfromColumn: Fact_ApplianceSubmeter.ApplianceID",
            "\ttoColumn: Dim_Appliance.ApplianceID",
            "",
            "relationship rel_Date_Submeter",
            "\tfromColumn: Fact_ApplianceSubmeter.Date",
            "\ttoColumn: Dim_Date.Date",
            ""
        ]
        with open(os.path.join(sm_def, "relationships.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(rels_tmdl))

        # 7. TMDL: Table files
        # --- Fact_EnergyConsumption ---
        fact_tmdl = [
            "table Fact_EnergyConsumption",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            # Measures
            "\tmeasure 'Total Active Consumption (GWh)' = DIVIDE(SUM(Fact_EnergyConsumption[ActivePower_kWh]), 1000000)",
            "\t\tformatString: #,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Total Electricity Spend (Cr)' = DIVIDE(SUM(Fact_EnergyConsumption[Cost_INR]), 10000000)",
            "\t\tformatString: \\₹#,0.00;(\\₹#,0.00);\\₹#,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Total Solar Generation (GWh)' = DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), 1000000)",
            "\t\tformatString: #,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Solar Penetration %' = DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), SUM(Fact_EnergyConsumption[ActivePower_kWh]), 0)",
            "\t\tformatString: 0.0%",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Campus Peak Demand (kW)' = MAXX(VALUES(Fact_EnergyConsumption[Timestamp]), CALCULATE(SUM(Fact_EnergyConsumption[ActivePower_kWh])))",
            "\t\tformatString: #,0.0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Carbon Footprint (tCO2e)' = DIVIDE(SUM(Fact_EnergyConsumption[Carbon_kgCO2]), 1000)",
            "\t\tformatString: #,0.0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Clean Energy Offset (tCO2e)' = DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]) * 0.82, 1000)",
            "\t\tformatString: #,0.0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Operational Anomaly Count' = CALCULATE(COUNTROWS(Fact_EnergyConsumption), Fact_EnergyConsumption[AnomalyFlag] = 1)",
            "\t\tformatString: #,0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Net Grid Import (GWh)' = DIVIDE(SUM(Fact_EnergyConsumption[NetImport_kWh]), 1000000)",
            "\t\tformatString: #,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Average Power Factor' = AVERAGE(Fact_EnergyConsumption[PowerFactor])",
            "\t\tformatString: 0.000",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Peak Period Consumption (GWh)' = CALCULATE([Total Active Consumption (GWh)], Dim_Time[PeakTariffFlag] = 1)",
            "\t\tformatString: #,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Off-Peak Consumption (GWh)' = CALCULATE([Total Active Consumption (GWh)], Dim_Time[PeakTariffFlag] = 0)",
            "\t\tformatString: #,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            # Columns
            "\tcolumn Timestamp",
            "\t\tdataType: dateTime",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Timestamp",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Date",
            "\t\tdataType: dateTime",
            "\t\tformatString: yyyy-mm-dd",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Date",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Hour",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Hour",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn FacilityID",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: FacilityID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn TariffID",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: TariffID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ActivePower_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: ActivePower_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ReactivePower_kVARh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: ReactivePower_kVARh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn PowerFactor",
            "\t\tdataType: double",
            "\t\tformatString: 0.000",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: PowerFactor",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Voltage_V",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: Voltage_V",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn TariffBand",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: TariffBand",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn PeakPeriodFlag",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: PeakPeriodFlag",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn SolarGeneration_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: SolarGeneration_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn NetGridImport_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: NetGridImport_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Cost_INR",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Cost_INR",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn CarbonEmission_kgCO2",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: CarbonEmission_kgCO2",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn AnomalyFlag",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: AnomalyFlag",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn AnomalyType",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: AnomalyType",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Carbon_kgCO2",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Carbon_kgCO2",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn NetImport_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: NetImport_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn SolarSelfConsumptionRatio",
            "\t\tdataType: double",
            "\t\tformatString: 0.0%",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: SolarSelfConsumptionRatio",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            # Partition M
            "\tpartition Fact_EnergyConsumption = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Fact_EnergyConsumption.csv"), [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Timestamp", type datetime}, {"Date", type date}, {"Hour", Int64.Type}, {"FacilityID", type text},',
            '\t\t\t        {"TariffID", type text}, {"ActivePower_kWh", type number}, {"ReactivePower_kVARh", type number},',
            '\t\t\t        {"PowerFactor", type number}, {"Voltage_V", type number}, {"TariffBand", type text},',
            '\t\t\t        {"PeakPeriodFlag", Int64.Type}, {"SolarGeneration_kWh", type number}, {"NetGridImport_kWh", type number},',
            '\t\t\t        {"Cost_INR", type number}, {"CarbonEmission_kgCO2", type number}, {"AnomalyFlag", Int64.Type},',
            '\t\t\t        {"AnomalyType", type text}, {"Carbon_kgCO2", type number}, {"NetImport_kWh", type number},',
            '\t\t\t        {"SolarSelfConsumptionRatio", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Fact_EnergyConsumption.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(fact_tmdl))

        # --- Dim_Facility ---
        fac_tmdl = [
            "table Dim_Facility",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Average Energy Star Rating' = AVERAGE(Dim_Facility[EnergyStarRating])",
            "\t\tformatString: 0.0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn FacilityID",
            "\t\tdataType: string",
            "\t\tisKey",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: FacilityID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn FacilityName",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: FacilityName",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Category",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Category",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Area_SqFt",
            "\t\tdataType: int64",
            "\t\tformatString: #,0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Area_SqFt",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Occupancy_Capacity",
            "\t\tdataType: int64",
            "\t\tformatString: #,0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Occupancy_Capacity",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Baseline_kW",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Baseline_kW",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn PeakDesign_kW",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: PeakDesign_kW",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn EnergyStarRating",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: EnergyStarRating",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn SubstationZone",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: SubstationZone",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Solar_kWp",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Solar_kWp",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Dim_Facility = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Dim_Facility.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"FacilityID", type text}, {"FacilityName", type text}, {"Category", type text},',
            '\t\t\t        {"Area_SqFt", Int64.Type}, {"Occupancy_Capacity", Int64.Type}, {"Baseline_kW", type number},',
            '\t\t\t        {"PeakDesign_kW", type number}, {"EnergyStarRating", Int64.Type}, {"SubstationZone", type text}, {"Solar_kWp", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Dim_Facility.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(fac_tmdl))

        # --- Dim_Date ---
        date_tmdl = [
            "table Dim_Date",
            "\tdataCategory: Time",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Date",
            "\t\tdataType: dateTime",
            "\t\tisKey",
            "\t\tformatString: yyyy-mm-dd",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Date",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Year",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Year",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Quarter",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Quarter",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Month",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Month",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn MonthName",
            "\t\tdataType: string",
            "\t\tsortByColumn: Month",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: MonthName",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn WeekNum",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: WeekNum",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn DayOfMonth",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: DayOfMonth",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn DayOfWeek",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: DayOfWeek",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn DayName",
            "\t\tdataType: string",
            "\t\tsortByColumn: DayOfWeek",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: DayName",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn IsWeekend",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: IsWeekend",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Season",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Season",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Dim_Date = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Dim_Date.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Date", type date}, {"Year", Int64.Type}, {"Quarter", type text}, {"Month", Int64.Type},',
            '\t\t\t        {"MonthName", type text}, {"WeekNum", Int64.Type}, {"DayOfMonth", Int64.Type}, {"DayOfWeek", Int64.Type},',
            '\t\t\t        {"DayName", type text}, {"IsWeekend", Int64.Type}, {"Season", type text}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Dim_Date.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(date_tmdl))

        # --- Dim_Time ---
        time_tmdl = [
            "table Dim_Time",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Hour",
            "\t\tdataType: int64",
            "\t\tisKey",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Hour",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn HourFormatted",
            "\t\tdataType: string",
            "\t\tsortByColumn: Hour",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: HourFormatted",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Hour12",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Hour12",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn PeriodOfDay",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: PeriodOfDay",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn TariffBand",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: TariffBand",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn PeakTariffFlag",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: PeakTariffFlag",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Dim_Time = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Dim_Time.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Hour", Int64.Type}, {"HourFormatted", type text}, {"Hour12", type text},',
            '\t\t\t        {"PeriodOfDay", type text}, {"TariffBand", type text}, {"PeakTariffFlag", Int64.Type}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Dim_Time.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(time_tmdl))

        # --- Dim_Tariff ---
        tariff_tmdl = [
            "table Dim_Tariff",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn TariffID",
            "\t\tdataType: string",
            "\t\tisKey",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: TariffID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn TariffName",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: TariffName",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Category",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Category",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn PeakRate_INR",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: PeakRate_INR",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ShoulderRate_INR",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: ShoulderRate_INR",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn OffPeakRate_INR",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: OffPeakRate_INR",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn DemandCharge_INR_kW",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: DemandCharge_INR_kW",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn CarbonFactor_kgCO2_kWh",
            "\t\tdataType: double",
            "\t\tformatString: 0.000",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: CarbonFactor_kgCO2_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Dim_Tariff = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Dim_Tariff.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"TariffID", type text}, {"TariffName", type text}, {"Category", type text},',
            '\t\t\t        {"PeakRate_INR", type number}, {"ShoulderRate_INR", type number}, {"OffPeakRate_INR", type number},',
            '\t\t\t        {"DemandCharge_INR_kW", type number}, {"CarbonFactor_kgCO2_kWh", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Dim_Tariff.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(tariff_tmdl))

        # --- Dim_Weather ---
        weather_tmdl = [
            "table Dim_Weather",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Date",
            "\t\tdataType: dateTime",
            "\t\tformatString: yyyy-mm-dd",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Date",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Hour",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Hour",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn AmbientTemp_C",
            "\t\tdataType: double",
            "\t\tformatString: 0.0",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: AmbientTemp_C",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Humidity_Pct",
            "\t\tdataType: double",
            "\t\tformatString: 0.0%",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: Humidity_Pct",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn SolarIrradiance_W_m2",
            "\t\tdataType: double",
            "\t\tformatString: #,0",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: SolarIrradiance_W_m2",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn CoolingDegreeHours",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: CoolingDegreeHours",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn HeatingDegreeHours",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: HeatingDegreeHours",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Dim_Weather = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Dim_Weather.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Date", type date}, {"Hour", Int64.Type}, {"AmbientTemp_C", type number}, {"Humidity_Pct", type number},',
            '\t\t\t        {"SolarIrradiance_W_m2", type number}, {"CoolingDegreeHours", type number}, {"HeatingDegreeHours", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Dim_Weather.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(weather_tmdl))

        # --- Dim_Appliance ---
        app_tmdl = [
            "table Dim_Appliance",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ApplianceID",
            "\t\tdataType: string",
            "\t\tisKey",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: ApplianceID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn SubmeterCategory",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: SubmeterCategory",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Description",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Description",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn AvgShare_Pct",
            "\t\tdataType: double",
            "\t\tformatString: 0.0%",
            "\t\tsummarizeBy: average",
            "\t\tsourceColumn: AvgShare_Pct",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Dim_Appliance = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Dim_Appliance.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"ApplianceID", type text}, {"SubmeterCategory", type text}, {"Description", type text}, {"AvgShare_Pct", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Dim_Appliance.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(app_tmdl))

        # --- Fact_DemandForecast ---
        fc_tmdl = [
            "table Fact_DemandForecast",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Forecast Projected Demand (kWh)' = SUM(Fact_DemandForecast[Forecast_kWh])",
            "\t\tformatString: #,0.0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Date",
            "\t\tdataType: dateTime",
            "\t\tformatString: yyyy-mm-dd",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Date",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Type",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Type",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Actual_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Actual_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Forecast_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Forecast_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Lower95_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Lower95_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Upper95_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Upper95_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Fact_DemandForecast = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Fact_DemandForecast.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Date", type date}, {"Type", type text}, {"Actual_kWh", type number}, {"Forecast_kWh", type number}, {"Lower95_kWh", type number}, {"Upper95_kWh", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Fact_DemandForecast.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(fc_tmdl))

        # --- Fact_Anomalies_Detailed ---
        anom_tmdl = [
            "table Fact_Anomalies_Detailed",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Wasted Anomaly Cost (INR)' = SUM(Fact_Anomalies_Detailed[WastedCost_INR])",
            "\t\tformatString: \\₹#,0.00;(\\₹#,0.00);\\₹#,0.00",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tmeasure 'Excess Unscheduled Load (kWh)' = SUM(Fact_Anomalies_Detailed[Excess_kWh])",
            "\t\tformatString: #,0.0",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Timestamp",
            "\t\tdataType: dateTime",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Timestamp",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn FacilityID",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: FacilityID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ActivePower_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: ActivePower_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn RollingMean_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: RollingMean_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn RollingStd_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: RollingStd_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn UpperLimit_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: UpperLimit_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Excess_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Excess_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn WastedCost_INR",
            "\t\tdataType: double",
            "\t\tformatString: #,0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: WastedCost_INR",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn AnomalyType",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: AnomalyType",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Severity",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Severity",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Fact_Anomalies_Detailed = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Fact_Anomalies_Detailed.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Timestamp", type datetime}, {"FacilityID", type text}, {"ActivePower_kWh", type number},',
            '\t\t\t        {"RollingMean_kWh", type number}, {"RollingStd_kWh", type number}, {"UpperLimit_kWh", type number},',
            '\t\t\t        {"Excess_kWh", type number}, {"WastedCost_INR", type number}, {"AnomalyType", type text}, {"Severity", type text}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Fact_Anomalies_Detailed.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(anom_tmdl))

        # --- Fact_LoadClusters ---
        cluster_tmdl = [
            "table Fact_LoadClusters",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn FacilityID",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: FacilityID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Date",
            "\t\tdataType: dateTime",
            "\t\tformatString: yyyy-mm-dd",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Date",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ClusterID",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: ClusterID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ClusterName",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: ClusterName",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn tSNE_1",
            "\t\tdataType: double",
            "\t\tformatString: 0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: tSNE_1",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn tSNE_2",
            "\t\tdataType: double",
            "\t\tformatString: 0.00",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: tSNE_2",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Fact_LoadClusters = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Fact_LoadClusters.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"FacilityID", type text}, {"Date", type date}, {"ClusterID", Int64.Type}, {"ClusterName", type text}, {"tSNE_1", type number}, {"tSNE_2", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Fact_LoadClusters.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(cluster_tmdl))

        # --- Fact_ApplianceSubmeter ---
        sub_tmdl = [
            "table Fact_ApplianceSubmeter",
            f"\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Date",
            "\t\tdataType: dateTime",
            "\t\tformatString: yyyy-mm-dd",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Date",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Hour",
            "\t\tdataType: int64",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: Hour",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn FacilityID",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: FacilityID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn ApplianceID",
            "\t\tdataType: string",
            "\t\tsummarizeBy: none",
            "\t\tsourceColumn: ApplianceID",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tcolumn Submeter_kWh",
            "\t\tdataType: double",
            "\t\tformatString: #,0.0",
            "\t\tsummarizeBy: sum",
            "\t\tsourceColumn: Submeter_kWh",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
            "\tpartition Fact_ApplianceSubmeter = m",
            "\t\tmode: import",
            "\t\tsource =",
            "\t\t\tlet",
            f'\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/Fact_ApplianceSubmeter.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
            '\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {',
            '\t\t\t        {"Date", type date}, {"Hour", Int64.Type}, {"FacilityID", type text}, {"ApplianceID", type text}, {"Submeter_kWh", type number}',
            "\t\t\t    })",
            "\t\t\tin",
            "\t\t\t    Typed\n"
        ]
        with open(os.path.join(sm_tables, "Fact_ApplianceSubmeter.tmdl"), "w", encoding="utf-8") as f:
            f.write("\n".join(sub_tmdl))

        # 8. Report definition files
        with open(os.path.join(rp_dir, ".platform"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                "metadata": {"type": "Report", "displayName": proj_name},
                "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}
            }, f, indent=2)

        with open(os.path.join(rp_dir, "definition.pbir"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
                "version": "4.0",
                "datasetReference": {
                    "byPath": {"path": f"../{proj_name}.SemanticModel"}
                }
            }, f, indent=2)

        with open(os.path.join(rp_def, "version.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
                "version": "2.0.0"
            }, f, indent=2)

        with open(os.path.join(rp_def, "report.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json",
                "themeCollection": {
                    "baseTheme": {
                        "name": "CY24SU10",
                        "reportVersionAtImport": {"visual": "2.12.0", "report": "3.4.0", "page": "2.3.1"},
                        "type": "SharedResources"
                    }
                },
                "objects": {
                    "section": [{"properties": {"verticalAlignment": {"expr": {"Literal": {"Value": "'Top'"}}}}}]
                }
            }, f, indent=2)

        # 9. Pages and Visuals
        p1_id = "e1001a1c" + vid("p1")[:12]
        p2_id = "e2002b2c" + vid("p2")[:12]
        p3_id = "e3003c3c" + vid("p3")[:12]

        with open(os.path.join(rp_pages, "pages.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
                "pageOrder": [p1_id, p2_id, p3_id],
                "activePageName": p1_id
            }, f, indent=2)

        # --- Page 1: Executive Overview ---
        p1_dir = os.path.join(rp_pages, p1_id)
        p1_vis_dir = os.path.join(p1_dir, "visuals")
        os.makedirs(p1_vis_dir, exist_ok=True)
        with open(os.path.join(p1_dir, "page.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": P_SCHEMA, "name": p1_id, "displayName": "1 Executive Campus HUD",
                "displayOption": "FitToPage", "height": 1080, "width": 1920
            }, f, indent=2)

        p1_visuals = [
            # 6 KPI cards
            make_visual("kpi_c1", "card", 40, 20, 290, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Total Active Consumption (GWh)")]}),
            make_visual("kpi_c2", "card", 350, 20, 290, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Total Electricity Spend (Cr)")]}),
            make_visual("kpi_c3", "card", 660, 20, 290, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Total Solar Generation (GWh)")]}),
            make_visual("kpi_c4", "card", 970, 20, 290, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Campus Peak Demand (kW)")]}),
            make_visual("kpi_c5", "card", 1280, 20, 290, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Carbon Footprint (tCO2e)")]}),
            make_visual("kpi_c6", "card", 1590, 20, 290, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Operational Anomaly Count")]}),

            # Slicers
            make_visual("slic_fac", "slicer", 40, 135, 420, 80, {"Values": [column_ref("Dim_Facility", "FacilityName")]}),
            make_visual("slic_sea", "slicer", 480, 135, 420, 80, {"Values": [column_ref("Dim_Date", "Season")]}),
            make_visual("slic_per", "slicer", 920, 135, 420, 80, {"Values": [column_ref("Dim_Time", "PeriodOfDay")]}),
            make_visual("slic_zone", "slicer", 1360, 135, 520, 80, {"Values": [column_ref("Dim_Facility", "SubstationZone")]}),

            # Diurnal Power Flow Line Chart
            make_visual("chart_diurnal", "lineChart", 40, 230, 1140, 480, {
                "Category": [column_ref("Dim_Time", "HourFormatted")],
                "Y": [
                    sum_ref("Fact_EnergyConsumption", "ActivePower_kWh"),
                    sum_ref("Fact_EnergyConsumption", "SolarGeneration_kWh"),
                    sum_ref("Fact_EnergyConsumption", "NetGridImport_kWh")
                ]
            }),

            # Facility Consumption Ranking Bar Chart
            make_visual("chart_fac_rank", "clusteredBarChart", 1200, 230, 680, 480, {
                "Category": [column_ref("Dim_Facility", "FacilityName")],
                "Y": [measure_ref("Fact_EnergyConsumption", "Total Active Consumption (GWh)")]
            }),

            # Facility Table Benchmark
            make_visual("tbl_fac_detail", "tableEx", 40, 730, 1840, 310, {
                "Values": [
                    column_ref("Dim_Facility", "FacilityID"),
                    column_ref("Dim_Facility", "FacilityName"),
                    column_ref("Dim_Facility", "Category"),
                    column_ref("Dim_Facility", "Area_SqFt"),
                    column_ref("Dim_Facility", "EnergyStarRating"),
                    measure_ref("Fact_EnergyConsumption", "Total Active Consumption (GWh)"),
                    measure_ref("Fact_EnergyConsumption", "Total Electricity Spend (Cr)"),
                    measure_ref("Fact_EnergyConsumption", "Total Solar Generation (GWh)"),
                    measure_ref("Fact_EnergyConsumption", "Solar Penetration %")
                ]
            })
        ]
        for v in p1_visuals:
            v_folder = os.path.join(p1_vis_dir, v["name"])
            os.makedirs(v_folder, exist_ok=True)
            with open(os.path.join(v_folder, "visual.json"), "w", encoding="utf-8") as f:
                json.dump(v, f, indent=2)

        # --- Page 2: 24x7 Matrix & Submetering ---
        p2_dir = os.path.join(rp_pages, p2_id)
        p2_vis_dir = os.path.join(p2_dir, "visuals")
        os.makedirs(p2_vis_dir, exist_ok=True)
        with open(os.path.join(p2_dir, "page.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": P_SCHEMA, "name": p2_id, "displayName": "2 24x7 Matrix & Submetering",
                "displayOption": "FitToPage", "height": 1080, "width": 1920
            }, f, indent=2)

        p2_visuals = [
            make_visual("p2_c1", "card", 40, 20, 430, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Peak Period Consumption (GWh)")]}),
            make_visual("p2_c2", "card", 500, 20, 430, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Off-Peak Consumption (GWh)")]}),
            make_visual("p2_c3", "card", 960, 20, 430, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Average Power Factor")]}),
            make_visual("p2_c4", "card", 1420, 20, 460, 100, {"Values": [measure_ref("Fact_EnergyConsumption", "Net Grid Import (GWh)")]}),

            # 24x7 Heatmap Pivot Matrix
            make_visual("matrix_247", "pivotTable", 40, 140, 1180, 520, {
                "Rows": [column_ref("Dim_Date", "DayName")],
                "Columns": [column_ref("Dim_Time", "HourFormatted")],
                "Values": [sum_ref("Fact_EnergyConsumption", "ActivePower_kWh")]
            }),

            # Donut: Appliance Submetering
            make_visual("donut_submeter", "donutChart", 1240, 140, 640, 520, {
                "Category": [column_ref("Dim_Appliance", "SubmeterCategory")],
                "Y": [sum_ref("Fact_ApplianceSubmeter", "Submeter_kWh")]
            }),

            # Tariff Category Column Chart
            make_visual("col_tariff", "clusteredColumnChart", 40, 680, 940, 360, {
                "Category": [column_ref("Dim_Tariff", "TariffName")],
                "Y": [sum_ref("Fact_EnergyConsumption", "Cost_INR")]
            }),

            # Submeter Detail Table
            make_visual("tbl_sub_detail", "tableEx", 1000, 680, 880, 360, {
                "Values": [
                    column_ref("Dim_Appliance", "ApplianceID"),
                    column_ref("Dim_Appliance", "SubmeterCategory"),
                    column_ref("Dim_Appliance", "Description"),
                    sum_ref("Fact_ApplianceSubmeter", "Submeter_kWh")
                ]
            })
        ]
        for v in p2_visuals:
            v_folder = os.path.join(p2_vis_dir, v["name"])
            os.makedirs(v_folder, exist_ok=True)
            with open(os.path.join(v_folder, "visual.json"), "w", encoding="utf-8") as f:
                json.dump(v, f, indent=2)

        # --- Page 3: ML Forecasting & Anomalies ---
        p3_dir = os.path.join(rp_pages, p3_id)
        p3_vis_dir = os.path.join(p3_dir, "visuals")
        os.makedirs(p3_vis_dir, exist_ok=True)
        with open(os.path.join(p3_dir, "page.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": P_SCHEMA, "name": p3_id, "displayName": "3 ML Forecast & Anomaly Audit",
                "displayOption": "FitToPage", "height": 1080, "width": 1920
            }, f, indent=2)

        p3_visuals = [
            make_visual("p3_c1", "card", 40, 20, 580, 100, {"Values": [measure_ref("Fact_DemandForecast", "Forecast Projected Demand (kWh)")]}),
            make_visual("p3_c2", "card", 660, 20, 580, 100, {"Values": [measure_ref("Fact_Anomalies_Detailed", "Wasted Anomaly Cost (INR)")]}),
            make_visual("p3_c3", "card", 1280, 20, 600, 100, {"Values": [measure_ref("Fact_Anomalies_Detailed", "Excess Unscheduled Load (kWh)")]}),

            # Forecast Line Chart with Confidence Bounds
            make_visual("chart_forecast", "lineChart", 40, 140, 1140, 480, {
                "Category": [column_ref("Fact_DemandForecast", "Date")],
                "Y": [
                    sum_ref("Fact_DemandForecast", "Actual_kWh"),
                    sum_ref("Fact_DemandForecast", "Forecast_kWh"),
                    sum_ref("Fact_DemandForecast", "Upper95_kWh"),
                    sum_ref("Fact_DemandForecast", "Lower95_kWh")
                ]
            }),

            # Shewhart Control Chart
            make_visual("chart_shewhart", "lineChart", 1200, 140, 680, 480, {
                "Category": [column_ref("Fact_Anomalies_Detailed", "Timestamp")],
                "Y": [
                    sum_ref("Fact_Anomalies_Detailed", "ActivePower_kWh"),
                    sum_ref("Fact_Anomalies_Detailed", "UpperLimit_kWh"),
                    sum_ref("Fact_Anomalies_Detailed", "RollingMean_kWh")
                ]
            }),

            # Detailed Anomaly Audit Table
            make_visual("tbl_anom_audit", "tableEx", 40, 640, 1840, 400, {
                "Values": [
                    column_ref("Fact_Anomalies_Detailed", "Timestamp"),
                    column_ref("Fact_Anomalies_Detailed", "FacilityID"),
                    column_ref("Fact_Anomalies_Detailed", "ActivePower_kWh"),
                    column_ref("Fact_Anomalies_Detailed", "RollingMean_kWh"),
                    column_ref("Fact_Anomalies_Detailed", "UpperLimit_kWh"),
                    column_ref("Fact_Anomalies_Detailed", "Excess_kWh"),
                    column_ref("Fact_Anomalies_Detailed", "WastedCost_INR"),
                    column_ref("Fact_Anomalies_Detailed", "AnomalyType"),
                    column_ref("Fact_Anomalies_Detailed", "Severity")
                ]
            })
        ]
        for v in p3_visuals:
            v_folder = os.path.join(p3_vis_dir, v["name"])
            os.makedirs(v_folder, exist_ok=True)
            with open(os.path.join(v_folder, "visual.json"), "w", encoding="utf-8") as f:
                json.dump(v, f, indent=2)

        print(f"Successfully generated Power BI Project (.pbip) in {base_folder}")

if __name__ == "__main__":
    build_solution()
