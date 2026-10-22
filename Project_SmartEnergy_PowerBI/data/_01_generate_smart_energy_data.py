"""
Smart Energy Consumption Visualization Dashboard
Data Generation Engine - Star Schema & High-Fidelity Energy Telemetry
Course: MACSE603 - Visual Analytics Lab
Team: Vedant Nimkar (26MML0045), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)
"""
import os
import datetime
import numpy as np
import pandas as pd

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

print("--- Generating Star-Schema Smart Energy Telemetry ---")

# 1. Dim_Facility
facilities = [
    {
        "FacilityID": "FAC001",
        "FacilityName": "Main Tech Tower (Tower A)",
        "Category": "Commercial",
        "Area_SqFt": 185000,
        "Occupancy_Capacity": 1200,
        "Baseline_kW": 120.0,
        "PeakDesign_kW": 750.0,
        "EnergyStarRating": 84,
        "SubstationZone": "Zone 1 - North Campus",
        "Solar_kWp": 250.0
    },
    {
        "FacilityID": "FAC002",
        "FacilityName": "Computing & Data Center (Wing C)",
        "Category": "DataCenter",
        "Area_SqFt": 45000,
        "Occupancy_Capacity": 80,
        "Baseline_kW": 360.0,
        "PeakDesign_kW": 520.0,
        "EnergyStarRating": 91,
        "SubstationZone": "Zone 2 - Central Grid",
        "Solar_kWp": 0.0
    },
    {
        "FacilityID": "FAC003",
        "FacilityName": "Advanced Engineering Labs & Workshop",
        "Category": "Industrial",
        "Area_SqFt": 95000,
        "Occupancy_Capacity": 450,
        "Baseline_kW": 85.0,
        "PeakDesign_kW": 620.0,
        "EnergyStarRating": 76,
        "SubstationZone": "Zone 3 - West Grid",
        "Solar_kWp": 80.0
    },
    {
        "FacilityID": "FAC004",
        "FacilityName": "Student Hostel Cluster (Block B & C)",
        "Category": "Residential",
        "Area_SqFt": 220000,
        "Occupancy_Capacity": 1600,
        "Baseline_kW": 95.0,
        "PeakDesign_kW": 580.0,
        "EnergyStarRating": 79,
        "SubstationZone": "Zone 1 - North Campus",
        "Solar_kWp": 120.0
    },
    {
        "FacilityID": "FAC005",
        "FacilityName": "Academic & Administrative Complex",
        "Category": "Educational",
        "Area_SqFt": 130000,
        "Occupancy_Capacity": 900,
        "Baseline_kW": 70.0,
        "PeakDesign_kW": 460.0,
        "EnergyStarRating": 88,
        "SubstationZone": "Zone 2 - Central Grid",
        "Solar_kWp": 100.0
    },
    {
        "FacilityID": "FAC006",
        "FacilityName": "Healthcare & Medical Center",
        "Category": "Healthcare",
        "Area_SqFt": 65000,
        "Occupancy_Capacity": 250,
        "Baseline_kW": 110.0,
        "PeakDesign_kW": 380.0,
        "EnergyStarRating": 82,
        "SubstationZone": "Zone 3 - West Grid",
        "Solar_kWp": 40.0
    }
]
df_facility = pd.DataFrame(facilities)
df_facility.to_csv(os.path.join(DATA_DIR, "Dim_Facility.csv"), index=False)
print(f" Dim_Facility.csv: {len(df_facility)} records written.")

# 2. Dim_Tariff
tariffs = [
    {
        "TariffID": "TAR_TOU_HT",
        "TariffName": "High Tension Time-of-Use (HT-ToU)",
        "Category": "Commercial/Industrial",
        "PeakRate_INR": 11.50,
        "ShoulderRate_INR": 7.80,
        "OffPeakRate_INR": 4.50,
        "DemandCharge_INR_kW": 350.0,
        "CarbonFactor_kgCO2_kWh": 0.82
    },
    {
        "TariffID": "TAR_TOU_LT",
        "TariffName": "Low Tension Commercial/Inst (LT-ToU)",
        "Category": "Institutional",
        "PeakRate_INR": 10.20,
        "ShoulderRate_INR": 7.10,
        "OffPeakRate_INR": 4.20,
        "DemandCharge_INR_kW": 280.0,
        "CarbonFactor_kgCO2_kWh": 0.82
    },
    {
        "TariffID": "TAR_RES_SLAB",
        "TariffName": "Residential Telescopic ToU",
        "Category": "Residential",
        "PeakRate_INR": 8.80,
        "ShoulderRate_INR": 6.20,
        "OffPeakRate_INR": 3.80,
        "DemandCharge_INR_kW": 150.0,
        "CarbonFactor_kgCO2_kWh": 0.82
    }
]
df_tariff = pd.DataFrame(tariffs)
df_tariff.to_csv(os.path.join(DATA_DIR, "Dim_Tariff.csv"), index=False)
print(f" Dim_Tariff.csv: {len(df_tariff)} records written.")

