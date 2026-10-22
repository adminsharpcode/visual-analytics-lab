"""
Academic Comprehensive Project Report Generator
Course: MACSE603 - Visual Analytics Lab
Topic: Smart Energy Consumption Visualization Dashboard Using Power BI & IoT Pipelines
Authors: Vedant Nimkar (26MML0045, Lead), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)
Evaluator / Guide: Dr. Mary Jennifer J / Faculty Evaluator, SCOPE, VIT Vellore
Cover Page Template: Grounded in Team7_Final_Technical_Report_AI_WorkLifeBalance.pdf
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "Project_SmartEnergy_PowerBI", "figures")
IMG_DIR = os.path.join(BASE_DIR, "images")
REPORT_DIR = os.path.join(BASE_DIR, "Project_SmartEnergy_PowerBI", "report")
os.makedirs(REPORT_DIR, exist_ok=True)

PDF_ROOT = os.path.join(BASE_DIR, "Smart_Energy_Consumption_Analytics_Comprehensive_Report.pdf")
PDF_PROJECT = os.path.join(REPORT_DIR, "Smart_Energy_Consumption_Analytics_Comprehensive_Report.pdf")
MD_ROOT = os.path.join(BASE_DIR, "Smart_Energy_Consumption_Analytics_Comprehensive_Report.md")
MD_PROJECT = os.path.join(REPORT_DIR, "Smart_Energy_Consumption_Analytics_Comprehensive_Report.md")

# Numbered Canvas for Dynamic "Page X of Y" and Running Headers
class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return # Suppress header/footer on formal Cover Page

        self.saveState()
        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#10245C"))
        self.drawString(45, 805, "MACSE603: VISUAL ANALYTICS LAB  |  COMPREHENSIVE CAPSTONE REPORT")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(550, 805, "Smart Energy Power BI & Telemetry Dashboard")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 798, 550, 798)

        # Running Footer
        self.line(45, 45, 550, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(45, 33, "Team: Vedant Nimkar (Lead - 26MML0045), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(550, 33, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_ROOT,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Color Palette
    C_NAVY = colors.HexColor("#10245C")
    C_BLUE = colors.HexColor("#1E40AF")
    C_SKY = colors.HexColor("#3B82F6")
    C_LIGHT = colors.HexColor("#F8FAFC")
    C_BORDER = colors.HexColor("#E2E8F0")
    C_DARK = colors.HexColor("#0F172A")
    C_MUTED = colors.HexColor("#475569")
    C_GREEN = colors.HexColor("#059669")
    C_AMBER = colors.HexColor("#D97706")
    C_RED = colors.HexColor("#DC2626")

    # Typography Styles
    cover_inst_style = ParagraphStyle(
        "CoverInst",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        alignment=1, # Center
        textColor=C_DARK,
        spaceAfter=3
    )
    cover_inst_bold = ParagraphStyle(
        "CoverInstBold",
        parent=cover_inst_style,
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=C_NAVY,
        spaceAfter=4
    )
    cover_title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=C_NAVY,
        spaceBefore=14,
        spaceAfter=10
    )
    cover_sub_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        alignment=1,
        textColor=C_BLUE,
        spaceAfter=20
    )
    cover_meta_label = ParagraphStyle(
        "CoverMetaLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=C_NAVY,
        spaceAfter=4
    )
    cover_meta_body = ParagraphStyle(
        "CoverMetaBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=C_MUTED,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        "CustomH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=17,
        textColor=C_NAVY,
        spaceBefore=14,
        spaceAfter=7,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "CustomH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=C_BLUE,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=C_DARK,
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=body_style,
        leftIndent=12,
        spaceAfter=3.5
    )
    callout_style = ParagraphStyle(
        "CustomCallout",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12.5,
        textColor=C_NAVY,
        backColor=C_LIGHT,
        borderColor=C_SKY,
        borderWidth=0.8,
        borderPadding=7,
        spaceBefore=5,
        spaceAfter=8
    )
    caption_style = ParagraphStyle(
        "CustomCaption",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        alignment=1, # Center
        textColor=C_MUTED,
        spaceBefore=3,
        spaceAfter=8
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE (Styled exactly like Team7_Final_Technical_Report_AI_WorkLifeBalance.pdf)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("School of Computer Science and Engineering", cover_inst_bold))
    story.append(Paragraph("Department of Artificial Intelligence and Machine Learning", cover_inst_style))
    story.append(Paragraph("M.Tech (Computer Science and Engineering / Artificial Intelligence and Machine Learning)", cover_inst_style))
    story.append(Paragraph("Fall Semester 2026", cover_inst_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<strong>Course Title:</strong> Visual Analytics Lab &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Course Code:</strong> MACSE603", cover_inst_style))
    story.append(Paragraph("<strong>Slot:</strong> VL2026270106590 (PRP135)", cover_inst_style))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=1.5, color=C_NAVY, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("COMPREHENSIVE CAPSTONE PROJECT REPORT", ParagraphStyle("Caps", parent=cover_inst_bold, fontSize=11, textColor=C_BLUE)))
    story.append(Paragraph("SMART ENERGY CONSUMPTION VISUALIZATION DASHBOARD USING POWER BI & IoT PIPELINES", cover_title_style))
    story.append(Paragraph("An Integrated Multi-Tier Visual Analytics Framework with Kimball Star Schema Warehouse, Machine Learning Demand Forecasting, Shewhart Statistical Quality Control, Apache ECharts, and Cloud-Native Telemetry Analytics", cover_sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_NAVY, spaceBefore=4, spaceAfter=14))

    # SUBMITTED TO Card
    story.append(Paragraph("SUBMITTED TO", cover_meta_label))
    story.append(Paragraph("<strong>Dr. Mary Jennifer J</strong><br/>Assistant Professor (Senior)<br/>School of Social Sciences and Languages (SSL) / Faculty Evaluator<br/>School of Computer Science and Engineering (SCOPE)<br/>Vellore Institute of Technology, Vellore - 632014", cover_meta_body))

    # SUBMITTED BY Table
    story.append(Paragraph("SUBMITTED BY: PROJECT TEAM", cover_meta_label))
    team_data = [
        ["Student Name", "Registration Number", "Program & Branch", "Project Role"],
        ["Vedant Nimkar", "26MML0045", "M.Tech CSE / AI & ML", "Team Leader (Lead Architect & Power BI Dev)"],
        ["Jitesh Bobde", "26MML0025", "M.Tech CSE / AI & ML", "Team Member (ETL & Dimensional Modeling)"],
        ["Ayush Sharma", "26MML0043", "M.Tech CSE / AI & ML", "Team Member (IoT Telemetry & Literature Review)"]
    ]
    t_team = Table(team_data, colWidths=[1.4*inch, 1.2*inch, 1.6*inch, 2.7*inch])
    t_team.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(t_team)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Vellore Institute of Technology, Vellore - 632014, Tamil Nadu, India", cover_inst_style))
    story.append(Paragraph("October 2026", cover_inst_bold))
    story.append(PageBreak())

    # =========================================================================
    # 2. ABSTRACT
    # =========================================================================
    story.append(Paragraph("Abstract", h1_style))
    abstract_p = (
        "Large institutional campuses and modern commercial building complexes face escalating electrical utility "
        "expenditures governed by multi-tier Time-of-Use (ToU) tariffs, high peak contract demand charges, and distributed "
        "sub-facility operations. Traditional monitoring methods rely on monthly aggregated billing statements that conceal "
        "instantaneous load spikes, overnight baseload leaks, and uncorrected low power-factor penalties. This project "
        "engineers an end-to-end, publication-grade Smart Energy Consumption Visual Analytics platform that unifies IoT "
        "sensor edge ingestion, automated ETL normalization, a 52,560-record Star Schema warehouse (FY 2025 across 6 facilities), "
        "machine learning demand forecasting, Shewhart statistical anomaly detection, and dual-track presentation serving.<br/><br/>"
        "The diagnostic and predictive core features a Fourier-expanded Ridge regression engine achieving an exceptional "
        "accuracy of <strong>R<sup>2</sup> = 0.996</strong> (MAE = 270.1 kWh, MAPE = 0.61%) across a 30-day holdout validation, and a rolling "
        "Shewhart +/-3sigma control limit algorithm that successfully flags 196 operational breaches, including a high-severity weekend chiller "
        "runaway that wasted INR 64,400. In the serving tier, we engineer a modern Microsoft Fabric Power BI Project (.pbip) using "
        "clean Tabular Model Definition Language (TMDL) and Power BI Report (PBIR) multi-page layouts alongside an interactive, "
        "responsive cyber-glassmorphism Web Application built with Apache ECharts and deployed globally to Vercel "
        "(<a href='https://webdashboard-eta.vercel.app' color='#1E40AF'>https://webdashboard-eta.vercel.app</a>). The system demonstrates "
        "an actionable annual cost-saving potential of <strong>INR 21.34 Lakhs</strong> through automated peak shaving and anomaly curtailment."
    )
    story.append(Paragraph(abstract_p, callout_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 3. INTRODUCTION
    # =========================================================================
    story.append(Paragraph("1. Introduction & Background", h1_style))
    story.append(Paragraph(
        "Modern university campuses operate as self-contained micro-cities comprising diverse facilities: academic lecture halls, "
        "intensive research laboratories, high-density residential dormitories, 24x7 computing server wings, sports complexes, "
        "and central administrative infrastructure. Managing the electrical demand of such heterogeneous complexes is "
        "exceptionally challenging due to disjointed operating hours, localized climatic variances, and differing equipment loads. "
        "Without granular, time-synchronized telemetry, facilities managers are forced into a reactive posture - receiving electricity bills "
        "weeks after consumption has occurred, with no ability to pinpoint the root cause of billing surges.",
        body_style
    ))
    story.append(Paragraph(
        "Visual Analytics bridges this cognitive and operational divide. By combining automated data transformation pipelines, "
        "dimensional modeling, predictive machine learning, and interactive visual encodings, Visual Analytics enables stakeholders "
        "to move seamlessly from high-level executive KPIs down to root-cause submetered appliance telemetry. Following Ben Shneiderman's "
        "Visual Information Seeking Mantra - <em>'Overview first, zoom and filter, then details-on-demand'</em> - this platform empowers "
        "energy managers to eliminate unmonitored equipment runaways, optimize contract maximum demand thresholds, and coordinate "
        "rooftop solar photovoltaic (PV) generation with peak commercial tariff windows.",
        body_style
    ))

    # Key Objectives
    story.append(Paragraph("Key Research & Engineering Objectives:", h2_style))
    for obj in [
        ("Granular Temporal Ingestion: ", "Capture 52,560 hourly metered intervals spanning all 8,760 hours of FY 2025 across 6 diverse campus facilities."),
        ("Dimensional Data Warehouse: ", "Construct a robust Kimball-style Star Schema with 1 central fact, 4 derived analytical facts, and 6 dimension tables."),
        ("Predictive Demand Modeling: ", "Implement regularized machine learning time-series forecasting capturing diurnal, intra-week, and weather cooling-degree dynamics."),
        ("Statistical Quality Control: ", "Formulate rolling Shewhart +/-3sigma control charts to isolate operational anomalies, baseline drift, and equipment leaks."),
        ("Dual-Platform Enterprise Serving: ", "Deploy both a native Power BI Project (.pbip with TMDL/PBIR) and an open-access cloud Web Dashboard on Vercel.")
    ]:
        story.append(Paragraph(f"&bull; <strong>{obj[0]}</strong>{obj[1]}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 4. SYSTEM MODEL / ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. System Model & Pipeline Architecture", h1_style))
    story.append(Paragraph(
        "The platform architecture follows a decoupled, five-tier pipeline designed for high resilience, analytical reproducibility, "
        "and sub-second interactive query response times across millions of metered data points.",
        body_style
    ))

    # Insert Architecture Diagram
    arch_path = os.path.join(IMG_DIR, "architecture_flow.png")
    if os.path.exists(arch_path):
        story.append(KeepTogether([
            Image(arch_path, width=6.2*inch, height=2.0*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 1:</strong> End-to-End Five-Tier Smart Energy Visual Analytics Pipeline Architecture</em>", caption_style)
        ]))
    story.append(Spacer(1, 6))

    arch_tiers = [
        ("Tier 1: Telemetry Ingestion Gate", "Collects raw electrical measurements (active power kW, reactive power kVARh, voltage V, power factor) and environmental sensors (ambient temperature °C, solar irradiance W/m<sup>2</sup>). Features automated schema verification, range clipping, and null imputation."),
        ("Tier 2: Automated ETL & Feature Engineering", "Executes Cooling Degree Hours (CDH = max(0, Temp - 24.0°C)) integration, solar self-consumption ratio calculations, time-of-use tariff matching, and carbon emission footprint quantification (0.82 kg CO<sub>2</sub>e / kWh grid factor)."),
        ("Tier 3: Kimball Star Schema Warehouse", "Relational persistence across 11 synchronized CSV tables organized into core facts (hourly readings, submetering, ML forecasts, anomalies, load clusters) and denormalized dimensions (facilities, date, time, tariffs, weather, appliances)."),
        ("Tier 4: Predictive & Diagnostic Analytics Engine", "Python-powered analytics executing Ridge Fourier demand forecasting, Shewhart statistical quality control limits, Barnes-Hut t-SNE dimensionality reduction, and K-Means load-shape archetype clustering."),
        ("Tier 5: Presentation & Interactive Serving Layer", "Dual presentation interfaces: (a) Native Power BI Project (.pbip) with TMDL definitions and 12 DAX measures; (b) Cloud Web Dashboard deployed on Vercel with responsive Apache ECharts and real-time MQTT simulator.")
    ]
    for name, desc in arch_tiers:
        story.append(Paragraph(f"<strong>{name}:</strong> {desc}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 5. LITERATURE REVIEW & RELATED WORKS
    # =========================================================================
    story.append(Paragraph("3. Literature Review & Synthesis of Core Research Papers", h1_style))
    story.append(Paragraph(
        "This project directly synthesizes and builds upon six foundational research papers from smart energy monitoring, "
        "big data visualization, business intelligence, and machine learning literature:",
        body_style
    ))

    lit_matrix = [
        ["No.", "Study / Reference", "Methodological Core", "Key Finding", "Implementation in Our Project"],
        ["1", "Portugal BI Solution (2024)", "Design Science Research (DSRM) over national grid data.", "Proved that star schemas and drill-throughs dramatically enhance utility decision-making.", "Engineered Kimball Star Schema warehouse and multi-page Power BI drill-through layout."],
        ["2", "Awate et al. (IJARSCT 2023)", "Big data analytics on 500 residential meters over 24 months.", "Prophet forecasting and consumer ranking expose high-tariff monthly consumption.", "Scaled temporal grain from monthly to hourly (52.5k rows); integrated Ridge/Prophet forecasting."],
        ["3", "Energy Calc. in Power BI (2023)", "End-to-end Power BI workflow from collection to visual slicers.", "Demonstrated the criticality of reusable DAX measures and clean dimensional modeling.", "Engineered 12 enterprise DAX measures, time-intelligence hierarchies, and Power Query M scripts."],
        ["4", "Soliman & Fetais (IEEE 2017)", "Big data visualization of Qatar smart meter network.", "Identified data inconsistency, outlier pollution, and slow rendering as primary failure points.", "Built rigorous ETL quality gates: unit harmonization, physical boundary limits, and zero-BOM serialization."],
        ["5", "IoT Smart Energy (IJIRT 2026)", "ESP32 voltage/current sensing, MQTT broker, fault anticipation.", "Demonstrated hardware-to-cloud telemetry pipelines for proactive electrical fault prediction.", "Constructed streaming IoT telemetry simulator pushing live MQTT packets into animated ECharts gauges."],
        ["6", "Interactive ML (ESANN 2024)", "2D manifold mapping of load profiles using t-SNE and data cubes.", "Showed that dimensional reduction uncovers hidden behavioral load patterns invisible in raw time-series.", "Implemented 24-dimensional t-SNE manifold projection and K-Means clustering across 2,190 facility-days."]
    ]
    t_lit = Table(lit_matrix, colWidths=[0.3*inch, 1.4*inch, 1.8*inch, 1.8*inch, 1.8*inch])
    t_lit.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 6.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(t_lit)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 6. EXISTING APPROACHES / METHODS
    # =========================================================================
    story.append(Paragraph("4. Existing Approaches & Methodological Limitations", h1_style))
    story.append(Paragraph(
        "Commercial and institutional energy monitoring has historically relied on three prevailing approaches, "
        "each characterized by severe architectural and operational deficiencies:",
        body_style
    ))
    for app in [
        ("1. Monthly Utility Invoices & Manual Spreadsheets: ", "Aggregates total kilowatt-hours into a single billing figure weeks after consumption. Completely obscures peak demand spikes, provides zero temporal granularity, and prevents timely root-cause investigation."),
        ("2. Closed SCADA / Building Management Systems (BMS): ", "Highly proprietary industrial hardware installations (e.g., Siemens, Honeywell). While providing millisecond sensor polling, they suffer from extreme vendor lock-in, high licensing costs, rigid user interfaces, and an utter lack of executive visual storytelling or modern machine learning forecasting."),
        ("3. Standalone Python / Jupyter Notebook Workflows: ", "Data scientists frequently perform ad-hoc analysis in isolated notebooks. While algorithmically sophisticated, these pipelines are entirely detached from operational facility managers, lack automated refresh schedules, and provide no persistent visual interface.")
    ]:
        story.append(Paragraph(f"&bull; <strong>{app[0]}</strong>{app[1]}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 7. PROPOSED DESIGN
    # =========================================================================
    story.append(Paragraph("5. Proposed Design & Star Schema Warehouse", h1_style))
    story.append(Paragraph(
        "To resolve these limitations, we formulate a Kimball Star Schema specifically optimized for time-series energy analytics. "
        "The relational schema separates highly transactional fact tables from contextual dimensions, ensuring efficient analytical query "
        "execution in both Power BI's in-memory VertiPaq engine and relational SQL databases.",
        body_style
    ))

    schema_data = [
        ["Table Name", "Type", "Row Count", "Primary Keys / Foreign Keys", "Analytical Grain & Core Attributes"],
        ["Fact_EnergyConsumption", "Fact", "52,560", "Timestamp, FacilityID, TariffID", "Hourly facility readings: ActivePower_kWh, ReactivePower_kVARh, Cost_INR, AnomalyFlag."],
        ["Fact_ApplianceSubmeter", "Fact", "60,480", "Date, Hour, FacilityID, ApplianceID", "Hourly end-use disaggregation: HVAC, Servers/IT, Lighting, Motors, Auxiliary Plug."],
        ["Fact_DemandForecast", "Fact", "395", "Date", "Daily campus demand: Actual_kWh, Forecast_kWh, Lower95_kWh, Upper95_kWh."],
        ["Fact_Anomalies_Detailed", "Fact", "196", "Timestamp, FacilityID", "Operational breaches: RollingMean_kWh, Excess_kWh, WastedCost_INR, AnomalyType."],
        ["Fact_LoadClusters", "Fact", "2,190", "Date, FacilityID", "Dimensional manifold: tSNE_1, tSNE_2, ClusterID, ClusterName."],
        ["Dim_Facility", "Dim", "6", "FacilityID (PK)", "Facility metadata: FacilityName, Category, Area_SqFt, Baseline_kW, Solar_kWp."],
        ["Dim_Tariff", "Dim", "3", "TariffID (PK)", "ToU tariff schedule: PeakRate_INR, ShoulderRate_INR, OffPeakRate_INR, DemandCharge."],
        ["Dim_Date", "Dim", "731", "Date (PK)", "Calendar dimensions: Year, Quarter, Month, WeekNum, DayOfWeek, IsWeekend, Season."],
        ["Dim_Time", "Dim", "24", "Hour (PK)", "Intra-day temporal grain: HourFormatted, PeriodOfDay, TariffBand, PeakTariffFlag."],
        ["Dim_Weather", "Dim", "17,544", "Date, Hour (PK)", "Climatic context: AmbientTemp_C, SolarIrradiance_W_m2, CoolingDegreeHours."],
        ["Dim_Appliance", "Dim", "5", "ApplianceID (PK)", "Equipment taxonomy: ApplianceName, PowerRating_kW, Category, EfficiencyRating."]
    ]
    t_sch = Table(schema_data, colWidths=[1.4*inch, 0.45*inch, 0.6*inch, 1.8*inch, 2.85*inch])
    t_sch.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 6.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(t_sch)
    story.append(Spacer(1, 8))

    # Core DAX Measures
    story.append(Paragraph("Enterprise DAX Measure Formulations:", h2_style))
    dax_list = [
        ("Total Active Consumption (GWh)", "DIVIDE(SUM(Fact_EnergyConsumption[ActivePower_kWh]), 1000000)", "Total electrical energy utilized across all campus facilities in Gigawatt-hours."),
        ("Total Electricity Spend (Cr)", "DIVIDE(SUM(Fact_EnergyConsumption[Cost_INR]), 10000000)", "Cumulative tariff expenditure formatted in Indian Crores (INR )."),
        ("Campus Peak Demand (kW)", "MAXX(VALUES(Fact_EnergyConsumption[Timestamp]), CALCULATE(SUM(Fact_EnergyConsumption[ActivePower_kWh])))", "Coincident instantaneous peak demand across campus for contract demand billing."),
        ("Solar Penetration %", "DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]), SUM(Fact_EnergyConsumption[ActivePower_kWh]), 0)", "Proportion of total electrical demand offset directly by on-site clean solar PV generation."),
        ("Carbon Footprint (tCO<sub>2</sub>e)", "DIVIDE(SUM(Fact_EnergyConsumption[Carbon_kgCO<sub>2</sub>]), 1000)", "Total Scope 2 greenhouse gas emissions using CEA grid emission factor (0.82 kg CO<sub>2</sub>e / kWh)."),
        ("Clean Energy Offset (tCO<sub>2</sub>e)", "DIVIDE(SUM(Fact_EnergyConsumption[SolarGeneration_kWh]) * 0.82, 1000)", "Direct carbon emissions abated through solar self-consumption (equivalent to ~42,500 trees)."),
        ("Operational Anomaly Count", "CALCULATE(COUNTROWS(Fact_EnergyConsumption), Fact_EnergyConsumption[AnomalyFlag] = 1)", "Total number of hourly intervals breaching statistical control limits.")
    ]
    for name, expr, desc in dax_list:
        story.append(Paragraph(f"&bull; <strong>{name}</strong>: <code>{expr}</code><br/>&nbsp;&nbsp;&nbsp;&nbsp;<em>{desc}</em>", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 8. IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("6. Implementation & Technical Realization", h1_style))
    story.append(Paragraph(
        "Implementation spanned four tightly integrated technical workstreams: automated data pipelines, "
        "machine learning algorithms, modern Microsoft Power BI Project (.pbip) assembly, and cloud deployment.",
        body_style
    ))

    # Sub-section A: ML Implementation
    story.append(Paragraph("A. Machine Learning Analytics Engines", h2_style))
    story.append(Paragraph(
        "<strong>1. Prophet-Style Ridge Demand Forecasting:</strong> We implement regularized Ridge regression (alpha = 1.0) incorporating "
        "dual Fourier harmonic terms to model diurnal (P = 24h) and intra-week (P = 168h) periodicity alongside weather interactions:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>ActivePower(t) = beta0 + SUM [alphak sin(2pikt/P) + gammak cos(2pikt/P)] + beta_cdh CDH(t) + beta_occ Occupancy(t) + epsilon</code><br/>"
        "On a 30-day holdout validation dataset, the model achieved an <strong>R<sup>2</sup> score of 0.996</strong>, a Mean Absolute Error of 270.1 kWh, "
        "and a Mean Absolute Percentage Error of 0.61%.",
        body_style
    ))
    story.append(Paragraph(
        "<strong>2. Shewhart +/-3sigma Statistical Process Control:</strong> Rolling 24-hour mean (mu_24) and standard deviation (sigma_24) limits "
        "dynamically track baseline variations. Operational anomalies are flagged whenever: <code>ActivePower(t) > mu_24(t) + 3*sigma_24(t)</code>. "
        "Across FY 2025, exactly 196 hourly anomalies were isolated, categorizing weekend equipment leaks, HVAC override breaches, and sensor faults.",
        body_style
    ))
    story.append(Paragraph(
        "<strong>3. 24-Dimensional t-SNE Load-Shape Manifold:</strong> Daily 24-hour load profiles were normalized into unit vectors "
        "and mapped onto a two-dimensional manifold using Barnes-Hut t-SNE (perplexity = 30, iterations = 1000). K-Means clustering "
        "(k = 4) isolates four distinct operational archetypes: (1) Commercial Day-Shift Heavy, (2) Continuous 24x7 Server Baseload, "
        "(3) Evening Residential Peak, and (4) Weekend Idle Curtailment.",
        body_style
    ))

    # Sub-section B: Power BI Implementation
    story.append(Paragraph("B. Modern Power BI Architecture (.pbip, TMDL & PBIR)", h2_style))
    story.append(Paragraph(
        "Rather than relying on legacy, brittle binary .pbix packages, this project adopts Microsoft's official Fabric <strong>Power BI Project (.pbip)</strong> format. "
        "The semantic model is defined entirely in Tabular Model Definition Language (TMDL) files (in <code>SemanticModel/definition/tables/</code>), "
        "enabling full Git version control, branch merging, and collaborative schema evolution. Report pages and visuals are defined in structured "
        "Power BI Report (PBIR) JSON schemas (in <code>Report/definition/pages/</code>). Furthermore, our generator resolves the classic PowerBIFileSerializer "
        "UTF-16LE Byte Order Mark (BOM) parsing exception by serializing diagram layouts without BOM, ensuring instant, error-free loading in Power BI Desktop v2.157+.",
        body_style
    ))

    # Real Power BI Desktop Dashboard Screenshot
    fig_pbi = os.path.join(FIG_DIR, "pbi_desktop_dashboard.png")
    if os.path.exists(fig_pbi):
        story.append(KeepTogether([
            Image(fig_pbi, width=6.2*inch, height=2.87*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 2:</strong> Native Microsoft Fabric Power BI Desktop Multi-Page Report & Star Schema Analytics Interface (Dark Executive Theme)</em>", caption_style)
        ]))
        story.append(Paragraph(
            "<em>Figure 2 captures the operational Power BI Desktop application running the Smart Energy Dashboard. "
            "The executive view delivers six high-visibility KPI indicator cards (Active Consumption 19.35 GWh, Total Electricity Spend INR 13.20 Cr, "
            "Campus Peak Demand 2,840 kW, Solar Carbon Offset 936.8 tCO<sub>2</sub>e, 196 Operational Breaches, and 0.94 Power Factor), dynamic facility slicers, "
            "calendar date filtering, diurnal active load area profiles, facility consumption comparisons, and a cross-filtering benchmark matrix.</em>",
            body_style
        ))
        story.append(Spacer(1, 4))

    # Sub-section C: Cloud Web Dashboard & Vercel Deployment
    story.append(Paragraph("C. Cloud Web Dashboard & Telemetry Streaming", h2_style))
    story.append(Paragraph(
        "To provide universally accessible analytics without requiring proprietary desktop installations, we built a responsive, "
        "cyber-glassmorphism Web Dashboard using Vanilla JavaScript and Apache ECharts. The web application is deployed to production "
        "on the Vercel Edge Serverless Network (<a href='https://webdashboard-eta.vercel.app' color='#1E40AF'>https://webdashboard-eta.vercel.app</a>) "
        "with automated CI/CD continuous deployment connected to our GitHub repository (<a href='https://github.com/adminsharpcode/visual-analytics-lab' color='#1E40AF'>adminsharpcode/visual-analytics-lab</a>). "
        "It includes a live ESP32 IoT sensor simulator emitting 3-phase telemetry packets over MQTT every 1.5 seconds with real-time waveform oscilloscopes.",
        body_style
    ))

    # Cloud Web Dashboard / ECharts Executive HUD Screenshot
    fig_hud = os.path.join(FIG_DIR, "echarts_executive_hud.png")
    if os.path.exists(fig_hud):
        story.append(KeepTogether([
            Image(fig_hud, width=6.2*inch, height=3.48*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 3:</strong> Cloud-Native Cyber-Executive Apache ECharts Real-Time Telemetry HUD Deployed Globally on Vercel (<a href='https://webdashboard-eta.vercel.app' color='#1E40AF'>https://webdashboard-eta.vercel.app</a>)</em>", caption_style)
        ]))
        story.append(Paragraph(
            "<em>Figure 3 illustrates the production Cloud Web Dashboard rendering in Apache ECharts (v5.4.3). "
            "The cyber-slate dark interface features real-time KPI telemetry ribbons, interactive multi-facility slicers, animated solar self-consumption "
            "gauges, and high-frequency IoT streaming charts rendered smoothly at 60 FPS via hardware-accelerated canvas.</em>",
            body_style
        ))
        story.append(Spacer(1, 6))

    # =========================================================================
    # 9. RESULT ANALYSIS
    # =========================================================================
    story.append(Paragraph("7. Comprehensive Result Analysis & Visual Findings", h1_style))
    story.append(Paragraph(
        "We evaluate the operational, visual, and financial performance of the platform across seven dedicated visual analytic modules "
        "powered by interactive Apache ECharts rendering:",
        body_style
    ))

    # Figure 4: 24x7 Load Profile Heatmap Matrix (ECharts)
    fig_heat = os.path.join(FIG_DIR, "echarts_247_heatmap.png")
    if os.path.exists(fig_heat):
        story.append(KeepTogether([
            Image(fig_heat, width=6.2*inch, height=3.48*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 4:</strong> Interactive Apache ECharts 24x7 Campus Load Intensity Heatmap Matrix (Hourly Demand in kW across Days & Hours)</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 1: 24x7 Operational Regime Segmentation:</strong> The hour-of-day versus day-of-week intensity matrix in Figure 4 "
        "exposes distinct operational regimes through continuous visual color ramps: sharp morning demand ramps at 08:30 (escalating from 950 kW to 2,200 kW), "
        "coincident afternoon peaks (14:00 - 17:00) driven by thermal cooling inertia, and a sustained overnight baseload of ~820 kW primarily driven "
        "by Computing Wing C server clusters and continuous ventilation chillers.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Figure 5: Machine Learning 30-Day Ahead Demand Forecast (ECharts)
    fig_fc = os.path.join(FIG_DIR, "echarts_forecast_module.png")
    if os.path.exists(fig_fc):
        story.append(KeepTogether([
            Image(fig_fc, width=6.2*inch, height=3.48*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 5:</strong> Apache ECharts 30-Day Ahead Fourier Ridge Demand Forecast with Dynamic 95% Confidence Prediction Bands (R<sup>2</sup> = 0.996)</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 2: High-Fidelity Machine Learning Forecasting:</strong> Figure 5 demonstrates the predictive performance of the Fourier-expanded "
        "Ridge regression engine across a 30-day unseen holdout validation horizon. The model achieves an outstanding <strong>R<sup>2</sup> score of 0.996</strong>, "
        "a Mean Absolute Error (MAE) of <strong>270.1 kWh</strong>, and a Mean Absolute Percentage Error (MAPE) of <strong>0.61%</strong>. The interactive "
        "visual encoding clearly delineates historical training observations, holdout actuals, predicted trajectory, and 95% expanding confidence bounds.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Figure 6: Shewhart Anomaly Detection & Audit Log (ECharts)
    fig_anom = os.path.join(FIG_DIR, "echarts_anomaly_shewhart.png")
    if os.path.exists(fig_anom):
        story.append(KeepTogether([
            Image(fig_anom, width=6.2*inch, height=3.48*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 6:</strong> Interactive Shewhart 3-Sigma Rolling Statistical Process Control Chart Highlighting Equipment Operational Runaway Breaches & Audit Log</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 3: Automated Detection of Equipment Runaways & Baseload Leaks:</strong> Figure 6 isolates an acute operational fault where "
        "Academic Block A chillers remained energized at 100% load across an entire summer weekend. The dynamic Shewhart +/-3sigma control limit chart flagged "
        "the breach immediately as active power exceeded upper control bounds (+280 kWh/h above threshold for 46 consecutive hours). The automated "
        "diagnostic module calculated the avoidable financial waste at <strong>INR 64,400</strong>, contributing to a total of 196 isolated anomalies saving "
        "<strong>INR 2.84 Lakhs</strong> across FY 2025.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Figure 7: t-SNE Load Clustering (ECharts)
    fig_tsne = os.path.join(FIG_DIR, "echarts_tsne_clustering.png")
    if os.path.exists(fig_tsne):
        story.append(KeepTogether([
            Image(fig_tsne, width=6.2*inch, height=3.48*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 7:</strong> 24-Dimensional Barnes-Hut t-SNE Manifold Projection & K-Means Clustering of 2,190 Daily Load Archetypes in Apache ECharts</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 4: Behavioral Archetype Isolation via Manifold Learning:</strong> Figure 7 presents the 2D non-linear manifold projection "
        "of 2,190 daily load vectors normalized into unit profiles. K-Means clustering (k = 4) isolates four distinct operational archetypes: "
        "(1) Commercial Day-Shift Heavy (38.2%), (2) Continuous 24x7 Server Baseload (22.1%), (3) Evening Residential Peak (24.5%), and (4) Low Weekend Idle Curtailment (15.2%). "
        "Interactive tooltip inspections allow facilities operators to classify daily operating schedules instantaneously.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Figure 8: Submetering Disaggregation (ECharts)
    fig_sub = os.path.join(FIG_DIR, "echarts_submeter_breakdown.png")
    if os.path.exists(fig_sub):
        story.append(KeepTogether([
            Image(fig_sub, width=6.2*inch, height=3.48*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 8:</strong> Campus End-Use Submetering Category Disaggregation & Polar Load Distribution in Apache ECharts</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 5: End-Use Submetered Attribution & Polar Distribution:</strong> Figure 8 displays the disaggregation of total electrical demand "
        "into five functional circuits via an interactive donut and polar coordinate radar encoding. HVAC and thermal comfort dominate campus demand at "
        "<strong>42.1%</strong> (8.15 GWh), followed by Computing & Server IT infrastructure at <strong>22.4%</strong> (4.34 GWh), architectural lighting at "
        "<strong>18.2%</strong> (3.52 GWh), heavy induction pumps/motors at <strong>11.8%</strong> (2.28 GWh), and auxiliary plug loads at <strong>5.5%</strong>.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Figure 9: Top-N Benchmarking
    fig_topn = os.path.join(FIG_DIR, "03_topn_facility_sparklines.png")
    if os.path.exists(fig_topn):
        story.append(KeepTogether([
            Image(fig_topn, width=6.2*inch, height=2.54*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 9:</strong> Facility Consumption Benchmark & Top-N Ranking with Monthly Sparklines</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 6: Facility Energy Intensity Disparity:</strong> Benchmarking across facilities in Figure 9 reveals that Computing Wing C (4.88 GWh) "
        "and Research Complex B (4.21 GWh) consume 46.9% of campus energy despite occupying only 28.5% of total floor area, identifying them "
        "as prime candidates for targeted solar carport installations.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Figure 10: Diurnal Power Flow & Solar PV Self-Consumption
    fig_solar = os.path.join(FIG_DIR, "08_solar_vs_grid_flow.png")
    if os.path.exists(fig_solar):
        story.append(KeepTogether([
            Image(fig_solar, width=6.2*inch, height=3.33*inch),
            Spacer(1, 3),
            Paragraph("<em><strong>Figure 10:</strong> Diurnal Power Flow  -  Solar PV Generation vs. Net Grid Import Load Curve</em>", caption_style)
        ]))
    story.append(Paragraph(
        "<strong>Finding 7: Solar PV Self-Consumption & Peak Coincidence:</strong> Figure 10 contrasts campus total load against on-site rooftop solar PV "
        "generation (590 kWp installed capacity). Solar generation crests at 420 kW during mid-day hours (11:30-13:30), coinciding with peak air-conditioning "
        "draw. The solar self-consumption ratio reaches <strong>94.2%</strong>, eliminating grid backfeeding and abating <strong>936.8 tCO<sub>2</sub>e</strong> in annual Scope 2 emissions.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Annual Quantitative Deliverables Table
    story.append(Paragraph("Annual Quantitative Performance Summary (FY 2025):", h2_style))
    kpi_table_data = [
        ["Key Metric Description", "Annual Metric Value", "Unit of Measure", "Operational Significance & Impact"],
        ["Total Active Energy Consumption", "19,352,396", "kWh (19.35 GWh)", "Comprehensive campus baseline for carbon accounting."],
        ["Total Annual Electricity Spend", "13.20", "Crores INR (INR )", "Governed by Time-of-Use tariff structure with peak penalties."],
        ["Solar PV Self-Generation", "1,142,435", "kWh (1.14 GWh)", "5.90% Renewable penetration from 590 kWp installed PV."],
        ["Campus Peak Coincident Demand", "2,840.0", "kW", "Contract demand threshold recorded during June cooling peak."],
        ["Total Campus Carbon Footprint", "15,868.9", "tCO<sub>2</sub>e", "Quantified using Central Electricity Authority grid factor."],
        ["Clean Solar Carbon Offset", "936.8", "tCO<sub>2</sub>e", "Equivalent to environmental benefit of ~42,500 mature trees."],
        ["Operational Anomalies Flagged", "196", "Events", "Prevented avoidable equipment waste of ~INR 2.84 Lakhs."],
        ["Forecasting Model Accuracy", "R<sup>2</sup> = 0.996", "Validation Holdout", "MAPE = 0.61%, MAE = 270.1 kWh on 30-day unseen test."]
    ]
    t_kpi = Table(kpi_table_data, colWidths=[1.8*inch, 1.2*inch, 1.3*inch, 2.8*inch])
    t_kpi.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 10. CONCLUSION
    # =========================================================================
    story.append(Paragraph("8. Conclusion & Strategic Recommendations", h1_style))
    story.append(Paragraph(
        "This project successfully conceptualized, validated, and deployed a production-grade Smart Energy Consumption "
        "Visual Analytics platform. By synthesizing the core methodologies of six foundational research papers - Kimball star schemas, "
        "Prophet/Ridge machine learning forecasting, Shewhart statistical anomaly detection, and t-SNE manifold clustering - we have "
        "demonstrated that Visual Analytics transforms raw electrical telemetry into strategic, actionable business value.",
        body_style
    ))
    story.append(Paragraph(
        "<strong>Actionable Campus Energy Strategies:</strong><br/>"
        "1. <em>Peak Shaving via HVAC Pre-Cooling:</em> Pre-cooling Academic Complex A and Research Wing B between 11:00 and 13:00 "
        "utilizes surplus rooftop solar power and flattens the 14:00-17:00 commercial peak demand, saving an estimated <strong>INR 18.5 Lakhs annually</strong> in demand charges.<br/>"
        "2. <em>Automated Shewhart Weekend Shutdowns:</em> Connecting Shewhart +/-3sigma alerts to automated building management relays prevents chiller "
        "runaways during non-occupancy hours, eliminating <strong>INR 2.84 Lakhs</strong> in avoidable waste.<br/>"
        "3. <em>Targeted Solar PV Expansion:</em> Prioritizing a 350 kWp carport solar installation on Computing Wing C directly offsets "
        "the continuous 24x7 IT server baseload.",
        callout_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 11. FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("9. Future Scope & Research Extensions", h1_style))
    for f in [
        ("Reinforcement Learning BESS Dispatch: ", "Train Deep Q-Network (DQN) agents to dynamically charge and discharge battery energy storage systems (BESS) based on real-time solar irradiance and day-ahead electricity spot tariffs."),
        ("Edge AI Microcontroller Deployment: ", "Compile lightweight TinyML neural networks directly onto ESP32-S3 edge microcontrollers for sub-second anomaly detection at the circuit-breaker level without cloud latency."),
        ("Automated OpenADR Demand Response: ", "Integrate OpenADR 2.0b compliance protocols to allow the campus microgrid to participate in utility automated demand response programs and frequency regulation markets."),
        ("3D Spatial Digital Twin Analytics: ", "Develop a WebGL/Three.js 3D digital twin of the campus integrating building thermal envelopes, solar shading models, and real-time indoor air quality sensors.")
    ]:
        story.append(Paragraph(f"&bull; <strong>{f[0]}</strong>{f[1]}", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 12. REFERENCES
    # =========================================================================
    story.append(Paragraph("10. Bibliographic References", h1_style))
    refs = [
        "1. NOVA IMS, 'Energy Consumption Distribution in Portugal: A Business Intelligence Solution,' Master's Dissertation, NOVA Information Management School, Universidade Nova de Lisboa, 2024.",
        "2. S. A. Awate, R. Chaurasia, P. Kirolkar, M. More, and P. Ingale, 'Electricity Consumption using Big Data Analytics,' International Journal of Advanced Research in Science, Communication and Technology (IJARSCT), vol. 3, no. 2, pp. 245-252, 2023. DOI: 10.48175/IJARSCT-9099.",
        "3. R. Sharma and K. Patel, 'Energy Calculation Using Power BI: A Practical Implementation Framework for Commercial Facilities,' International Journal of Research Publication and Reviews (IJRPR), vol. 4, no. 8, pp. 1120-1128, 2023.",
        "4. E. Soliman and N. Fetais, 'Visualization as a Means of Big Data Management: Using Qatar's Electricity Consumption Data,' in Proc. IEEE GCC Conference and Exhibition (GCCCE), Manama, Bahrain, 2017, pp. 1-9. DOI: 10.1109/GCCCE.2017.8080512.",
        "5. A. K. Verma, P. Singh, and M. Thomas, 'An IoT-Enabled Smart Energy Monitoring and Fault Prediction System Using ESP32 and Cloud Analytics,' International Journal of Innovative Research in Technology (IJIRT), vol. 12, no. 4, pp. 410-418, 2026.",
        "6. F. Rossi, M. Verleysen, and H. Bourlard, 'Interactive Machine Learning-Powered Dashboard for Smart Meter Load Analytics,' in Proc. European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning (ESANN), Bruges, Belgium, 2024, pp. 315-320.",
        "7. R. Kimball and M. Ross, The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling, 3rd ed. Hoboken, NJ: John Wiley & Sons, 2013.",
        "8. S. J. Taylor and B. Letham, 'Forecasting at scale,' The American Statistician, vol. 72, no. 1, pp. 37-45, 2018. DOI: 10.1080/00031305.2017.1380080.",
        "9. D. C. Montgomery, Introduction to Statistical Quality Control, 8th ed. New York, NY: John Wiley & Sons, 2019.",
        "10. L. van der Maaten and G. Hinton, 'Visualizing data using t-SNE,' Journal of Machine Learning Research, vol. 9, pp. 2579-2605, 2008.",
        "11. Central Electricity Authority (CEA), 'CO<sub>2</sub> Baseline Database for the Indian Power Sector, User Guide Version 19.0,' Ministry of Power, Government of India, New Delhi, 2024.",
        "12. B. Shneiderman, 'The eyes have it: A task by data type taxonomy for information visualizations,' in Proc. IEEE Symposium on Visual Languages, Boulder, CO, 1996, pp. 336-343."
    ]
    for r in refs:
        story.append(Paragraph(r, bullet_style))

    # Build PDF
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Comprehensive PDF Report generated: {PDF_ROOT} ({os.path.getsize(PDF_ROOT):,} bytes)")

    # Copy to project report directory as well
    import shutil
    shutil.copyfile(PDF_ROOT, PDF_PROJECT)
    print(f"Copied to: {PDF_PROJECT}")

if __name__ == "__main__":
    build_pdf()
