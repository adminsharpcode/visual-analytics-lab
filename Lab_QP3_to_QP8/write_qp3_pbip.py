"""
Generates the VisualAnalytics_QP3.pbip Power BI Project for Assessment 3.
Copies and extends the semantic model, adding dedicated pages for:
  Page 1: 1 Executive Overview & Slicers
  Page 2: 2 Product Hierarchy & Drill-Down
  Page 3: 3 AI Decomposition Tree Analysis
Author: Vedant Nimkar | Reg No: 26MML0045
"""

import json
import os
import shutil
import hashlib

SRC_BASE = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP1_QP2"
DST_BASE = r"c:\Users\ROG\Desktop\Mtech Classwork\Visual analytics\Lab_QP3_to_QP8"

PBIP_FILE = os.path.join(DST_BASE, "VisualAnalytics_QP3.pbip")
REPORT_DIR = os.path.join(DST_BASE, "VisualAnalytics_QP3.Report")
MODEL_DIR = os.path.join(DST_BASE, "VisualAnalytics_QP3.SemanticModel")

SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
V_SCHEMA = f"{SCH}/visualContainer/2.12.0/schema.json"
P_SCHEMA = f"{SCH}/page/2.1.0/schema.json"
PS_SCHEMA = f"{SCH}/pagesMetadata/1.1.0/schema.json"

# 1. Copy Semantic Model
if os.path.exists(MODEL_DIR):
    shutil.rmtree(MODEL_DIR)
shutil.copytree(os.path.join(SRC_BASE, "Visual1.SemanticModel"), MODEL_DIR)

# 2. Setup Report Directory
if os.path.exists(REPORT_DIR):
    shutil.rmtree(REPORT_DIR)
os.makedirs(os.path.join(REPORT_DIR, "definition", "pages"), exist_ok=True)
shutil.copy(os.path.join(SRC_BASE, "Visual1.Report", "definition.pbir"), os.path.join(REPORT_DIR, "definition.pbir"))

# Also copy definition/report.json and definition/version.json
for fn in ["report.json", "version.json"]:
    src_f = os.path.join(SRC_BASE, "Visual1.Report", "definition", fn)
    if os.path.exists(src_f):
        shutil.copy(src_f, os.path.join(REPORT_DIR, "definition", fn))

# Copy StaticResources (theme etc.)
src_res = os.path.join(SRC_BASE, "Visual1.Report", "StaticResources")
if os.path.exists(src_res):
    shutil.copytree(src_res, os.path.join(REPORT_DIR, "StaticResources"), dirs_exist_ok=True)

# Update definition.pbir to point to local semantic model
with open(os.path.join(REPORT_DIR, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump({
        "version": "4.0",
        "datasetReference": {
            "byPath": {
                "path": "../VisualAnalytics_QP3.SemanticModel"
            },
            "byConnection": None
        }
    }, f, indent=2)

# Create .pbip root file
with open(PBIP_FILE, "w", encoding="utf-8") as f:
    json.dump({
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "VisualAnalytics_QP3.Report"
                }
            }
        ],
        "settings": {
            "enableAutoRecovery": True
        }
    }, f, indent=2)

# Helper functions to build visuals
_ids = set()
def vid(seed):
    h = hashlib.sha1(seed.encode()).hexdigest()[:20]
    while h in _ids:
        h = hashlib.sha1((seed + "_").encode()).hexdigest()[:20]
    _ids.add(h)
    return h

def measure(entity, prop):
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop
    }

def column(entity, prop):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop
    }

def visual(seed, vtype, x, y, w, h, roles, z=0):
    qs = {r: {"projections": p} for r, p in roles.items() if p}
    return {
        "$schema": V_SCHEMA,
        "name": vid(seed),
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z * 1000},
        "visual": {
            "visualType": vtype,
            "query": {"queryState": qs},
            "drillFilterOtherVisuals": True
        }
    }

F, P, D, T, C = "FactSales", "DimProduct", "DimDate", "DimTerritory", "DimCustomer"

# --- PAGE 1: Executive Overview with Multi-Field Slicers (Exp 7) ---
p1 = []
x = 40
for label in ["Total Sales", "Total Quantity", "Total Profit", "Profit Margin %", "YoY Growth %"]:
    p1.append(visual(f"p1_c_{label}", "card", x, 30, 340, 120, {"Values": [measure(F, label)]}))
    x += 360

p1.append(visual("p1_line_trend", "lineChart", 40, 170, 920, 420, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Total Sales"), measure(F, "Sales PY")]
}))

