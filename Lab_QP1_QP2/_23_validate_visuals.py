"""Validate Visual1_withVisuals.pbix before opening it."""
import json
import os
import re
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(BASE, "Visual1_withVisuals.pbix")
TMDL = os.path.join(BASE, "tmdl", "PHASE1_tables_and_relationships.tmdl")

ok = True


def fail(m):
    global ok
    ok = False
    print("  FAIL:", m)


z = zipfile.ZipFile(DST)
bad = z.testzip()
print("Zip integrity:", "OK" if not bad else f"corrupt {bad}")
if bad:
    fail("corrupt archive")

# essential pbix parts must survive
for need in ["Version", "[Content_Types].xml", "DataModel", "Settings",
             "Metadata", "SecurityBindings",
             "Report/definition/report.json",
             "Report/definition/version.json"]:
    if need not in z.namelist():
        fail(f"missing part {need}")
print("Essential parts:", "all present" if ok else "MISSING")
dm = z.getinfo("DataModel").file_size
print(f"DataModel preserved: {dm:,} bytes")

# ---- collect model names from the TMDL we applied ----
tm = open(TMDL, encoding="utf-8").read()
tables = set(re.findall(r"^\ttable\s+'?([^'\n]+?)'?$", tm, re.M))
tables |= {"Top 5 Products", "Product Category Summary"}
cols, meas = set(), set()
cur = None
for ln in tm.split("\n"):
    m = re.match(r"^\ttable\s+'?([^'\n]+?)'?$", ln)
    if m:
        cur = m.group(1)
    m = re.match(r"^\t\tcolumn\s+'?([^'=\n]+?)'?\s*(=|$)", ln)
    if m and cur:
        cols.add((cur, m.group(1).strip()))
    m = re.match(r"^\t\tmeasure\s+'?([^'=\n]+?)'?\s*=", ln)
    if m and cur:
        meas.add((cur, m.group(1).strip()))

# calculated table columns are inferred - allow them
inferred = {("Top 5 Products", "ProductName"), ("Top 5 Products", "Category"),
            ("Top 5 Products", "Units Sold"), ("Top 5 Products", "Revenue"),
            ("Product Category Summary", "Category")}
cols |= inferred

print(f"\nModel: {len(tables)} tables, {len(cols)} columns, "
      f"{len(meas)} measures")

# ---- walk the visuals ----
pages = {}
for n in z.namelist():
    m = re.match(r"Report/definition/pages/([^/]+)/page\.json", n)
    if m:
        pages[m.group(1)] = json.loads(z.read(n).decode("utf-8"))

pmeta = json.loads(
    z.read("Report/definition/pages/pages.json").decode("utf-8"))
print(f"\nPages ({len(pages)}), order = {pmeta['pageOrder']}")
for pid in pmeta["pageOrder"]:
    p = pages[pid]
    vis = [n for n in z.namelist()
           if n.startswith(f"Report/definition/pages/{pid}/visuals/")]
    print(f"  {p['displayName']:<32} {p['width']}x{p['height']}  "
          f"{len(vis)} visuals")

print("\nField reference check")
checked = 0
for n in z.namelist():
    if not n.endswith("/visual.json"):
        continue
    v = json.loads(z.read(n).decode("utf-8"))
    vt = v["visual"]["visualType"]
    pos = v["position"]
    if pos["x"] + pos["width"] > 1920 or pos["y"] + pos["height"] > 1080:
        fail(f"{vt} extends past canvas: x={pos['x']} y={pos['y']} "
             f"w={pos['width']} h={pos['height']}")
    for role, blk in v["visual"]["query"]["queryState"].items():
        for pr in blk["projections"]:
            f_ = pr["field"]
            if "Measure" in f_:
                ent = f_["Measure"]["Expression"]["SourceRef"]["Entity"]
                prop = f_["Measure"]["Property"]
                if (ent, prop) not in meas:
                    fail(f"{vt}/{role}: measure {ent}[{prop}] not in model")
            elif "Column" in f_:
                ent = f_["Column"]["Expression"]["SourceRef"]["Entity"]
                prop = f_["Column"]["Property"]
                if (ent, prop) not in cols:
                    fail(f"{vt}/{role}: column {ent}[{prop}] not in model")
            elif "Aggregation" in f_:
                c = f_["Aggregation"]["Expression"]["Column"]
                ent = c["Expression"]["SourceRef"]["Entity"]
                prop = c["Property"]
                if (ent, prop) not in cols:
                    fail(f"{vt}/{role}: agg column {ent}[{prop}] not in model")
            checked += 1
print(f"  {checked} field bindings checked")

print("\n" + "=" * 58)
print("VALIDATION PASSED" if ok else "VALIDATION FAILED")
print("=" * 58)
