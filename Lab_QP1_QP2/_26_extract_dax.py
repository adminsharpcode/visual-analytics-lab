"""
Extracts every DAX object from the APPLIED model in the PBIP project and
writes code/APPLIED_DAX.md - so the record shows the real code, not a
hand-maintained copy.

Reads: Visual1.SemanticModel/definition/tables/*.tmdl
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
TDIR = os.path.join(BASE, "Visual1.SemanticModel", "definition", "tables")
RELF = os.path.join(BASE, "Visual1.SemanticModel", "definition",
                    "relationships.tmdl")
OUT = os.path.join(BASE, "code", "APPLIED_DAX.md")

if not os.path.isdir(TDIR):
    raise SystemExit(f"project model folder not found: {TDIR}")


def dedent_block(lines):
    """Strip the common leading tabs from a captured expression block."""
    real = [l for l in lines if l.strip()]
    if not real:
        return ""
    pad = min(len(l) - len(l.lstrip("\t")) for l in real)
    return "\n".join(l[pad:] if l.strip() else "" for l in lines).rstrip()


def indent_of(line):
    return len(line) - len(line.lstrip("\t"))


def read_expr(lines, i, tail, decl_indent):
    """
    Read an expression that follows '<decl> = <tail>'.

    Power BI writes multi-line expressions UNFENCED, delimited purely by
    indentation: the body sits deeper than the object's property lines.
    Fenced (```) blocks are also accepted since that is valid TMDL too.

    Returns (expression, index_of_last_consumed_line).
    """
    tail = tail.strip()

    if tail == "```":                       # fenced block
        body, i = [], i + 1
        while i < len(lines) and lines[i].strip() != "```":
            body.append(lines[i])
            i += 1
        return dedent_block(body), i

    if tail:                                # single line, inline
        return tail, i

    # unfenced: body is any line indented deeper than a property line
    body, j = [], i + 1
    while j < len(lines):
        ln = lines[j]
        if not ln.strip():
            body.append(ln)
            j += 1
            continue
        if indent_of(ln) <= decl_indent + 1:
            break
        body.append(ln)
        j += 1
    return dedent_block(body), j - 1


def parse(path):
    """Return (table_name, dataCategory, calc_cols, measures, calc_partition)."""
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")

    m = re.search(r"^table\s+'?([^'\n]+?)'?\s*$", txt, re.M)
    tname = m.group(1) if m else os.path.splitext(os.path.basename(path))[0]
    dc = re.search(r"^\tdataCategory:\s*(\S+)", txt, re.M)

    calc_cols, measures = [], []
    calc_src = None
    i = 0
    while i < len(lines):
        ln = lines[i]

        # calculated column / measure, fenced or inline
        m = re.match(r"^\t(column|measure)\s+'?([^'=\n]+?)'?\s*=\s*(.*)$", ln)
        if m:
            kind, name, tail = m.group(1), m.group(2).strip(), m.group(3)
            expr, i = read_expr(lines, i, tail, indent_of(ln))
            fmt = None
            for k in range(i + 1, min(i + 8, len(lines))):
                if indent_of(lines[k]) != indent_of(ln) + 1:
                    if lines[k].strip():
                        break
                    continue
                fm = re.match(r"^\t+formatString:\s*(.+)$", lines[k])
                if fm:
                    fmt = fm.group(1).strip()
                    break
            rec = (name, expr, fmt)
            (calc_cols if kind == "column" else measures).append(rec)

        # calculated table partition
        if re.match(r"^\tpartition\s+.*=\s*calculated\s*$", ln):
            k = i + 1
            while k < len(lines) and not re.match(r"^\t+source\s*=",
                                                  lines[k]):
                k += 1
            if k < len(lines):
                sm = re.match(r"^(\t+)source\s*=\s*(.*)$", lines[k])
                calc_src, _ = read_expr(lines, k, sm.group(2),
                                        len(sm.group(1)))
        i += 1

    return tname, (dc.group(1) if dc else None), calc_cols, measures, calc_src


tabs = []
for fn in sorted(os.listdir(TDIR)):
    if fn.endswith(".tmdl"):
        tabs.append(parse(os.path.join(TDIR, fn)))

# group measures by display folder for readability
def folder_of(txt, name):
    m = re.search(r"measure\s+'?" + re.escape(name)
                  + r"'?\s*=(?:.|\n)*?displayFolder:\s*(.+)", txt)
    return m.group(1).strip() if m else ""


M = []
A = M.append

A("# Applied DAX — extracted from the semantic model")
A("")
A("Every expression below was read directly out of the applied model "
  "(`Visual1.SemanticModel/definition/tables/*.tmdl`), so it is the code "
  "actually running in the report — not a separately maintained listing.")
A("")

n_cc = sum(len(t[2]) for t in tabs)
n_m = sum(len(t[3]) for t in tabs)
n_ct = sum(1 for t in tabs if t[4])

A("| Object type | Count |")
A("|---|---|")
A(f"| Tables | {len(tabs)} |")
A(f"| Calculated columns | {n_cc} |")
A(f"| Measures | {n_m} |")
A(f"| Calculated tables | {n_ct} |")
A("")

# ---------------- calculated columns ----------------
A("## Calculated columns")
A("")
for tname, dc, cc, ms, cs in tabs:
    if not cc:
        continue
    A(f"### {tname}")
    A("")
    A("```dax")
    for name, expr, fmt in cc:
        A(f"{name} =")
        for ln in expr.split("\n"):
            A("    " + ln if ln.strip() else "")
        A("")
    A("```")
    A("")

# ---------------- measures ----------------
A("## Measures")
A("")
for tname, dc, cc, ms, cs in tabs:
    if not ms:
        continue
    txt = open(os.path.join(TDIR, tname + ".tmdl"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(TDIR, tname + ".tmdl")) else ""
    groups = {}
    for name, expr, fmt in ms:
        groups.setdefault(folder_of(txt, name) or "General", []).append(
            (name, expr, fmt))
    for g in sorted(groups):
        A(f"### {g}")
        A("")
        A("```dax")
        for name, expr, fmt in groups[g]:
            A(f"{name} =")
            for ln in expr.split("\n"):
                A("    " + ln if ln.strip() else "")
            A("")
        A("```")
        A("")

# ---------------- calculated tables ----------------
A("## Calculated tables")
A("")
for tname, dc, cc, ms, cs in tabs:
    if not cs:
        continue
    A(f"### {tname}")
    A("")
    A("```dax")
    A(f"{tname} =")
    for ln in cs.split("\n"):
        A("    " + ln if ln.strip() else "")
    A("```")
    A("")

# ---------------- relationships ----------------
if os.path.exists(RELF):
    rt = open(RELF, encoding="utf-8").read()
    rels = re.findall(
        r"relationship\s+(\S+)((?:\n\t.*)+)", rt)
    A("## Relationships")
    A("")
    A("| Name | From | To | Active |")
    A("|---|---|---|---|")
    for name, body in rels:
        fc = re.search(r"fromColumn:\s*(\S+)", body)
        tc = re.search(r"toColumn:\s*(\S+)", body)
        act = "No" if "isActive: false" in body else "Yes"
        A(f"| `{name}` | `{fc.group(1) if fc else '?'}` | "
          f"`{tc.group(1) if tc else '?'}` | {act} |")
    A("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(M))

print(f"wrote {os.path.relpath(OUT, BASE)}")
print(f"  tables            : {len(tabs)}")
print(f"  calculated columns: {n_cc}")
print(f"  measures          : {n_m}")
print(f"  calculated tables : {n_ct}")
for tname, dc, cc, ms, cs in tabs:
    flag = "  [date table]" if dc == "Time" else ""
    print(f"    {tname:<26} cols={len(cc)} meas={len(ms)} "
          f"calc={'yes' if cs else 'no'}{flag}")
