# School of Computer Science and Engineering
### Department of Artificial Intelligence and Machine Learning
**Master of Technology (M.Tech) in Computer Science and Engineering / Artificial Intelligence and Machine Learning**  
**Fall Semester 2026**  
**Course Title:** Visual Analytics Lab &nbsp;|&nbsp; **Course Code:** MACSE603 &nbsp;|&nbsp; **Slot:** VL2026270106590 (PRP135)  

---

# COMPREHENSIVE CAPSTONE PROJECT REPORT

# SMART ENERGY CONSUMPTION VISUALIZATION DASHBOARD USING POWER BI & IoT PIPELINES
### *An Integrated Multi-Tier Visual Analytics Framework with Kimball Star Schema Warehouse, Machine Learning Demand Forecasting, Shewhart Statistical Quality Control, Apache ECharts, and Cloud-Native Telemetry Analytics*

---

### **SUBMITTED TO:**
**Dr. Mary Jennifer J**  
Assistant Professor (Senior)  
School of Social Sciences and Languages (SSL) / Faculty Evaluator  
School of Computer Science and Engineering (SCOPE)  
Vellore Institute of Technology, Vellore – 632014, Tamil Nadu, India  

---

### **SUBMITTED BY: PROJECT TEAM**
| Student Name | Registration Number | Degree & Branch | Project Responsibilities |
| :--- | :--- | :--- | :--- |
| **Vedant Nimkar** | **26MML0045** | M.Tech CSE / AI & ML | **Team Leader** (System Architecture, Data Pipelines, ML Analytics & Power BI Dev) |
| **Jitesh Bobde** | **26MML0025** | M.Tech CSE / AI & ML | **Team Member** (Star Schema Dimensional Modeling, Power Query M ETL & DAX Library) |
| **Ayush Sharma** | **26MML0043** | M.Tech CSE / AI & ML | **Team Member** (IoT Telemetry Simulation, Web Analytics UI & Literature Review) |

**Vellore Institute of Technology, Vellore – 632014, Tamil Nadu, India**  
**October 2026**  

---

## Executive Abstract
Large institutional campuses and modern commercial building complexes face escalating electrical utility expenditures governed by multi-tier Time-of-Use (ToU) tariffs, high peak contract demand charges, and distributed sub-facility operations. Traditional monitoring methods rely on monthly aggregated billing statements that conceal instantaneous load spikes, overnight baseload leaks, and uncorrected low power-factor penalties. This project engineers an end-to-end, publication-grade Smart Energy Consumption Visual Analytics platform that unifies IoT sensor edge ingestion, automated ETL normalization, a 52,560-record Star Schema warehouse (FY 2025 across 6 facilities), machine learning demand forecasting, Shewhart statistical anomaly detection, and dual-track presentation serving.

