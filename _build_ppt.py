"""
Visual Analytics Lab (MACSE603) - Final Project Presentation Deck
Smart Energy Consumption Visualization Dashboard Using Power BI & IoT Pipelines
Team:
  - Vedant Nimkar (26MML0045) - Team Leader
  - Jitesh Bobde (26MML0025) - Team Member
  - Ayush Sharma (26MML0043) - Team Member
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

NAVY = RGBColor(0x10, 0x24, 0x5C)
BLUE = RGBColor(0x33, 0x66, 0xCC)
SKY = RGBColor(0x6F, 0xA3, 0xFF)
LIGHT = RGBColor(0xF3, 0xF7, 0xFF)
BORDER = RGBColor(0xC8, 0xD4, 0xEE)
DARK = RGBColor(0x1C, 0x1C, 0x1C)
MUTED = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x1E, 0x7A, 0x4F)
AMBER = RGBColor(0xB0, 0x6A, 0x00)
RED = RGBColor(0xC0, 0x39, 0x2B)

W, H = Inches(13.333), Inches(7.5)
COURSE = "MACSE603 - Visual Analytics Lab"

MEMBERS = [
    ("Vedant Nimkar", "26MML0045", "Team Leader"),
    ("Jitesh Bobde", "26MML0025", "Member"),
    ("Ayush Sharma", "26MML0043", "Member"),
]

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
PAGE = [0]

FOLDER = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(FOLDER, "images")

def blank():
    return prs.slides.add_slide(prs.slide_layouts[6])

def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    return sh

def textbox(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    return tf

def para(tf, text, size=14, bold=False, color=DARK, space_after=6,
         align=PP_ALIGN.LEFT, first=False, italic=False, line_spacing=1.15):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = "Segoe UI"
    return p

def bullet(tf, text, size=13.5, lead=None, first=False, space_after=8, marker="\u25aa"):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.line_spacing = 1.18
    r0 = p.add_run()
    r0.text = marker + "   "
    r0.font.size = Pt(size)
    r0.font.color.rgb = BLUE
    r0.font.name = "Segoe UI"
    if lead:
        rb = p.add_run()
        rb.text = lead
        rb.font.size = Pt(size)
        rb.font.bold = True
        rb.font.color.rgb = NAVY
        rb.font.name = "Segoe UI"
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = DARK
    r.font.name = "Segoe UI"
    return p

def header(slide, num, title):
    rect(slide, Inches(0), Inches(0), W, Inches(0.14), fill=NAVY)
    rect(slide, Inches(0.55), Inches(0.36), Inches(0.62), Inches(0.62), fill=BLUE)
    t = textbox(slide, Inches(0.55), Inches(0.47), Inches(0.62), Inches(0.4))
    para(t, str(num), size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER, first=True)
    t = textbox(slide, Inches(1.35), Inches(0.42), Inches(11.4), Inches(0.6))
    para(t, title, size=25, bold=True, color=NAVY, first=True)
    rect(slide, Inches(1.35), Inches(1.11), Inches(1.15), Inches(0.05), fill=BLUE)

def footer(slide):
    PAGE[0] += 1
    t = textbox(slide, Inches(0.55), Inches(7.04), Inches(9.5), Inches(0.28))
    para(t, f"{COURSE}  |  Smart Energy Consumption Visualization Dashboard Using Power BI & IoT Pipelines",
         size=9, color=MUTED, first=True)
    t = textbox(slide, Inches(12.1), Inches(7.04), Inches(0.7), Inches(0.28))
    para(t, str(PAGE[0]), size=9, bold=True, color=BLUE, align=PP_ALIGN.RIGHT, first=True)

def divider(kicker, title, subtitle):
    s = blank()
    rect(s, Inches(0), Inches(0), W, H, fill=NAVY)
    rect(s, Inches(0), Inches(3.3), W, Inches(0.055), fill=BLUE)
    t = textbox(s, Inches(1.1), Inches(2.3), Inches(11), Inches(0.45))
    para(t, kicker, size=13, bold=True, color=SKY, first=True)
    t = textbox(s, Inches(1.1), Inches(3.6), Inches(11.2), Inches(1.8))
    para(t, title, size=36, bold=True, color=WHITE, space_after=8, first=True)
    para(t, subtitle, size=15, color=SKY, line_spacing=1.2)
    footer(s)

def visual_slide(num, title, img, caption, blocks, img_h=Inches(3.1), source=None):
    s = blank()
    header(s, num, title)
    img_path = os.path.join(IMG, img)
    if os.path.exists(img_path):
        pic = s.shapes.add_picture(img_path, Inches(0.55), Inches(1.3), height=img_h)
        pic.left = int((W - pic.width) / 2)
    rect(s, Inches(0.55), Inches(1.3) + img_h + Inches(0.06), Inches(12.22), Inches(0.03), fill=BORDER)

    t = textbox(s, Inches(0.55), Inches(1.3) + img_h + Inches(0.14), Inches(12.22), Inches(0.3))
    para(t, caption, size=10.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, first=True)

    y = Inches(1.3) + img_h + Inches(0.48)
    bw = Inches(12.22 / len(blocks)) - Inches(0.16)
    x = Inches(0.55)
    avail = Inches(7.0) - y - Inches(0.1)
    for label, body, accent in blocks:
        rect(s, x, y, bw, avail, fill=LIGHT, line=BORDER)
        rect(s, x, y, bw, Inches(0.06), fill=accent)
        t = textbox(s, x + Inches(0.2), y + Inches(0.16), bw - Inches(0.4), Inches(0.28))
        para(t, label, size=9.5, bold=True, color=accent, first=True)
        t = textbox(s, x + Inches(0.2), y + Inches(0.48), bw - Inches(0.4), avail - Inches(0.6))
        para(t, body, size=10.2, color=DARK, first=True, line_spacing=1.15)
        x += bw + Inches(0.16)

    if source:
        t = textbox(s, Inches(0.55), Inches(6.74), Inches(12.22), Inches(0.26))
        para(t, source, size=9, italic=True, color=BLUE, align=PP_ALIGN.RIGHT, first=True)
    footer(s)

# ============================================================ SLIDE 1: Title
s = blank()
rect(s, Inches(0), Inches(0), W, Inches(0.5), fill=NAVY)
rect(s, Inches(0), Inches(0.5), W, Inches(0.08), fill=BLUE)
rect(s, Inches(0), Inches(7.2), W, Inches(0.3), fill=NAVY)

t = textbox(s, Inches(0.85), Inches(0.11), Inches(11.6), Inches(0.32))
para(t, COURSE.upper(), size=12, bold=True, color=SKY, first=True)

t = textbox(s, Inches(0.85), Inches(1.15), Inches(11.6), Inches(0.35))
para(t, "ACADEMIC FINAL PROJECT DEFENSE", size=12.5, bold=True, color=BLUE, first=True)

t = textbox(s, Inches(0.85), Inches(1.68), Inches(11.6), Inches(2.0))
para(t, "Smart Energy Consumption", size=38, bold=True, color=NAVY, space_after=2, first=True)
para(t, "Visualization Dashboard", size=38, bold=True, color=NAVY, space_after=2)
para(t, "Using Power BI & IoT Pipelines", size=38, bold=True, color=BLUE)

rect(s, Inches(0.85), Inches(3.92), Inches(1.4), Inches(0.05), fill=BLUE)

t = textbox(s, Inches(0.85), Inches(4.2), Inches(11.6), Inches(0.32))
para(t, "PROJECT TEAM MEMBERS", size=11.5, bold=True, color=MUTED, first=True)

cx = Inches(0.85)
for name, reg, role in MEMBERS:
    rect(s, cx, Inches(4.65), Inches(3.72), Inches(1.5), fill=LIGHT, line=BORDER)
    rect(s, cx, Inches(4.65), Inches(3.72), Inches(0.07), fill=BLUE)
    t = textbox(s, cx + Inches(0.3), Inches(4.9), Inches(3.15), Inches(1.1))
    para(t, name, size=16.5, bold=True, color=NAVY, space_after=4, first=True)
    para(t, f"Reg. No. {reg}", size=12, color=MUTED, space_after=6)
    para(t, role.upper(), size=9.5, bold=True, color=(GREEN if role == "Team Leader" else BLUE))
    cx += Inches(3.97)

t = textbox(s, Inches(0.85), Inches(6.42), Inches(11.6), Inches(0.35))
para(t, "Full Implementation: Star Schema (52.5k rows) • ML Demand Forecast • Shewhart 3σ Anomalies • Apache ECharts & Power BI",
     size=12, italic=True, color=MUTED, first=True)

t = textbox(s, Inches(0.85), Inches(7.25), Inches(11.6), Inches(0.24))
para(t, "M.Tech - Computer Science and Engineering", size=10, color=SKY, first=True)

# ============================================================ SLIDE 2: Abstract
s = blank()
header(s, 2, "Abstract & Problem Statement")
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(5.35), fill=LIGHT, line=BORDER)
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(0.07), fill=BLUE)
t = textbox(s, Inches(0.9), Inches(1.66), Inches(5.3), Inches(0.3))
para(t, "PROJECT ABSTRACT", size=11.5, bold=True, color=BLUE, first=True)
t = textbox(s, Inches(0.9), Inches(2.08), Inches(5.3), Inches(4.4))
para(t, "This project implements an enterprise-grade Smart Energy Consumption Visual Analytics platform "
        "addressing the operational complexities of modern multi-facility campuses.", size=12.5, first=True, space_after=10)
para(t, "It unifies IoT edge-sensor ingestion (ESP32 via MQTT), an automated ETL pipeline with Cooling Degree Hours, "
        "an 11-table Star Schema warehouse (52,560 hourly metered readings for FY 2025 across 6 facilities), and advanced machine learning.",
     size=12.5, space_after=10)
para(t, "Core analytical capabilities include Ridge/Prophet time-series demand forecasting (R² = 0.996), Shewhart 3-sigma "
        "anomaly detection (196 operational breaches flagged), and t-SNE 2D clustering across four behavioral archetypes.",
     size=12.5, space_after=10)
para(t, "Delivery is realized via both a production Power BI Desktop model (50+ DAX measures) and an interactive "
        "Apache ECharts Web Dashboard with real-time IoT streaming simulation.", size=12.5)

rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(5.35), fill=WHITE, line=BORDER)
rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(0.07), fill=AMBER)
t = textbox(s, Inches(7.13), Inches(1.66), Inches(5.3), Inches(0.3))
para(t, "CORE OPERATIONAL CHALLENGES ADDRESSED", size=11.5, bold=True, color=AMBER, first=True)
t = textbox(s, Inches(7.13), Inches(2.08), Inches(5.3), Inches(4.4))
for i, (lead, body) in enumerate([
    ("Fragmented Telemetry - ", "Smart meters, BMS sensors and bills reside in silos with inconsistent temporal granularity."),
    ("Unmonitored Peak Demand - ", "Summer afternoon coincident peaks trigger severe utility demand charges (INR 350/kW)."),
    ("Silent Equipment Runaways - ", "Chillers, AHUs, and exhaust fans left running on weekends remain undetected for billing cycles."),
    ("Inflexible Monthly Reporting - ", "Traditional accounting bills report past spend without forward forecasting or uncertainty bounds."),
    ("Disconnected BI & IoT - ", "Academic IoT prototypes rarely integrate with enterprise dimensional modeling and business intelligence."),
]):
    bullet(t, body, lead=lead, size=12.2, first=(i == 0), space_after=12)
footer(s)

# ============================================================ SLIDE 3: Objectives
s = blank()
header(s, 3, "Project Objectives & Scope")
objectives = [
    ("End-to-End IoT Pipeline", "Build automated ingestion and ETL pipelines standardizing 52,560 hourly records with strict quality gates.", BLUE),
    ("Star Schema Data Warehouse", "Design an 11-table Kimball dimensional model with fact tables for energy, submeters, forecasts, and anomalies.", NAVY),
    ("ML Demand Forecasting", "Implement time-series demand forecasting with Fourier seasonality and 95% expanding uncertainty bands.", BLUE),
    ("Statistical Anomaly Engine", "Deploy Shewhart 3-sigma control limits to automatically detect and cost operational equipment breaches.", NAVY),
    ("High-Dimensional Load Profiling", "Normalize 24-hour diurnal load vectors and map them to 2D manifold coordinates using t-SNE and K-Means.", BLUE),
    ("Dual Enterprise Serving", "Deliver both an enterprise Power BI model (50+ DAX measures) and an interactive Apache ECharts Web Dashboard.", NAVY),
]
for i, (title, body, accent) in enumerate(objectives):
    col = Inches(0.55) if i < 3 else Inches(6.78)
    row_y = Inches(1.42 + (i % 3) * 1.82)
    rect(s, col, row_y, Inches(5.99), Inches(1.68), fill=LIGHT, line=BORDER)
    rect(s, col, row_y, Inches(5.99), Inches(0.06), fill=accent)
    t = textbox(s, col + Inches(0.28), row_y + Inches(0.18), Inches(5.4), Inches(0.32))
    para(t, f"0{i+1}.  {title}", size=14, bold=True, color=NAVY, first=True)
    t = textbox(s, col + Inches(0.28), row_y + Inches(0.56), Inches(5.4), Inches(0.98))
    para(t, body, size=12, color=DARK, first=True, line_spacing=1.18)
footer(s)

# ============================================================ SLIDE 4: Literature Review
s = blank()
header(s, 4, "Literature Review & Synthesis of Core Papers")
t = textbox(s, Inches(0.55), Inches(1.28), Inches(12.2), Inches(0.32))
para(t, "Synthesis of six foundational research papers — two papers reviewed per team member:", size=12.5, italic=True, color=MUTED, first=True)
papers = [
    ("Paper 1: Portugal Energy Distribution (2024)", "DSRM methodology for national hourly & geographic distribution in Power BI.", "Adopted star schema, role-specific views, and DSRM lifecycle.", "Vedant Nimkar"),
    ("Paper 2: Awate et al. (IJARSCT 2023)", "Analyzed 500 residential meters over 24 months with Prophet demand forecasting.", "Transitioned to hourly telemetry; integrated Prophet seasonal models.", "Vedant Nimkar"),
    ("Paper 3: Energy Calculation in Power BI (2023)", "End-to-end dashboard sequence: collection, modeling, visuals, filters.", "Constructed 50+ DAX library, time intelligence, and Power Query M scripts.", "Jitesh Bobde"),
    ("Paper 4: Soliman & Fetais (IEEE GCCCE 2017)", "Big data visualization of Qatar smart meter network; standardization and speed.", "Implemented ETL quality gates, boundary checks, and null treatment.", "Jitesh Bobde"),
    ("Paper 5: IoT Smart Energy System (IJIRT 2026)", "ESP32 voltage/current sensing, MQTT broker, cloud ingestion, fault prediction.", "Engineered streaming IoT telemetry simulator emitting 3-phase readings.", "Ayush Sharma"),
    ("Paper 6: Interactive ML Dashboard (ESANN 2024)", "2D manifold mapping of daily load profiles using t-SNE, sparklines, data cubes.", "Normalized 24-hr load vectors with t-SNE projection and K-Means clustering.", "Ayush Sharma"),
]
y = Inches(1.72)
for title, summary, takeaway, member in papers:
    rect(s, Inches(0.55), y, Inches(12.22), Inches(0.78), fill=LIGHT, line=BORDER)
    rect(s, Inches(0.55), y, Inches(0.07), Inches(0.78), fill=BLUE)
    t = textbox(s, Inches(0.8), y + Inches(0.12), Inches(3.6), Inches(0.55))
    para(t, title, size=11, bold=True, color=NAVY, first=True)
    para(t, f"Reviewed by: {member}", size=9.5, italic=True, color=BLUE)
    t = textbox(s, Inches(4.55), y + Inches(0.12), Inches(4.0), Inches(0.55))
    para(t, summary, size=10, color=DARK, first=True)
    t = textbox(s, Inches(8.75), y + Inches(0.12), Inches(3.85), Inches(0.55))
    para(t, f"System Takeaway: {takeaway}", size=10, color=GREEN, bold=True, first=True)
    y += Inches(0.86)
footer(s)

# ============================================================ SLIDE 5: Pipeline Architecture
s = blank()
header(s, 5, "End-to-End System & Pipeline Architecture")
t = textbox(s, Inches(0.55), Inches(1.3), Inches(12.2), Inches(0.3))
para(t, "A decoupled 5-tier production pipeline orchestrating ingestion through dual analytical delivery:", size=12, italic=True, color=MUTED, first=True)

stages = [
    ("1. INGESTION GATE", "ESP32 edge-sensor telemetry (MQTT) + batch meter CSVs. Schema validation and boundary enforcement.", BLUE),
    ("2. ETL & QUALITY", "Unit standardization (kWh, kVA, kW peak), Cooling Degree Hours (CDH), missing value imputation, foreign-key audit.", NAVY),
    ("3. STAR SCHEMA WAREHOUSE", "11 Fact and Dimension tables (52,560 hourly rows for FY 2025 across 6 facilities). Optimized VertiPaq compression.", BLUE),
    ("4. ML ANALYTICS ENGINE", "Prophet/Ridge regression demand forecasting, Shewhart 3σ statistical anomaly engine, t-SNE 2D manifold clustering.", NAVY),
    ("5. DUAL SERVING", "Enterprise Power BI Desktop model (50+ DAX measures) + Interactive Apache ECharts Web Dashboard with live MQTT stream.", GREEN),
]
y = Inches(1.75)
for title, desc, accent in stages:
    rect(s, Inches(0.55), y, Inches(12.22), Inches(0.92), fill=LIGHT, line=BORDER)
    rect(s, Inches(0.55), y, Inches(2.6), Inches(0.92), fill=accent)
    t = textbox(s, Inches(0.75), y + Inches(0.3), Inches(2.3), Inches(0.35))
    para(t, title, size=11, bold=True, color=WHITE, first=True)
    t = textbox(s, Inches(3.35), y + Inches(0.2), Inches(9.2), Inches(0.55))
    para(t, desc, size=11.5, color=DARK, first=True, line_spacing=1.18)
    y += Inches(1.02)
footer(s)

# ============================================================ SLIDE 6: Star Schema
s = blank()
header(s, 6, "Star-Schema Dimensional Warehouse Model")
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(5.35), fill=LIGHT, line=BORDER)
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(0.07), fill=NAVY)
t = textbox(s, Inches(0.85), Inches(1.65), Inches(5.4), Inches(0.3))
para(t, "WAREHOUSE TABLE INVENTORY & CARDINALITY", size=11.5, bold=True, color=NAVY, first=True)
t = textbox(s, Inches(0.85), Inches(2.05), Inches(5.4), Inches(4.5))
for lead, body in [
    ("Fact_EnergyConsumption (52,560 rows) - ", "Central grain: hourly active power, solar gen, grid import, cost, and anomaly flags."),
    ("Fact_ApplianceSubmeter (60,480 rows) - ", "End-use breakdown: HVAC, IT servers, lighting, industrial motors, and auxiliary."),
    ("Fact_DemandForecast (395 rows) - ", "Historical observed demand + 30-day forward ML projection with 95% confidence bounds."),
    ("Fact_Anomalies_Detailed (196 rows) - ", "Rolling baseline breaches with excess energy (kWh), wasted cost (INR), and root cause."),
    ("Fact_LoadClusters (2,190 rows) - ", "24-hour normalized load vectors mapped to 2D t-SNE coordinates and cluster IDs."),
]:
    bullet(t, body, lead=lead, size=11, space_after=10)

rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(5.35), fill=WHITE, line=BORDER)
rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(0.07), fill=BLUE)
t = textbox(s, Inches(7.1), Inches(1.65), Inches(5.4), Inches(0.3))
para(t, "DIMENSIONAL ATTRIBUTES & QUALITY GATES", size=11.5, bold=True, color=BLUE, first=True)
t = textbox(s, Inches(7.1), Inches(2.05), Inches(5.4), Inches(4.5))
for lead, body in [
    ("Dim_Facility (6 rows) - ", "Facility name, square footage, baseline kW, peak design kW, solar kWp, and Energy Star score."),
    ("Dim_Tariff (3 rows) - ", "Time-of-Use tariffs (HT-ToU, LT-ToU, Residential) with Peak, Shoulder, and Off-Peak rates."),
    ("Dim_Date & Dim_Time (731 + 24 rows) - ", "Calendar hierarchies, day parts, weekend indicators, and peak tariff flags."),
    ("Dim_Weather (17,544 rows) - ", "Ambient temperature, relative humidity, solar irradiance, and Cooling Degree Hours (CDH)."),
    ("Referential Integrity Gate - ", "100% verified foreign key consistency; zero orphaned records or unmapped tariffs."),
]:
    bullet(t, body, lead=lead, size=11, space_after=10)
footer(s)

# ============================================================ SLIDE 7: Heatmap Visual
visual_slide(
    7, "24x7 Diurnal Load-Profile Heatmap Matrix",
    "02_load_profile_heatmap_matrix.png",
    "Implemented Visualization: Hourly load intensity (kW) across day-of-week and hour-of-day for the complete campus micro-grid.",
    [
        ("OPERATIONAL PATTERN", "Reveals consistent morning ramp at 08:30, high plateau during working hours (09:00 - 17:00), coincident peak (14:00 - 17:00), and sharp weekend drop.", BLUE),
        ("POWER BI & ECHARTS", "Rendered as an interactive matrix visual in Power BI with conditional color gradient and in ECharts with dynamic visualMap range filtering.", NAVY),
        ("STRATEGIC IMPACT", "Directs equipment pre-cooling and load staggering specifically at peak tariff hours rather than broad day-long curtailment.", GREEN),
    ],
    source="Traces to Paper 2 (hourly granularity) and Paper 6 (visual analytics)")

# ============================================================ SLIDE 8: Forecasting Visual
visual_slide(
    8, "Prophet/Ridge Time-Series Demand Forecasting",
    "04_prophet_demand_forecast.png",
    "Implemented Visualization: 30-day forward demand trajectory with expanding 95% prediction confidence interval.",
    [
        ("MODEL ACCURACY", "R² = 0.996, MAPE = 0.61%, MAE = 270.1 kWh on a 30-day holdout validation horizon using Fourier harmonic decomposition.", BLUE),
        ("WEATHER COUPLING", "Explicitly incorporates Cooling Degree Hours (CDH) to model non-linear summer chiller surges as ambient temperature exceeds 24°C.", NAVY),
        ("CAPACITY PLANNING", "Enables utility procurement and contract demand setting against an expected range rather than unreliable single-point estimates.", GREEN),
    ],
    source="Traces to Paper 2 (Prophet forecasting) and Paper 5 (regression forecasting)")

# ============================================================ SLIDE 9: Anomaly Visual
visual_slide(
    9, "Shewhart 3-Sigma Automated Anomaly Engine",
    "05_anomaly_detection_control_limits.png",
    "Implemented Visualization: Real-time telemetry evaluated against centered rolling Shewhart ±3σ statistical control limits.",
    [
        ("BREACH DETECTION", "Identified 196 operational breaches. Successfully caught a weekend chiller runaway in Main Tech Tower (+280 kWh/h) wasting INR 64,400.", RED),
        ("AUTOMATED TRIAGE", "Replaces passive end-of-month utility bill review with automated hourly alerts, classifying events by severity (Critical vs Warning).", NAVY),
        ("ROOT CAUSE ISOLATION", "Distinguishes weather-induced surges from true faults (e.g., night baseload leaks, solar inverter midday dropouts).", GREEN),
    ],
    source="Traces to Paper 4 (outlier handling) and Paper 5 (fault anticipation)")

# ============================================================ SLIDE 10: Clustering Visual
visual_slide(
    10, "t-SNE 2D Manifold Load-Shape Clustering",
    "06_tsne_load_shape_clusters.png",
    "Implemented Visualization: Non-linear projection of 24-dimensional diurnal load vectors into four distinct operational archetypes.",
    [
        ("FOUR ARCHETYPES", "Cluster 1: Commercial Day-Shift Heavy (Blue); Cluster 2: Continuous Baseload (Green); Cluster 3: Residential Hostels (Amber); Cluster 4: Weekend Idle (Purple).", BLUE),
        ("NORMALIZED SHAPE", "Vectors are min-max normalized by daily peak load to cluster buildings by behavioral schedule rather than absolute size.", NAVY),
        ("TARGETED POLICIES", "Allows demand-management initiatives to be customized per cluster (e.g. hostel evening shifting vs tech tower pre-cooling).", GREEN),
    ],
    source="Traces to Paper 6 (t-SNE load profiling and morphing projections)")

# ============================================================ SLIDE 11: Top-N Benchmarking
visual_slide(
    11, "Facility Benchmarking & Top-N Sparklines",
    "03_topn_facility_sparklines.png",
    "Implemented Visualization: Annual consumption ranking with inline monthly sparklines, category tags, and Energy Star ratings.",
    [
        ("PARETO CONCENTRATION", "Main Tech Tower (5.34 GWh) and Data Center (4.88 GWh) account for over 52.8% of total campus energy expenditure.", BLUE),
        ("MOMENTUM & TREND", "Inline sparklines allow facility managers to instantly separate entities with accelerating consumption from those improving.", NAVY),
        ("PORTFOLIO VIEW", "Integrates Energy Star scores (76 to 91) and floor area benchmarking (kWh/sq.ft) to prioritize retrofit capital expenditure.", GREEN),
    ],
    source="Traces to Paper 2 (consumer ranking) and Paper 6 (sparklines)")

# ============================================================ SLIDE 12: Appliance Submetering
visual_slide(
    12, "Appliance Submetering & End-Use Breakdown",
    "07_appliance_submeter_breakdown.png",
    "Implemented Visualization: Campus-wide disaggregation across major electrical submetering categories.",
    [
        ("CHILLER DOMINANCE", "HVAC & Chillers constitute 42.0% (8.13 GWh) of total campus consumption, representing the single largest target for optimization.", BLUE),
        ("INFLEXIBLE BASELOAD", "Server & IT Infrastructure contributes 22.0% (4.26 GWh), operating at an uninterrupted continuous flat load curve.", NAVY),
        ("CONTROLLABLE LOADS", "Lighting (18.0%) and Machinery (12.0%) offer rapid payback opportunities through automated occupancy sensors and VFD retrofits.", GREEN),
    ],
    source="Traces to Paper 3 (appliance calculations) and Paper 1 (submetering)")

# ============================================================ SLIDE 13: Solar & Grid Balance
visual_slide(
    13, "Renewable Solar Flow & Grid Balance",
    "08_solar_vs_grid_flow.png",
    "Implemented Visualization: Average diurnal power flow comparing total demand, solar generation, and net grid import.",
    [
        ("SOLAR GENERATION", "Total annual solar generation of 1.14 GWh across 590 kWp installed rooftop capacity (5.9% total campus penetration).", GREEN),
        ("PEAK OFFSET", "Solar peaks between 11:00 and 14:00, perfectly coinciding with rising daytime cooling demand and shaving contract grid draw.", BLUE),
        ("CARBON ABATEMENT", "Directly offsets 936.8 metric tons of CO2e annually (CEA grid emission factor of 0.82 kg/kWh), equivalent to ~42,500 trees.", NAVY),
    ],
    source="Integrates Papers 1, 3, 4 and 5")

# ============================================================ SLIDE 14: Apache ECharts & Web Dashboard
s = blank()
header(s, 14, "Interactive Apache ECharts & Web Dashboard")
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(5.35), fill=LIGHT, line=BORDER)
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(0.07), fill=BLUE)
t = textbox(s, Inches(0.85), Inches(1.65), Inches(5.4), Inches(0.3))
para(t, "APACHE ECHARTS INTERACTIVE SUITE", size=11.5, bold=True, color=BLUE, first=True)
t = textbox(s, Inches(0.85), Inches(2.05), Inches(5.4), Inches(4.5))
for lead, body in [
    ("Rich Visual Aesthetics - ", "Engineered with Apache ECharts 5.5, dark cyber-glassmorphism, smooth bezier curves, and gradient area fills."),
    ("24x7 Heatmap with visualMap - ", "Interactive continuous slider allows real-time dynamic filtering of load intensity cells."),
    ("Reactive Global Slicers - ", "Dropdown facility selector instantly updates all KPI cards, diurnal curves, and highlights t-SNE scatter points."),
    ("Submeter Nightingale Donut - ", "Rounded-corner doughnut layout with hover expansion and center metric summary."),
    ("Zero Cloud Dependencies - ", "Bundled standalone echarts.min.js and dashboard_data.js for 100% offline local execution."),
]:
    bullet(t, body, lead=lead, size=11, space_after=10)

rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(5.35), fill=WHITE, line=BORDER)
rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(0.07), fill=GREEN)
t = textbox(s, Inches(7.1), Inches(1.65), Inches(5.4), Inches(0.3))
para(t, "LIVE IOT SENSOR STREAMING SIMULATION", size=11.5, bold=True, color=GREEN, first=True)
t = textbox(s, Inches(7.1), Inches(2.05), Inches(5.4), Inches(4.5))
for lead, body in [
    ("Live ESP32 MQTT Emulation - ", "Simulates incoming sensor packets every 1.5s with realistic 3-phase electrical noise and occasional surge anomalies."),
    ("Real-Time ECharts Gauge - ", "Animated power gauge meter dynamically tracking instantaneous active demand against operational thresholds."),
    ("Rolling Oscilloscope Chart - ", "Live 30-point rolling waveform displaying real-time power fluctuations and voltage stability."),
    ("Live Terminal Ingestion Log - ", "Timestamped MQTT JSON messages logged live with packet counter, latency monitor, and quality flag."),
    ("Anomaly Inspector Modal - ", "Tabular event log displaying excess kW, root cause, and wasted financial cost for every detected breach."),
]:
    bullet(t, body, lead=lead, size=11, space_after=10)
footer(s)

# ============================================================ SLIDE 15: Decision Support & ROI
s = blank()
header(s, 15, "Decision Support & Financial Impact")
roi_cards = [
    ("Peak Shaving Optimization", "Shifting HVAC load via 11:00-13:00 pre-cooling reduces contract demand by 15%, saving an estimated INR 18.5 Lakhs annually in tariff demand charges.", BLUE),
    ("Weekend Equipment Shutdown", "Automated Shewhart 3σ alerts prevent unmonitored chiller runaways, eliminating ~INR 2.84 Lakhs in avoidable weekend waste.", NAVY),
    ("Targeted Solar Expansion", "Analysis pinpoints Computing Wing C (4.88 GWh baseload, 0% solar) as the highest-return location for a 350 kWp carport solar PV array.", GREEN),
    ("Power Factor Correction", "Continuous monitoring of reactive power (kVARh) maintains power factor above 0.95, avoiding utility penalty surcharges.", BLUE),
]
for i, (title, body, accent) in enumerate(roi_cards):
    col = Inches(0.55) if i < 2 else Inches(6.78)
    row_y = Inches(1.5 + (i % 2) * 2.65)
    rect(s, col, row_y, Inches(5.99), Inches(2.45), fill=LIGHT, line=BORDER)
    rect(s, col, row_y, Inches(5.99), Inches(0.07), fill=accent)
    t = textbox(s, col + Inches(0.3), row_y + Inches(0.22), Inches(5.4), Inches(0.35))
    para(t, title, size=15, bold=True, color=NAVY, first=True)
    t = textbox(s, col + Inches(0.3), row_y + Inches(0.7), Inches(5.4), Inches(1.6))
    para(t, body, size=12.5, color=DARK, first=True, line_spacing=1.2)
footer(s)

# ============================================================ SLIDE 16: Summary of Achievements
s = blank()
header(s, 16, "Project Summary & Quantitative Achievements")
rect(s, Inches(0.55), Inches(1.38), Inches(12.22), Inches(5.35), fill=LIGHT, line=BORDER)
rect(s, Inches(0.55), Inches(1.38), Inches(12.22), Inches(0.07), fill=NAVY)

t = textbox(s, Inches(0.9), Inches(1.68), Inches(11.5), Inches(0.35))
para(t, "KEY QUANTITATIVE DELIVERABLES (FY 2025)", size=13, bold=True, color=NAVY, first=True)

metrics = [
    ("Total Active Energy", "19.35 GWh", "52,560 hourly metered readings across 6 campus facilities"),
    ("Electricity Spend", "₹13.20 Cr", "Time-of-Use tariff structure with peak penalty accounting"),
    ("Solar Generation", "1.14 GWh", "5.90% Renewable penetration from 590 kWp installed PV"),
    ("Campus Peak Demand", "2,840 kW", "Coincident summer cooling peak recorded in June"),
    ("Carbon Offset", "936.8 tCO2e", "Direct clean generation abatement (0.82 kg/kWh CEA factor)"),
    ("Forecasting Accuracy", "R² = 0.996", "MAPE = 0.61%, MAE = 270.1 kWh on 30-day holdout validation"),
    ("Operational Breaches", "196 Flagged", "Shewhart ±3σ control limits identifying equipment leaks"),
    ("Interactive Serving", "Dual Delivery", "Power BI Desktop (50+ DAX measures) & Apache ECharts Web UI"),
]
y_m = Inches(2.15)
for i, (label, val, note) in enumerate(metrics):
    col_x = Inches(0.9) if i < 4 else Inches(6.8)
    cur_y = y_m + (i % 4) * Inches(1.05)
    rect(s, col_x, cur_y, Inches(5.6), Inches(0.9), fill=WHITE, line=BORDER)
    rect(s, col_x, cur_y, Inches(0.08), Inches(0.9), fill=BLUE)
    t = textbox(s, col_x + Inches(0.2), cur_y + Inches(0.12), Inches(2.4), Inches(0.35))
    para(t, label, size=10, bold=True, color=MUTED, first=True)
    t = textbox(s, col_x + Inches(0.2), cur_y + Inches(0.42), Inches(2.4), Inches(0.4))
    para(t, val, size=16, bold=True, color=NAVY, first=True)
    t = textbox(s, col_x + Inches(2.7), cur_y + Inches(0.2), Inches(2.75), Inches(0.6))
    para(t, note, size=9.5, color=DARK, first=True, line_spacing=1.1)
footer(s)

# ============================================================ SAVE
def save_presentation():
    saved_paths = []
    for suffix in ["_v2", "_v3", ""]:
        path = os.path.join(FOLDER, f"Team_VisualAnalytics_SmartEnergy_PowerBI{suffix}.pptx")
        try:
            prs.save(path)
            saved_paths.append(path)
            print(f"Saved: {path}")
        except PermissionError:
            print(f"  Note: {os.path.basename(path)} is locked by another process.")
    return saved_paths

saved = save_presentation()
print(f"Presentation build complete! Total slides: {len(prs.slides._sldIdLst)}")
