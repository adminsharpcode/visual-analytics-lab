"""
Generates all report visuals into a copy of Visual1.pbix.

The PBIR envelope is copied verbatim from the visual Power BI itself wrote
(Report/definition/pages/<page>/visuals/<id>/visual.json, schema 2.12.0), so
the field-binding shape is known-correct rather than guessed.

Output: Visual1_withVisuals.pbix   (original left untouched)
"""
import hashlib
import json
import os
import shutil
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Visual1.pbix")
DST = os.path.join(BASE, "Visual1_withVisuals.pbix")

SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
V_SCHEMA = f"{SCH}/visualContainer/2.12.0/schema.json"
P_SCHEMA = f"{SCH}/page/2.1.0/schema.json"
PS_SCHEMA = f"{SCH}/pagesMetadata/1.1.0/schema.json"

_ids = set()


def vid(seed):
    """Deterministic 20-hex-char id, matching Power BI's id shape."""
    h = hashlib.sha1(seed.encode()).hexdigest()[:20]
    while h in _ids:
        h = hashlib.sha1((seed + "x").encode()).hexdigest()[:20]
    _ids.add(h)
    return h


# ---------------------------------------------------------------- fields
def measure(entity, prop):
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}},
                              "Property": prop}},
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }


def column(entity, prop):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}},
                             "Property": prop}},
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }


def sum_column(entity, prop):
    return {
        "field": {"Aggregation": {
            "Expression": {"Column": {
                "Expression": {"SourceRef": {"Entity": entity}},
                "Property": prop}},
            "Function": 0}},
        "queryRef": f"Sum({entity}.{prop})",
        "nativeQueryRef": f"Sum of {prop}",
    }


def visual(name_seed, vtype, x, y, w, h, roles, z=0):
    """roles: dict of dataRole -> list of projections"""
    qs = {role: {"projections": projs} for role, projs in roles.items()
          if projs}
    return {
        "$schema": V_SCHEMA,
        "name": vid(name_seed),
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h,
                     "tabOrder": z * 1000},
        "visual": {
            "visualType": vtype,
            "query": {"queryState": qs},
            "drillFilterOtherVisuals": True,
        },
    }


F = "FactSales"
P = "DimProduct"
D = "DimDate"
T = "DimTerritory"
C = "DimCustomer"

# ============================================================ PAGE 1
p1 = []

# --- KPI cards -------------------------------------------------------
cards = [
    ("Total Sales", "01 Sales"),
    ("Total Quantity", None),
    ("Total Profit", None),
    ("Profit Margin %", None),
    ("YoY Growth %", None),
]
x = 40
for label, _ in cards:
    p1.append(visual(f"card_{label}", "card", x, 30, 340, 120,
                     {"Values": [measure(F, label)]}))
    x += 360

# --- sales trend vs prior year --------------------------------------
p1.append(visual("line_trend", "lineChart", 40, 170, 900, 380, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Total Sales"), measure(F, "Sales PY")],
}))

# --- category performance by year -----------------------------------
p1.append(visual("col_category", "stackedColumnChart", 960, 170, 920, 380, {
    "Category": [column(P, "Category")],
    "Y": [measure(F, "Total Sales")],
    "Series": [column(D, "Year")],
}))

# --- top products by units ------------------------------------------
p1.append(visual("bar_products", "clusteredBarChart", 40, 570, 700, 340, {
    "Category": [column(P, "ProductName")],
    "Y": [measure(F, "Total Quantity")],
}))

# --- regional split --------------------------------------------------
p1.append(visual("donut_region", "donutChart", 760, 570, 440, 340, {
    "Category": [column(T, "Region")],
    "Y": [measure(F, "Total Sales")],
}))

# --- category detail table ------------------------------------------
p1.append(visual("table_category", "tableEx", 1220, 570, 660, 340, {
    "Values": [column(P, "Category"),
               measure(F, "Total Sales"),
               measure(F, "Avg Sales per Order"),
               measure(F, "Category Share %")],
}))

# --- slicers ---------------------------------------------------------
slicers = [(D, "Year"), (P, "Category"), (T, "Region"), (C, "Segment")]
x = 40
for ent, col in slicers:
    p1.append(visual(f"slicer_{col}", "slicer", x, 930, 440, 120,
                     {"Values": [column(ent, col)]}))
    x += 460

# ============================================================ PAGE 2
p2 = []

