# Smart Energy Consumption Visualization Dashboard Using Power BI & IoT Pipelines
**Comprehensive Final Project Report**  
*Course:* MACSE603 - Visual Analytics Lab  
*Program:* Master of Technology (M.Tech) in Computer Science and Engineering  
*Academic Year:* 2025–2026  

---

### Project Team Members
| Name | Registration Number | Role | Contribution Area |
| :--- | :--- | :--- | :--- |
| **Vedant Nimkar** | `26MML0045` | **Team Leader** | Architecture, Data Pipeline, ML Analytics & Power BI Modeling |
| **Jitesh Bobde** | `26MML0025` | **Team Member** | Star Schema Dimensional Design, ETL Engineering & DAX Library |
| **Ayush Sharma** | `26MML0043` | **Team Member** | IoT Sensor Telemetry Simulation, Web Analytics UI & Literature Review |

---

## Executive Summary & Abstract
Commercial and educational campuses represent complex micro-grids characterized by dynamic load variations, distinct departmental operational rhythms, distributed renewable generation, and stringent tariff penalties for peak-demand breaches. Traditional energy monitoring systems frequently suffer from architectural fragmentation, displaying historical utility bills in passive tabular reports without operational context, predictive foresight, or root-cause diagnostics.

This project delivers an **end-to-end Smart Energy Consumption Visual Analytics Solution** integrating:
1. **IoT Telemetry Ingestion Pipeline**: Real-time ESP32 edge-sensor emulation and smart meter batch ingestion publishing over MQTT protocols.
2. **Automated ETL & Quality Assurance Pipeline**: Unit standardization (kWh, kVA, kW peak), weather integration (Cooling Degree Hours), foreign-key relational validation, and physical consistency bounds checking.
3. **Star-Schema Dimensional Warehouse**: A high-performance 11-table dimensional model comprising 52,560 hourly fact records for fiscal year 2025 across 6 campus facilities, enriched with submetering, tariffs, and meteorological features.
4. **Advanced Machine Learning Pipeline**: 
   - A Ridge/Prophet time-series demand forecasting engine achieving $R^2 = 0.996$ and $\text{MAPE} = 0.61\%$ on a 30-day holdout horizon.
   - Shewhart statistical $\pm 3\sigma$ control limits and Isolation Forest anomaly detection identifying 196 operational breaches (including weekend chiller runaways, baseload leaks, and solar inverter failures).
   - A 24-dimensional diurnal load profile normalization with $t$-Distributed Stochastic Neighbor Embedding ($t$-SNE) and $K$-Means clustering grouping facilities into four interpretable operational archetypes.
5. **Dual Visual Analytics Delivery**: A production Power BI Desktop model with 50+ DAX measures and a cyber-glassmorphism responsive Web Analytics Dashboard featuring interactive 24x7 heatmap matrices, facility benchmarking sparklines, appliance end-use donuts, and real-time streaming telemetry simulation.

---

## 1. Introduction & Background
Electricity expenditure forms one of the largest operational costs in higher education institutions and large corporate campuses. With the expansion of computing infrastructure, air-conditioned research complexes, and electric vehicle fleets, modern campuses experience substantial peak demands. Electricity utilities penalize peak power draw through Time-of-Use (ToU) tariffs and maximum demand charges ($\text{INR/kW}$). 

Visual Analytics provides the critical methodology to combine human cognitive reasoning with high-performance computational pipelines. By transforming raw meter telemetry into interactive multi-scale visual encodings, campus facility managers can instantly diagnose operational inefficiencies, shave expensive peak loads, evaluate solar PV self-consumption, and track decarbonization commitments.

---

## 2. Literature Review & Synthesis of Core Papers
The system design synthesizes foundational principles and empirical methodologies from six core peer-reviewed studies:

