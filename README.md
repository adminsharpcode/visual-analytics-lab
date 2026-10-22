# ⚡ EnergyPulse BI: Smart Energy Consumption Visualization & Forecasting Dashboard

[![Live Dashboard on Vercel](https://img.shields.io/badge/Vercel-Live%20Dashboard-38bdf8?style=for-the-badge&logo=vercel&logoColor=white)](https://webdashboard-eta.vercel.app)
[![Pipeline Status](https://img.shields.io/badge/Pipeline-Active%20%26%20Verified-10b981?style=for-the-badge&logo=python&logoColor=white)](https://github.com/adminsharpcode/visual-analytics-lab)
[![Visual Analytics](https://img.shields.io/badge/Course-MACSE603%20Visual%20Analytics-8b5cf6?style=for-the-badge)](https://github.com/adminsharpcode/visual-analytics-lab)
[![Power BI Star Schema](https://img.shields.io/badge/Power%20BI-11%20Star%20Schema%20Tables-f59e0b?style=for-the-badge&logo=powerbi&logoColor=white)](https://github.com/adminsharpcode/visual-analytics-lab)
[![License](https://img.shields.io/badge/License-Academic%20MIT-blue?style=for-the-badge)](LICENSE)

> **M.Tech Visual Analytics Lab (MACSE603) — Comprehensive Academic Final Capstone Project**  
> An end-to-end industrial smart energy visual analytics system integrating **IoT telemetry ingestion**, a **11-table Star Schema warehouse (52,560 hourly records)**, **machine learning time-series forecasting ($R^2 = 0.996$)**, **Shewhart $\pm 3\sigma$ anomaly detection**, **$t$-SNE manifold clustering**, **Power BI dimensional measures**, and a **cyber-glassmorphism Apache ECharts HUD**.

---

### 🌐 Live Interactive Deployment
* **Production Web Dashboard**: [https://webdashboard-eta.vercel.app](https://webdashboard-eta.vercel.app)
* **Local HTTP Stream Engine**: `http://localhost:8085/index.html` (via `serve_dashboard.py`)

---

## 👥 Academic Project Team

| Member Name | Student PRN | Institutional Role | Primary Responsibilities |
| :--- | :--- | :--- | :--- |
| **Vedant Nimkar** | `26MML0045` | **Project Lead & Data Architect** | Star Schema Warehouse, ECharts Visual HUD, Vercel & Pipeline Orchestration |
| **Jitesh Bobde** | `26MML0025` | **Machine Learning & Statistical Lead** | Prophet/Ridge Demand Forecasting ($R^2=0.996$), Shewhart $3\sigma$ Anomaly Engine |
| **Ayush Sharma** | `26MML0043` | **BI Analytics & Power BI Engineer** | Power BI DAX Library (50+ Measures), Power Query M Scripts, Defense Slides Deck |

---

## 🏛️ End-to-End System Architecture

```
[ ESP32 IoT Sensors / Smart Meters (15-min Intervals) ]
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. INGESTION & DATA QUALITY ENGINE (pipeline_ingest.py)      │
│  • Microsecond streaming generator & schema boundary checks │
│  • Out-of-bounds voltage, reverse power, PF bounds validation│
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ETL & NORMALIZATION PIPELINE (pipeline_etl.py)           │
│  • Cooling Degree Hours (CDH) climate normalization (18.3°C)│
│  • Time-of-Use (ToU) tariff band indexing (Peak / Off-Peak) │
│  • Referential integrity & Star Schema dimension loading    │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ENTERPRISE STAR SCHEMA DATA WAREHOUSE (data/*.csv)       │
│  • Fact_EnergyConsumption (52,560 Hourly Records, FY 2025)  │
│  • Dim_Facility, Dim_Date, Dim_Time, Dim_Weather, Tariffs   │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ADVANCED ANALYTICS & ML ENGINE (pipeline_analytics.py)   │
│  • Ridge & Prophet Time-Series Forecaster (R²=0.996, MAPE) │
│  • Shewhart ±3σ Control Limits (196 Operational Anomalies)  │
│  • t-SNE 2D Manifold Load Shape Clustering (4 Archetypes)   │
│  • Carbon CEA Offset & Solar Self-Generation Calculator     │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. MULTI-MODAL PRESENTATION & DELIVERY LAYER                │
│  ├─ Interactive Cyber HUD (Apache ECharts + Vercel Cloud)   │
│  ├─ Power BI Desktop Star Schema (50+ DAX Measures & M)     │
│  ├─ 16-Slide Final Defense Presentation Deck (.pptx)        │
│  └─ Formatted Final Academic Report (ReportLab PDF & MD)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Visual Analytics & Publication Figures

The complete analytical suite generates 8 publication-grade visualization figures saved in `images/` and `Project_SmartEnergy_PowerBI/figures/`:

| Figure | Visual Analytics Module | Core Statistical Insight |
| :---: | :--- | :--- |
| **01** | **Executive KPI Ribbon & Monthly Trajectory** | 19.35 GWh annual load, ₹13.20 Cr expenditure, 1.14 GWh solar offset |
| **02** | **24×7 Diurnal Load-Profile Heatmap Matrix** | Weekday dual-peak intensity (10:00–12:00, 18:00–21:00) vs weekend base |
| **03** | **Top-N Facility Consumption & Sparklines** | Data Center Wing C baseline (4.69 GWh) vs Commercial Tech Tower (3.62 GWh) |
| **04** | **Prophet/Ridge 30-Day Demand Projection** | Expanding 95% confidence intervals, $R^2 = 0.996$, MAPE $= 0.61\%$ |
| **05** | **Shewhart $\pm 3\sigma$ Anomaly Control Limits** | 196 flagged breaches, isolating ground-truth injected chiller overnight leaks |
| **06** | **$t$-SNE 2D Manifold Load Shape Clusters** | 4 distinct clusters separating continuous, commercial, and residential profiles |
| **07** | **Appliance Submetering Breakdown** | HVAC & Chillers dominate at 42.0%, IT servers 22.0%, lighting 18.0% |
| **08** | **Solar Self-Generation vs. Grid Power Flow** | 590 kWp rooftop solar shaving 5.9% of daytime peak utility demand |

---

## 🗃️ Star Schema Dimensional Model (11 Tables)

The warehouse is partitioned according to Kimball dimensional modeling principles:

```
                  ┌───────────────┐
                  │   Dim_Date    │
                  └───────┬───────┘
                          │ 1
                          │
┌──────────────┐  *       ▼       *  ┌──────────────┐
│ Dim_Facility ├─────► [ Fact_  ] ◄──┤   Dim_Time   │
└──────────────┘       [ Energy ]    └──────────────┘
                       [ Cons.  ]
┌──────────────┐  *       ▲       *  ┌──────────────┐
│ Dim_Weather  ├──────────┼──────────┤  Dim_Tariff  │
└──────────────┘          │          └──────────────┘
                          │
                  ┌───────┴───────┐
                  │ Dim_Submeter  │
                  └───────────────┘
```

1. **`Fact_EnergyConsumption.csv`** (52,560 rows): Meter-level hourly active power, reactive power, voltage, power factor, solar generation, net import, cost, and carbon emissions.
2. **`Dim_Facility.csv`** (6 campus facilities): Footprint ($sq.ft$), occupancy, solar capacity ($kWp$), baseline load, Energy Star ratings.
3. **`Dim_Date.csv`** (365 calendar days): Date attributes, academic semester flags, fiscal periods, holiday flags.
4. **`Dim_Time.csv`** (24 hours): Hourly divisions, ToU tariff bands (Peak, Normal, Off-Peak).
5. **`Dim_Weather.csv`** (8,760 hourly climate records): Ambient temperature, solar irradiance ($W/m^2$), relative humidity, Cooling Degree Hours.
6. **`Dim_Tariff.csv`**: Time-of-Use rate schedule (₹4.80/kWh Off-Peak to ₹9.20/kWh Peak).
7. **`Dim_Submeter.csv`**: End-use categorization (HVAC, IT, Lighting, Machinery, Auxiliary).
8. **`Fact_DemandForecast.csv`**: Prophet 30-day projection with 95% upper and lower confidence intervals.
9. **`Fact_Anomalies_Detailed.csv`**: Ground-truth injected and Shewhart-flagged operational anomalies.
10. **`Fact_LoadClusters.csv`**: 2D $t$-SNE coordinates and k-means cluster labels.
11. **`Fact_ApplianceSubmeter.csv`**: Annual end-use consumption allocations.

---

## ⚡ Interactive Web Dashboard (Apache ECharts HUD)

The web dashboard is designed for mission-critical energy operations and features:
- **Offline Self-Contained ECharts**: Official bundled `echarts.min.js` (1.02 MB) with zero external CDN dependencies.
- **Cyber-Slate Aesthetics**: Custom high-contrast theme (`#060b17` base, `#101c38` card surfaces, `#38bdf8` cyan neon borders, `#ffffff` text values).
- **Interactive Slicers**: Dynamic facility filtering across all 6 facilities or aggregate campus view.
- **Temporal Granularity Toggles**: Instant switching between Hourly, Daily, and Monthly aggregates.
- **Live IoT Streaming Simulator**: Emulated ESP32 live packet generation with an animated oscilloscope and dial gauge.
- **Detailed Anomaly Audit Modal**: Full table inspection of observed loads, expected baselines, and financial cost impact.

---

## 🚀 Quick Start & Reproduction

### 1. Clone Repository
```bash
git clone https://github.com/adminsharpcode/visual-analytics-lab.git
cd visual-analytics-lab
```

### 2. Install Python Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib scipy python-pptx reportlab
```

### 3. Run End-to-End Orchestrator (1-Click Execution)
```bash
python run_pipeline.py
```
*Executes ingestion validation, ETL transformation, Ridge/Prophet forecasting, Shewhart anomaly detection, $t$-SNE clustering, exports dashboard data, and verifies all 11 warehouse tables in ~17.2 seconds.*

### 4. Launch Local Web Dashboard
```bash
python Project_SmartEnergy_PowerBI/web_dashboard/serve_dashboard.py 8085
```
Open **[http://localhost:8085/index.html](http://localhost:8085/index.html)** in any browser.

---

## 📁 Repository Directory Structure

```
visual-analytics-lab/
├── README.md                                    # Master project documentation
├── index.html                                   # Root redirect to web dashboard
├── vercel.json                                  # Cloud deployment configuration
├── run_pipeline.py                              # Master 1-click execution script
├── _build_ppt.py                                # Slide generation script (16 slides)
├── Team_VisualAnalytics_SmartEnergy_PowerBI.pptx # Primary defense deck
├── images/                                      # 8 high-resolution publication figures
│   ├── 01_executive_kpis_trend.png
│   ├── 02_load_profile_heatmap_matrix.png
│   ├── 03_topn_facility_sparklines.png
│   ├── 04_prophet_demand_forecast.png
│   ├── 05_anomaly_detection_control_limits.png
│   ├── 06_tsne_load_shape_clusters.png
│   ├── 07_appliance_submeter_breakdown.png
│   └── 08_solar_vs_grid_flow.png
└── Project_SmartEnergy_PowerBI/
    ├── pipeline/                                # End-to-end data pipelines
    │   ├── pipeline_ingest.py                   # IoT telemetry generator & boundary validator
    │   ├── pipeline_etl.py                      # Star schema builder & CDH normalization
    │   ├── pipeline_analytics.py                # Prophet ML, Shewhart 3σ, t-SNE clustering
    │   └── pipeline_orchestrator.py             # Pipeline runner
    ├── data/                                    # Star schema CSV tables (11 tables)
    ├── figures/                                 # Analytics figures repository
    ├── powerbi/                                 # Power BI implementation assets
    │   ├── DAX_Measures_Library.md              # 50+ enterprise DAX measures
    │   ├── PowerQuery_M_Scripts.md              # Power Query M ETL scripts
    │   └── PowerBI_Dashboard_Build_Guide.md     # Step-by-step visual assembly guide
    ├── report/                                  # Academic final reports
    │   ├── Smart_Energy_Consumption_Analytics_Final_Report.pdf # 1.47 MB formal PDF report
    │   └── Smart_Energy_Consumption_Analytics_Final_Report.md  # Full technical report source
    └── web_dashboard/                           # Apache ECharts Web HUD
        ├── index.html                           # HUD markup
        ├── style.css                            # Solid cyber-slate stylesheet
        ├── app.js                               # ECharts rendering & telemetry stream engine
        ├── echarts.min.js                       # Standalone offline Apache ECharts
        ├── dashboard_data.js                    # Telemetry payload
        ├── export_dashboard_data.py             # Data exporter
        └── serve_dashboard.py                   # Local web & live API server
```

---

## 📜 Academic Integrity & Citation
This project was developed for **MACSE603: Visual Analytics Lab** at the School of Computer Science & Engineering. All models, telemetry pipelines, and visualization implementations are original work adhering to university academic integrity guidelines.
