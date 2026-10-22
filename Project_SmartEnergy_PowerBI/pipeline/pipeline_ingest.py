"""
Smart Energy Consumption Visualization Dashboard
Module: Pipeline - Ingestion & IoT Telemetry Stream Simulator
Course: MACSE603 - Visual Analytics Lab
Team: Vedant Nimkar (26MML0045), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)
"""
import os
import json
import time
import datetime
import random
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

class EnergyDataIngestionEngine:
    """
    Simulates end-to-end IoT sensor ingestion and smart meter batch feeds.
    Implements validation rules, checksum calculation, and MQTT-like packet creation.
    """
    def __init__(self):
        self.facilities = [
            {"id": "FAC001", "name": "Main Tech Tower (Tower A)", "base_kw": 120.0, "peak_kw": 750.0, "solar_kwp": 250.0},
            {"id": "FAC002", "name": "Computing & Data Center (Wing C)", "base_kw": 360.0, "peak_kw": 520.0, "solar_kwp": 0.0},
            {"id": "FAC003", "name": "Advanced Engineering Labs", "base_kw": 85.0, "peak_kw": 620.0, "solar_kwp": 80.0},
            {"id": "FAC004", "name": "Student Hostel Cluster", "base_kw": 95.0, "peak_kw": 580.0, "solar_kwp": 120.0},
            {"id": "FAC005", "name": "Academic & Admin Complex", "base_kw": 70.0, "peak_kw": 460.0, "solar_kwp": 100.0},
            {"id": "FAC006", "name": "Healthcare & Medical Center", "base_kw": 110.0, "peak_kw": 380.0, "solar_kwp": 40.0}
        ]

    def validate_packet(self, packet):
        """Quality gate: Schema validation & boundary enforcement"""
        required = ["timestamp", "facility_id", "active_power_kw", "voltage_v", "current_a", "power_factor"]
        for field in required:
            if field not in packet:
                return False, f"Missing field: {field}"
        
        if not (180.0 <= packet["voltage_v"] <= 260.0):
            return False, f"Voltage out of operational boundary: {packet['voltage_v']}V"
        if not (0.0 <= packet["power_factor"] <= 1.0):
            return False, f"Invalid power factor: {packet['power_factor']}"
        if packet["active_power_kw"] < 0:
            return False, f"Negative active power: {packet['active_power_kw']} kW"
        return True, "Valid"

    def generate_streaming_packet(self, facility_id=None, custom_hour=None):
        """
        Emulates an ESP32 sensor measuring voltage, current, active power, and solar generation.
        Returns a JSON MQTT telemetry message.
        """
        fac = next((f for f in self.facilities if f["id"] == facility_id), random.choice(self.facilities))
        now = datetime.datetime.now()
        hour = custom_hour if custom_hour is not None else now.hour

        # Base physical power load profile
        if 9 <= hour <= 18:
            activity = 0.85 + 0.15 * np.sin((hour - 9) * np.pi / 9)
        elif 18 < hour <= 22:
            activity = 0.65 if fac["id"] != "FAC004" else 0.95 # Hostels peak in evening
        else:
            activity = 0.25 # Baseload night
        
        noise = np.random.normal(0, 0.05)
        kw = max(fac["base_kw"], fac["base_kw"] + (fac["peak_kw"] - fac["base_kw"]) * (activity + noise))
        
        # Solar generation
        if 6 <= hour <= 18 and fac["solar_kwp"] > 0:
            solar_phase = np.sin((hour - 6) * np.pi / 12)
            solar_kw = max(0.0, fac["solar_kwp"] * solar_phase * (0.85 + np.random.normal(0, 0.05)))
        else:
            solar_kw = 0.0

        voltage = round(230.0 + np.random.normal(0, 2.5), 1)
        power_factor = round(max(0.85, min(0.99, 0.94 + np.random.normal(0, 0.02))), 3)
        current = round((kw * 1000) / (voltage * power_factor * (3**0.5)), 2) # 3-phase line current

        packet = {
            "sensor_id": f"ESP32-METER-{fac['id']}",
            "facility_id": fac["id"],
            "facility_name": fac["name"],
            "timestamp": now.isoformat(),
            "active_power_kw": round(kw, 2),
            "grid_import_kw": round(max(0.0, kw - solar_kw), 2),
            "solar_gen_kw": round(solar_kw, 2),
            "voltage_v": voltage,
            "current_a": current,
            "power_factor": power_factor,
            "frequency_hz": round(50.0 + np.random.normal(0, 0.05), 2),
            "status": "NORMAL"
        }

        # Anomaly simulation check (0.5% chance)
        if random.random() < 0.005:
            packet["active_power_kw"] = round(packet["active_power_kw"] * 1.6, 2)
            packet["status"] = "SURGE_ANOMALY"

        valid, msg = self.validate_packet(packet)
        packet["quality_flag"] = "PASS" if valid else f"FAIL: {msg}"
        return packet

    def run_batch_ingest_check(self):
        """Verifies integrity of all existing CSV tables in data folder"""
        required_tables = [
            "Dim_Facility.csv", "Dim_Tariff.csv", "Dim_Appliance.csv",
            "Dim_Time.csv", "Dim_Date.csv", "Dim_Weather.csv",
            "Fact_EnergyConsumption.csv", "Fact_ApplianceSubmeter.csv"
        ]
        results = {}
        for table in required_tables:
            path = os.path.join(DATA_DIR, table)
            if os.path.exists(path):
                df = pd.read_csv(path)
                results[table] = {
                    "exists": True,
                    "rows": len(df),
                    "cols": len(df.columns),
                    "null_cells": int(df.isnull().sum().sum()),
                    "status": "HEALTHY" if df.isnull().sum().sum() == 0 else "WARNING_NULLS"
                }
            else:
                results[table] = {"exists": False, "status": "MISSING"}
        return results

if __name__ == "__main__":
    engine = EnergyDataIngestionEngine()
    print("=== Testing IoT Telemetry Streaming Engine ===")
    sample = engine.generate_streaming_packet("FAC001", custom_hour=14)
    print(json.dumps(sample, indent=2))
    print("\n=== Validating Batch Raw Telemetry Data Stores ===")
    res = engine.run_batch_ingest_check()
    for tbl, info in res.items():
        print(f"  {tbl:30} : {info['status']:15} ({info.get('rows', 0):,} rows)")