| No. | Paper Citation | Core Contribution | Architectural Takeaway for This Project |
| :---: | :--- | :--- | :--- |
| **1** | *Energy Consumption Distribution in Portugal: A BI Solution* (2024) | Design Science Research Methodology (DSRM) applied to national hourly and geographic energy distribution in Power BI. | Adopted user-centric DSRM, dimensional star schema modeling, role-specific pages, and drill-through navigation. |
| **2** | Awate et al., *Electricity Consumption using Big Data Analytics* (IJARSCT 2023) | Analyzed 500 residential consumers across 24 months using Power BI and Prophet demand forecasting. | Transitioned from monthly granularity to hourly telemetry; integrated Prophet time-series decomposition. |
| **3** | *Energy Calculation Using Power BI* (IJRPR 2023) | Step-by-step practical dashboard lifecycle: collection, transformation, modeling, visuals, filters, and sharing. | Engineered 50+ DAX measures library, Time Intelligence measures, and standardized Power Query M scripts. |
| **4** | Soliman & Fetais, *Visualization as a Means of Big Data Management: Qatar Energy Data* (IEEE GCCCE 2017) | Emphasized data standardization, outlier handling, missing value treatment, and query response velocity. | Constructed automated quality gates in ETL pipeline: boundary enforcement, unit harmonization, null checks. |
| **5** | *IoT-Enabled Smart Energy Monitoring and Fault Prediction* (IJIRT 2026) | ESP32 microcontroller sensors, MQTT cloud broker, regression forecasting, and electrical fault detection. | Implemented streaming IoT telemetry simulator emitting 3-phase voltage, current, and active power with MQTT schema. |
| **6** | *Interactive Machine Learning-Powered Dashboard* (ESANN 2024) | High-dimensional load profiling via $t$-SNE 2D manifold projections, sparklines, and data-cube filtering. | Implemented 24-hour diurnal vector normalization with $t$-SNE projection and $K$-Means profile segmentation. |

---

## 3. Problem Statement & Research Gaps
While existing research addresses individual facets of energy monitoring, critical gaps remain:
1. **The Telemetry-to-BI Chasm**: Academic IoT studies develop sensor prototypes without enterprise business intelligence models; conversely, enterprise BI dashboards often rely on static monthly billing CSVs lacking physical sensor fidelity.
2. **Observation Without Action**: Typical energy dashboards display historical aggregate consumption without statistical baselines, leaving users unable to distinguish expected operational spikes from anomalous equipment leaks.
3. **Rigid Temporal Hierarchies**: Inability to seamlessly transition between high-level annual campus spend and micro-level 15-minute submeter readings.

Our proposed system bridges these gaps by pairing a high-throughput Python data pipeline with an enterprise Star Schema warehouse, predictive ML engines, and an interactive dual Power BI / Web dashboard.

---

## 4. End-to-End System Architecture & Data Pipelines
The system operates as a five-stage automated pipeline:

```
[IoT Sensors / ESP32] ---> [MQTT Broker / Ingestion Gate] ---> [ETL & Quality Gates]
                                                                      |
                                                                      v
[Power BI & Web Serving] <--- [Analytics: Forecast/Anom/t-SNE] <--- [Star Schema Data Warehouse]
```

### 4.1 Ingestion Pipeline (`pipeline_ingest.py`)
- Emulates ESP32 microcontrollers deployed at six campus substations.
- Measures 3-phase line voltage ($230\text{V} \pm 2.5\text{V}$), line current ($I_{\text{line}}$), active power ($P = \sqrt{3} V I \cos\phi$), frequency ($50.0\text{Hz}$), and solar generation.
- Formats messages according to the JSON MQTT telemetry payload specification:
  ```json
  {
    "sensor_id": "ESP32-METER-FAC001",
    "facility_id": "FAC001",
    "timestamp": "2025-05-17T14:00:00",
    "active_power_kw": 756.4,
    "voltage_v": 231.2,
    "current_a": 194.5,
    "power_factor": 0.965,
    "quality_flag": "PASS"
  }
  ```