# 3. Dim_Appliance / Submeter
appliances = [
    {"ApplianceID": "APP_HVAC", "SubmeterCategory": "HVAC & Chillers", "Description": "Central chillers, cooling towers, air handling units (AHUs)", "AvgShare_Pct": 42.0},
    {"ApplianceID": "APP_LIGHT", "SubmeterCategory": "Lighting & Receptacles", "Description": "LED arrays, architectural lighting, wall sockets", "AvgShare_Pct": 18.0},
    {"ApplianceID": "APP_IT", "SubmeterCategory": "Server & IT Infrastructure", "Description": "Server racks, UPS systems, network switches, workstation bays", "AvgShare_Pct": 22.0},
    {"ApplianceID": "APP_MACH", "SubmeterCategory": "Heavy Machinery & Motors", "Description": "Elevators, hydraulic pumps, CNC machines, ventilation fans", "AvgShare_Pct": 12.0},
    {"ApplianceID": "APP_AUX", "SubmeterCategory": "Auxiliary & Water Systems", "Description": "Water treatment, booster pumps, perimeter security", "AvgShare_Pct": 6.0}
]
df_appliance = pd.DataFrame(appliances)
df_appliance.to_csv(os.path.join(DATA_DIR, "Dim_Appliance.csv"), index=False)
print(f" Dim_Appliance.csv: {len(df_appliance)} records written.")

# 4. Dim_Time (24 hours)
time_records = []
for h in range(24):
    if 6 <= h < 9:
        period = "Morning Rush"
        t_band = "Shoulder"
    elif 9 <= h < 17:
        period = "Working Day"
        t_band = "Shoulder"
    elif 17 <= h < 22:
        period = "Evening Peak"
        t_band = "Peak"
    else:
        period = "Night Baseload"
        t_band = "Off-Peak"
    
    time_records.append({
        "Hour": h,
        "HourFormatted": f"{h:02d}:00",
        "Hour12": f"{(h%12 if h%12!=0 else 12)} {'AM' if h < 12 else 'PM'}",
        "PeriodOfDay": period,
        "TariffBand": t_band,
        "PeakTariffFlag": 1 if t_band == "Peak" else 0
    })
df_time = pd.DataFrame(time_records)
df_time.to_csv(os.path.join(DATA_DIR, "Dim_Time.csv"), index=False)
print(f" Dim_Time.csv: {len(df_time)} records written.")

# 5. Date Dimension & Weather Generation (2024-01-01 to 2025-12-31 = 731 days)
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2025, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq="D")

date_records = []
weather_records = []