The diagnostic and predictive core features a Fourier-expanded Ridge regression engine achieving an exceptional accuracy of **$R^2 = 0.996$** (MAE = 270.1 kWh, MAPE = 0.61%) across a 30-day holdout validation, and a rolling Shewhart $\pm 3\sigma$ control limit algorithm that successfully flags 196 operational breaches, including a high-severity weekend chiller runaway that wasted INR 64,400. In the serving tier, we engineer a modern Microsoft Fabric Power BI Project (`.pbip`) using clean Tabular Model Definition Language (TMDL) and Power BI Report (PBIR) multi-page layouts alongside an interactive, responsive cyber-glassmorphism Web Application built with Apache ECharts and deployed globally to Vercel ([https://webdashboard-eta.vercel.app](https://webdashboard-eta.vercel.app)). The system demonstrates an actionable annual cost-saving potential of **INR 21.34 Lakhs** through automated peak shaving and anomaly curtailment.

---

## 1. Introduction & Background
### 1.1 Context and Industrial Motivation
Higher education university campuses represent complex socio-technical microgrids. A contemporary university campus houses tens of thousands of students and faculty distributed across specialized physical assets: multi-story academic lecture halls, high-power compute clusters and data centers, wet and dry research laboratories, central dining halls, sports stadiums, and high-density student residence dormitories. Consequently, annual electricity expenditure routinely exceeds tens of crores of rupees (amounting to **INR 13.20 Crores** across the 6 campus facilities analyzed in this study).

Managing these energy budgets has historically been undermined by the 'black box' nature of bulk commercial utility billing. Traditional utility meters record aggregate cumulative energy (kWh) and peak apparent power (kVA) over a monthly billing cycle. This coarse temporal aggregation conceals critical operational dysfunctions:
1. **Unmonitored Equipment Runaways:** Chillers, ventilation air handling units (AHUs), and laboratory exhaust fans frequently run continuously over weekends and holiday breaks due to manual override switches or malfunctioning timers.
2. **Coincident Peak Demand Surges:** Commercial utility billing imposes severe financial penalties based on the single maximum 15-minute or 30-minute peak demand recorded during the entire billing period. Uncoordinated simultaneous startup of major loads spikes demand charges.
3. **Suboptimal Renewable Integration:** Campuses with distributed rooftop solar photovoltaic (PV) arrays often fail to synchronize heavy deferred loads (e.g., thermal chilled-water storage charging, pumping) with maximum solar generation hours.
4. **Reactive Power Penalties:** Operating aging inductive loads (motors, induction fans, transformers) without automated capacitor bank switching drags power factor below 0.90, incurring heavy utility surcharges.

### 1.2 The Visual Analytics Imperative
Visual Analytics—the science of analytical reasoning facilitated by interactive visual interfaces—provides the decisive solution to this information asymmetry. By combining automated data transformation pipelines, dimensional modeling, predictive machine learning, and interactive visual encodings, Visual Analytics enables stakeholders to move seamlessly from high-level executive KPIs down to root-cause submetered appliance telemetry. Following Ben Shneiderman’s Visual Information Seeking Mantra—*“Overview first, zoom and filter, then details-on-demand”*—this platform translates raw electrical telemetry into high-density visual narratives that empower facilities teams to transition from passive bill paying to proactive, algorithmic energy stewardship.

### 1.3 Key Research & Engineering Objectives
1. **Granular Temporal Telemetry:** Ingest and normalize 52,560 hourly metered readings spanning all 8,760 hours of FY 2025 across 6 heterogeneous campus facilities.
2. **Kimball Star Schema Warehouse:** Architect an 11-table dimensional warehouse with strict primary/foreign key relationships optimized for rapid in-memory analytical querying.
3. **High-Fidelity Predictive Modeling:** Formulate a regularized time-series forecasting engine capturing diurnal ($P=24\text{h}$), intra-week ($P=168\text{h}$), and weather Cooling Degree Hours (CDH) interactions.
4. **Statistical Quality Control Limits:** Implement dynamic Shewhart $\pm 3\sigma$ rolling control limits to detect operational equipment leaks and quantify avoidable financial waste.
5. **Non-Linear Manifold Load Clustering:** Project 24-dimensional daily load vectors using Barnes-Hut $t$-SNE into interpretable operational archetypes.
6. **Dual-Track Enterprise Serving:** Deliver the complete visual system both as a native Microsoft Fabric Power BI Project (`.pbip` with TMDL/PBIR) and as a cloud-native, responsive Web Dashboard deployed globally on Vercel.

---

## 2. System Model & Pipeline Architecture
The system architecture follows a decoupled, five-tier pipeline designed for high resilience, analytical reproducibility, and sub-second interactive query response times across millions of metered data points.

``![Figure 1: End-to-End Five-Tier Smart Energy Visual Analytics Pipeline Architecture](images/architecture_flow.png)
*Figure 1: End-to-End Five-Tier Smart Energy Visual Analytics Pipeline Architecture*

`
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             TIER 1: INGESTION GATE                               │
│  ESP32 3-Phase Smart Meters  ──►  MQTT Edge Broker  ──►  Schema Validator & Log  │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     TIER 2: AUTOMATED ETL & DATA ENGINEERING                     │
│  Range Clipping  ──►  CDH Weather Calc  ──►  ToU Tariff Map  ──►  Carbon Footprint│
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   TIER 3: KIMBALL STAR SCHEMA DATA WAREHOUSE                     │
│   Fact_EnergyConsumption (52.5k)   │   Dim_Facility (6)     │   Dim_Date (731)   │
│   Fact_ApplianceSubmeter (60.5k)   │   Dim_Tariff (3)       │   Dim_Time (24)    │
│   Fact_DemandForecast (395)        │   Dim_Weather (17.5k)  │   Dim_Appliance (5)│
│   Fact_Anomalies_Detailed (196)    │   Fact_LoadClusters (2,190 facility-days)   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                 TIER 4: PREDICTIVE & DIAGNOSTIC ANALYTICS ENGINES                │
│  Fourier Ridge Forecast (R²=0.996) │ Shewhart ±3σ Anomaly │ t-SNE 2D Clustering │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    TIER 5: DUAL PRESENTATION & SERVING LAYER                     │
│  Native Power BI (.pbip / TMDL / PBIR)  │  Cloud Web Dashboard (Vercel / ECharts)│
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Pipeline Tiers
- **Tier 1: Ingestion Gate:** Collects active power (kWh), reactive power (kVARh), line voltage (V), power factor, and weather parameters. Validates schema types, clips physical sensor dropouts (e.g., negative voltage spikes), and logs pipeline metrics.
- **Tier 2: Automated ETL & Feature Engineering:** Enriches raw intervals with Cooling Degree Hours ($\text{CDH} = \max(0, \text{Temp} - 24.0^\circ\text{C})$), calculates solar self-consumption ratios, evaluates multi-tier ToU tariffs, and derives Scope 2 emissions using the Central Electricity Authority (CEA) grid emission factor of $0.82\text{ kg CO}_2\text{e/kWh}$.
- **Tier 3: Star Schema Relational Store:** Houses 11 synchronized tables organized into central transactional facts and denormalized dimensions, ensuring zero redundant calculation at visual query time.
- **Tier 4: Analytics Engines:** Implements Scikit-Learn Ridge regression with harmonic basis expansions, rolling Shewhart process control algorithms, and scikit-learn Barnes-Hut $t$-Distributed Stochastic Neighbor Embedding.
- **Tier 5: Dual Serving:** Deploys (a) Microsoft Power BI Desktop project with 12 enterprise DAX measures and 23 visual containers, and (b) responsive Vanilla JS/CSS Apache ECharts dashboard on Vercel with real-time MQTT telemetry emulation.

---

## 3. Literature Review & Synthesis of Core Research Papers
The design and analytical architecture of this project is rigorously grounded in the findings of six foundational research studies spanning business intelligence, IoT sensing, big data visualization, and machine learning:

### 3.1 Systematic Review of Foundational Literature
1. **Energy Consumption Distribution in Portugal: A Business Intelligence Solution (NOVA IMS, 2024):**  
   *Methodology:* Applied Design Science Research Methodology (DSRM) to national-scale electricity consumption data across Portugal, creating a multi-layer Power BI reporting framework.  
   *Key Takeaway:* Established that utility decision-making relies on beginning with explicit business questions, mapping them to a clean dimensional model, and structuring visual dashboards with top-level executive KPIs backed by drill-through detail views.  
   *Adoption in Project:* We adopted the DSRM lifecycle to design our 3-page Power BI executive layout, linking top-level campus cards directly to facility-level drill-through pages.

2. **Electricity Consumption using Big Data Analytics (Awate et al., IJARSCT 2023):**  
   *Methodology:* Analyzed 24 months of smart meter data across 500 residential consumers using Power BI, consumer ranking matrices, and Facebook Prophet time-series forecasting.  
   *Key Takeaway:* Proved that combining comparative consumer ranking with time-series forecasting identifies high-consumption contributors and seasonal peak months. However, the study was limited by coarse monthly temporal resolution.  
   *Adoption in Project:* We expanded the temporal grain from monthly to hourly (52,560 intervals), allowing fine-grained identification of daily operational peaks while integrating regularized Ridge/Prophet forecasting.

3. **Energy Calculation Using Power BI (Sharma & Patel, IJRPR 2023):**  
   *Methodology:* Outlined a practical end-to-end Power BI workflow: collection, transformation, model relationships, DAX measures, visual slicers, and collaborative publishing.  
   *Key Takeaway:* Emphasized that visualization clarity and reusable DAX calculation libraries are far more critical for organizational adoption than isolated technical metrics.  
   *Adoption in Project:* We implemented a comprehensive library of 12 production DAX measures (Total GWh, Cost Cr, Peak kW, Solar Penetration %, Power Factor, Carbon Abated) with dedicated display folders and formatting strings.

4. **Visualization as a Means of Big Data Management: Qatar Electricity Consumption Data (Soliman & Fetais, IEEE GCCCE 2017):**  
   *Methodology:* Investigated big data visualization challenges across smart meter networks in Qatar, identifying data quality bottlenecks, inconsistent units, and rendering latencies.  
   *Key Takeaway:* Data quality gates—standardized engineering units, physical boundary validation, and transparent ETL audit logs—are strict prerequisites for trustworthy energy dashboards.  
   *Adoption in Project:* We engineered automated ETL validation checks: physical power factor clamping ($0.70 \le \text{PF} \le 1.0$), active power non-negativity, voltage consistency checks ($210\text{V} \le V \le 250\text{V}$), and zero-BOM UTF-16LE serialization.

5. **An IoT-Enabled Smart Energy Monitoring and Fault Prediction System (Verma et al., IJIRT 2026):**  
   *Methodology:* Deployed ESP32 microcontrollers with current/voltage transformers, streaming telemetry via MQTT broker to a cloud analytics engine for real-time fault anticipation.  
   *Key Takeaway:* Real-time hardware telemetry streams can anticipate electrical faults and equipment breakdowns before physical damage occurs.  
   *Adoption in Project:* We constructed a live IoT sensor simulation module in Python and JavaScript that emits 3-phase telemetry packets over MQTT every 1.5 seconds, feeding animated ECharts gauge meters and oscilloscope charts.

6. **Interactive Machine Learning-Powered Dashboard for Smart Meter Analytics (Rossi et al., ESANN 2024):**  
   *Methodology:* Combined unsupervised machine learning with interactive visual analytics, utilizing 2D $t$-SNE projection maps, sparklines, and data-cube filtering to cluster residential daily load profiles.  
   *Key Takeaway:* Non-linear manifold learning projects 24-dimensional daily load vectors into interpretable 2D spaces, isolating distinct behavioral consumer archetypes invisible in time-series plots.  
   *Adoption in Project:* We normalized 2,190 facility-day vectors into 24-dimensional hourly profiles, executed Barnes-Hut $t$-SNE dimensionality reduction, and applied K-Means clustering ($k=4$) to automatically classify operational regimes.

### 3.2 Literature Synthesis & Research Gap Analysis
| Research Dimension | Existing Literature Focus | Identified Gap | Our Project Contribution |
| :--- | :--- | :--- | :--- |
| **Temporal Granularity** | Monthly or daily aggregated data | Inability to detect intra-day load spikes or ToU tariff breaches | 52,560 hourly metered intervals spanning all 8,760 hours of FY 2025 |
| **Data Warehouse Model** | Flat single-table CSVs or ad-hoc SQL views | Slow query execution, data redundancy, maintenance overhead | Kimball Star Schema with 11 tables, strict primary/foreign keys, and surrogate dimensions |
| **Analytics Integration** | Either purely descriptive BI or isolated ML scripts | Disconnect between predictive models and executive visual dashboards | Integrated Ridge/Prophet forecasting ($R^2=0.996$), Shewhart $\pm 3\sigma$, and $t$-SNE clustering |
| **Delivery Mechanism** | Desktop-only files or closed proprietary BMS | High license barriers, lack of accessibility for non-analyst stakeholders | Dual delivery: Microsoft Fabric `.pbip` project + Global Vercel serverless cloud deployment |

---

## 4. Existing Approaches & Methodological Limitations
Traditional energy monitoring across academic and commercial institutions suffers from three pervasive methodological paradigms:

1. **Retrospective Utility Billing Analysis:**  
   Most organizations rely entirely on monthly utility invoices. Because utility companies issue statements 15 to 30 days after the close of a billing cycle, facility managers operate in a permanently reactive state. If a water chiller valve sticks open on the 2nd day of the month, the continuous electricity waste persists undetected for 28 days until the inflated bill arrives.
2. **Siloed Building Management Systems (BMS / SCADA):**  
   Proprietary industrial systems (e.g., Johnson Controls, Honeywell, Schneider Electric) capture high-frequency sensor readings at central chillers and substations. However, these systems are locked behind proprietary communication protocols, operate on closed workstation computers in mechanical rooms, feature outdated user interfaces, and completely lack modern machine learning forecasting or public-facing executive dashboards.
3. **Disconnected Jupyter / Python Analytics:**  
   Data science teams often extract historical energy data into isolated Jupyter notebooks to run advanced models. While statistically sound, these analyses remain static snapshots: they do not refresh automatically, cannot be filtered interactively by business stakeholders, and fail to translate mathematical insights into operational decisions.

---

## 5. Proposed Design & Star Schema Warehouse
### 5.1 Kimball Dimensional Architecture
To provide a unified, enterprise-grade analytical foundation, we designed an 11-table Star Schema warehouse adhering to Kimball dimensional modeling principles:

```
                  ┌─────────────────┐        ┌─────────────────┐
                  │  Dim_Facility   │        │    Dim_Date     │
                  │  FacilityID(PK) │        │    Date (PK)    │
                  └────────┬────────┘        └────────┬────────┘
                           │                          │
                           │  1:N                     │  1:N
                           ▼                          ▼
                 ┌──────────────────────────────────────────────┐
                 │           Fact_EnergyConsumption             │
                 │  Timestamp(PK), FacilityID(FK), TariffID(FK) │
                 │  ActivePower_kWh, ReactivePower_kVARh, Cost  │
                 └─────────┬──────────────────────────┬─────────┘
                           │  N:1                     │  N:1
                           ▼                          ▼
                  ┌─────────────────┐        ┌─────────────────┐
                  │    Dim_Time     │        │   Dim_Tariff    │
                  │    Hour (PK)    │        │  TariffID (PK)  │
                  └─────────────────┘        └─────────────────┘
```

### 5.2 Warehouse Table Specifications
| Table Name | Entity Type | Record Count | Primary / Foreign Keys | Core Analytical Attributes |
| :--- | :--- | :--- | :--- | :--- |
| **Fact_EnergyConsumption** | Transaction Fact | 52,560 | `Timestamp`, `FacilityID`, `TariffID` | `ActivePower_kWh`, `ReactivePower_kVARh`, `Voltage_V`, `PowerFactor`, `Cost_INR`, `Carbon_kgCO2`, `AnomalyFlag` |
| **Fact_ApplianceSubmeter** | Periodic Fact | 60,480 | `Date`, `Hour`, `FacilityID`, `ApplianceID` | `Submeter_kWh` (Disaggregated into HVAC, Server/IT, Lighting, Heavy Motors, Aux Plug) |
| **Fact_DemandForecast** | Analytical Fact | 395 | `Date` | `Actual_kWh`, `Forecast_kWh`, `Lower95_kWh`, `Upper95_kWh`, `ModelError_kWh` |
| **Fact_Anomalies_Detailed**| Diagnostic Fact | 196 | `Timestamp`, `FacilityID` | `RollingMean_kWh`, `ControlLimit_kWh`, `Excess_kWh`, `WastedCost_INR`, `AnomalyType` |
| **Fact_LoadClusters** | Manifold Fact | 2,190 | `Date`, `FacilityID` | `tSNE_1`, `tSNE_2`, `ClusterID`, `ClusterName`, `NormalizedEnergyVector` |
| **Dim_Facility** | Dimension | 6 | `FacilityID` (PK) | `FacilityName`, `Category`, `Area_SqFt`, `Occupancy_Capacity`, `Baseline_kW`, `Solar_kWp` |
| **Dim_Tariff** | Dimension | 3 | `TariffID` (PK) | `TariffName`, `PeakRate_INR`, `ShoulderRate_INR`, `OffPeakRate_INR`, `DemandCharge_INR_kVA` |
| **Dim_Date** | Dimension | 731 | `Date` (PK) | `Year`, `Quarter`, `Month`, `MonthName`, `WeekNum`, `DayOfMonth`, `DayOfWeek`, `IsWeekend`, `Season` |
| **Dim_Time** | Dimension | 24 | `Hour` (PK) | `HourFormatted`, `Hour12`, `PeriodOfDay`, `TariffBand`, `PeakTariffFlag` |
| **Dim_Weather** | Dimension | 17,544 | `Date`, `Hour` (PK) | `AmbientTemp_C`, `SolarIrradiance_W_m2`, `RelativeHumidity_Pct`, `CoolingDegreeHours` |
| **Dim_Appliance** | Dimension | 5 | `ApplianceID` (PK) | `ApplianceName`, `Category`, `NominalPower_kW`, `OperatingVoltage_V`, `EfficiencyRating` |

### 5.3 Enterprise DAX Measure Formulations
To ensure consistent, high-performance aggregation across all visual containers, we engineered 12 core DAX measures:

1. **Total Active Consumption (GWh):**
   ```dax
   Total Active Consumption (GWh) = 
   DIVIDE(SUM(Fact_EnergyConsumption[ActivePower_kWh]), 1000000, 0)
   ```
2. **Total Electricity Spend (Cr):**
   ```dax
   Total Electricity Spend (Cr) = 
   DIVIDE(SUM(Fact_EnergyConsumption[Cost_INR]), 10000000, 0)
   ```
3. **Total Solar Generation (GWh):**
   ```dax
   Total Solar Generation (GWh) = 
   DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), 1000000, 0)
   ```
4. **Solar Penetration %:**
   ```dax
   Solar Penetration % = 
   DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), SUM(Fact_EnergyConsumption[ActivePower_kWh]), 0)
   ```
5. **Campus Peak Demand (kW):**
   ```dax
   Campus Peak Demand (kW) = 
   MAXX(VALUES(Fact_EnergyConsumption[Timestamp]), CALCULATE(SUM(Fact_EnergyConsumption[ActivePower_kWh])))
   ```
6. **Carbon Footprint (tCO2e):**
   ```dax
   Carbon Footprint (tCO2e) = 
   DIVIDE(SUM(Fact_EnergyConsumption[Carbon_kgCO2]), 1000, 0)
   ```
7. **Clean Energy Offset (tCO2e):**
   ```dax
   Clean Energy Offset (tCO2e) = 
   DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]) * 0.82, 1000, 0)
   ```
8. **Operational Anomaly Count:**
   ```dax
   Operational Anomaly Count = 
   CALCULATE(COUNTROWS(Fact_EnergyConsumption), Fact_EnergyConsumption[AnomalyFlag] = 1)
   ```
9. **Average Power Factor:**
   ```dax
   Average Power Factor = 
   AVERAGE(Fact_EnergyConsumption[PowerFactor])
   ```
10. **Peak Period Consumption (GWh):**
    ```dax
    Peak Period Consumption (GWh) = 
    CALCULATE([Total Active Consumption (GWh)], Dim_Time[PeakTariffFlag] = 1)
    ```
11. **Off-Peak Consumption (GWh):**
    ```dax
    Off-Peak Consumption (GWh) = 
    CALCULATE([Total Active Consumption (GWh)], Dim_Time[PeakTariffFlag] = 0)
    ```
12. **Net Grid Import (GWh):**
    ```dax
    Net Grid Import (GWh) = 
    DIVIDE(SUM(Fact_EnergyConsumption[NetImport_kWh]), 1000000, 0)
    ```

---

## 6. Implementation & Technical Realization
### 6.1 Machine Learning Analytics Engines
1. **Fourier-Expanded Ridge Regression Demand Forecasting:**  
   To capture multi-frequency cyclicality without overfitting, we formulated a regularized linear model incorporating Fourier series expansion for diurnal ($P_1 = 24\text{ hours}$) and intra-week ($P_2 = 168\text{ hours}$) seasonality:
   $$\hat{y}(t) = eta_0 + \sum_{k=1}^{K_1} \left[ lpha_k \sin\left(rac{2\pi k t}{24}
ight) + \gamma_k \cos\left(rac{2\pi k t}{24}
ight) 
ight] + \sum_{m=1}^{K_2} \left[ 	heta_m \sin\left(rac{2\pi m t}{168}
ight) + \phi_m \cos\left(rac{2\pi m t}{168}
ight) 
ight] + eta_{\text{cdh}} \text{CDH}(t) + eta_{\text{occ}} \text{Occ}(t)$$
   The objective minimizes the Ridge loss function:
   $$\mathcal{L}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda \|\mathbf{w}\|_2^2 \quad (\lambda = 1.0)$$
   On an unseen 30-day validation horizon, the model achieved **$R^2 = 0.996$**, **$\text{MAE} = 270.1\text{ kWh}$**, and **$\text{MAPE} = 0.61\%$**.

2. **Shewhart $\pm 3\sigma$ Statistical Process Control:**  
   Statistical quality control limits dynamically adapt to baseline shifts using a rolling 24-hour window:
   $$\mu_{24}(t) = rac{1}{24}\sum_{i=0}^{23} y(t-i), \quad \sigma_{24}(t) = \sqrt{rac{1}{23}\sum_{i=0}^{23} (y(t-i) - \mu_{24}(t))^2}$$
   $$\text{UCL}(t) = \mu_{24}(t) + 3\sigma_{24}(t), \quad \text{LCL}(t) = \max\left(0, \mu_{24}(t) - 3\sigma_{24}(t)
ight)$$
   An operational anomaly is flagged when $y(t) > \text{UCL}(t)$ for two or more consecutive intervals.

3. **Barnes-Hut $t$-SNE 2D Manifold Clustering:**  
   Each facility-day is characterized by a 24-dimensional normalized load profile vector $\mathbf{x}_i \in \mathbb{R}^{24}$, where $\sum_{h=1}^{24} x_{i,h} = 1$. The Barnes-Hut $t$-SNE algorithm minimizes the Kullback-Leibler divergence between high-dimensional joint probabilities $p_{ij}$ and low-dimensional Student-$t$ probabilities $q_{ij}$:
   $$KL(P || Q) = \sum_{i 
e j} p_{ij} \log rac{p_{ij}}{q_{ij}}$$
   K-Means clustering on the resulting 2D coordinates ($\mathbf{y}_i \in \mathbb{R}^2$) cleanly segments 2,190 facility-days into 4 distinct operational archetypes.

### 6.2 Modern Power BI Architecture (.pbip, TMDL & PBIR)
![Figure 2: Native Microsoft Fabric Power BI Desktop Multi-Page Report & Star Schema Analytics Interface](Project_SmartEnergy_PowerBI/figures/pbi_desktop_dashboard.png)  
*Figure 2: Native Microsoft Fabric Power BI Desktop Multi-Page Report & Star Schema Analytics Interface (Dark Executive Theme)*

Legacy binary `.pbix` files package schemas, reports, and binary VertiPaq databases into an opaque zip structure that is prone to serialization errors and incompatible with Git version control. This project implements the modern Microsoft Fabric **Power BI Project (`.pbip`)** architecture:
- **TMDL Semantic Model (`SmartEnergy_Analytics_Dashboard.SemanticModel`):** All 11 tables are declared in human-readable Tabular Model Definition Language files (`definition/tables/*.tmdl`), complete with M partition expressions, column data types, format strings, and DAX measures.
- **PBIR Report Engine (`SmartEnergy_Analytics_Dashboard.Report`):** Visual containers are declared as structured JSON definitions in `definition/pages/`, mapping exact $(x, y, w, h)$ positions, visual types, query state projections, and cross-filtering rules across 3 executive report pages.
- **Zero-BOM Encoding Resolution:** Fixed the underlying `Newtonsoft.Json` parsing bug by ensuring that all package text metadata (`DiagramLayout`, `Settings`, `Metadata`) is encoded strictly as UTF-16LE **without BOM**, allowing Power BI Desktop (v2.157+) to open and compile the model instantly.

### 6.3 Cloud Web Dashboard & Vercel Deployment
![Figure 3: Cloud-Native Cyber-Executive Apache ECharts Real-Time Telemetry HUD Deployed Globally on Vercel](Project_SmartEnergy_PowerBI/figures/echarts_executive_hud.png)  
*Figure 3: Cloud-Native Cyber-Executive Apache ECharts Real-Time Telemetry HUD Deployed Globally on Vercel ([https://webdashboard-eta.vercel.app](https://webdashboard-eta.vercel.app))*

To ensure universal accessibility without software licensing barriers, we built and deployed an interactive, responsive Web Application:
- **Architecture:** Lightweight Vanilla HTML5/CSS3/JavaScript utilizing Apache ECharts (v5.4.3) for high-performance canvas rendering.
- **Cyber-Slate Aesthetics:** Implemented high-contrast dark-mode styling (`#0b1120` deep slate background, `#f8fafc` crisp typography) exceeding WCAG AA contrast standards.
- **Cloud Edge Serving:** Deployed to production on Vercel at [https://webdashboard-eta.vercel.app](https://webdashboard-eta.vercel.app) with edge CDN caching and explicit zero-cache headers (`Cache-Control: public, max-age=0, must-revalidate`).
- **Live IoT Simulation:** Integrated WebSocket/MQTT telemetry simulator generating 3-phase electrical readings with animated gauge meters and rolling oscilloscope charts.
- **GitHub Synchronization:** Hosted in full at [adminsharpcode/visual-analytics-lab](https://github.com/adminsharpcode/visual-analytics-lab) with automated CI/CD integration.

---

## 7. Comprehensive Result Analysis & Visual Findings
We evaluate the operational, visual, and financial performance of the platform across eight dedicated visual analytic modules:

### 7.7 Diurnal Power Flow & Solar Penetration
![Figure 10: Diurnal Power Flow — Solar PV Generation vs. Net Grid Import Load Curve](Project_SmartEnergy_PowerBI/figures/08_solar_vs_grid_flow.png)  
*Figure 10: Diurnal Power Flow — Solar PV Generation vs. Net Grid Import Load Curve*

The diurnal load profile illustrates the interplay between active campus demand, rooftop solar PV generation, and net utility grid import. On-site solar generation reaches a peak capacity of **420 kW** between 11:30 and 13:30, coinciding with the campus mid-day cooling surge. Annual solar self-consumption ratio averages **94.2%**, directly abating **936.8 $\text{tCO}_2\text{e}$** of greenhouse gas emissions.

### 7.1 24x7 Load-Profile Heatmap Matrix
![Figure 4: Interactive Apache ECharts 24x7 Campus Load Intensity Heatmap Matrix](Project_SmartEnergy_PowerBI/figures/echarts_247_heatmap.png)  
*Figure 4: Interactive Apache ECharts 24x7 Campus Load Intensity Heatmap Matrix (Hourly Demand in kW across Days & Hours)*

The hour-of-day versus day-of-week intensity matrix exposes distinct operational regimes:
- **Morning Ramp (08:00 - 10:00):** Rapid demand escalation from 950 kW to 2,200 kW as academic lecture halls and labs activate HVAC and lighting.
- **Coincident Afternoon Peak (14:00 - 17:00):** Heavy coincident cooling load pushing total campus demand to the annual maximum of **2,840.0 kW** in mid-June.
- **Overnight Baseload (00:00 - 06:00):** Sustained demand of ~820 kW primarily driven by Computing Wing C servers and baseline chilled-water circulation.

### 7.6 Facility Benchmarking & Top-N Rankings
![Figure 9: Facility Consumption Benchmark & Top-N Ranking with Monthly Sparklines](Project_SmartEnergy_PowerBI/figures/03_topn_facility_sparklines.png)  
*Figure 9: Facility Consumption Benchmark & Top-N Ranking with Monthly Sparklines*

Cross-facility comparative analytics reveals significant consumption disparities:
- **Computing Wing C:** Consumes **4.88 GWh** annually with an exceptionally flat, non-seasonal load profile driven by 24x7 IT server racks.
- **Research Complex B:** Consumes **4.21 GWh** annually with high seasonal sensitivity due to cleanroom ventilation and thermal chambers.
- **Combined Impact:** Computing Wing C and Research Complex B account for **46.9%** of total campus electricity expenditure while occupying only 28.5% of total floor area, identifying them as prime targets for solar carport expansion and power factor correction.

### 7.2 Predictive Machine Learning Demand Forecast
![Figure 5: Apache ECharts 30-Day Ahead Fourier Ridge Demand Forecast with Dynamic 95% Confidence Prediction Bands](Project_SmartEnergy_PowerBI/figures/echarts_forecast_module.png)  
*Figure 5: Apache ECharts 30-Day Ahead Fourier Ridge Demand Forecast with Dynamic 95% Confidence Prediction Bands (^2 = 0.996$)*

The Fourier-expanded Ridge regression model was validated on an unseen 30-day holdout horizon:
- **Coefficient of Determination ($R^2$):** **0.996**
- **Mean Absolute Error (MAE):** **270.1 kWh**
- **Mean Absolute Percentage Error (MAPE):** **0.61%**
- **Peak Hour Capture:** Faithfully captures daily morning ramps and evening drop-offs within 95% expanding prediction uncertainty bounds.

### 7.3 Shewhart $\pm 3\sigma$ Anomaly Audit & Equipment Leaks
![Figure 6: Interactive Shewhart 3-Sigma Rolling Statistical Process Control Chart Highlighting Equipment Operational Runaway Breaches](Project_SmartEnergy_PowerBI/figures/echarts_anomaly_shewhart.png)  
*Figure 6: Interactive Shewhart 3-Sigma Rolling Statistical Process Control Chart Highlighting Equipment Operational Runaway Breaches & Audit Log*

Across FY 2025, the rolling Shewhart control limit algorithm isolated exactly **196 operational breaches**:
- **High-Severity Chiller Runaway:** On Saturday, July 12, Academic Block A chillers failed to enter weekend setback mode, drawing +280 kWh/h above the upper control limit for 46 consecutive hours. Total avoidable financial waste was calculated at **INR 64,400**.
- **Cumulative Waste:** Total avoidable financial waste identified across all 196 anomalies amounted to **INR 2.84 Lakhs**.

### 7.6 $t$-SNE 2D Manifold Clustering
Non-linear dimensionality reduction on 2,190 facility-day load vectors isolated 4 distinct operational archetypes:
1. **Cluster 1 (Commercial Day-Shift Heavy - 38.2%):** Sharp 08:30–18:00 bell curve characteristic of Academic Complexes A and D.
2. **Cluster 2 (Continuous 24x7 Server Baseload - 22.1%):** Flat horizontal load profile characteristic of Computing Wing C.
3. **Cluster 3 (Evening Residential Surge - 24.5%):** Pronounced 18:00–23:00 peak characteristic of Student Residence Dormitory E.
4. **Cluster 4 (Low Weekend Idle - 15.2%):** Flattened baseload with zero daytime operational ramps.

### 7.5 End-Use Submetering Disaggregation
![Figure 8: Campus End-Use Submetering Category Disaggregation & Polar Load Distribution in Apache ECharts](Project_SmartEnergy_PowerBI/figures/echarts_submeter_breakdown.png)  
*Figure 8: Campus End-Use Submetering Category Disaggregation & Polar Load Distribution in Apache ECharts*

Disaggregated circuit submetering across all 6 facilities allocates electrical consumption into 5 core end-use categories:
- **HVAC & Thermal Conditioning:** **42.1%** (8.15 GWh)
- **Servers, Network & IT Infrastructure:** **22.4%** (4.34 GWh)
- **Lighting & Auxiliary Power:** **18.2%** (3.52 GWh)
- **Heavy Induction Motors & Pumps:** **11.8%** (2.28 GWh)
- **Auxiliary Receptacles & Misc Plug Loads:** **5.5%** (1.06 GWh)

### 7.8 Summary of Quantitative Campus Deliverables (FY 2025)
| Performance Indicator | Annual Metric Value | Engineering Unit | Strategic Operational Impact |
| :--- | :--- | :--- | :--- |
| **Total Active Consumption** | **19,352,396** | kWh (19.35 GWh) | Formal campus baseline for environmental sustainability compliance |
| **Total Electricity Spend** | **13.20** | Crores INR (₹) | Total utility expenditure under multi-tier Time-of-Use tariffs |
| **Solar PV Self-Generation** | **1,142,435** | kWh (1.14 GWh) | 5.90% Renewable penetration from 590 kWp installed rooftop PV |
| **Campus Peak Coincident Demand**| **2,840.0** | kW | Annual billing contract threshold recorded during June cooling peak |
| **Total Campus Carbon Footprint**| **15,868.9** | $\text{tCO}_2\text{e}$ | Quantified using Central Electricity Authority factor (0.82 kg/kWh) |
| **Clean Solar Carbon Offset** | **936.8** | $\text{tCO}_2\text{e}$ | Direct Scope 2 abatement equivalent to planting ~42,500 trees |
| **Operational Anomalies Flagged**| **196** | Detected Events | Identified avoidable equipment waste of ~INR 2.84 Lakhs |
| **Forecasting Model Fidelity** | **$R^2 = 0.996$** | 30-Day Holdout | $\text{MAPE} = 0.61\%$, $\text{MAE} = 270.1\text{ kWh}$ across unseen test horizon |

---

## 8. Conclusion & Strategic Recommendations
### 8.1 Summary of Findings
This project successfully designed, implemented, and validated an enterprise-grade Smart Energy Consumption Visual Analytics platform. By synthesizing the core methodologies of six foundational research papers—Kimball dimensional star schemas, Prophet/Ridge machine learning forecasting, Shewhart statistical process control, and $t$-SNE manifold clustering—we have demonstrated that Visual Analytics transforms raw electrical telemetry into strategic, actionable business value.

### 8.2 Strategic Energy Efficiency Recommendations
1. **Algorithmic Peak Shaving via HVAC Pre-Cooling:**  
   Pre-cooling Academic Complex A and Research Complex B between 11:00 and 13:00 utilizes surplus rooftop solar PV power and reduces chilled-water demand during the 14:00–17:00 commercial peak tariff window. This reduces coincident contract demand by **15%**, yielding annual financial savings of **INR 18.5 Lakhs**.
2. **Automated Shewhart Weekend Curtailment:**  
   Connecting the Shewhart $\pm 3\sigma$ anomaly detection engine directly to Building Management System (BMS) relays prevents unmonitored chiller runaways during non-occupancy weekends, saving **INR 2.84 Lakhs** annually.
3. **Targeted Solar Expansion on Computing Wing C:**  
   Computing Wing C currently operates with 0 kWp solar PV despite consuming 4.88 GWh of continuous baseload energy. Constructing a 350 kWp carport solar PV array will directly offset 680 MWh of server energy annually with an estimated simple payback period of 3.8 years.
4. **Power Factor Optimization:**  
   Installing automated power factor correction (APFC) capacitor banks on the Research Complex B substation will raise average power factor from 0.89 to 0.98, avoiding monthly utility reactive power penalty surcharges.

---

## 9. Future Scope & Research Extensions
1. **Reinforcement Learning BESS Dispatch:** Train Deep Q-Network (DQN) agents to autonomously schedule charging and discharging of Battery Energy Storage Systems (BESS) based on day-ahead electricity spot pricing and weather forecasts.
2. **Edge AI Microcontroller Deployment:** Compile lightweight TinyML quantized neural networks directly onto ESP32-S3 edge microcontrollers for sub-second anomaly detection at the circuit-breaker level without cloud latency.
3. **Automated OpenADR Demand Response:** Implement OpenADR 2.0b compliance protocols to allow the campus microgrid to participate in utility automated demand response programs and frequency regulation markets.
4. **3D Spatial Digital Twin Analytics:** Develop a WebGL/Three.js 3D digital twin of the campus integrating building thermal envelopes, solar shading models, and real-time indoor air quality sensors.

---

## 10. Bibliographic References
1. NOVA IMS, “Energy Consumption Distribution in Portugal: A Business Intelligence Solution,” Master's Dissertation, NOVA Information Management School, Universidade Nova de Lisboa, Lisbon, Portugal, 2024.
2. S. A. Awate, R. Chaurasia, P. Kirolkar, M. More, and P. Ingale, “Electricity Consumption using Big Data Analytics,” *International Journal of Advanced Research in Science, Communication and Technology (IJARSCT)*, vol. 3, no. 2, pp. 245–252, 2023. DOI: 10.48175/IJARSCT-9099.
3. R. Sharma and K. Patel, “Energy Calculation Using Power BI: A Practical Implementation Framework for Commercial Facilities,” *International Journal of Research Publication and Reviews (IJRPR)*, vol. 4, no. 8, pp. 1120–1128, 2023.
4. E. Soliman and N. Fetais, “Visualization as a Means of Big Data Management: Using Qatar's Electricity Consumption Data,” in *Proc. IEEE GCC Conference and Exhibition (GCCCE)*, Manama, Bahrain, 2017, pp. 1–9. DOI: 10.1109/GCCCE.2017.8080512.
5. A. K. Verma, P. Singh, and M. Thomas, “An IoT-Enabled Smart Energy Monitoring and Fault Prediction System Using ESP32 and Cloud Analytics,” *International Journal of Innovative Research in Technology (IJIRT)*, vol. 12, no. 4, pp. 410–418, 2026.
6. F. Rossi, M. Verleysen, and H. Bourlard, “Interactive Machine Learning-Powered Dashboard for Smart Meter Load Analytics,” in *Proc. European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning (ESANN)*, Bruges, Belgium, 2024, pp. 315–320.
7. R. Kimball and M. Ross, *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*, 3rd ed. Hoboken, NJ: John Wiley & Sons, 2013.
8. S. J. Taylor and B. Letham, “Forecasting at scale,” *The American Statistician*, vol. 72, no. 1, pp. 37–45, 2018. DOI: 10.1080/00031305.2017.1380080.
9. D. C. Montgomery, *Introduction to Statistical Quality Control*, 8th ed. New York, NY: John Wiley & Sons, 2019.
10. L. van der Maaten and G. Hinton, “Visualizing data using t-SNE,” *Journal of Machine Learning Research*, vol. 9, pp. 2579–2605, 2008.
11. Central Electricity Authority (CEA), “CO2 Baseline Database for the Indian Power Sector, User Guide Version 19.0,” Ministry of Power, Government of India, New Delhi, 2024.
12. B. Shneiderman, “The eyes have it: A task by data type taxonomy for information visualizations,” in *Proc. IEEE Symposium on Visual Languages*, Boulder, CO, 1996, pp. 336–343.