### 4.2 ETL & Data Cleaning Pipeline (`pipeline_etl.py`)
- **Unit Harmonization**: Ensures all active energy is represented in Kilowatt-hours ($\text{kWh}$), apparent power in $\text{kVA}$, and peak demand in $\text{kW}$.
- **Cooling Degree Hours ($\text{CDH}$)**: Computed relative to a $24^\circ\text{C}$ comfort base:
  $$\text{CDH}_t = \max(0, T_{\text{ambient}, t} - 24.0)$$
- **Quality Gates**: Enforces foreign-key relational integrity across dimensions; rejects packets with out-of-boundary voltages ($<180\text{V}$ or $>260\text{V}$) or invalid power factors ($<0.70$ or $>1.00$).

---

## 5. Star-Schema Dimensional Data Model
The data warehouse is structured in a Kimball-style Star Schema optimized for DAX in-memory VertiPaq engine compression:

```
                    +--------------------+
                    |    Dim_Facility    |
                    |--------------------|
                    | FacilityID (PK)    |
                    | FacilityName       |
                    | Category           |
                    | Area_SqFt          |
                    | PeakDesign_kW      |
                    +---------+----------+
                              | 1
                              |
                              | *
+--------------------+ *   +---+-------------------------+   * +--------------------+
|      Dim_Date      |-----+   Fact_EnergyConsumption    +-----|     Dim_Tariff     |
|--------------------|     |-----------------------------|     |--------------------|
| Date (PK)          |     | Timestamp                   |     | TariffID (PK)      |
| Year, Month        |     | Date (FK), Hour (FK)        |     | PeakRate_INR       |
| DayOfWeek, Season  |     | FacilityID (FK), Tariff(FK) |     | ShoulderRate_INR   |
+--------------------+     | ActivePower_kWh             |     | OffPeakRate_INR    |
                           | SolarGeneration_kWh         |     +--------------------+
+--------------------+     | NetGridImport_kWh           |
|      Dim_Time      |-----+ Cost_INR                    |
|--------------------|  *  | Carbon_kgCO2                |
| Hour (PK)          |     | AnomalyFlag, AnomalyType    |
| PeriodOfDay        |     +--------------+--------------+
| TariffBand         |                    |
+--------------------+                    | 1
                                          |
                                          | *
                               +----------+--------------+
                               |  Fact_ApplianceSubmeter |
                               |-------------------------|
                               | Date (FK), Hour (FK)    |
                               | FacilityID (FK)         |
                               | ApplianceID (FK)        |
                               | Submeter_kWh            |
                               +-------------------------+
```

### Table Inventory & Cardinality
1. **`Fact_EnergyConsumption`** (52,560 rows): Granular hourly telemetry for 6 facilities over 365 days.
2. **`Fact_ApplianceSubmeter`** (60,480 rows): Granular end-use submetering across HVAC, IT, Lighting, Machinery, and Auxiliary.
3. **`Fact_DemandForecast`** (395 rows): 365 days historical + 30 days forward projection with 95% confidence bands.
4. **`Fact_Anomalies_Detailed`** (196 rows): Operational breaches with rolling baseline deviations and wasted expenditure.
5. **`Fact_LoadClusters`** (2,190 facility-days): Normalized 24-hour diurnal profiles mapped to 2D $t$-SNE manifold coordinates.
6. **`Dim_Facility`** (6 rows): Campus buildings with metadata, categories, areas, and solar capacity.
7. **`Dim_Tariff`** (3 rows): Time-of-Use tariff rate structures (Peak, Shoulder, Off-Peak).
8. **`Dim_Date`** (731 rows): Comprehensive calendar hierarchy spanning 2024–2025.
9. **`Dim_Time`** (24 rows): Hourly breakdown, day parts, and peak flags.
10. **`Dim_Weather`** (17,544 rows): Hourly ambient temperature, humidity, solar irradiance, and CDH.
11. **`Dim_Appliance`** (5 rows): Submeter definitions and benchmark percentage shares.

---

## 6. Advanced Machine Learning Analytics Engine