for dt in date_range:
    d_str = dt.strftime("%Y-%m-%d")
    month = dt.month
    day_of_week = dt.weekday() # 0 = Monday, 6 = Sunday
    is_weekend = 1 if day_of_week >= 5 else 0
    day_name = dt.strftime("%A")
    month_name = dt.strftime("%B")
    quarter = f"Q{(month-1)//3 + 1}"
    year = dt.year
    
    # Season
    if month in [12, 1, 2]:
        season = "Winter"
        base_temp = 21.0
    elif month in [3, 4, 5]:
        season = "Summer"
        base_temp = 34.0
    elif month in [6, 7, 8, 9]:
        season = "Monsoon"
        base_temp = 28.0
    else:
        season = "Post-Monsoon"
        base_temp = 25.0
        
    date_records.append({
        "Date": d_str,
        "Year": year,
        "Quarter": quarter,
        "Month": month,
        "MonthName": month_name,
        "WeekNum": dt.isocalendar()[1],
        "DayOfMonth": dt.day,
        "DayOfWeek": day_of_week,
        "DayName": day_name,
        "IsWeekend": is_weekend,
        "Season": season
    })
    
    # Hourly weather simulation for this day
    # Diurnal temperature cycle: lowest at 05:00, peak at 14:00
    daily_t_amp = 7.5 + np.random.normal(0, 1.0)
    for h in range(24):
        # Sine wave peaked at hour 14
        t_phase = (h - 9) * (2 * np.pi / 24)
        t_hour = base_temp + (daily_t_amp / 2.0) * np.sin(t_phase) + np.random.normal(0, 0.4)
        
        # Solar irradiance (W/m2): zero before 06:00 and after 18:30
        if 6 <= h <= 18:
            sol_phase = (h - 6) * (np.pi / 12)
            max_sol = 880 if season == "Summer" else (620 if season == "Monsoon" else 750)
            solar_irr = max_sol * np.sin(sol_phase) + np.random.normal(0, 20)
            solar_irr = max(0.0, solar_irr)
        else:
            solar_irr = 0.0
            
        humidity = max(20.0, min(95.0, 65.0 - 0.9 * (t_hour - 25.0) + np.random.normal(0, 3.5)))
        
        cdd = max(0.0, t_hour - 24.0) # Cooling Degree Hours (>24 C)
        hdd = max(0.0, 18.0 - t_hour) # Heating Degree Hours (<18 C)
        
        weather_records.append({
            "Date": d_str,
            "Hour": h,
            "AmbientTemp_C": round(t_hour, 2),
            "Humidity_Pct": round(humidity, 1),
            "SolarIrradiance_W_m2": round(solar_irr, 1),
            "CoolingDegreeHours": round(cdd, 2),
            "HeatingDegreeHours": round(hdd, 2)
        })

df_date = pd.DataFrame(date_records)
df_date.to_csv(os.path.join(DATA_DIR, "Dim_Date.csv"), index=False)
print(f" Dim_Date.csv: {len(df_date)} records written.")

df_weather = pd.DataFrame(weather_records)
df_weather.to_csv(os.path.join(DATA_DIR, "Dim_Weather.csv"), index=False)
print(f" Dim_Weather.csv: {len(df_weather)} records written.")

# 6. Fact_EnergyConsumption Generation
# To balance file size and granular analytics, we generate 1 full year of hourly telemetry
# for all 6 facilities (2025: 365 days * 24 hours * 6 facilities = 52,560 records).
print("Simulating physics-based energy consumption across all facilities for 2025...")

target_dates = [d for d in date_records if d["Year"] == 2025]
weather_dict = {(w["Date"], w["Hour"]): w for w in weather_records if w["Date"].startswith("2025")}

fact_records = []
appliance_records = []

# Mapping facility to tariff
fac_tariff_map = {
    "FAC001": "TAR_TOU_HT",
    "FAC002": "TAR_TOU_HT",
    "FAC003": "TAR_TOU_HT",
    "FAC004": "TAR_RES_SLAB",
    "FAC005": "TAR_TOU_LT",
    "FAC006": "TAR_TOU_LT",
}

# Precompute injected anomalies for demonstration
# Anomaly 1: Weekend Chiller Stuck On (FAC001) - 2025-05-17 and 2025-05-18 (Saturday & Sunday)
# Anomaly 2: Night Baseload Leak (FAC003) - 2025-08-11 to 2025-08-14 (Hours 00:00 - 05:00)
# Anomaly 3: Solar Inverter Dropout (FAC001) - 2025-07-08 (Midday solar collapsed to 0)
# Anomaly 4: Extreme Summer Surge (FAC005) - 2025-06-03 (Chiller overload)

