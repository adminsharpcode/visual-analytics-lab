"""Dump the PBIR definition JSONs from Visual1.pbix so we learn the schema."""
import json
import os
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "Visual1.pbix")
OUTDIR = os.path.join(BASE, "_pbir_seed")
os.makedirs(OUTDIR, exist_ok=True)

z = zipfile.ZipFile(P)
for n in z.namelist():
    if not n.startswith("Report/definition/"):
        continue
    raw = z.read(n)
    bom = 0
    enc = "utf-8"
    if raw.startswith(b"\xef\xbb\xbf"):
        bom = 3
    elif raw.startswith(b"\xff\xfe"):
        bom, enc = 2, "utf-16-le"
    text = raw[bom:].decode(enc)
    print("=" * 74)
    print(n, f"  ({len(raw)} B, {enc}, bom={bom})")
    print("=" * 74)
    print(text)
    print()
    # save a copy
    dest = os.path.join(OUTDIR, n.replace("Report/definition/", "")
                        .replace("/", "__"))
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)

print("copies saved to", OUTDIR)