### 6.1 Prophet-Style Time-Series Demand Forecasting
Campus demand exhibits multiple seasonality cycles: diurnal (24 hours), intra-week (workdays vs. weekends), and seasonal climate variations (summer cooling demand). We formulate the demand forecasting model using a Ridge regression engine with Fourier harmonic expansions:
$$y(t) = \beta_0 + \beta_1 t + \sum_{k=1}^2 \left( a_k \sin\frac{2\pi k t}{365.25} + b_k \cos\frac{2\pi k t}{365.25} \right) + \sum_{m=1}^2 \left( c_m \sin\frac{2\pi m d_t}{7} + d_m \cos\frac{2\pi m d_t}{7} \right) + \gamma \text{CDH}_t + \epsilon_t$$

**Holdout Validation Results (30-Day Evaluation Horizon):**
- **Coefficient of Determination ($R^2$):** $0.996$
- **Mean Absolute Error ($\text{MAE}$):** $270.1\text{ kWh}$
- **Root Mean Squared Error ($\text{RMSE}$):** $321.9\text{ kWh}$
- **Mean Absolute Percentage Error ($\text{MAPE}$):** $0.61\%$

The forward 30-day projection incorporates an expanding heteroskedastic uncertainty envelope ($95\%\text{ CI}$):
$$\hat{y}(t) \pm 1.96 \cdot \sigma_{\text{residuals}} \sqrt{1 + 0.005(t - t_{\text{train}})}$$

### 6.2 Shewhart Statistical Anomaly Detection ($\pm 3\sigma$)
To automatically detect operational deviations without requiring manual threshold tuning, the system computes centered rolling statistics over a 24-hour window:
$$\mu_{t} = \frac{1}{24} \sum_{i=-12}^{11} P_{t+i}, \quad \sigma_{t} = \sqrt{\frac{1}{24} \sum_{i=-12}^{11} (P_{t+i} - \mu_{t})^2}$$
$$\text{UCL}_t = \mu_t + 2.2 \sigma_t, \quad \text{LCL}_t = \max(0, \mu_t - 2.2 \sigma_t)$$

When observed load $P_t > \text{UCL}_t$, an anomaly event is logged with its excess energy:
$$\Delta E_t = P_t - \mu_t$$
$$\text{Wasted Cost}_t = \Delta E_t \times \text{TariffRate}_t$$

**Identified Operational Breaches:**
- **Incident 1 (FAC001 - Main Tech Tower):** Weekend Chiller Runaway on May 17–18, 2025. Chillers remained running at full load over Saturday and Sunday despite zero building occupancy, causing $+280\text{ kWh/h}$ excess demand and wasting $\text{INR } 64,400$.
- **Incident 2 (FAC003 - Engineering Labs):** Night Baseload Leak on August 11–14, 2025 ($00:00 - 05:00$). Exhaust ventilation fans left energized overnight, contributing $+145\text{ kWh/h}$ excess load.
- **Incident 3 (FAC001 - Solar Inverter Dropout):** Midday inverter trip on July 8, 2025 during peak irradiance, dropping solar generation from $220\text{ kW}$ to $0\text{ kW}$ and shifting load to the grid at peak tariff rates.

### 6.3 24-Hour Load Profile Manifold Projection ($t$-SNE & $K$-Means)
Each facility-day is transformed into a 24-dimensional diurnal load vector $\mathbf{x} = [p_0, p_1, \dots, p_{23}]^T$. Vectors are min-max normalized by daily peak load to isolate the *shape* of daily consumption from its absolute *scale*:
$$\tilde{p}_h = \frac{p_h}{\max_{0 \le j < 24} p_j}$$

$K$-Means clustering ($k=4$) paired with $t$-SNE non-linear projection maps the 2,190 facility-days into four operational archetypes:
1. **Cluster 1 (Commercial Day-Shift Heavy - Blue):** Tech Tower and Academic Complex; sharp morning ramp at 08:30, high plateau until 17:30, steep drop off.
2. **Cluster 2 (Continuous Baseload - Green):** Computing & Data Center; flat, uninterrupted $24\times7$ load curve ($\sim 380\text{ kW}$) with minimal weather sensitivity.
3. **Cluster 3 (Evening Residential - Amber):** Student Hostels; low daytime baseload, sharp dual evening peaks ($18:00 - 23:00$) driven by lighting, electronics, and water heating.
4. **Cluster 4 (Low Weekend Idle - Purple):** Saturday/Sunday non-working profiles characterized by standby equipment and emergency lighting.

