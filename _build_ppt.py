"""
Visual Analytics Lab (MACSE603) - 6-slide review presentation.

Required format:
  1 Title / team members
  2 Abstract / problem statement
  3 Objectives
  4 Literature review & related works   (6 papers, 2 per member)
  5 Research gap identified
  6 Proposed system design / architecture / methods

Source: "Visual Analytics Lab Power Bi topic.pdf.pdf"
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
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


def blank():
    return prs.slides.add_slide(prs.slide_layouts[6])


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0,
         shape=MSO_SHAPE.RECTANGLE):
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


def bullet(tf, text, size=13.5, lead=None, first=False, space_after=8,
           marker="\u25aa"):
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
    rect(slide, Inches(0.55), Inches(0.36), Inches(0.62), Inches(0.62),
         fill=BLUE)
    t = textbox(slide, Inches(0.55), Inches(0.47), Inches(0.62), Inches(0.4))
    para(t, str(num), size=19, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, first=True)
    t = textbox(slide, Inches(1.35), Inches(0.42), Inches(11.4), Inches(0.6))
    para(t, title, size=25, bold=True, color=NAVY, first=True)
    rect(slide, Inches(1.35), Inches(1.11), Inches(1.15), Inches(0.05),
         fill=BLUE)


def footer(slide):
    PAGE[0] += 1
    t = textbox(slide, Inches(0.55), Inches(7.04), Inches(9.5), Inches(0.28))
    para(t, f"{COURSE}  |  Smart Energy Consumption Visualization Dashboard "
            f"Using Power BI", size=9, color=MUTED, first=True)
    t = textbox(slide, Inches(12.1), Inches(7.04), Inches(0.7), Inches(0.28))
    para(t, str(PAGE[0]), size=9, bold=True, color=BLUE,
         align=PP_ALIGN.RIGHT, first=True)


# ============================================================ SLIDE 1
s = blank()
rect(s, Inches(0), Inches(0), W, Inches(0.5), fill=NAVY)
rect(s, Inches(0), Inches(0.5), W, Inches(0.08), fill=BLUE)
rect(s, Inches(0), Inches(7.2), W, Inches(0.3), fill=NAVY)

t = textbox(s, Inches(0.85), Inches(0.11), Inches(11.6), Inches(0.32))
para(t, COURSE.upper(), size=12, bold=True, color=SKY, first=True)

t = textbox(s, Inches(0.85), Inches(1.15), Inches(11.6), Inches(0.35))
para(t, "PROJECT PRESENTATION", size=12.5, bold=True, color=BLUE, first=True)

t = textbox(s, Inches(0.85), Inches(1.68), Inches(11.6), Inches(2.0))
para(t, "Smart Energy Consumption", size=38, bold=True, color=NAVY,
     space_after=2, first=True)
para(t, "Visualization Dashboard", size=38, bold=True, color=NAVY,
     space_after=2)
para(t, "Using Power BI", size=38, bold=True, color=BLUE)

rect(s, Inches(0.85), Inches(3.92), Inches(1.4), Inches(0.05), fill=BLUE)

t = textbox(s, Inches(0.85), Inches(4.2), Inches(11.6), Inches(0.32))
para(t, "TEAM MEMBERS", size=11.5, bold=True, color=MUTED, first=True)

cx = Inches(0.85)
for name, reg, role in MEMBERS:
    rect(s, cx, Inches(4.65), Inches(3.72), Inches(1.5), fill=LIGHT,
         line=BORDER)
    rect(s, cx, Inches(4.65), Inches(3.72), Inches(0.07), fill=BLUE)
    t = textbox(s, cx + Inches(0.3), Inches(4.9), Inches(3.15), Inches(1.1))
    para(t, name, size=16.5, bold=True, color=NAVY, space_after=4, first=True)
    para(t, f"Reg. No. {reg}", size=12, color=MUTED, space_after=6)
    para(t, role.upper(), size=9.5, bold=True,
         color=(GREEN if role == "Team Leader" else BLUE))
    cx += Inches(3.97)

t = textbox(s, Inches(0.85), Inches(6.42), Inches(11.6), Inches(0.35))
para(t, "Literature review of six research papers  -  two papers per team "
        "member", size=12.5, italic=True, color=MUTED, first=True)

t = textbox(s, Inches(0.85), Inches(7.25), Inches(11.6), Inches(0.24))
para(t, "M.Tech - Computer Science and Engineering", size=10, color=SKY,
     first=True)


# ============================================================ SLIDE 2
s = blank()
header(s, 2, "Abstract & Problem Statement")

rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(5.35), fill=LIGHT,
     line=BORDER)
rect(s, Inches(0.55), Inches(1.38), Inches(6.0), Inches(0.07), fill=BLUE)
t = textbox(s, Inches(0.9), Inches(1.66), Inches(5.3), Inches(0.3))
para(t, "ABSTRACT", size=11.5, bold=True, color=BLUE, first=True)
t = textbox(s, Inches(0.9), Inches(2.08), Inches(5.3), Inches(4.4))
para(t, "This work reviews six studies on smart energy monitoring, "
        "electricity-consumption analytics, interactive visualization, "
        "forecasting and Power BI dashboards.", size=13, first=True,
     space_after=10, line_spacing=1.2)
para(t, "The literature shows that effective dashboards depend on reliable "
        "data collection, data cleaning, dimensional modeling, meaningful "
        "visual encoding, interactivity and actionable analytics.",
     size=13, space_after=10, line_spacing=1.2)
para(t, "These findings support the proposed project: a Power BI dashboard "
        "that helps users understand consumption trends, detect high-use "
        "periods, compare consumers or facilities, and support "
        "energy-efficiency decisions.", size=13, line_spacing=1.2)

rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(5.35), fill=WHITE,
     line=BORDER)
rect(s, Inches(6.78), Inches(1.38), Inches(5.99), Inches(0.07), fill=AMBER)
t = textbox(s, Inches(7.13), Inches(1.66), Inches(5.3), Inches(0.3))
para(t, "PROBLEM STATEMENT", size=11.5, bold=True, color=AMBER, first=True)
t = textbox(s, Inches(7.13), Inches(2.08), Inches(5.3), Inches(4.4))
for i, (lead, body) in enumerate([
    ("Fragmented data - ",
     "consumption readings are spread across smart meters, sensors and "
     "billing records with no common format."),
    ("Poor standardisation - ",
     "inconsistent units, missing values and outliers make raw energy data "
     "difficult to trust."),
    ("No single view - ",
     "stakeholders cannot easily see trends, peak periods or compare "
     "consumers in one place."),
    ("Observation without action - ",
     "most reports describe past usage but do not flag anomalies or forecast "
     "future demand."),
    ("Disconnected solutions - ",
     "existing work addresses Power BI reporting, IoT monitoring or machine "
     "learning separately, not together."),
]):
    bullet(t, body, lead=lead, size=12.5, first=(i == 0), space_after=13)
footer(s)


# ============================================================ SLIDE 3
s = blank()
header(s, 3, "Objectives")

objectives = [
    ("Build the dashboard",
     "Develop an interactive Power BI dashboard for smart energy "
     "consumption using a documented ETL and star-schema model.", BLUE),
    ("Report core KPIs",
     "Present total energy and cost KPIs with explainable DAX measures so "
     "every number can be traced to its source.", NAVY),
    ("Reveal consumption patterns",
     "Show daily, weekly, monthly and hourly trends and identify "
     "peak-demand periods and load profiles.", BLUE),
    ("Enable comparison",
     "Compare consumers, buildings or facilities and rank the Top-N "
     "high-consumption entities.", NAVY),
    ("Add diagnostic analytics",
     "Flag anomalies, provide forecast charts and show renewable-versus-grid "
     "contribution where data allows.", BLUE),
    ("Support investigation",
     "Provide slicers for date, location, consumer, tariff and appliance "
     "plus drill-through pages for detail.", NAVY),
]
y = Inches(1.42)
for i, (title, body, accent) in enumerate(objectives):
    col = Inches(0.55) if i < 3 else Inches(6.78)
    yy = y + Inches(1.82) * (i % 3)
    rect(s, col, yy, Inches(5.99), Inches(1.62), fill=LIGHT, line=BORDER)
    rect(s, col, yy, Inches(0.075), Inches(1.62), fill=accent)
    t = textbox(s, col + Inches(0.35), yy + Inches(0.2), Inches(0.45),
                Inches(0.4))
    para(t, f"0{i+1}", size=15, bold=True, color=SKY, first=True)
    t = textbox(s, col + Inches(1.0), yy + Inches(0.2), Inches(4.75),
                Inches(1.25))
    para(t, title, size=14, bold=True, color=NAVY, space_after=4, first=True)
    para(t, body, size=11.5, color=DARK, line_spacing=1.16)
footer(s)


# ============================================================ SLIDE 4
s = blank()
header(s, 4, "Literature Review & Related Works")

t = textbox(s, Inches(0.55), Inches(1.26), Inches(12.2), Inches(0.3))
para(t, "Six papers reviewed - two per team member - covering BI workflows, "
        "big-data visualization, IoT sensing and machine-learning analytics.",
     size=11.5, italic=True, color=MUTED, first=True)

rows = [
    ("1", "Energy Consumption Distribution in Portugal: A Business "
          "Intelligence Solution",
     "NOVA IMS, 2024",
     "Design Science Research Methodology; BI conceptual model and interactive "
     "Power BI dashboard over monthly, hourly and geographic data. Lesson: start "
     "from explicit business questions.",
     "Vedant Nimkar"),
    ("2", "Electricity Consumption using Big Data Analytics",
     "Awate et al., IJARSCT 3(2), 2023",
     "500 residential consumers over 24 months. Power BI visuals plus Prophet "
     "forecasting and consumer ranking. Limitation: monthly data restricts "
     "temporal granularity.",
     "Vedant Nimkar"),
    ("3", "Energy Calculation Using Power BI",
     "IJRPR, 2023",
     "End-to-end workflow: collect, clean, transform, model, visualise, add "
     "slicers, test accuracy, publish. Emphasises usability and "
     "stakeholder-oriented layout.",
     "Jitesh Bobde"),
    ("4", "Visualization as a Means of Big Data Management: Qatar Electricity "
          "Consumption Data",
     "Soliman & Fetais, IEEE GCCCE, 2017",
     "Visualization converts large inconsistent energy data into information. "
     "Identifies standardisation, integration, speed and outlier challenges.",
     "Jitesh Bobde"),
    ("5", "An IoT-Enabled Smart Energy Monitoring and Fault Prediction System",
     "IJIRT, 2026",
     "ESP32 voltage/current sensing with calibration, MQTT to cloud, real-time "
     "dashboards, regression forecasting and fault anticipation. Dashboard is "
     "web-based, not Power BI.",
     "Ayush Sharma"),
    ("6", "Interactive Machine Learning-Powered Dashboard",
     "ESANN Proceedings, 2024",
     "Machine learning with interactive visual analytics: t-SNE maps of daily "
     "demand profiles, data-cube filtering, sparklines and morphing "
     "projections.",
     "Ayush Sharma"),
]

tbl = s.shapes.add_table(7, 5, Inches(0.55), Inches(1.68),
                         Inches(12.22), Inches(5.05)).table
for i, wd in enumerate([Inches(0.42), Inches(3.15), Inches(1.75),
                        Inches(5.25), Inches(1.65)]):
    tbl.columns[i].width = wd

for j, htxt in enumerate(["#", "Paper / Study", "Source", "Key contribution",
                          "Reviewer"]):
    c = tbl.cell(0, j)
    c.text = htxt
    c.fill.solid()
    c.fill.fore_color.rgb = NAVY
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    c.margin_left = c.margin_right = Inches(0.07)
    r = c.text_frame.paragraphs[0].runs[0]
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = WHITE
    r.font.name = "Segoe UI"

for i, row in enumerate(rows, start=1):
    for j, val in enumerate(row):
        c = tbl.cell(i, j)
        c.text = val
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE if i % 2 else LIGHT
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.margin_left = c.margin_right = Inches(0.07)
        c.margin_top = c.margin_bottom = Inches(0.04)
        for pr in c.text_frame.paragraphs:
            pr.line_spacing = 1.05
            for r in pr.runs:
                r.font.name = "Segoe UI"
                r.font.size = Pt(8.5)
                r.font.color.rgb = DARK
                if j == 0:
                    r.font.size = Pt(11)
                    r.font.bold = True
                    r.font.color.rgb = BLUE
                elif j == 1:
                    r.font.size = Pt(9)
                    r.font.bold = True
                    r.font.color.rgb = NAVY
                elif j == 2:
                    r.font.size = Pt(8)
                    r.font.italic = True
                    r.font.color.rgb = MUTED
                elif j == 4:
                    r.font.size = Pt(9)
                    r.font.bold = True
                    r.font.color.rgb = BLUE
footer(s)


# ============================================================ SLIDE 5
s = blank()
header(s, 5, "Research Gap Identified")

t = textbox(s, Inches(0.55), Inches(1.32), Inches(6.05), Inches(0.3))
para(t, "RECURRING REQUIREMENTS ACROSS THE SIX PAPERS", size=11,
     bold=True, color=BLUE, first=True)
reqs = [
    "Reliable and standardized data",
    "A clear, documented ETL pipeline",
    "A well-structured analytical model",
    "Interactive visuals that answer stakeholder questions",
    "Predictive or diagnostic features that turn observation into action",
]
y = Inches(1.72)
for i, rq in enumerate(reqs):
    rect(s, Inches(0.55), y, Inches(6.05), Inches(0.72), fill=LIGHT,
         line=BORDER)
    rect(s, Inches(0.55), y, Inches(0.07), Inches(0.72), fill=BLUE)
    t = textbox(s, Inches(0.88), y + Inches(0.17), Inches(0.4), Inches(0.4))
    para(t, str(i + 1), size=13, bold=True, color=SKY, first=True)
    t = textbox(s, Inches(1.3), y + Inches(0.14), Inches(5.1), Inches(0.5))
    para(t, rq, size=12, color=DARK, first=True, line_spacing=1.1)
    y += Inches(0.82)

t = textbox(s, Inches(0.55), Inches(5.95), Inches(6.05), Inches(0.75))
para(t, "Power BI suits the reporting and exploration layer, while Python, "
        "SQL, IoT platforms and ML services provide data preparation and "
        "advanced analytics.", size=11.5, italic=True, color=MUTED,
     first=True, line_spacing=1.15)

# gap panel
rect(s, Inches(6.85), Inches(1.32), Inches(5.92), Inches(2.28), fill=WHITE,
     line=AMBER, line_w=1.5)
rect(s, Inches(6.85), Inches(1.32), Inches(5.92), Inches(0.07), fill=AMBER)
t = textbox(s, Inches(7.2), Inches(1.58), Inches(5.25), Inches(0.3))
para(t, "THE GAP", size=11, bold=True, color=AMBER, first=True)
t = textbox(s, Inches(7.2), Inches(1.98), Inches(5.25), Inches(1.5))
para(t, "Existing work focuses on either Power BI reporting, IoT monitoring, "
        "or machine-learning analytics in isolation.", size=13,
     bold=True, color=NAVY, first=True, space_after=8, line_spacing=1.18)
para(t, "No single study integrates all three layers into one practical, "
        "documented and evaluated dashboard.", size=12.5, color=DARK,
     line_spacing=1.18)

rect(s, Inches(6.85), Inches(3.78), Inches(5.92), Inches(2.92), fill=LIGHT,
     line=BORDER)
rect(s, Inches(6.85), Inches(3.78), Inches(5.92), Inches(0.07), fill=GREEN)
t = textbox(s, Inches(7.2), Inches(4.04), Inches(5.25), Inches(0.3))
para(t, "OUR PROPOSED CONTRIBUTION", size=11, bold=True, color=GREEN,
     first=True)
t = textbox(s, Inches(7.2), Inches(4.44), Inches(5.25), Inches(2.15))
for i, b in enumerate([
    "Integrate reporting, IoT data and analytics in one dashboard",
    "Document explicit data-quality checks",
    "Provide role-specific views for different stakeholders",
    "Use explainable KPIs traceable to source data",
    "Evaluate on usability and decision usefulness",
]):
    bullet(t, b, size=11.5, first=(i == 0), space_after=9)
footer(s)


# ============================================================ SLIDE 6
s = blank()
header(s, 6, "Proposed System Design, Architecture & Methods")

layers = [
    ("DATA SOURCES", "Smart meters  |  IoT sensors (ESP32 via MQTT)  |  "
                     "Billing records  |  Weather / tariff reference data",
     NAVY),
    ("INGESTION & ETL", "Power Query cleaning  |  unit standardisation  |  "
                        "missing-value treatment  |  outlier handling  |  "
                        "scheduled refresh", BLUE),
    ("ANALYTICAL MODEL", "Star schema (fact: consumption readings; dimensions: "
                         "date, consumer, location, tariff, appliance)  |  "
                         "DAX measures", NAVY),
    ("ANALYTICS LAYER", "Forecasting (Prophet / regression)  |  anomaly "
                        "detection  |  load-shape clustering with t-SNE  |  "
                        "Top-N ranking", BLUE),
    ("PRESENTATION - POWER BI", "KPI cards  |  trend & peak-demand charts  |  "
                                "load heatmaps  |  comparisons  |  slicers  |  "
                                "drill-through pages", NAVY),
]
y = Inches(1.35)
for i, (name, body, accent) in enumerate(layers):
    rect(s, Inches(0.55), y, Inches(8.2), Inches(0.86), fill=LIGHT,
         line=BORDER)
    rect(s, Inches(0.55), y, Inches(2.35), Inches(0.86), fill=accent)
    t = textbox(s, Inches(0.72), y + Inches(0.28), Inches(2.05), Inches(0.35))
    para(t, name, size=10.5, bold=True, color=WHITE, first=True)
    t = textbox(s, Inches(3.05), y + Inches(0.16), Inches(5.55), Inches(0.62))
    para(t, body, size=10, color=DARK, first=True, line_spacing=1.12)
    if i < len(layers) - 1:
        rect(s, Inches(4.55), y + Inches(0.88), Inches(0.22), Inches(0.16),
             fill=SKY, shape=MSO_SHAPE.DOWN_ARROW)
    y += Inches(1.04)

# methods panel
rect(s, Inches(9.0), Inches(1.35), Inches(3.78), Inches(2.75), fill=WHITE,
     line=BORDER)
rect(s, Inches(9.0), Inches(1.35), Inches(3.78), Inches(0.07), fill=BLUE)
t = textbox(s, Inches(9.3), Inches(1.6), Inches(3.2), Inches(0.3))
para(t, "METHODS", size=11, bold=True, color=BLUE, first=True)
t = textbox(s, Inches(9.3), Inches(1.98), Inches(3.2), Inches(2.0))
for i, b in enumerate([
    "Design Science Research Methodology",
    "Business questions defined first",
    "Iterative build with user feedback",
    "Star-schema dimensional modeling",
    "Accuracy testing before publishing",
]):
    bullet(t, b, size=10.5, first=(i == 0), space_after=8)

rect(s, Inches(9.0), Inches(4.28), Inches(3.78), Inches(2.42), fill=LIGHT,
     line=BORDER)
rect(s, Inches(9.0), Inches(4.28), Inches(3.78), Inches(0.07), fill=GREEN)
t = textbox(s, Inches(9.3), Inches(4.53), Inches(3.2), Inches(0.3))
para(t, "EVALUATION METRICS", size=11, bold=True, color=GREEN, first=True)
t = textbox(s, Inches(9.3), Inches(4.91), Inches(3.2), Inches(1.7))
for i, b in enumerate([
    "Refresh reliability",
    "Visual clarity and usability",
    "Forecast error where used",
    "Actionable energy-saving findings",
]):
    bullet(t, b, size=10.5, first=(i == 0), space_after=9)
footer(s)


# ============================================================ IMAGERY
import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


def divider(kicker, title, subtitle):
    s = blank()
    rect(s, Inches(0), Inches(0), W, H, fill=NAVY)
    rect(s, Inches(0), Inches(3.3), W, Inches(0.055), fill=BLUE)
    t = textbox(s, Inches(1.1), Inches(2.3), Inches(11), Inches(0.45))
    para(t, kicker, size=13, bold=True, color=SKY, first=True)
    t = textbox(s, Inches(1.1), Inches(3.6), Inches(11.2), Inches(1.8))
    para(t, title, size=36, bold=True, color=WHITE, space_after=8, first=True)
    para(t, subtitle, size=15, color=SKY, line_spacing=1.2)
    page(s) if False else footer(s)


def visual_slide(num, title, img, caption, blocks, img_h=Inches(3.05),
                 source=None):
    """Image on top, explanatory blocks underneath."""
    s = blank()
    header(s, num, title)
    pic = s.shapes.add_picture(os.path.join(IMG, img), Inches(0.55),
                               Inches(1.3), height=img_h)
    # centre horizontally
    pic.left = int((W - pic.width) / 2)
    rect(s, Inches(0.55), Inches(1.3) + img_h + Inches(0.06),
         Inches(12.22), Inches(0.03), fill=BORDER)

    t = textbox(s, Inches(0.55), Inches(1.3) + img_h + Inches(0.15),
                Inches(12.22), Inches(0.3))
    para(t, caption, size=10.5, italic=True, color=MUTED,
         align=PP_ALIGN.CENTER, first=True)

    y = Inches(1.3) + img_h + Inches(0.55)
    bw = Inches(12.22 / len(blocks)) - Inches(0.16)
    x = Inches(0.55)
    avail = Inches(7.0) - y - Inches(0.1)
    for label, body, accent in blocks:
        rect(s, x, y, bw, avail, fill=LIGHT, line=BORDER)
        rect(s, x, y, bw, Inches(0.06), fill=accent)
        t = textbox(s, x + Inches(0.22), y + Inches(0.22),
                    bw - Inches(0.44), Inches(0.28))
        para(t, label, size=9.5, bold=True, color=accent, first=True)
        t = textbox(s, x + Inches(0.22), y + Inches(0.56),
                    bw - Inches(0.44), avail - Inches(0.7))
        para(t, body, size=10.5, color=DARK, first=True, line_spacing=1.16)
        x += bw + Inches(0.16)

    if source:
        t = textbox(s, Inches(0.55), Inches(6.72), Inches(12.22), Inches(0.26))
        para(t, source, size=9, italic=True, color=BLUE,
             align=PP_ALIGN.RIGHT, first=True)
    footer(s)


divider("APPENDIX",
        "Visual Design Concepts",
        "Illustrative renderings of the analytical visuals the dashboard "
        "will deliver")

# ---- 8 heatmap
visual_slide(
    8, "Load-Profile Heatmap",
    "heatmap_load_profile.png",
    "Synthetic illustration: hour-of-day against day-of-week consumption "
    "intensity, with one injected anomaly highlighted.",
    [
        ("WHAT IT SHOWS",
         "Each cell is average consumption for one hour on one weekday. "
         "Colour intensity exposes the building's daily rhythm at a glance - "
         "a morning ramp, a dominant evening peak, and a clearly different "
         "weekend pattern.", BLUE),
        ("HOW IT IS BUILT",
         "A matrix visual in Power BI over the consumption fact table, with "
         "hour and weekday pulled from the date dimension. Conditional "
         "formatting drives the colour scale from a DAX average measure.",
         NAVY),
        ("DECISION IT SUPPORTS",
         "Identifies exactly when peak demand occurs so tariff shifting, "
         "load staggering and equipment scheduling can be targeted at the "
         "right hours instead of the whole day.", GREEN),
    ],
    source="Traces to Paper 2 (hourly granularity) and Paper 6 "
           "(load-profile visuals)")

# ---- 9 forecast
visual_slide(
    9, "Demand Forecast with Uncertainty",
    "forecast_band.png",
    "Synthetic illustration: historical consumption with a forward forecast "
    "and 95% prediction interval.",
    [
        ("WHAT IT SHOWS",
         "The solid line is measured history; the dashed line projects future "
         "demand. The widening band communicates that confidence decays the "
         "further ahead the model predicts.", BLUE),
        ("HOW IT IS BUILT",
         "Prophet decomposes the series into trend plus weekly and monthly "
         "seasonality. Results are written back to the model and rendered as "
         "a Power BI line-and-area combination.", NAVY),
        ("DECISION IT SUPPORTS",
         "Enables procurement and capacity planning against an expected "
         "range rather than a single number, and makes forecast error "
         "measurable as an evaluation metric.", GREEN),
    ],
    source="Traces to Paper 2 (Prophet forecasting) and Paper 5 "
           "(regression forecasting)")

# ---- 10 anomaly
visual_slide(
    10, "Automated Anomaly Detection",
    "anomaly_timeline.png",
    "Synthetic illustration: consumption against a statistical control band, "
    "with deviations flagged and quantified.",
    [
        ("WHAT IT SHOWS",
         "The shaded band is expected behaviour derived from rolling "
         "statistics. Points breaching the threshold are marked in red and "
         "annotated with the size of the deviation in kWh.", BLUE),
        ("HOW IT IS BUILT",
         "A DAX measure computes a rolling mean and standard deviation; any "
         "reading beyond 2.2 sigma is flagged. The flag becomes a field that "
         "drives both the marker and an alert card.", NAVY),
        ("DECISION IT SUPPORTS",
         "Converts passive reporting into action - equipment faults, meter "
         "errors and wasteful overnight loads surface immediately instead of "
         "at the end of a billing cycle.", GREEN),
    ],
    source="Traces to Paper 4 (outlier handling) and Paper 5 "
           "(fault prediction)")

# ---- 11 clusters
visual_slide(
    11, "Load-Shape Clustering",
    "tsne_clusters.png",
    "Synthetic illustration: t-SNE projection grouping consumers by the "
    "shape of their daily demand curve.",
    [
        ("WHAT IT SHOWS",
         "Every point is one consumer-day compressed from 24 hourly readings "
         "into two dimensions. Points that sit together behave alike, so "
         "distinct usage personalities emerge as visible clusters.", BLUE),
        ("HOW IT IS BUILT",
         "Hourly profiles are normalised, then t-SNE reduces them to two "
         "dimensions in Python. Cluster labels return to Power BI as a "
         "dimension that every other visual can filter on.", NAVY),
        ("DECISION IT SUPPORTS",
         "Allows efficiency programmes to be tailored per segment, and makes "
         "the irregular cluster a natural watch-list for investigation.",
         GREEN),
    ],
    img_h=Inches(3.35),
    source="Traces to Paper 6 (t-SNE maps, morphing projections)")

# ---- 12 top-n
visual_slide(
    12, "Top-N Ranking with Sparklines",
    "topn_sparklines.png",
    "Synthetic illustration: highest-consuming entities with inline trend "
    "sparklines and period-on-period change.",
    [
        ("WHAT IT SHOWS",
         "Rank, absolute consumption, a compact trend line and a directional "
         "delta sit on a single row, so magnitude and momentum are readable "
         "together without opening another page.", BLUE),
        ("HOW IT IS BUILT",
         "A Power BI table visual with data bars, native sparklines and a "
         "DAX time-intelligence measure for the percentage change. Top-N "
         "filtering is applied through a rank measure.", NAVY),
        ("DECISION IT SUPPORTS",
         "Directs limited engineering attention to the few entities that "
         "dominate the bill, and separates the ones getting worse from the "
         "ones already improving.", GREEN),
    ],
    source="Traces to Paper 2 (consumer ranking) and Paper 6 (sparklines)")

# ---- 13 architecture
visual_slide(
    13, "End-to-End Data Flow",
    "architecture_flow.png",
    "Reference architecture: raw sensing through to the published Power BI "
    "dashboard, with quality gates at every hand-off.",
    [
        ("INGESTION",
         "Smart meters, ESP32 sensors and billing extracts publish over MQTT "
         "into a cloud store, giving one landing zone regardless of source "
         "format.", BLUE),
        ("PREPARATION & MODEL",
         "Power Query standardises units and treats missing values, then "
         "loads a star schema whose DAX measures keep every KPI traceable to "
         "its source rows.", NAVY),
        ("ANALYTICS & DELIVERY",
         "Forecasting, anomaly detection and clustering enrich the model "
         "before Power BI publishes role-specific pages with slicers and "
         "drill-through.", GREEN),
    ],
    source="Integrates Papers 1, 3, 4 and 5")


FOLDER = os.path.dirname(os.path.abspath(__file__))
BASE = "Team_VisualAnalytics_SmartEnergy_PowerBI"


def save_presentation():
    """Save, falling back to a free filename if the file is open."""
    for suffix in ["", "_v2", "_v3", "_v4"]:
        path = os.path.join(FOLDER, f"{BASE}{suffix}.pptx")
        try:
            prs.save(path)
            return path
        except PermissionError:
            print(f"  note: {os.path.basename(path)} is open; trying next name")
    raise SystemExit("All candidate filenames are locked. Close PowerPoint.")


out = save_presentation()
print("Saved:", out)
print("Slides:", len(prs.slides._sldIdLst))
