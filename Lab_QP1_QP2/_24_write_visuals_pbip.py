"""
Writes all report visuals directly into the PBIP report folder.

No archive, no signature - PBIP keeps the report definition as loose JSON
files, so this cannot corrupt the package.

Field bindings are validated against the ACTUAL model TMDL in the project
before anything is written.
"""
import json
import os
import re
import shutil
import hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(BASE, "Visual1.Report", "definition")
MODEL = os.path.join(BASE, "Visual1.SemanticModel", "definition")
PAGES = os.path.join(REPORT, "pages")

SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
V_SCHEMA = f"{SCH}/visualContainer/2.12.0/schema.json"
P_SCHEMA = f"{SCH}/page/2.1.0/schema.json"
PS_SCHEMA = f"{SCH}/pagesMetadata/1.1.0/schema.json"

# ------------------------------------------------------- read the real model
tables, cols, meas = set(), set(), set()
tdir = os.path.join(MODEL, "tables")
for fn in os.listdir(tdir):
    if not fn.endswith(".tmdl"):
        continue
    txt = open(os.path.join(tdir, fn), encoding="utf-8").read()
    m = re.search(r"^table\s+'?([^'\n]+?)'?\s*$", txt, re.M)
    tname = m.group(1) if m else os.path.splitext(fn)[0]
    tables.add(tname)
    for cm in re.finditer(r"^\tcolumn\s+'?([^'=\n]+?)'?\s*(?:=|$)", txt, re.M):
        cols.add((tname, cm.group(1).strip()))
    for mm in re.finditer(r"^\tmeasure\s+'?([^'=\n]+?)'?\s*=", txt, re.M):
        meas.add((tname, mm.group(1).strip()))

print(f"Model read from project: {len(tables)} tables, {len(cols)} columns, "
      f"{len(meas)} measures")

_ids = set()


def vid(seed):
    h = hashlib.sha1(seed.encode()).hexdigest()[:20]
    while h in _ids:
        h = hashlib.sha1((seed + "_").encode()).hexdigest()[:20]
    _ids.add(h)
    return h


PROBLEMS = []


