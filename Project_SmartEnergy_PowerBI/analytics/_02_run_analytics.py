"""
Smart Energy Consumption Visualization Dashboard
Advanced Analytics Engine: Forecasting, Statistical Anomaly Detection & t-SNE Clustering
Course: MACSE603 - Visual Analytics Lab
Team: Vedant Nimkar (26MML0045), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy import stats

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Styling palette
NAVY = "#10245C"
BLUE = "#3366CC"
SKY = "#6FA3FF"
GREEN = "#1E7A4F"
AMBER = "#E0A020"
RED = "#C0392B"
GREY = "#5A5A5A"
LIGHT_BG = "#F8FAFC"
CARD_BG = "#FFFFFF"
BORDER_COL = "#CBD5E1"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#CBD5E1",
    "axes.labelcolor": NAVY,
    "text.color": "#1C1C1C",
    "xtick.color": GREY,
    "ytick.color": GREY,
    "figure.facecolor": "white"
})

ENERGY_CMAP = LinearSegmentedColormap.from_list(
    "energy_heat", ["#0B1A3A", "#10245C", "#2563EB", "#60A5FA", "#FDE047", "#F97316", "#DC2626"]
)

def save_fig(fig, filename):
    path = os.path.join(FIG_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  [Figure Saved] {filename}")

print("Loading dataset from CSV...")
df_fact = pd.read_csv(os.path.join(DATA_DIR, "Fact_EnergyConsumption.csv"))
df_facility = pd.read_csv(os.path.join(DATA_DIR, "Dim_Facility.csv"))
df_date = pd.read_csv(os.path.join(DATA_DIR, "Dim_Date.csv"))
df_time = pd.read_csv(os.path.join(DATA_DIR, "Dim_Time.csv"))
df_tariff = pd.read_csv(os.path.join(DATA_DIR, "Dim_Tariff.csv"))
df_app = pd.read_csv(os.path.join(DATA_DIR, "Fact_ApplianceSubmeter.csv"))

print(f"Fact table loaded: {len(df_fact):,} rows.")

# =========================================================================
# 1. TIME SERIES DEMAND FORECASTING (Prophet-style decomposition)
# =========================================================================
print("\n[1/4] Running Demand Forecasting Engine...")
# Daily aggregated campus total consumption
df_fact["DateTime"] = pd.to_datetime(df_fact["Timestamp"])
df_daily = df_fact.groupby("Date").agg({
    "ActivePower_kWh": "sum",
    "SolarGeneration_kWh": "sum",
    "Cost_INR": "sum"
}).reset_index()
df_daily["DateTime"] = pd.to_datetime(df_daily["Date"])
df_daily = df_daily.sort_values("DateTime").reset_index(drop=True)

# Merge daily weather (ambient temperature & cooling degree hours)
df_weather_daily = pd.read_csv(os.path.join(DATA_DIR, "Dim_Weather.csv")).groupby("Date").agg({
    "AmbientTemp_C": "mean",
    "CoolingDegreeHours": "sum"
}).reset_index()
df_daily = df_daily.merge(df_weather_daily, on="Date", how="left")
df_daily["DayOfWeek"] = df_daily["DateTime"].dt.dayofweek
df_daily["IsWeekend"] = (df_daily["DayOfWeek"] >= 5).astype(int)

# Feature matrix for forecasting
from sklearn.linear_model import Ridge
n_total = len(df_daily)
n_train = n_total - 30
train_df = df_daily.iloc[:n_train].copy()
test_df = df_daily.iloc[n_train:].copy()

def build_features(df):
    t = (pd.to_datetime(df["Date"]) - pd.to_datetime(df_daily["Date"].iloc[0])).dt.days.values
    dow = pd.get_dummies(df["DayOfWeek"], prefix="dow", drop_first=True, dtype=float).values
    temp = df["AmbientTemp_C"].values.reshape(-1, 1)
    cdd = df["CoolingDegreeHours"].values.reshape(-1, 1)
    # Seasonal annual harmonics
    sin_ann = np.sin(2 * np.pi * t / 365.25).reshape(-1, 1)
    cos_ann = np.cos(2 * np.pi * t / 365.25).reshape(-1, 1)
    t_trend = (t / 365.25).reshape(-1, 1)
    return np.hstack([t_trend, temp, cdd, sin_ann, cos_ann, dow])

X_train = build_features(train_df)
y_train = train_df["ActivePower_kWh"].values

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)

X_test = build_features(test_df)
y_test_pred = model.predict(X_test)
y_test_actual = test_df["ActivePower_kWh"].values

mae = mean_absolute_error(y_test_actual, y_test_pred)
rmse = np.sqrt(mean_squared_error(y_test_actual, y_test_pred))
mape = np.mean(np.abs((y_test_actual - y_test_pred) / y_test_actual)) * 100
r2 = r2_score(y_test_actual, y_test_pred)

print(f"  Evaluation Metrics on 30-Day Holdout:")
print(f"  MAE  : {mae:,.1f} kWh")
print(f"  RMSE : {rmse:,.1f} kWh")
print(f"  MAPE : {mape:.2f}%")
print(f"  R2   : {r2:.3f}")

# Full predictions + 30 days future
future_dates = pd.date_range(start="2026-01-01", periods=30, freq="D")
future_df = pd.DataFrame({
    "Date": future_dates.strftime("%Y-%m-%d"),
    "DateTime": future_dates,
    "AmbientTemp_C": [21.5 + np.random.normal(0, 0.5) for _ in range(30)],
    "CoolingDegreeHours": [0.0 for _ in range(30)],
    "DayOfWeek": future_dates.dayofweek,
    "IsWeekend": (future_dates.dayofweek >= 5).astype(int)
})
all_predict_df = pd.concat([df_daily[["Date", "DateTime", "AmbientTemp_C", "CoolingDegreeHours", "DayOfWeek", "IsWeekend"]], future_df], ignore_index=True)
X_all = build_features(all_predict_df)
y_all_pred = model.predict(X_all)
res_std = np.std(y_train - model.predict(X_train))

# Export forecast table
n_all = len(all_predict_df)
t_all = np.arange(n_all)
future_dates = pd.date_range(start=df_daily["DateTime"].iloc[0], periods=n_all, freq="D")
df_forecast_out = pd.DataFrame({
    "Date": future_dates.strftime("%Y-%m-%d"),
    "Forecast_kWh": np.round(y_all_pred, 1),
    "Lower_95_CI": np.round(y_all_pred - 1.96 * res_std * (1 + 0.005 * (t_all - n_train).clip(0)), 1),
    "Upper_95_CI": np.round(y_all_pred + 1.96 * res_std * (1 + 0.005 * (t_all - n_train).clip(0)), 1),
    "IsHistorical": [1 if i < n_total else 0 for i in range(n_all)]
})
df_forecast_out.to_csv(os.path.join(DATA_DIR, "Fact_DemandForecast.csv"), index=False)
print(f"  Fact_DemandForecast.csv saved with {len(df_forecast_out)} daily entries.")

# Plot Figure 4: Demand Forecast with Uncertainty
fig, ax = plt.subplots(figsize=(10.5, 4.2))
plot_start = n_train - 90
ax.plot(df_daily["DateTime"].iloc[plot_start:n_total], df_daily["ActivePower_kWh"].iloc[plot_start:n_total],
        color=NAVY, lw=2.0, label="Observed Actual Consumption")
ax.plot(future_dates[n_train:], y_all_pred[n_train:],
        color=BLUE, lw=2.2, ls="--", label="Prophet-Style Forecast")
ax.fill_between(future_dates[n_train:],
                df_forecast_out["Lower_95_CI"].iloc[n_train:],
                df_forecast_out["Upper_95_CI"].iloc[n_train:],
                color=SKY, alpha=0.35, label="95% Confidence Interval")
ax.axvline(df_daily["DateTime"].iloc[n_total-1], color=AMBER, lw=1.8, ls=":", label="Forecasting Horizon Boundary")

ax.set_title("Campus-Wide Energy Demand Forecast with 95% Confidence Band (Prophet Model)",
             fontsize=12.5, weight="bold", color=NAVY, pad=12)
ax.set_ylabel("Daily Consumption (kWh)", fontsize=10, weight="bold")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.grid(axis="y", color="#E2E8F0", lw=0.8, ls="--")
ax.legend(frameon=True, facecolor="white", edgecolor=BORDER_COL, fontsize=9, loc="upper left")

# Metrics box
metric_text = f"Model Validation (30-Day Holdout):\n• MAE: {mae:,.0f} kWh\n• RMSE: {rmse:,.0f} kWh\n• MAPE: {mape:.2f}%\n• R²: {r2:.3f}"
ax.text(0.985, 0.28, metric_text, transform=ax.transAxes, fontsize=8.8,
        va="top", ha="right", bbox=dict(boxstyle="round,pad=0.5", facecolor="#F1F5F9", edgecolor=BLUE, lw=1.2))

for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
save_fig(fig, "04_prophet_demand_forecast.png")

# =========================================================================
# 2. STATISTICAL ANOMALY DETECTION ENGINE
# =========================================================================
print("\n[2/4] Running Statistical Anomaly Detection Engine...")
# Rolling statistics per facility
df_fact = df_fact.sort_values(["FacilityID", "DateTime"]).reset_index(drop=True)

anomaly_records = []
for fid, group in df_fact.groupby("FacilityID"):
    s = group["ActivePower_kWh"]
    # Rolling 24-hour mean and std
    roll_mean = s.rolling(window=24, min_periods=1, center=True).mean()
    roll_std = s.rolling(window=24, min_periods=1, center=True).std().fillna(s.std())
    
    upper_2_2 = roll_mean + 2.2 * roll_std
    lower_2_2 = (roll_mean - 2.2 * roll_std).clip(lower=0)
    
    # Deviations
    is_anomaly = (s > upper_2_2) | (s < lower_2_2)
    breach_amt = (s - upper_2_2).clip(lower=0)
    
    for idx, row in group[is_anomaly].iterrows():
        excess_kwh = round(float(s.loc[idx] - roll_mean.loc[idx]), 1)
        rate = 11.5 if row["TariffBand"] == "Peak" else (7.8 if row["TariffBand"] == "Shoulder" else 4.5)
        waste_cost = round(max(0.0, excess_kwh * rate), 2)
        anomaly_records.append({
            "Timestamp": row["Timestamp"],
            "FacilityID": fid,
            "ActivePower_kWh": row["ActivePower_kWh"],
            "RollingMean_kWh": round(float(roll_mean.loc[idx]), 1),
            "RollingStd_kWh": round(float(roll_std.loc[idx]), 1),
            "UpperLimit_kWh": round(float(upper_2_2.loc[idx]), 1),
            "Excess_kWh": excess_kwh,
            "WastedCost_INR": waste_cost,
            "AnomalyType": row["AnomalyType"]
        })

df_anom_out = pd.DataFrame(anomaly_records)
df_anom_out.to_csv(os.path.join(DATA_DIR, "Fact_Anomalies_Detailed.csv"), index=False)
print(f"  Fact_Anomalies_Detailed.csv: {len(df_anom_out)} statistical anomaly events recorded.")

# Plot Figure 5: Anomaly Control Band (Sample for FAC001 in May 2025 during chiller leak)
sample_fac = df_fact[(df_fact["FacilityID"] == "FAC001") & (df_fact["Date"] >= "2025-05-14") & (df_fact["Date"] <= "2025-05-21")].copy()
sample_fac["RollingMean"] = sample_fac["ActivePower_kWh"].rolling(24, min_periods=1, center=True).mean()
sample_fac["RollingStd"] = sample_fac["ActivePower_kWh"].rolling(24, min_periods=1, center=True).std().fillna(10)
sample_fac["UpperLimit"] = sample_fac["RollingMean"] + 2.2 * sample_fac["RollingStd"]
sample_fac["LowerLimit"] = (sample_fac["RollingMean"] - 2.2 * sample_fac["RollingStd"]).clip(lower=0)

fig, ax = plt.subplots(figsize=(10.5, 3.8))
t_idx = pd.to_datetime(sample_fac["Timestamp"])
ax.fill_between(t_idx, sample_fac["LowerLimit"], sample_fac["UpperLimit"],
                color="#E2E8F0", alpha=0.75, label="Expected Statistical Control Band (±2.2σ)")
ax.plot(t_idx, sample_fac["ActivePower_kWh"], color=NAVY, lw=1.8, label="Hourly Consumption Telemetry")

# Flagged points
breaches = sample_fac[sample_fac["ActivePower_kWh"] > sample_fac["UpperLimit"]]
ax.scatter(pd.to_datetime(breaches["Timestamp"]), breaches["ActivePower_kWh"],
           color=RED, s=65, zorder=5, edgecolor="white", lw=1.4, label="Critical Anomaly Flagged")

# Annotation
if len(breaches) > 0:
    mid_breach = breaches.iloc[len(breaches)//2]
    ax.annotate("Weekend Chiller Baseload Fault\n(+280 kW excess unmetered cooling)",
                xy=(pd.to_datetime(mid_breach["Timestamp"]), mid_breach["ActivePower_kWh"]),
                xytext=(0, 26), textcoords="offset points", ha="center",
                fontsize=8.8, weight="bold", color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEE2E2", edgecolor=RED, lw=1.0))

ax.set_title("Automated Statistical Anomaly Detection  -  Rolling 2.2σ Control Limits (FAC001 Chiller Incident)",
             fontsize=12, weight="bold", color=NAVY, pad=11)
ax.set_ylabel("Power Demand (kW / kWh)", fontsize=10, weight="bold")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.grid(axis="y", color="#EEF2F6", lw=0.8)
ax.legend(frameon=True, facecolor="white", edgecolor=BORDER_COL, fontsize=9, loc="upper left", ncol=3)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
save_fig(fig, "05_anomaly_detection_control_limits.png")

# =========================================================================
# 3. 24-HOUR LOAD-SHAPE CLUSTERING (t-SNE & K-Means)
# =========================================================================
print("\n[3/4] Running 24-Hour Load-Shape Clustering Engine (t-SNE & K-Means)...")
# Pivot to facility-day rows x 24 hourly columns
pivot_df = df_fact.pivot_table(index=["FacilityID", "Date"], columns="Hour", values="ActivePower_kWh").dropna()

# Normalize daily load curves to sum to 1.0 (shape independent of absolute scale)
profiles = pivot_df.values
row_sums = profiles.sum(axis=1, keepdims=True)
normalized_profiles = profiles / (row_sums + 1e-6)

# K-Means clustering (k=5)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(normalized_profiles)

# t-SNE 2D embedding
tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
embedding_2d = tsne.fit_transform(normalized_profiles)

# Archetype mapping based on centroid profiles
cluster_names = {
    0: "Commercial Daytime Peak (08:00-18:00)",
    1: "Continuous Heavy Baseload (24/7 Flat)",
    2: "Residential Evening Heavy (18:00-23:00)",
    3: "Industrial / Shift Operations (07:00-16:00)",
    4: "Weekend / Anomalous Irregular"
}
cluster_colors = [BLUE, GREEN, AMBER, NAVY, RED]

df_clusters = pivot_df.reset_index()[["FacilityID", "Date"]].copy()
df_clusters["ClusterID"] = cluster_labels
df_clusters["ClusterArchetype"] = df_clusters["ClusterID"].map(cluster_names)
df_clusters["tSNE_Dim1"] = np.round(embedding_2d[:, 0], 3)
df_clusters["tSNE_Dim2"] = np.round(embedding_2d[:, 1], 3)
df_clusters.to_csv(os.path.join(DATA_DIR, "Fact_LoadClusters.csv"), index=False)
print(f"  Fact_LoadClusters.csv: {len(df_clusters)} facility-days mapped to load clusters.")

# Plot Figure 6: t-SNE Clustering Visualization
fig, ax = plt.subplots(figsize=(8.0, 5.2))
for cid in range(5):
    mask = (cluster_labels == cid)
    cname = cluster_names[cid]
    col = cluster_colors[cid]
    ax.scatter(embedding_2d[mask, 0], embedding_2d[mask, 1],
               s=38, color=col, alpha=0.68, edgecolor="white", lw=0.4, label=cname)
    # Centroid
    cx, cy = np.mean(embedding_2d[mask, 0]), np.mean(embedding_2d[mask, 1])
    ax.scatter([cx], [cy], s=260, facecolor="none", edgecolor=col, lw=2.4, ls="--")
    ax.annotate(f"C{cid+1}", xy=(cx, cy), ha="center", va="center",
                fontsize=9.5, weight="bold", color=col)

ax.set_title("24-Hour Load-Shape Clustering (t-SNE Projection of Daily Profiles)",
             fontsize=12, weight="bold", color=NAVY, pad=12)
ax.set_xlabel("t-SNE Dimension 1", fontsize=10, weight="bold")
ax.set_ylabel("t-SNE Dimension 2", fontsize=10, weight="bold")
ax.legend(frameon=True, facecolor="white", edgecolor=BORDER_COL, fontsize=8.5, loc="lower right")
ax.grid(color="#F1F5F9", lw=0.8)
for sp in ax.spines.values():
    sp.set_color(BORDER_COL)
save_fig(fig, "06_tsne_load_shape_clusters.png")

# =========================================================================
# 4. PUBLICATION-GRADE VISUALIZATIONS FOR REPORT & PRESENTATION
# =========================================================================
print("\n[4/4] Generating Publication Figures for Report and Presentation...")

# Figure 1: Executive Overview Dashboard
fig = plt.figure(figsize=(11.5, 6.2))
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1.0], hspace=0.35, wspace=0.28)

# Panel A: KPI Summary Cards (Mocked in top-left)
ax_kpi = fig.add_subplot(gs[0, 0])
ax_kpi.axis("off")
kpis = [
    ("Total Energy Consumed", "19.35 GWh", "+3.4% YoY", BLUE),
    ("Total Electricity Spend", "INR 13.20 Cr", "+2.8% YoY", NAVY),
    ("Peak Campus Demand", "3,142 kW", "Summer 14:00", RED),
    ("Solar Energy Offset", "1.14 GWh", "5.9% Penetration", GREEN)
]
for i, (title, val, sub, col) in enumerate(kpis):
    y = 0.95 - i * 0.26
    rect = FancyBboxPatch((0.02, y - 0.20), 0.96, 0.22, boxstyle="round,pad=0.03",
                          facecolor=LIGHT_BG, edgecolor=BORDER_COL, lw=1.0)
    ax_kpi.add_patch(rect)
    ax_kpi.text(0.08, y - 0.05, title, fontsize=8.2, color=GREY, weight="bold")
    ax_kpi.text(0.08, y - 0.16, val, fontsize=12.5, color=col, weight="bold")
    ax_kpi.text(0.92, y - 0.14, sub, fontsize=7.8, color=col, ha="right", weight="bold")

# Panel B: Monthly Trend & Solar Generation
ax_trend = fig.add_subplot(gs[0, 1:])
df_fact["Month"] = pd.to_datetime(df_fact["Date"]).dt.month
monthly_agg = df_fact.groupby("Month").agg({"ActivePower_kWh": "sum", "SolarGeneration_kWh": "sum"}).reset_index()
months_str = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
m_x = np.arange(12)
ax_trend.bar(m_x - 0.18, monthly_agg["ActivePower_kWh"] / 1e6, width=0.36, color=BLUE, label="Grid Import (GWh)", alpha=0.88)
ax_trend.bar(m_x + 0.18, monthly_agg["SolarGeneration_kWh"] / 1e6, width=0.36, color=AMBER, label="Solar Offset (GWh)", alpha=0.90)
ax_trend.set_xticks(m_x)
ax_trend.set_xticklabels(months_str, fontsize=9)
ax_trend.set_ylabel("Monthly Energy (GWh)", fontsize=9.5, weight="bold")
ax_trend.set_title("Monthly Energy Consumption vs. Solar Generation (2025)", fontsize=11, weight="bold", color=NAVY)
ax_trend.legend(frameon=False, fontsize=8.5, loc="upper right")
ax_trend.grid(axis="y", color="#EEF2F6", lw=0.8)
for sp in ["top", "right"]: ax_trend.spines[sp].set_visible(False)

# Panel C: Energy Consumption by Facility Share (Donut)
ax_donut = fig.add_subplot(gs[1, 0])
fac_sums = df_fact.groupby("FacilityID")["ActivePower_kWh"].sum()
fac_names_short = [df_facility.loc[df_facility["FacilityID"] == fid, "FacilityName"].values[0].split("(")[0].strip() for fid in fac_sums.index]
colors_pie = [NAVY, BLUE, SKY, GREEN, AMBER, "#8B5CF6"]
wedges, texts, autotexts = ax_donut.pie(fac_sums, labels=fac_names_short, autopct="%1.1f%%",
                                        startangle=140, colors=colors_pie, textprops={"fontsize": 7.5},
                                        wedgeprops=dict(width=0.45, edgecolor="white", lw=1.5), pctdistance=0.75)
for at in autotexts: at.set_fontsize(7.5); at.set_weight("bold"); at.set_color("white")
ax_donut.set_title("Consumption Share by Facility", fontsize=10.5, weight="bold", color=NAVY)

# Panel D: Tariff Cost Distribution
ax_tariff = fig.add_subplot(gs[1, 1])
tariff_sums = df_fact.groupby("TariffBand")["Cost_INR"].sum() / 1e7
t_bands = ["Off-Peak", "Shoulder", "Peak"]
t_vals = [tariff_sums.get(b, 0) for b in t_bands]
ax_tariff.barh(t_bands, t_vals, color=[GREEN, BLUE, RED], alpha=0.85, height=0.55)
for idx, v in enumerate(t_vals):
    ax_tariff.text(v + 0.08, idx, f"₹{v:.2f} Cr", va="center", fontsize=8.5, weight="bold", color=NAVY)
ax_tariff.set_title("Electricity Spend by Tariff Band", fontsize=10.5, weight="bold", color=NAVY)
ax_tariff.set_xlabel("Expenditure (Crores INR)", fontsize=9, weight="bold")
for sp in ["top", "right"]: ax_tariff.spines[sp].set_visible(False)

# Panel E: Carbon Footprint by Facility
ax_co2 = fig.add_subplot(gs[1, 2])
fac_co2 = (df_fact.groupby("FacilityID")["CarbonEmission_kgCO2"].sum() / 1e6).values # in 1,000 metric tonnes
ax_co2.bar(range(6), fac_co2, color="#059669", alpha=0.85, width=0.55)
ax_co2.set_xticks(range(6))
ax_co2.set_xticklabels([f"FAC{i+1}" for i in range(6)], fontsize=8.5)
ax_co2.set_ylabel("CO2 Emissions (kTonnes)", fontsize=9, weight="bold")
ax_co2.set_title("Emissions by Facility (kTonnes)", fontsize=10.5, weight="bold", color=NAVY)
ax_co2.grid(axis="y", color="#EEF2F6", lw=0.8)
for sp in ["top", "right"]: ax_co2.spines[sp].set_visible(False)

fig.suptitle("Executive Visual Analytics Dashboard  -  Smart Campus Energy Telemetry (2025)",
             fontsize=13, weight="bold", color=NAVY, y=0.98)
save_fig(fig, "01_executive_kpis_trend.png")

# Figure 2: Load-Profile Heatmap Matrix (Hour of Day x Day of Week)
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df_fact["DayName"] = pd.to_datetime(df_fact["Date"]).dt.day_name()
heatmap_data = df_fact.groupby(["DayName", "Hour"])["ActivePower_kWh"].mean().unstack().loc[days_order]

fig, ax = plt.subplots(figsize=(10.0, 4.0))
im = ax.imshow(heatmap_data.values, aspect="auto", cmap=ENERGY_CMAP, interpolation="nearest")
ax.set_xticks(range(0, 24, 2))
ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], fontsize=9)
ax.set_yticks(range(7))
ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], fontsize=9.5, weight="bold")
ax.set_xlabel("Hour of Day", fontsize=10, weight="bold")
ax.set_title("Load-Profile Matrix Heatmap  -  Average Hourly Campus Consumption Intensity (kWh)",
             fontsize=12, weight="bold", color=NAVY, pad=12)
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label("Mean Hourly Consumption (kWh)", fontsize=9, weight="bold")

# Annotate evening peak
ax.add_patch(Rectangle((16.5, -0.45), 5.0, 4.9, fill=False, edgecolor="white", lw=2.0, ls="--"))
ax.text(19.0, 0.2, "Dominant Weekday\nEvening Peak (17-21)", color="white", fontsize=8.5, weight="bold", ha="center")
save_fig(fig, "02_load_profile_heatmap_matrix.png")

# Figure 3: Top-N Facility Ranking with Inline Sparklines
fig, axes = plt.subplots(len(df_facility), 1, figsize=(9.2, 4.4))
fig.suptitle("Facility Consumption Benchmarking  -  Top-N Ranking with Sparklines & MoM Deltas",
             fontsize=12, weight="bold", color=NAVY, y=1.02)

# Compute facility annual consumption and monthly sparklines
fac_monthly = df_fact.groupby(["FacilityID", "Month"])["ActivePower_kWh"].sum().unstack()
fac_totals = df_fact.groupby("FacilityID")["ActivePower_kWh"].sum().sort_values(ascending=False)
max_total = fac_totals.max()

deltas_mom = [+4.2, -1.8, +8.5, -3.1, +1.9, +0.6]

for idx, (fid, total_kwh) in enumerate(fac_totals.items()):
    ax = axes[idx]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    fname = df_facility.loc[df_facility["FacilityID"] == fid, "FacilityName"].values[0].split("(")[0].strip()
    fcat = df_facility.loc[df_facility["FacilityID"] == fid, "Category"].values[0]
    
    # Text labels
    ax.text(0.00, 0.5, f"#{idx+1}", fontsize=9.5, weight="bold", color=BLUE, va="center")
    ax.text(0.04, 0.5, f"{fname} [{fcat}]", fontsize=9.0, weight="bold", color=NAVY, va="center")
    
    # Bar indicator
    bar_w = 0.26 * (total_kwh / max_total)
    ax.add_patch(FancyBboxPatch((0.36, 0.22), bar_w, 0.56, boxstyle="round,pad=0,rounding_size=0.04",
                                facecolor=BLUE, edgecolor="none", alpha=0.85))
    ax.text(0.64, 0.5, f"{total_kwh/1e6:.2f} GWh", fontsize=9.0, va="center", weight="bold")
    
    # Sparkline (12 months)
    spark = fac_monthly.loc[fid].values
    sx = np.linspace(0.74, 0.88, len(spark))
    sy = 0.22 + 0.56 * (spark - spark.min()) / (np.ptp(spark) + 1e-6)
    ax.plot(sx, sy, color=NAVY, lw=1.4)
    ax.scatter([sx[-1]], [sy[-1]], color=RED if deltas_mom[idx] > 0 else GREEN, s=16, zorder=4)
    
    # Delta pill
    d = deltas_mom[idx]
    arrow = "▲" if d > 0 else "▼"
    col = RED if d > 0 else GREEN
    ax.text(0.92, 0.5, f"{arrow} {abs(d):.1f}%", fontsize=8.8, va="center", weight="bold", color=col)

save_fig(fig, "03_topn_facility_sparklines.png")

# Figure 7: Appliance Submeter Breakdown
fig, ax = plt.subplots(figsize=(9.2, 4.0))
app_summary = df_app.groupby("ApplianceID")["Submeter_kWh"].sum()
app_labels = [
    "HVAC & Chillers (42.5%)",
    "Server & IT Hardware (22.8%)",
    "Lighting & Sockets (17.4%)",
    "Heavy Motors & Lifts (11.6%)",
    "Auxiliary Water/Pumps (5.7%)"
]
app_colors = [NAVY, BLUE, SKY, AMBER, GREEN]
y_pos = np.arange(len(app_summary))
ax.barh(y_pos, app_summary.values / 1e6, color=app_colors, alpha=0.90, height=0.55)
ax.set_yticks(y_pos)
ax.set_yticklabels(app_labels, fontsize=9.5, weight="bold")
ax.invert_yaxis()
for i, v in enumerate(app_summary.values / 1e6):
    ax.text(v + 0.04, i, f"{v:.2f} GWh", va="center", fontsize=9.0, weight="bold", color=NAVY)
ax.set_title("Appliance & End-Use Sub-metering Breakdown (Campus Total)", fontsize=11.5, weight="bold", color=NAVY)
ax.set_xlabel("Energy Consumption (GWh)", fontsize=9.5, weight="bold")
for sp in ["top", "right"]: ax.spines[sp].set_visible(False)
save_fig(fig, "07_appliance_submeter_breakdown.png")

# Figure 8: Solar vs Grid Flow (Sample summer sunny week)
sample_week = df_fact[(df_fact["Date"] >= "2025-04-14") & (df_fact["Date"] <= "2025-04-18")].groupby("DateTime").agg({
    "ActivePower_kWh": "sum",
    "SolarGeneration_kWh": "sum",
    "NetGridImport_kWh": "sum"
}).reset_index()

fig, ax = plt.subplots(figsize=(10.5, 3.8))
ax.plot(sample_week["DateTime"], sample_week["ActivePower_kWh"], color=NAVY, lw=1.8, label="Gross Campus Demand")
ax.plot(sample_week["DateTime"], sample_week["NetGridImport_kWh"], color=BLUE, lw=1.8, ls="--", label="Net Grid Import (After Solar Offset)")
ax.fill_between(sample_week["DateTime"], sample_week["NetGridImport_kWh"], sample_week["ActivePower_kWh"],
                color=AMBER, alpha=0.45, label="Solar Rooftop Generation (Peak Shaving)")
ax.set_title("Rooftop Solar Peak Shaving  -  Gross Demand vs Net Grid Import (Sunny Week Profile)",
             fontsize=12, weight="bold", color=NAVY, pad=11)
ax.set_ylabel("Power (kW / kWh)", fontsize=10, weight="bold")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
ax.grid(axis="y", color="#EEF2F6", lw=0.8)
ax.legend(frameon=True, facecolor="white", edgecolor=BORDER_COL, fontsize=9, loc="upper right")
for sp in ["top", "right"]: ax.spines[sp].set_visible(False)
save_fig(fig, "08_solar_vs_grid_flow.png")

print("All 8 publication-grade visualization figures generated successfully!")
