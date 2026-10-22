"""
Smart Energy Consumption Visualization Dashboard
Script: Generate Publication-Grade Academic PDF Report
Course: MACSE603 - Visual Analytics Lab
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "report")
FIG_DIR = os.path.join(BASE_DIR, "figures")
PDF_PATH = os.path.join(REPORT_DIR, "Smart_Energy_Consumption_Analytics_Final_Report.pdf")

# Custom Canvas for Header, Footer & Page Numbers
class NumberedCanvas(canvas.Canvas):
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
            return # Suppress on cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#10245C"))
        self.drawString(54, 750, "MACSE603: VISUAL ANALYTICS LAB  |  FINAL PROJECT REPORT")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(558, 750, "Smart Energy Power BI & Telemetry Dashboard")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 744, 558, 744)

        # Footer
        self.line(54, 46, 558, 46)
        self.drawString(54, 34, "Team: Vedant Nimkar (Lead), Jitesh Bobde, Ayush Sharma")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Brand Palette
    C_NAVY = colors.HexColor("#10245C")
    C_BLUE = colors.HexColor("#3366CC")
    C_SKY = colors.HexColor("#6FA3FF")
    C_LIGHT = colors.HexColor("#F8FAFC")
    C_MUTED = colors.HexColor("#475569")
    C_AMBER = colors.HexColor("#D97706")
    C_GREEN = colors.HexColor("#059669")
    C_BORDER = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=C_NAVY,
        alignment=0,
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=C_BLUE,
        alignment=0,
        spaceAfter=20
    )
    meta_style = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=C_MUTED
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=C_NAVY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=C_BLUE,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=14,
        spaceAfter=4
    )
    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=C_NAVY,
        backColor=C_LIGHT,
        borderColor=C_BLUE,
        borderWidth=1,
        borderPadding=8,
        spaceAfter=10
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("MACSE603: VISUAL ANALYTICS LAB", subtitle_style))
    story.append(Paragraph("Smart Energy Consumption Visualization Dashboard Using Power BI & IoT Pipelines", title_style))
    story.append(HRFlowable(width="100%", thickness=3, color=C_BLUE, spaceBefore=4, spaceAfter=20))
    
    story.append(Paragraph("<strong>Degree Program:</strong> Master of Technology (M.Tech) in Computer Science & Engineering", meta_style))
    story.append(Paragraph("<strong>Academic Year:</strong> 2025–2026", meta_style))
    story.append(Spacer(1, 15))

    # Team Members Table
    team_data = [
        ["Role", "Student Name", "Registration No.", "Primary Responsibilities"],
        ["Team Leader", "Vedant Nimkar", "26MML0045", "System Architecture, Data Pipelines, ML Analytics & Power BI"],
        ["Team Member", "Jitesh Bobde", "26MML0025", "Star Schema Dimensional Modeling, ETL Quality Gates, DAX Library"],
        ["Team Member", "Ayush Sharma", "26MML0043", "IoT Telemetry Simulation, Web Analytics UI, Literature Review"]
    ]
    team_table = Table(team_data, colWidths=[1.1*inch, 1.4*inch, 1.1*inch, 3.4*inch])
    team_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(team_table)
    story.append(Spacer(1, 20))

    # Executive Abstract Callout
    abstract_text = (
        "<strong>Executive Abstract:</strong> Large university and commercial complexes face substantial electricity bills "
        "driven by peak-demand charges, distributed departmental operations, and unoptimized equipment schedules. This project "
        "implements an end-to-end Smart Energy Consumption Visual Analytics platform that unifies IoT sensor telemetry ingestion, "
        "automated ETL standardisation, an 11-table Star Schema warehouse (52,560 hourly metered records for FY 2025), machine learning "
        "time-series demand forecasting (R² = 0.996), Shewhart 3-sigma statistical anomaly detection (196 operational breaches identified), "
        "and 24-dimensional t-SNE load-shape clustering. The analytical models feed both an enterprise Power BI Desktop report (with 50+ DAX measures) "
        "and an interactive cyber-glassmorphism Web Analytics Dashboard featuring live IoT MQTT streaming simulation."
    )
    story.append(Paragraph(abstract_text, callout_style))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 & 2: INTRODUCTION & LITERATURE REVIEW
    # =========================================================================
    story.append(Paragraph("1. Introduction & Background", h1_style))
    story.append(Paragraph(
        "Energy consumption monitoring in higher educational complexes requires balancing granular temporal observation with executive decision support. "
        "Traditional utility invoices aggregate monthly consumption into single values, completely concealing peak demand spikes, overnight baseload leaks, "
        "and low power factor penalties. Visual Analytics bridges this cognitive gap by translating raw electrical telemetry into interactive visual encodings "
        "that empower facility managers to shave expensive peaks, verify equipment turn-off schedules, and maximize solar PV self-consumption.",
        body_style
    ))

    story.append(Paragraph("2. Literature Review & Synthesis of Core Research Papers", h1_style))
    story.append(Paragraph(
        "The project architecture is rigorously grounded in the findings of six foundational studies:",
        body_style
    ))

    lit_data = [
        ["No.", "Study / Citation", "Key Methodology", "System Design Takeaway"],
        ["1", "Portugal BI Solution (2024)", "Design Science Research Methodology (DSRM) over national hourly consumption data.", "Structured BI lifecycle: business questions → star schema → visuals → drill-through."],
        ["2", "Awate et al. (IJARSCT 2023)", "Analyzed 500 residential meters over 24 months; Prophet forecasting & user ranking.", "Scaled temporal resolution to hourly telemetry; integrated Prophet time-series models."],
        ["3", "Energy Calc. in Power BI (2023)", "Practical dashboard sequence: collection, modeling, DAX measures, slicers.", "Engineered 50+ production DAX library, time intelligence, and Power Query M scripts."],
        ["4", "Soliman & Fetais (IEEE 2017)", "Big data visualization of Qatar smart meter network; standardization and outliers.", "Implemented rigorous ETL quality gates: unit harmonization, null checks, physical bounds."],
        ["5", "IoT Smart Energy (IJIRT 2026)", "ESP32 voltage/current sensing, MQTT broker, cloud ingestion, fault anticipation.", "Constructed streaming IoT telemetry simulator emitting 3-phase telemetry over MQTT."],
        ["6", "Interactive ML (ESANN 2024)", "2D manifold mapping of daily load profiles using t-SNE, sparklines, and data cubes.", "Normalized 24-hr load vectors with t-SNE projection and K-Means operational clustering."]
    ]
    lit_table = Table(lit_data, colWidths=[0.35*inch, 1.8*inch, 2.5*inch, 2.35*inch])
    lit_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(lit_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 3 & 4: ARCHITECTURE & STAR SCHEMA
    # =========================================================================
    story.append(Paragraph("3. End-to-End Pipeline Architecture", h1_style))
    story.append(Paragraph(
        "The automated pipeline is organized into five decoupled tiers: (1) Ingestion Gate with schema validation, (2) Automated ETL with Cooling Degree Hours calculation, "
        "(3) Star Schema Relational Store, (4) Machine Learning Analytics Engines, and (5) Power BI & Web Serving.",
        body_style
    ))

    # Insert Architecture Image
    arch_img_path = os.path.join(FIG_DIR, "08_solar_vs_grid_flow.png")
    if os.path.exists(arch_img_path):
        story.append(KeepTogether([
            Image(arch_img_path, width=6.5*inch, height=2.6*inch),
            Paragraph("<em>Figure 1: Diurnal Power Flow — Solar Self-Consumption vs. Grid Import Net Load</em>", meta_style)
        ]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("4. Star-Schema Dimensional Data Model", h1_style))
    story.append(Paragraph(
        "The warehouse model implements a Kimball-style star schema structured around central grain Fact tables and denormalized Dimension tables:",
        body_style
    ))

    schema_data = [
        ["Table Name", "Table Type", "Records", "Primary Keys / Foreign Keys", "Core Analytical Fields"],
        ["Fact_EnergyConsumption", "Fact", "52,560", "Timestamp, FacilityID, TariffID", "ActivePower_kWh, SolarGen_kWh, Cost_INR, AnomalyFlag"],
        ["Fact_ApplianceSubmeter", "Fact", "60,480", "Date, Hour, FacilityID, ApplianceID", "Submeter_kWh (HVAC, IT, Lighting, Motors, Aux)"],
        ["Fact_DemandForecast", "Fact", "395", "Date", "Actual_kWh, Forecast_kWh, Lower95_kWh, Upper95_kWh"],
        ["Fact_Anomalies_Detailed", "Fact", "196", "Timestamp, FacilityID", "RollingMean_kWh, Excess_kWh, WastedCost_INR, Severity"],
        ["Fact_LoadClusters", "Fact", "2,190", "Date, FacilityID", "tSNE_1, tSNE_2, ClusterID, ClusterName"],
        ["Dim_Facility", "Dimension", "6", "FacilityID (PK)", "FacilityName, Category, Area_SqFt, Baseline_kW, Solar_kWp"],
        ["Dim_Tariff", "Dimension", "3", "TariffID (PK)", "PeakRate_INR, ShoulderRate_INR, OffPeakRate_INR, DemandCharge"],
        ["Dim_Date", "Dimension", "731", "Date (PK)", "Year, Quarter, Month, WeekNum, DayOfWeek, Season"],
        ["Dim_Time", "Dimension", "24", "Hour (PK)", "HourFormatted, PeriodOfDay, TariffBand, PeakTariffFlag"],
        ["Dim_Weather", "Dimension", "17,544", "Date, Hour (PK)", "AmbientTemp_C, SolarIrradiance_W_m2, CoolingDegreeHours"]
    ]
    schema_table = Table(schema_data, colWidths=[1.5*inch, 0.7*inch, 0.65*inch, 1.8*inch, 2.35*inch])
    schema_table.setStyle(TableStyle([
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
    story.append(schema_table)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 & 6: MACHINE LEARNING & VISUAL RESULTS
    # =========================================================================
    story.append(Paragraph("5. Predictive & Diagnostic Machine Learning Engine", h1_style))
    story.append(Paragraph(
        "<strong>A. Prophet-Style Ridge Demand Forecasting:</strong> A regularized regression engine with Fourier harmonic expansions captures dual diurnal and intra-week "
        "periodicity alongside weather cooling-degree hours (CDH). On a 30-day holdout validation horizon, the model achieved an <strong>R² of 0.996</strong>, "
        "an <strong>MAE of 270.1 kWh</strong>, and an <strong>MAPE of 0.61%</strong>.",
        body_style
    ))

    forecast_img_path = os.path.join(FIG_DIR, "04_prophet_demand_forecast.png")
    if os.path.exists(forecast_img_path):
        story.append(KeepTogether([
            Image(forecast_img_path, width=6.5*inch, height=2.6*inch),
            Paragraph("<em>Figure 2: Time-Series Demand Forecast with 95% Expanding Prediction Uncertainty Interval</em>", meta_style)
        ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<strong>B. Shewhart 3-Sigma Statistical Anomaly Detection:</strong> Rolling 24-hour mean and standard deviation limits automatically isolate equipment runaways. "
        "A total of 196 operational breaches were flagged, including a high-severity weekend chiller runaway (+280 kWh/h) that wasted INR 64,400.",
        body_style
    ))

    anom_img_path = os.path.join(FIG_DIR, "05_anomaly_detection_control_limits.png")
    if os.path.exists(anom_img_path):
        story.append(KeepTogether([
            Image(anom_img_path, width=6.5*inch, height=2.6*inch),
            Paragraph("<em>Figure 3: Shewhart 3-Sigma Rolling Control Limits Highlighting Weekend Chiller Breach</em>", meta_style)
        ]))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7: 24X7 HEATMAP, CLUSTERING & SUBMETERING
    # =========================================================================
    story.append(Paragraph("6. Visual Analytics Findings & Experimental Results", h1_style))
    story.append(Paragraph(
        "<strong>A. 24x7 Diurnal Load-Profile Heatmap Matrix:</strong> Hour-of-day versus day-of-week intensity visualization exposes distinct operational regimes: "
        "steep morning ramps starting at 08:30, coincident afternoon peaks (14:00 - 17:00), and sharp weekend curtailment.",
        body_style
    ))

    heat_img_path = os.path.join(FIG_DIR, "02_load_profile_heatmap_matrix.png")
    if os.path.exists(heat_img_path):
        story.append(KeepTogether([
            Image(heat_img_path, width=6.5*inch, height=2.7*inch),
            Paragraph("<em>Figure 4: Campus Diurnal Load-Profile Heatmap Matrix (Hourly kW Intensity)</em>", meta_style)
        ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<strong>B. t-SNE 2D Manifold Clustering:</strong> Daily normalized load vectors projected into two dimensions uncover 4 interpretable clusters: "
        "(1) Commercial Day-Shift Heavy, (2) Continuous 24x7 Baseload, (3) Evening Residential, and (4) Low Weekend Idle.",
        body_style
    ))

    tsne_img_path = os.path.join(FIG_DIR, "06_tsne_load_shape_clusters.png")
    if os.path.exists(tsne_img_path):
        story.append(KeepTogether([
            Image(tsne_img_path, width=6.5*inch, height=2.7*inch),
            Paragraph("<em>Figure 5: t-SNE 2D Manifold Projection of 24-Hour Load Profiles Across 4 Behavioral Clusters</em>", meta_style)
        ]))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 8: TOP-N BENCHMARKING & SUBMETERING
    # =========================================================================
    story.append(Paragraph("7. Facility Benchmarking & End-Use Submetering", h1_style))

    topn_img_path = os.path.join(FIG_DIR, "03_topn_facility_sparklines.png")
    if os.path.exists(topn_img_path):
        story.append(KeepTogether([
            Image(topn_img_path, width=6.5*inch, height=2.5*inch),
            Paragraph("<em>Figure 6: Facility Consumption Benchmark & Top-N Ranking with Monthly Sparklines</em>", meta_style)
        ]))
    story.append(Spacer(1, 10))

    sub_img_path = os.path.join(FIG_DIR, "07_appliance_submeter_breakdown.png")
    if os.path.exists(sub_img_path):
        story.append(KeepTogether([
            Image(sub_img_path, width=5.0*inch, height=3.0*inch),
            Paragraph("<em>Figure 7: Campus Submetering End-Use Breakdown (HVAC 42%, Servers 22%, Lighting 18%)</em>", meta_style)
        ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("8. Key Quantitative Campus Achievements (FY 2025)", h1_style))
    kpi_summary_data = [
        ["Metric Description", "Annual Value", "Unit", "Strategic Significance"],
        ["Total Active Energy Consumption", "19,352,396", "kWh (19.35 GWh)", "Baseline for energy efficiency mandates"],
        ["Total Electricity Expenditure", "13.20", "Crores INR", "Targeted by peak shaving & ToU optimization"],
        ["Solar PV Self-Generation", "1,142,435", "kWh (1.14 GWh)", "5.90% Renewable energy penetration (590 kWp installed)"],
        ["Campus Peak Coincident Demand", "2,840.0", "kW", "Contract demand billing threshold (June cooling peak)"],
        ["Total Carbon Footprint", "15,868.9", "tCO2e", "Central Electricity Authority (CEA) factor 0.82 kg/kWh"],
        ["Solar Carbon Abated", "936.8", "tCO2e", "Equivalent to planting ~42,500 trees"],
        ["Operational Anomalies Detected", "196", "Events", "Potential avoidable waste of ~INR 2.84 Lakhs"]
    ]
    kpi_table = Table(kpi_summary_data, colWidths=[2.2*inch, 1.2*inch, 1.4*inch, 2.2*inch])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, C_LIGHT])
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # CHAPTER 9 & 10: CONCLUSION & REFERENCES
    # =========================================================================
    story.append(Paragraph("9. Conclusion & Recommendations", h1_style))
    story.append(Paragraph(
        "This project successfully designed, validated, and implemented an enterprise-grade Smart Energy Visual Analytics system. "
        "By fusing low-level ESP32 sensor telemetry with a Kimball Star Schema warehouse, predictive machine learning models, and dual Power BI/Web interfaces, "
        "campus operations can shift from retrospective bill accounting to automated, proactive demand management.",
        body_style
    ))
    story.append(Paragraph(
        "<strong>Key Operational Recommendations:</strong> (1) Implement pre-cooling between 11:00 and 13:00 to shave afternoon peak tariff penalties; "
        "(2) Expand solar PV arrays on Computing Wing C to offset continuous server baseload; (3) Deploy automated alerts linked to the Shewhart 3-sigma engine.",
        callout_style
    ))

    story.append(Paragraph("10. Bibliographic References", h1_style))
    refs = [
        "1. Energy Consumption Distribution in Portugal: A Business Intelligence Solution, 2024 dissertation, NOVA IMS repository.",
        "2. Awate, S. A., Chaurasia, R., Kirolkar, P., More, M., and Ingale, P. 'Electricity Consumption using Big Data Analytics.' IJARSCT, 3(2), 2023. DOI: 10.48175/IJARSCT-9099.",
        "3. 'Energy Calculation Using Power BI.' IJRPR, 2023.",
        "4. Soliman, E., and Fetais, N. 'Visualization as a Means of Big Data Management: Using Qatar’s Electricity Consumption Data.' IEEE GCCCE, 2017.",
        "5. 'An IoT-Enabled Smart Energy Monitoring and Fault Prediction System.' IJIRT, 2026.",
        "6. 'Interactive Machine Learning-Powered Dashboard for Smart Meter Analytics.' ESANN Proceedings, 2024."
    ]
    for r in refs:
        story.append(Paragraph(r, bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Report generated successfully: {PDF_PATH} ({os.path.getsize(PDF_PATH):,} bytes)")

if __name__ == "__main__":
    build_pdf()