def measure(entity, prop):
    if (entity, prop) not in meas:
        PROBLEMS.append(f"measure {entity}[{prop}] not in model")
    return {"field": {"Measure": {
        "Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}


def column(entity, prop):
    if (entity, prop) not in cols:
        PROBLEMS.append(f"column {entity}[{prop}] not in model")
    return {"field": {"Column": {
        "Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}


def sum_column(entity, prop):
    if (entity, prop) not in cols:
        PROBLEMS.append(f"agg column {entity}[{prop}] not in model")
    return {"field": {"Aggregation": {"Expression": {"Column": {
        "Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "Function": 0}},
        "queryRef": f"Sum({entity}.{prop})",
        "nativeQueryRef": f"Sum of {prop}"}


def visual(seed, vtype, x, y, w, h, roles, z=0):
    qs = {r: {"projections": p} for r, p in roles.items() if p}
    if x + w > 1920 or y + h > 1080:
        PROBLEMS.append(f"{vtype} off canvas ({x},{y},{w},{h})")
    return {"$schema": V_SCHEMA, "name": vid(seed),
            "position": {"x": x, "y": y, "z": z, "width": w, "height": h,
                         "tabOrder": z * 1000},
            "visual": {"visualType": vtype,
                       "query": {"queryState": qs},
                       "drillFilterOtherVisuals": True}}


F, P, D, T, C = "FactSales", "DimProduct", "DimDate", "DimTerritory", \
    "DimCustomer"
TOP5 = "Top 5 Products"

# ============================================================ PAGE 1
p1 = []
cards = [
    ("Total Sales", 40),
    ("Total Quantity", 415),
    ("Total Profit", 790),
    ("Profit Margin %", 1165),
    ("YoY Growth %", 1540),
]
for label, xpos in cards:
    p1.append(visual(f"c_{label}", "card", xpos, 25, 340, 110,
                     {"Values": [measure(F, label)]}))

p1.append(visual("sl_year", "slicer", 40, 150, 440, 85,
                 {"Values": [column(D, "Year")]}))
p1.append(visual("sl_cat", "slicer", 500, 150, 440, 85,
                 {"Values": [column(P, "Category")]}))
p1.append(visual("sl_reg", "slicer", 960, 150, 440, 85,
                 {"Values": [column(T, "Region")]}))
p1.append(visual("sl_seg", "slicer", 1420, 150, 460, 85,
                 {"Values": [column(C, "Segment")]}))

p1.append(visual("line_trend", "lineChart", 40, 250, 910, 420, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Total Sales"), measure(F, "Sales PY")]}))

p1.append(visual("col_cat", "columnChart", 970, 250, 910, 420, {
    "Category": [column(P, "Category")],
    "Y": [measure(F, "Total Sales")],
    "Series": [column(D, "Year")]}))

p1.append(visual("bar_prod", "clusteredBarChart", 40, 690, 600, 360, {
    "Category": [column(P, "ProductName")],
    "Y": [measure(F, "Total Quantity")]}))

p1.append(visual("donut_reg", "donutChart", 660, 690, 540, 360, {
    "Category": [column(T, "Region")],
    "Y": [measure(F, "Total Sales")]}))

p1.append(visual("tbl_cat", "tableEx", 1220, 690, 660, 360, {
    "Values": [column(P, "Category"), measure(F, "Total Sales"),
               measure(F, "Avg Sales per Order"),
               measure(F, "Category Share %")]}))

# ============================================================ PAGE 2
p2 = []
p2.append(visual("mtx_yoy", "pivotTable", 40, 30, 1180, 480, {
    "Rows": [column(P, "Category")],
    "Columns": [column(D, "Year")],
    "Values": [measure(F, "Total Sales"), measure(F, "Sales PY"),
               measure(F, "YoY Growth %")]}))

p2.append(visual("col_top5", "clusteredColumnChart", 1240, 30, 640, 480, {
    "Category": [column(TOP5, "ProductName")],
    "Y": [sum_column(TOP5, "Units Sold")]}))

p2.append(visual("area_cum", "areaChart", 40, 530, 580, 510, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Sales Cumulative")]}))

p2.append(visual("line_roll", "lineChart", 640, 530, 600, 510, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Total Sales"), measure(F, "Sales 3M Moving Avg")]}))

p2.append(visual("combo_ytd", "lineClusteredColumnComboChart", 1260, 530, 620, 510, {
    "Category": [column(D, "MonthName")],
    "Y": [measure(F, "Total Sales")],
    "Y2": [measure(F, "Sales YTD")]}))

# ============================================================ PAGE 3: AI DECOMPOSITION & HIERARCHY
p3 = []
p3.append(visual("c_sales_p3", "card", 40, 30, 340, 110,
                 {"Values": [measure(F, "Total Sales")]}))
p3.append(visual("c_profit_p3", "card", 400, 30, 340, 110,
                 {"Values": [measure(F, "Total Profit")]}))
p3.append(visual("c_margin_p3", "card", 760, 30, 340, 110,
                 {"Values": [measure(F, "Profit Margin %")]}))
p3.append(visual("sl_cat_p3", "slicer", 1120, 30, 370, 110,
                 {"Values": [column(P, "Category")]}))
p3.append(visual("sl_reg_p3", "slicer", 1510, 30, 370, 110,
                 {"Values": [column(T, "Region")]}))

p3.append(visual("decomp_tree", "decompositionTree", 40, 160, 1180, 880, {
    "Analyze": [measure(F, "Total Sales")],
    "ExplainBy": [column(P, "Category"), column(C, "Segment"), column(T, "Region")]}))

p3.append(visual("drill_col", "clusteredColumnChart", 1240, 160, 640, 880, {
    "Category": [column(P, "Category"), column(P, "Subcategory"), column(P, "ProductName")],
    "Y": [measure(F, "Total Sales")]}))

# ============================================================ validate first
if PROBLEMS:
    print("\nABORTING - field problems found:")
    for p in PROBLEMS:
        print("  -", p)
    raise SystemExit(1)
print("All field bindings resolve against the project model.")

# ============================================================ write
page1_id = vid("page1_sales_overview")
page2_id = vid("page2_category_time")
page3_id = vid("page3_ai_decomp")
print(f"\nPage 1: {page1_id}\nPage 2: {page2_id}\nPage 3: {page3_id}")


def W(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


# clear any existing page directories so layout is completely clean
for d in os.listdir(PAGES):
    p = os.path.join(PAGES, d)
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)

W(os.path.join(PAGES, "pages.json"), {
    "$schema": PS_SCHEMA,
    "pageOrder": [page1_id, page2_id, page3_id],
    "activePageName": page1_id})

W(os.path.join(PAGES, page1_id, "page.json"), {
    "$schema": P_SCHEMA, "name": page1_id,
    "displayName": "1 Sales Overview",
    "displayOption": "FitToPage", "height": 1080, "width": 1920})

W(os.path.join(PAGES, page2_id, "page.json"), {
    "$schema": P_SCHEMA, "name": page2_id,
    "displayName": "2 Category and Time Analysis",
    "displayOption": "FitToPage", "height": 1080, "width": 1920})

W(os.path.join(PAGES, page3_id, "page.json"), {
    "$schema": P_SCHEMA, "name": page3_id,
    "displayName": "3 AI Decomposition & Hierarchy",
    "displayOption": "FitToPage", "height": 1080, "width": 1920})

for v in p1:
    W(os.path.join(PAGES, page1_id, "visuals", v["name"], "visual.json"), v)
for v in p2:
    W(os.path.join(PAGES, page2_id, "visuals", v["name"], "visual.json"), v)
for v in p3:
    W(os.path.join(PAGES, page3_id, "visuals", v["name"], "visual.json"), v)

print(f"\nPage 1 - 1 Sales Overview  ({len(p1)} visuals)")
for v in p1:
    print(f"   {v['visual']['visualType']}")
print(f"\nPage 2 - 2 Category and Time Analysis  ({len(p2)} visuals)")
for v in p2:
    print(f"   {v['visual']['visualType']}")
print(f"\nPage 3 - 3 AI Decomposition & Hierarchy  ({len(p3)} visuals)")
for v in p3:
    print(f"   {v['visual']['visualType']}")
print(f"\nDone. Reopen Visual1.pbip in Power BI Desktop.")