---

## 7. Power BI Implementation & DAX Measure Engineering

### 7.1 Key DAX Measures Library
The model implements over 50 DAX measures organized into structured display folders:

```dax
// 1. Total Active Energy (kWh and GWh)
Total Active Energy (kWh) = SUM(Fact_EnergyConsumption[ActivePower_kWh])

Total Active Energy (GWh) = 
DIVIDE([Total Active Energy (kWh)], 1000000, 0)

// 2. Total Electricity Expenditure (INR Crores)
Total Electricity Spend (INR) = SUM(Fact_EnergyConsumption[Cost_INR])

Total Electricity Spend (Cr) = 
DIVIDE([Total Electricity Spend (INR)], 10000000, 0)

// 3. Solar Renewable Penetration Ratio (%)
Total Solar Generation (kWh) = SUM(Fact_EnergyConsumption[SolarGeneration_kWh])

Solar Penetration % = 
DIVIDE([Total Solar Generation (kWh)], [Total Active Energy (kWh)], 0) * 100

// 4. Time Intelligence: Month-over-Month Growth
Energy MoM Growth % = 
VAR CurrentMonth = [Total Active Energy (kWh)]
VAR PriorMonth = CALCULATE([Total Active Energy (kWh)], DATEADD(Dim_Date[Date], -1, MONTH))
RETURN
DIVIDE(CurrentMonth - PriorMonth, PriorMonth, 0)

// 5. Dynamic Top-N Facility Ranking
Facility Consumption Rank = 
RANKX(ALL(Dim_Facility[FacilityName]), [Total Active Energy (kWh)], , DESC, Dense)

// 6. Rolling Shewhart 3-Sigma Upper Control Limit
Shewhart Upper Limit (kWh) = 
VAR MeanLoad = 
    CALCULATE(
        AVERAGE(Fact_EnergyConsumption[ActivePower_kWh]),
        DATESINPERIOD(Dim_Date[Date], LASTDATE(Dim_Date[Date]), -7, DAY)
    )
VAR StdDevLoad = 
    CALCULATE(
        STDEV.P(Fact_EnergyConsumption[ActivePower_kWh]),
        DATESINPERIOD(Dim_Date[Date], LASTDATE(Dim_Date[Date]), -7, DAY)
    )
RETURN
MeanLoad + (3 * StdDevLoad)
```

---

## 8. Experimental Results & Visual Analytics Findings

### 8.1 Campus Energy & Financial Totals (2025)
- **Total Annual Energy Consumption:** $19,352,396\text{ kWh}$ ($19.35\text{ GWh}$)
- **Total Electricity Utility Expenditure:** $\text{INR } 132,036,213.51$ ($\text{INR } 13.20\text{ Crores}$)
- **Total Solar PV Generation:** $1,142,435\text{ kWh}$ ($1.14\text{ GWh}$)
- **Solar Generation Penetration:** $5.90\%$
- **Campus Coincident Peak Demand:** $2,840.0\text{ kW}$ (Occurred in June during peak afternoon cooling)
- **Total Carbon Footprint:** $15,868.9\text{ Metric Tons }\text{CO}_2\text{e}$
- **Solar Carbon Emissions Abated:** $936.8\text{ Metric Tons }\text{CO}_2\text{e}$

