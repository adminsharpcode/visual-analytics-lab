"""
Extracts the APPLIED Power Query (M) and model structure from the PBIP
project, for the QP1 record.

Writes:
  code/APPLIED_M.md      - the M expression of every imported table
  code/APPLIED_MODEL.md  - relationships, hierarchies, column properties
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(BASE, "Visual1.SemanticModel", "definition")
TDIR = os.path.join(MD, "tables")
RELF = os.path.join(MD, "relationships.tmdl")

if not os.path.isdir(TDIR):
    raise SystemExit(f"project model not found: {TDIR}")


def indent_of(l):
    return len(l) - len(l.lstrip("\t"))


def dedent(lines):
    real = [l for l in lines if l.strip()]
    if not real:
        return ""
    pad = min(indent_of(l) for l in real)
    return "\n".join(l[pad:] if l.strip() else "" for l in lines).rstrip()


def read_block(lines, i, tail, decl_indent):
    tail = tail.strip()
    if tail == "```":
        body, i = [], i + 1
        while i < len(lines) and lines[i].strip() != "```":
            body.append(lines[i])
            i += 1
        return dedent(body)
    if tail:
        return tail
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
    return dedent(body)


tables = []
for fn in sorted(os.listdir(TDIR)):
    if not fn.endswith(".tmdl"):
        continue
    lines = open(os.path.join(TDIR, fn), encoding="utf-8").read().split("\n")
    txt = "\n".join(lines)
    tm = re.search(r"^table\s+'?([^'\n]+?)'?\s*$", txt, re.M)
    tname = tm.group(1) if tm else fn[:-5]
    dc = re.search(r"^\tdataCategory:\s*(\S+)", txt, re.M)

    m_expr = None
    cols, hiers = [], []
    i = 0
    while i < len(lines):
        ln = lines[i]

        pm = re.match(r"^(\t+)partition\s+.*=\s*m\s*$", ln)
        if pm:
            k = i + 1
            while k < len(lines) and not re.match(r"^\t+source\s*=", lines[k]):
                k += 1
            if k < len(lines):
                sm = re.match(r"^(\t+)source\s*=\s*(.*)$", lines[k])
                m_expr = read_block(lines, k, sm.group(2), len(sm.group(1)))

        cm = re.match(r"^\tcolumn\s+'?([^'=\n]+?)'?\s*$", ln)
        if cm:
            name = cm.group(1).strip()
            props = {}
            j = i + 1
            while j < len(lines) and (not lines[j].strip()
                                      or indent_of(lines[j]) >= 2):
                pm2 = re.match(r"^\t\t(\w+):\s*(.+)$", lines[j])
                if pm2:
                    props[pm2.group(1)] = pm2.group(2).strip()
                elif re.match(r"^\t\t(isHidden|isKey)\s*$", lines[j]):
                    props[lines[j].strip()] = "true"
                elif lines[j].strip() and indent_of(lines[j]) < 2:
                    break
                j += 1
                if j < len(lines) and lines[j].strip() and \
                        indent_of(lines[j]) < 2:
                    break
            cols.append((name, props))

        hm = re.match(r"^\thierarchy\s+'?([^'\n]+?)'?\s*$", ln)
        if hm:
            hname = hm.group(1).strip()
            levels = []
            j = i + 1
            while j < len(lines):
                if lines[j].strip() and indent_of(lines[j]) < 2:
                    break
                lv = re.match(r"^\t\tlevel\s+'?([^'\n]+?)'?\s*$", lines[j])
                if lv:
                    levels.append(lv.group(1).strip())
                j += 1
            hiers.append((hname, levels))
        i += 1

    tables.append({"name": tname, "m": m_expr, "cols": cols,
                   "hiers": hiers, "date": dc.group(1) if dc else None})

# ============================================================ APPLIED_M.md
M = []
A = M.append
A("# Applied Power Query (M) — extracted from the semantic model")
A("")
A("Each expression below is the actual `partition ... = m` source stored in "
  "the applied model, so it is the transformation logic really executing on "
  "refresh.")
A("")
imported = [t for t in tables if t["m"]]
A(f"{len(imported)} imported tables.")
A("")
for t in imported:
    A(f"## {t['name']}")
    A("")
    A("```")
    A(t["m"])
    A("```")
    A("")

with open(os.path.join(BASE, "code", "APPLIED_M.md"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(M))

# ======================================================= APPLIED_MODEL.md
S = []
B = S.append
B("# Applied model structure — extracted from the semantic model")
B("")

# relationships
if os.path.exists(RELF):
    rt = open(RELF, encoding="utf-8").read()
    rels = re.findall(r"relationship\s+(\S+)((?:\n\t.*)+)", rt)
    B("## Relationships")
    B("")
    B("| Name | From (many) | To (one) | Active |")
    B("|---|---|---|---|")
    for name, body in rels:
        fc = re.search(r"fromColumn:\s*(\S+)", body)
        tc = re.search(r"toColumn:\s*(\S+)", body)
        act = "**No**" if "isActive: false" in body else "Yes"
        B(f"| `{name}` | `{fc.group(1) if fc else '?'}` | "
          f"`{tc.group(1) if tc else '?'}` | {act} |")
    B("")
    B(f"{len(rels)} relationships, "
      f"{sum(1 for _, b in rels if 'isActive: false' in b)} inactive.")
    B("")

# date table
dt = [t["name"] for t in tables if t["date"] == "Time"]
if dt:
    B("## Date table")
    B("")
    B(f"`{dt[0]}` carries `dataCategory: Time`, confirming it is marked as "
      f"the model date table. This is required for the Time Intelligence "
      f"functions used in Assessment 2.")
    B("")

# hierarchies
B("## Hierarchies")
B("")
B("| Table | Hierarchy | Levels |")
B("|---|---|---|")
for t in tables:
    for hname, levels in t["hiers"]:
        B(f"| `{t['name']}` | {hname} | {' → '.join(levels)} |")
B("")

# column properties of interest
B("## Column properties")
B("")
B("Only the properties configured in Step 3 are listed: hidden surrogate "
  "keys, formatting, summarisation and sort-by-column.")
B("")
for t in tables:
    rows = []
    for name, p in t["cols"]:
        hid = "Yes" if "isHidden" in p else ""
        fmt = p.get("formatString", "")
        summ = p.get("summarizeBy", "")
        sort = p.get("sortByColumn", "")
        if hid or fmt or sort or (summ and summ != "none"):
            rows.append((name, p.get("dataType", ""), fmt, summ, hid, sort))
    if not rows:
        continue
    B(f"### {t['name']}")
    B("")
    B("| Column | Type | Format | Summarise | Hidden | Sort by |")
    B("|---|---|---|---|---|---|")
    for name, dtp, fmt, summ, hid, sort in rows:
        B(f"| `{name}` | {dtp} | {fmt} | {summ} | {hid} | {sort} |")
    B("")

with open(os.path.join(BASE, "code", "APPLIED_MODEL.md"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(S))

print("wrote code/APPLIED_M.md and code/APPLIED_MODEL.md")
print(f"  imported tables with M : {len(imported)}")
for t in imported:
    print(f"    {t['name']:<26} {len(t['m'].splitlines()):>3} lines of M")
print(f"  hierarchies            : "
      f"{sum(len(t['hiers']) for t in tables)}")
print(f"  date table             : {dt[0] if dt else 'NOT MARKED'}")