for d in target_dates:
    d_str = d["Date"]
    is_weekend = d["IsWeekend"]
    
    for fac in facilities:
        fid = fac["FacilityID"]
        fcat = fac["Category"]
        base_kw = fac["Baseline_kW"]
        peak_des = fac["PeakDesign_kW"]
        solar_kwp = fac["Solar_kWp"]
        tid = fac_tariff_map[fid]
        tariff_info = next(t for t in tariffs if t["TariffID"] == tid)
        
        for h in range(24):
            w = weather_dict.get((d_str, h), {"AmbientTemp_C": 26.0, "SolarIrradiance_W_m2": 0.0, "CoolingDegreeHours": 2.0})
            temp_c = w["AmbientTemp_C"]
            irr = w["SolarIrradiance_W_m2"]
            cdd = w["CoolingDegreeHours"]
            
            # Base diurnal profile per facility category
            if fcat == "Commercial": # FAC001: 8 AM - 6 PM peak, reduced on weekends
                if is_weekend:
                    occ_factor = 0.12
                else:
                    occ_factor = 0.90 if 9 <= h <= 17 else (0.50 if (7 <= h < 9 or 17 < h <= 19) else 0.10)
                cooling_sensitivity = 14.5 # kW per degree above 24C
            
            elif fcat == "DataCenter": # FAC002: 24/7 flat baseload (~80-90% peak)
                occ_factor = 0.88 + 0.05 * np.sin(h * 2 * np.pi / 24)
                cooling_sensitivity = 6.0
                
            elif fcat == "Industrial": # FAC003: 7 AM - 4 PM shifts, low weekend
                if is_weekend:
                    occ_factor = 0.08
                else:
                    occ_factor = 0.92 if 8 <= h <= 16 else 0.15
                cooling_sensitivity = 8.0
                
            elif fcat == "Residential": # FAC004: Morning peak (7-9), strong evening peak (18-23)
                if 7 <= h <= 9:
                    occ_factor = 0.75
                elif 18 <= h <= 23:
                    occ_factor = 0.95
                elif 10 <= h <= 17:
                    occ_factor = 0.35 if not is_weekend else 0.65
                else:
                    occ_factor = 0.28
                cooling_sensitivity = 11.0
                
            elif fcat == "Educational": # FAC005: 8 AM - 5 PM
                occ_factor = 0.85 if (8 <= h <= 17 and not is_weekend) else 0.08
                cooling_sensitivity = 9.5
                
            elif fcat == "Healthcare": # FAC006: 24/7 continuous baseline with daytime activity
                occ_factor = 0.82 if 8 <= h <= 18 else 0.60
                cooling_sensitivity = 7.0
            
            # Active Power Demand (kW)
            weather_load = cdd * cooling_sensitivity
            noise = np.random.normal(0, base_kw * 0.04)
            kw_demand = base_kw + (peak_des - base_kw) * occ_factor + weather_load + noise
            kw_demand = max(base_kw * 0.75, kw_demand)
            
            # Anomaly injection
            anom_flag = 0
            anom_desc = "Normal"
            
            # Anomaly 1: Weekend Chiller Stuck On (FAC001)
            if fid == "FAC001" and d_str in ["2025-05-17", "2025-05-18"] and 8 <= h <= 20:
                kw_demand += 280.0 # Huge cooling load running empty
                anom_flag = 1
                anom_desc = "HVAC Weekend Fault / Baseload Leak"
                
            # Anomaly 2: Night Baseload Leak (FAC003)
            if fid == "FAC003" and d_str in ["2025-08-11", "2025-08-12", "2025-08-13", "2025-08-14"] and 0 <= h <= 5:
                kw_demand += 165.0 # Air compressor left running
                anom_flag = 1
                anom_desc = "Compressor Unattended Leak"
                
            # Anomaly 3: Solar Inverter Dropout (FAC001)
            solar_efficiency = 0.18
            if solar_kwp > 0:
                gen_kwh = (solar_kwp * (irr / 1000.0) * solar_efficiency * 5.2) + np.random.normal(0, 1.0)
                gen_kwh = max(0.0, gen_kwh)
                if fid == "FAC001" and d_str == "2025-07-08" and 10 <= h <= 15:
                    gen_kwh = 0.0
                    anom_flag = 1
                    anom_desc = "Rooftop Solar Inverter Trip"
            else:
                gen_kwh = 0.0
                
            # Anomaly 4: Extreme Summer Surge (FAC005)
            if fid == "FAC005" and d_str == "2025-06-03" and 12 <= h <= 16:
                kw_demand += 190.0
                anom_flag = 1
                anom_desc = "Thermal Overload / Peak Demand Spike"
                
            # 1 hour consumption in kWh = kw_demand * 1 hour
            active_kwh = round(kw_demand, 2)
            solar_kwh = round(gen_kwh, 2)
            net_grid_kwh = round(max(0.0, active_kwh - solar_kwh), 2)
            
            # Power factor & Reactive Power
            pf = np.random.uniform(0.92, 0.98) if anom_desc != "Compressor Unattended Leak" else 0.81
            reactive_kvarh = round(active_kwh * np.tan(np.arccos(pf)), 2)
            voltage = round(np.random.normal(415.0, 3.2), 1)
            
            # Tariff Calculation
            if 17 <= h < 22:
                rate = tariff_info["PeakRate_INR"]
                t_band = "Peak"
            elif 6 <= h < 17:
                rate = tariff_info["ShoulderRate_INR"]
                t_band = "Shoulder"
            else:
                rate = tariff_info["OffPeakRate_INR"]
                t_band = "Off-Peak"
                
            cost_inr = round(net_grid_kwh * rate, 2)
            co2_kg = round(net_grid_kwh * tariff_info["CarbonFactor_kgCO2_kWh"], 2)
            
            record = {
                "Timestamp": f"{d_str} {h:02d}:00:00",
                "Date": d_str,
                "Hour": h,
                "FacilityID": fid,
                "TariffID": tid,
                "ActivePower_kWh": active_kwh,
                "ReactivePower_kVARh": reactive_kvarh,
                "PowerFactor": round(pf, 3),
                "Voltage_V": voltage,
                "TariffBand": t_band,
                "PeakPeriodFlag": 1 if t_band == "Peak" else 0,
                "SolarGeneration_kWh": solar_kwh,
                "NetGridImport_kWh": net_grid_kwh,
                "Cost_INR": cost_inr,
                "CarbonEmission_kgCO2": co2_kg,
                "AnomalyFlag": anom_flag,
                "AnomalyType": anom_desc
            }
            fact_records.append(record)
            
            # Submeter / Appliance breakdown (for sample dates or aggregated)
            # To avoid creating 250k+ records while still enabling granular appliance drill-through,
            # we write appliance telemetry for 1 representative week per month (approx 12,000 records)
            if d["DayOfMonth"] <= 7:
                # Disaggregate active_kwh into 5 submeter categories
                # Categories: HVAC, Lighting, IT, Heavy Machinery, Auxiliary
                if fcat == "Commercial":
                    shares = [0.45, 0.22, 0.18, 0.10, 0.05]
                elif fcat == "DataCenter":
                    shares = [0.38, 0.05, 0.52, 0.02, 0.03]
                elif fcat == "Industrial":
                    shares = [0.25, 0.12, 0.08, 0.48, 0.07]
                elif fcat == "Residential":
                    shares = [0.42, 0.28, 0.12, 0.08, 0.10]
                elif fcat == "Educational":
                    shares = [0.40, 0.25, 0.20, 0.08, 0.07]
                else: # Healthcare
                    shares = [0.46, 0.18, 0.15, 0.14, 0.07]
                    
                for app_idx, app_id in enumerate(["APP_HVAC", "APP_LIGHT", "APP_IT", "APP_MACH", "APP_AUX"]):
                    sub_kwh = round(active_kwh * shares[app_idx] * np.random.uniform(0.96, 1.04), 2)
                    appliance_records.append({
                        "Date": d_str,
                        "Hour": h,
                        "FacilityID": fid,
                        "ApplianceID": app_id,
                        "Submeter_kWh": sub_kwh
                    })