### 8.2 Facility Benchmarking Summary
| Facility Name | Category | Floor Area (sq.ft) | Annual Energy (GWh) | Utility Cost (Cr) | Solar Share (%) | Energy Star |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Main Tech Tower (Tower A)** | Commercial | 185,000 | 5.341 | 3.65 | 7.8% | 84 |
| **Computing & Data Center (Wing C)** | DataCenter | 45,000 | 4.882 | 3.32 | 0.0% | 91 |
| **Student Hostel Cluster (Block B&C)** | Residential | 220,000 | 3.412 | 2.31 | 6.2% | 79 |
| **Academic & Admin Complex** | Educational | 130,000 | 2.518 | 1.72 | 8.1% | 88 |
| **Advanced Engineering Labs** | Industrial | 95,000 | 2.115 | 1.45 | 6.8% | 76 |
| **Healthcare & Medical Center** | Healthcare | 65,000 | 1.084 | 0.75 | 5.5% | 82 |

### 8.3 Appliance End-Use Disaggregation
- **HVAC & Central Chillers:** $42.0\%$ ($8.13\text{ GWh}$) — The primary driver of summer demand and tariff spikes.
- **Server Racks & IT Infrastructure:** $22.0\%$ ($4.26\text{ GWh}$) — Inflexible continuous $24\times7$ baseload.
- **Lighting & Receptacles:** $18.0\%$ ($3.48\text{ GWh}$) — Controllable through occupancy sensors and LED retrofits.
- **Industrial Machinery & Motors:** $12.0\%$ ($2.32\text{ GWh}$) — Lab equipment and ventilation pumps.
- **Auxiliary & Water Systems:** $6.0\%$ ($1.16\text{ GWh}$) — Water booster pumps and perimeter infrastructure.

---

## 9. Decision Support & Usability Evaluation
To assess the effectiveness of the visual analytics solution, we evaluated decision workflows against standard energy auditing procedures:

1. **Peak Shaving Actionability**: The $24\times7$ load matrix allows facility engineers to pinpoint coincident peak hours ($14:00 - 17:00$ weekdays). By precooling academic buildings between $11:00$ and $13:00$ using rooftop solar energy, the campus can reduce contract demand charges by up to $15\%$, saving an estimated $\text{INR } 18.5\text{ Lakhs}$ annually.
2. **Automated Anomaly Triage**: In place of monthly utility bill reconciliation, the Shewhart $\pm 3\sigma$ control engine flags breaches within one hour of occurrence. Facility technicians can verify chiller schedules before wasteful weekend runaways persist.
3. **Solar PV Expansion Prioritization**: Facilities with zero solar penetration (Computing Wing C) can be targeted for carport solar canopies to directly feed day-shift UPS battery banks.

---

## 10. Conclusion & Future Work
This project successfully implemented an end-to-end Smart Energy Consumption Visual Analytics platform integrating IoT data streaming, automated ETL pipelines, an enterprise Star Schema warehouse, machine learning forecasting and anomaly detection, and interactive visual dashboards.

**Future Enhancements:**
- Integration of live OpenADR 2.0 automated demand response protocols to dynamically cycle HVAC loads during utility grid distress.
- Reinforcement learning agents for automated battery energy storage system (BESS) dispatch.
- Integration of edge computing inference on ESP32 microcontrollers for localized sub-second arc-fault detection.

---

## References
1. *Energy Consumption Distribution in Portugal: A Business Intelligence Solution*, 2024 dissertation, NOVA IMS repository.
2. Awate, S. A., Chaurasia, R., Kirolkar, P., More, M., and Ingale, P., "Electricity Consumption using Big Data Analytics," *International Journal of Advanced Research in Science, Communication and Technology (IJARSCT)*, 3(2), 2023. DOI: `10.48175/IJARSCT-9099`.
3. "Energy Calculation Using Power BI," *International Journal of Research Publication and Reviews (IJRPR)*, 2023.
4. Soliman, E., and Fetais, N., "Visualization as a Means of Big Data Management: Using Qatar’s Electricity Consumption Data," *IEEE GCC Conference and Exhibition (GCCCE)*, 2017.
5. "An IoT-Enabled Smart Energy Monitoring and Fault Prediction System," *International Journal of Innovative Research in Technology (IJIRT)*, 2026.
6. "Interactive Machine Learning-Powered Dashboard for Smart Meter Data Analytics," *European Symposium on Artificial Neural Networks (ESANN)*, Proceedings, 2024.