p1.append(visual("p1_donut_reg", "donutChart", 980, 170, 440, 420, {
    "Category": [column(T, "Region")],
    "Y": [measure(F, "Total Sales")]
}))

p1.append(visual("p1_tbl_cat", "tableEx", 1440, 170, 440, 420, {
    "Values": [column(P, "Category"), measure(F, "Total Sales"), measure(F, "Profit Margin %")]
}))

# 3 Slicers across the bottom
p1.append(visual("p1_sl_date", "slicer", 40, 620, 600, 140, {"Values": [column(D, "Date")]}))
p1.append(visual("p1_sl_cat", "slicer", 660, 620, 580, 140, {"Values": [column(P, "Category")]}))
p1.append(visual("p1_sl_reg", "slicer", 1260, 620, 620, 140, {"Values": [column(T, "Region")]}))

# --- PAGE 2: Product Hierarchy & Interactive Drilldown (Exp 7) ---
p2 = []
# Clustered column chart with Product Hierarchy
p2.append(visual("p2_drill_col", "clusteredColumnChart", 40, 40, 1080, 520, {
    "Category": [column(P, "Category"), column(P, "Subcategory"), column(P, "ProductName")],
    "Y": [measure(F, "Total Sales")]
}))

# Matrix with hierarchical rows
p2.append(visual("p2_matrix_hier", "pivotTable", 1140, 40, 740, 520, {
    "Rows": [column(P, "Category"), column(P, "Subcategory"), column(P, "ProductName")],
    "Values": [measure(F, "Total Sales"), measure(F, "Total Profit"), measure(F, "Profit Margin %")]
}))

# Subcategory summary table
p2.append(visual("p2_subcat_bar", "clusteredBarChart", 40, 580, 1840, 440, {
    "Category": [column(P, "Subcategory")],
    "Y": [measure(F, "Total Sales")]
}))

# --- PAGE 3: AI Decomposition Tree Root Cause Analysis (Exp 7 & 8) ---
p3 = []
# Decomposition Tree Visual
p3.append(visual("p3_decomp_tree", "decompositionTree", 40, 40, 1840, 700, {
    "Analyze": [measure(F, "Total Sales")],
    "ExplainBy": [column(P, "Category"), column(P, "Subcategory"), column(C, "Segment"), column(T, "Region")]
}))

x = 40
for label in ["Total Sales", "Total Profit", "Average Order Value"]:
    p3.append(visual(f"p3_c_{label}", "card", x, 760, 580, 140, {"Values": [measure(F, label)]}))
    x += 620

# Write Pages into PBIP
PAGES_DIR = os.path.join(REPORT_DIR, "definition", "pages")
page1_id = vid("page1_slicers")
page2_id = vid("page2_drilldown")
page3_id = vid("page3_decomp")

def W(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

W(os.path.join(PAGES_DIR, "pages.json"), {
    "$schema": PS_SCHEMA,
    "pageOrder": [page1_id, page2_id, page3_id],
    "activePageName": page1_id
})

W(os.path.join(PAGES_DIR, page1_id, "page.json"), {
    "$schema": P_SCHEMA, "name": page1_id,
    "displayName": "1 Executive Overview & Slicers",
    "displayOption": "FitToPage", "height": 1080, "width": 1920
})

W(os.path.join(PAGES_DIR, page2_id, "page.json"), {
    "$schema": P_SCHEMA, "name": page2_id,
    "displayName": "2 Product Hierarchy & Drilldown",
    "displayOption": "FitToPage", "height": 1080, "width": 1920
})

W(os.path.join(PAGES_DIR, page3_id, "page.json"), {
    "$schema": P_SCHEMA, "name": page3_id,
    "displayName": "3 AI Decomposition Tree",
    "displayOption": "FitToPage", "height": 1080, "width": 1920
})

for v in p1: W(os.path.join(PAGES_DIR, page1_id, "visuals", v["name"], "visual.json"), v)
for v in p2: W(os.path.join(PAGES_DIR, page2_id, "visuals", v["name"], "visual.json"), v)
for v in p3: W(os.path.join(PAGES_DIR, page3_id, "visuals", v["name"], "visual.json"), v)

print(f"VisualAnalytics_QP3.pbip successfully generated!")
print(f"Location: {PBIP_FILE}")
print(f"   Page 1: 1 Executive Overview & Slicers ({len(p1)} visuals)")
print(f"   Page 2: 2 Product Hierarchy & Drilldown ({len(p2)} visuals)")
print(f"   Page 3: 3 AI Decomposition Tree ({len(p3)} visuals)")
