"""
Converts the lab model into a TMDL script you paste into TMDL view
(Power BI Desktop: GA, or Power BI service: preview) and press Apply.

This sidesteps the .pbit / .pbip package format entirely - TMDL view executes
the script directly against the semantic model.

Outputs:
  tmdl/01_tables.tmdl          tables + columns + measures + hierarchies + M
  tmdl/02_relationships.tmdl   the 5 relationships (1 inactive)
  tmdl/03_calc_tables.tmdl     the 2 calculated tables
  tmdl/ALL_IN_ONE.tmdl         everything, in dependency order
"""
import importlib.util
import os
import re
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "tmdl")
os.makedirs(OUT, exist_ok=True)

TAB = "\t"

# ------------------------------------------------------------ import model
spec = importlib.util.spec_from_file_location(
    "pbitbuild", os.path.join(BASE, "_10_build_pbit.py"))
mod = importlib.util.module_from_spec(spec)
_orig = zipfile.ZipFile


class _NoZip:
    def __init__(self, *a, **k):
        raise RuntimeError("suppressed")


try:
    zipfile.ZipFile = _NoZip
    try:
        spec.loader.exec_module(mod)
    except RuntimeError:
        pass
finally:
    zipfile.ZipFile = _orig

model = mod.model["model"]
tables = model["tables"]
rels = model["relationships"]

SIMPLE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def nm(name):
    """Quote a TMDL object name when it is not a bare identifier."""
    return name if SIMPLE.match(name) else f"'{name}'"


def block(expr, indent):
    """
    Render a multi-line DAX/M expression as a fenced TMDL block.

    The ``` fence is required: without it, a following property such as
    formatString is still indented deeper than the declaration line and
    would be absorbed into the expression.
    """
    pad = TAB * indent
    lines = expr.rstrip("\n").split("\n")
    body = "\n".join(pad + ln if ln.strip() else "" for ln in lines)
    return f"{body}\n{pad}```"


FENCE = "```"


def decl(keyword, name, expr, indent, out):
    """
    Emit  <keyword> <name> = <expr>   inline when single-line, or as a
    fenced block when the expression spans multiple lines.
    """
    pad = TAB * indent
    if "\n" in expr.strip():
        out.append(f"{pad}{keyword} {nm(name)} = {FENCE}")
        out.append(block(expr, indent + 2))
    else:
        out.append(f"{pad}{keyword} {nm(name)} = {expr.strip()}")


def emit_column(c, out):
    """A regular, calculated, or calculated-table column."""
    ctype = c.get("type")
    if ctype == "calculated":
        decl("column", c["name"], c["expression"], 1, out)
        if "dataType" in c:
            out.append(f"{TAB*2}dataType: {c['dataType']}")
    elif ctype == "calculatedTableColumn":
        out.append(f"{TAB}column {nm(c['name'])}")
        out.append(f"{TAB*2}dataType: {c['dataType']}")
        out.append(f"{TAB*2}sourceColumn: {c['sourceColumn']}")
        if c.get("isNameInferred"):
            out.append(f"{TAB*2}isNameInferred")
    else:
        out.append(f"{TAB}column {nm(c['name'])}")
        out.append(f"{TAB*2}dataType: {c['dataType']}")
        out.append(f"{TAB*2}sourceColumn: {c['sourceColumn']}")

    if c.get("formatString"):
        out.append(f"{TAB*2}formatString: {c['formatString']}")
    out.append(f"{TAB*2}summarizeBy: {c.get('summarizeBy', 'none')}")
    if c.get("isHidden"):
        out.append(f"{TAB*2}isHidden")
    if c.get("isKey"):
        out.append(f"{TAB*2}isKey")
    if c.get("sortByColumn"):
        out.append(f"{TAB*2}sortByColumn: {nm(c['sortByColumn'])}")
    out.append("")


def emit_measure(m, out):
    decl("measure", m["name"], m["expression"], 1, out)
    if m.get("formatString"):
        out.append(f"{TAB*2}formatString: {m['formatString']}")
    if m.get("displayFolder"):
        out.append(f"{TAB*2}displayFolder: {m['displayFolder']}")
    out.append("")


def emit_hierarchy(h, out):
    out.append(f"{TAB}hierarchy {nm(h['name'])}")
    for lv in h["levels"]:
        out.append(f"{TAB*2}level {nm(lv['name'])}")
        out.append(f"{TAB*3}column: {nm(lv['column'])}")
        out.append("")


def is_deferred(c):
    """
    Calculated columns using RELATED() cannot be created in the same pass as
    the tables: RELATED needs the target table AND an active relationship to
    already exist. These are emitted into a later phase script instead.
    """
    return (c.get("type") == "calculated"
            and "RELATED" in c.get("expression", ""))


DEFERRED = []


