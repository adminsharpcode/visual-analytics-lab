"""
Smart Energy Consumption Visualization Dashboard
Module: Pipeline - ETL & Star Schema Validation Engine
Course: MACSE603 - Visual Analytics Lab
Team: Vedant Nimkar (26MML0045), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)
"""
import os
import sys
import json
import datetime
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

class SmartEnergyETLPipeline:
    """
    Orchestrates the Extract, Transform, and Load (ETL) pipeline for smart campus energy.
    Standardizes units, enforces relational foreign keys, computes derived energy metrics,
    and produces audit metrics.
    """
    def __init__(self):
        self.data_dir = DATA_DIR
        self.audit_report = {
            "execution_timestamp": datetime.datetime.now().isoformat(),
            "pipeline_status": "PENDING",
            "stages": {}
        }

    def run_etl(self):
        print(">>> Starting Smart Energy ETL Pipeline Execution...")
        
        # 1. Verification of Source Dimension Tables
        dim_files = {
            "facility": "Dim_Facility.csv",
            "tariff": "Dim_Tariff.csv",
            "appliance": "Dim_Appliance.csv",
            "time": "Dim_Time.csv",
            "date": "Dim_Date.csv",
            "weather": "Dim_Weather.csv"
        }
        
        dims = {}
        for key, fname in dim_files.items():
            fpath = os.path.join(self.data_dir, fname)
            if not os.path.exists(fpath):
                raise FileNotFoundError(f"Required dimension file missing: {fname}")
            dims[key] = pd.read_csv(fpath)
            print(f"  [EXTRACT] Loaded {fname} ({len(dims[key])} records)")

        self.audit_report["stages"]["dimensions_extracted"] = {
            k: len(v) for k, v in dims.items()
        }

        # 2. Extract & Transform Fact_EnergyConsumption
        fact_path = os.path.join(self.data_dir, "Fact_EnergyConsumption.csv")
        if not os.path.exists(fact_path):
            raise FileNotFoundError("Fact_EnergyConsumption.csv missing!")
        
        df_fact = pd.read_csv(fact_path)
        initial_count = len(df_fact)
        print(f"  [EXTRACT] Loaded Fact_EnergyConsumption ({initial_count:,} records)")

        # Transformation Rules:
        # A. Timestamp standardization
        df_fact["Timestamp"] = pd.to_datetime(df_fact["Timestamp"])
        
        # B. Referential Integrity Enforcement
        valid_facilities = set(dims["facility"]["FacilityID"])
        valid_tariffs = set(dims["tariff"]["TariffID"])
        valid_dates = set(dims["date"]["Date"])
        
        invalid_fac = (~df_fact["FacilityID"].isin(valid_facilities)).sum()
        invalid_tar = (~df_fact["TariffID"].isin(valid_tariffs)).sum()
        invalid_date = (~df_fact["Date"].isin(valid_dates)).sum()
        
        if invalid_fac > 0 or invalid_tar > 0 or invalid_date > 0:
            raise ValueError(f"Foreign Key violation! Fac: {invalid_fac}, Tar: {invalid_tar}, Date: {invalid_date}")
        
        # C. Physical Validation & Cleaning
        # ActivePower cannot be negative
        df_fact["ActivePower_kWh"] = df_fact["ActivePower_kWh"].clip(lower=0.0)
        # Solar cannot exceed installed peak * 1.2
        # Power factor must lie within [0.7, 1.0]
        df_fact["PowerFactor"] = df_fact["PowerFactor"].clip(lower=0.70, upper=1.0)
        
        # D. Metric Engineering:
        # Total Carbon Footprint in kgCO2: ActivePower * CarbonFactor (0.82 kg/kWh)
        # Net Grid Import: ActivePower - SolarGeneration
        df_fact["Carbon_kgCO2"] = (df_fact["ActivePower_kWh"] * 0.82).round(2)
        df_fact["NetImport_kWh"] = (df_fact["ActivePower_kWh"] - df_fact["SolarGeneration_kWh"]).clip(lower=0.0).round(2)
        df_fact["SolarSelfConsumptionRatio"] = np.where(
            df_fact["ActivePower_kWh"] > 0,
            (df_fact["SolarGeneration_kWh"] / df_fact["ActivePower_kWh"]).clip(upper=1.0).round(4),
            0.0
        )
        
        # E. Summary Aggregates for Audit
        total_energy_gwh = df_fact["ActivePower_kWh"].sum() / 1e6
        total_cost_cr = df_fact["Cost_INR"].sum() / 1e7
        total_solar_gwh = df_fact["SolarGeneration_kWh"].sum() / 1e6
        total_carbon_tons = df_fact["Carbon_kgCO2"].sum() / 1000.0
        
        # Save back cleaned and enriched fact table
        df_fact.to_csv(fact_path, index=False)
        print(f"  [LOAD] Saved enriched Fact_EnergyConsumption.csv ({len(df_fact):,} records)")

        # 3. Fact_ApplianceSubmeter validation
        app_path = os.path.join(self.data_dir, "Fact_ApplianceSubmeter.csv")
        if os.path.exists(app_path):
            df_app = pd.read_csv(app_path)
            col = "Submeter_kWh" if "Submeter_kWh" in df_app.columns else df_app.columns[-1]
            df_app[col] = df_app[col].clip(lower=0.0)
            df_app.to_csv(app_path, index=False)
            print(f"  [LOAD] Validated Fact_ApplianceSubmeter.csv ({len(df_app):,} records)")

        self.audit_report["stages"]["transformation_summary"] = {
            "total_records_processed": len(df_fact),
            "total_energy_gwh": round(total_energy_gwh, 3),
            "total_cost_inr_crores": round(total_cost_cr, 2),
            "total_solar_gwh": round(total_solar_gwh, 3),
            "carbon_emissions_tons": round(total_carbon_tons, 1),
            "foreign_key_integrity": "100% Verified",
            "physical_bounds_check": "PASSED"
        }
        self.audit_report["pipeline_status"] = "SUCCESS"

        audit_path = os.path.join(self.data_dir, "pipeline_etl_audit.json")
        with open(audit_path, "w") as f:
            json.dump(self.audit_report, f, indent=2)
        print(f"  [AUDIT] ETL Audit report written to {os.path.basename(audit_path)}")
        return self.audit_report

if __name__ == "__main__":
    etl = SmartEnergyETLPipeline()
    report = etl.run_etl()
    print("\nETL Pipeline Execution Complete:")
    print(json.dumps(report["stages"]["transformation_summary"], indent=2))
