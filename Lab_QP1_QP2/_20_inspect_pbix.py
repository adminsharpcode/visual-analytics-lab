"""Inspect Visual1.pbix: parts, encodings, and the Report/Layout schema."""
import json
import os
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "Visual1.pbix")

z = zipfile.ZipFile(P)
print("Parts inside Visual1.pbix")
print("-" * 66)
for i in z.infolist():
    print(f"  {i.filename:<40} {i.file_size:>10,} B")

name = "Report/Layout"
if name not in z.namelist():
    print("\nNo Report/Layout part found.")
    raise SystemExit(0)

raw = z.read(name)
if raw.startswith(b"\xff\xfe"):
    enc, bom = "utf-16-le", 2
elif raw.startswith(b"\xef\xbb\xbf"):
    enc, bom = "utf-8", 3
else:
    enc, bom = ("utf-16-le", 0) if raw[:100].count(b"\x00") > 20 else ("utf-8", 0)

print(f"\nReport/Layout encoding: {enc}, BOM bytes={bom}")
lay = json.loads(raw[bom:].decode(enc))

print("\nTop-level keys:", sorted(lay.keys()))
cfg = lay.get("config")
if isinstance(cfg, str):
    try:
        c = json.loads(cfg)
        print("config.version:", c.get("version"))
        print("config keys   :", sorted(c.keys()))
    except Exception as e:
        print("config parse:", e)

print(f"\nSections: {len(lay.get('sections', []))}")
for s in lay.get("sections", []):
    vcs = s.get("visualContainers", [])
    print(f"  name={s.get('name')!r} display={s.get('displayName')!r} "
          f"{s.get('width')}x{s.get('height')} visuals={len(vcs)}")
    for vc in vcs:
        try:
            cj = json.loads(vc.get("config", "{}"))
            vt = (cj.get("singleVisual", {}) or {}).get("visualType")
            print(f"      visual: type={vt} x={vc.get('x')} y={vc.get('y')} "
                  f"w={vc.get('width')} h={vc.get('height')}")
            print(f"      config keys: {sorted(cj.keys())}")
            sv = cj.get("singleVisual", {})
            print(f"      singleVisual keys: {sorted(sv.keys())}")
            proj = sv.get("projections")
            if proj:
                print(f"      projections: {json.dumps(proj)[:300]}")
            pq = vc.get("query")
            if pq:
                print(f"      query: {str(pq)[:300]}")
            df = vc.get("dataTransforms")
            if df:
                print(f"      dataTransforms: {str(df)[:300]}")
        except Exception as e:
            print("      (config parse failed)", e)

# dump the full layout for reference
out = os.path.join(BASE, "_layout_dump.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(lay, f, indent=2, ensure_ascii=False)
print("\nfull layout ->", os.path.basename(out))