df_fact = pd.DataFrame(fact_records)
df_fact.to_csv(os.path.join(DATA_DIR, "Fact_EnergyConsumption.csv"), index=False)
print(f" Fact_EnergyConsumption.csv: {len(df_fact):,} records written.")

df_app_fact = pd.DataFrame(appliance_records)
df_app_fact.to_csv(os.path.join(DATA_DIR, "Fact_ApplianceSubmeter.csv"), index=False)
print(f" Fact_ApplianceSubmeter.csv: {len(df_app_fact):,} records written.")

# 7. Generate Summary Statistics
total_kwh = df_fact["ActivePower_kWh"].sum()
total_cost = df_fact["Cost_INR"].sum()
total_solar = df_fact["SolarGeneration_kWh"].sum()
total_anomalies = df_fact["AnomalyFlag"].sum()

print("\n--- Telemetry Generation Summary ---")
print(f"Total Active Energy: {total_kwh:,.1f} kWh ({total_kwh/1e6:.2f} GWh)")
print(f"Total Electricity Cost: INR {total_cost:,.2f} ({total_cost/1e7:.2f} Cr)")
print(f"Total Solar Generation: {total_solar:,.1f} kWh ({total_solar/total_kwh*100:.1f}% Solar Penetration)")
print(f"Total Operational Anomalies Flagged: {total_anomalies} events ({total_anomalies/len(df_fact)*100:.2f}%)")
print("All star schema tables successfully generated in data/ folder!")