def emit_table(t, include_deferred=False):
    """
    createOrReplace on a table replaces the ENTIRE table definition, so any
    script touching a table must contain all of its columns, measures,
    hierarchies and partition - never just the one column being added.
    """
    out = []
    out.append(f"table {nm(t['name'])}")
    if t.get("dataCategory"):
        out.append(f"{TAB}dataCategory: {t['dataCategory']}")
    out.append("")

    # Calculated tables: do NOT declare columns. Power BI infers them from the
    # DAX expression. Declaring sourceColumn: [Category] makes the parser try
    # to resolve [Category] as a DAX name outside any row context and fail.
    is_calc_table = t["partitions"][0]["source"]["type"] == "calculated"

    if not is_calc_table:
        for c in t.get("columns", []):
            if is_deferred(c):
                if not include_deferred:
                    DEFERRED.append((t["name"], c))
                    continue
            emit_column(c, out)
    for m in t.get("measures", []):
        emit_measure(m, out)
    for h in t.get("hierarchies", []):
        emit_hierarchy(h, out)

    p = t["partitions"][0]
    src = p["source"]
    kind = "m" if src["type"] == "m" else "calculated"
    expr = src["expression"]
    if isinstance(expr, list):
        expr = "\n".join(expr)

    out.append(f"{TAB}partition {nm(p['name'])} = {kind}")
    out.append(f"{TAB*2}mode: {p.get('mode', 'import')}")
    if "\n" in expr.strip():
        out.append(f"{TAB*2}source = {FENCE}")
        out.append(block(expr, 4))
    else:
        out.append(f"{TAB*2}source = {expr.strip()}")
    out.append("")
    return "\n".join(out)


def emit_relationship(r):
    out = [f"relationship {nm(r['name'])}"]
    if not r.get("isActive", True):
        out.append(f"{TAB}isActive: false")
    out.append(f"{TAB}fromColumn: {nm(r['fromTable'])}.{nm(r['fromColumn'])}")
    out.append(f"{TAB}toColumn: {nm(r['toTable'])}.{nm(r['toColumn'])}")
    out.append("")
    return "\n".join(out)


def wrap(body):
    """
    TMDL rules learned from the parser:
      * '//' comments are NOT supported anywhere
      * exactly ONE createOrReplace per script
      * every object under createOrReplace must be indented one level
    So: shift the whole body one tab right and prefix a single command.
    """
    shifted = "\n".join(TAB + ln if ln.strip() else ""
                        for ln in body.split("\n"))
    return "createOrReplace\n\n" + shifted


m_tables = [t for t in tables
            if t["partitions"][0]["source"]["type"] == "m"]
c_tables = [t for t in tables
            if t["partitions"][0]["source"]["type"] == "calculated"]

body_tables = "\n".join(emit_table(t) for t in m_tables)
body_rels = "\n".join(emit_relationship(r) for r in rels)
body_calc = "\n".join(emit_table(t) for t in c_tables)

# Phase 4: re-emit each affected table IN FULL, now including its RELATED
# column. Must be complete, because createOrReplace replaces the whole table.
affected = sorted({tname for tname, _ in DEFERRED})
body_related = "\n".join(
    emit_table(next(t for t in m_tables if t["name"] == tname),
               include_deferred=True)
    for tname in affected)

# ---------------------------------------------------------------- phasing
# Anything whose DAX crosses a relationship (calculated tables using
# SUMMARIZE over the fact table, RELATED columns) must be applied in a
# SEPARATE Apply, after the relationships have been committed. Inside one
# createOrReplace the relationships do not exist yet, so the DAX fails to
# resolve names such as DimProduct[Category].
phase1 = wrap(body_tables + "\n" + body_rels)   # tables + relationships
phase2 = wrap(body_calc)                        # calculated tables
phase3 = wrap(body_related) if body_related.strip() else ""


def w(name, text):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return p


for old in ["01_tables.tmdl", "02_relationships.tmdl", "03_calc_tables.tmdl",
            "04_related_columns.tmdl", "ALL_IN_ONE.tmdl"]:
    q = os.path.join(OUT, old)
    if os.path.exists(q):
        os.remove(q)

p1 = w("PHASE1_tables_and_relationships.tmdl", phase1)
p2 = w("PHASE2_calculated_tables.tmdl", phase2)
p = p2
if phase3:
    p = w("PHASE3_related_column.tmdl", phase3)

n_meas = sum(len(t.get("measures", [])) for t in tables)
n_cc = sum(1 for t in tables for c in t.get("columns", [])
           if c.get("type") == "calculated")
n_h = sum(len(t.get("hierarchies", [])) for t in tables)

print("TMDL scripts written to", OUT)
print("APPLY THESE IN ORDER - each needs its own Apply click:")
print(f"  1. PHASE1_tables_and_relationships.tmdl  "
      f"{len(phase1.splitlines()):>4} lines")
print(f"  2. PHASE2_calculated_tables.tmdl         "
      f"{len(phase2.splitlines()):>4} lines")
if phase3:
    print(f"  3. PHASE3_related_column.tmdl            "
          f"{len(phase3.splitlines()):>4} lines")
print()
print(f"  tables        : {len(m_tables)} imported + {len(c_tables)} calculated")
print(f"  measures      : {n_meas}")
print(f"  calc columns  : {n_cc}")
print(f"  hierarchies   : {n_h}")
print(f"  relationships : {len(rels)} (1 inactive)")