# --- YoY matrix ------------------------------------------------------
p2.append(visual("matrix_yoy", "pivotTable", 40, 30, 1200, 420, {
    "Rows": [column(P, "Category")],
    "Columns": [column(D, "Year")],
    "Values": [measure(F, "Total Sales"), measure(F, "Sales PY"),
               measure(F, "YoY Growth %")],
}))

# --- top 5 products (preserves the chart you made by hand) -----------
p2.append(visual("col_top5", "clusteredColumnChart", 1260, 30, 620, 420, {
    "Category": [column("Top 5 Products", "ProductName")],
    "Y": [sum_column("Top 5 Products", "Units Sold")],
}))

# --- cumulative sales ------------------------------------------------
p2.append(visual("area_cumulative", "areaChart", 40, 470, 900, 280, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Sales Cumulative")],
}))

# --- rolling average -------------------------------------------------
p2.append(visual("line_rolling", "lineChart", 960, 470, 920, 280, {
    "Category": [column(D, "YearMonth")],
    "Y": [measure(F, "Total Sales"), measure(F, "Sales 3M Moving Avg")],
}))

# --- monthly sales with YTD -----------------------------------------
p2.append(visual("combo_ytd", "lineClusteredColumnComboChart",
                 40, 770, 1840, 280, {
    "Category": [column(D, "MonthName")],
    "Y": [measure(F, "Total Sales")],
    "Y2": [measure(F, "Sales YTD")],
}))

# ============================================================ package
z = zipfile.ZipFile(SRC)
names = z.namelist()

# existing page id (reuse for page 1)
page1_id = None
for n in names:
    if n.startswith("Report/definition/pages/") and n.endswith("/page.json"):
        page1_id = n.split("/")[-2]
        break
if not page1_id:
    raise SystemExit("could not find existing page id")
page2_id = vid("page2_category_time")

print(f"Page 1 id : {page1_id}  (reused)")
print(f"Page 2 id : {page2_id}  (new)")

# drop any visuals the pbix already had - we lay out both pages cleanly
skip_prefixes = tuple(
    f"Report/definition/pages/{page1_id}/visuals/" for _ in [0])
dropped = [n for n in names if n.startswith(skip_prefixes)]

new_parts = {}


def J(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) \
        .encode("utf-8")


# pages.json - both pages, page 1 active
new_parts["Report/definition/pages/pages.json"] = J({
    "$schema": PS_SCHEMA,
    "pageOrder": [page1_id, page2_id],
    "activePageName": page1_id,
})

# page 1 - rename
new_parts[f"Report/definition/pages/{page1_id}/page.json"] = J({
    "$schema": P_SCHEMA, "name": page1_id,
    "displayName": "1 Sales Overview",
    "displayOption": "FitToPage", "height": 1080, "width": 1920,
})

# page 2
new_parts[f"Report/definition/pages/{page2_id}/page.json"] = J({
    "$schema": P_SCHEMA, "name": page2_id,
    "displayName": "2 Category and Time Analysis",
    "displayOption": "FitToPage", "height": 1080, "width": 1920,
})

for v in p1:
    new_parts[f"Report/definition/pages/{page1_id}/visuals/"
              f"{v['name']}/visual.json"] = J(v)
for v in p2:
    new_parts[f"Report/definition/pages/{page2_id}/visuals/"
              f"{v['name']}/visual.json"] = J(v)

if os.path.exists(DST):
    os.remove(DST)

with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as out:
    for item in z.infolist():
        if item.filename in dropped:
            continue
        if item.filename in new_parts:
            continue      # replaced below
        zi = zipfile.ZipInfo(item.filename, date_time=item.date_time)
        zi.compress_type = item.compress_type
        zi.external_attr = item.external_attr
        out.writestr(zi, z.read(item.filename))
    for path, data in new_parts.items():
        out.writestr(path, data)

print(f"\nremoved {len(dropped)} pre-existing visual file(s)")
print(f"wrote   {len(new_parts)} definition file(s)")
print(f"\nPage 1 - 1 Sales Overview        {len(p1)} visuals")
for v in p1:
    print(f"    {v['visual']['visualType']:<32} "
          f"{list(v['visual']['query']['queryState'].keys())}")
print(f"\nPage 2 - 2 Category and Time      {len(p2)} visuals")
for v in p2:
    print(f"    {v['visual']['visualType']:<32} "
          f"{list(v['visual']['query']['queryState'].keys())}")
print(f"\nCreated {os.path.basename(DST)} "
      f"({os.path.getsize(DST)/1024:.0f} KB)")
