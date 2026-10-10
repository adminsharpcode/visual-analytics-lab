"""Rename the generic Windows screenshots to the step names the PDF builders
look for. Identification came from OCR of each image."""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(BASE, "screenshots")

# source file -> (target step name, why)
MAP = {
    "Screenshot 2026-08-30 210555.png": (
        "qp1_08_model_view",
        "Model view - all 7 tables listed in the Tables pane"),
    "Screenshot 2026-08-30 210606.png": (
        "qp1_10_properties",
        "Data view - DimCustomer (220 rows) with columns and properties"),
    "Screenshot 2026-08-30 210819.png": (
        "qp2_06_calc_table",
        "Top 5 Products calculated table with its inferred columns"),
    "Screenshot 2026-08-30 212228.png": (
        "qp2_10_report_p1",
        "Report Page 1 - Sales Overview with KPI cards and visuals"),
    "Screenshot 2026-08-30 212214.png": (
        "qp2_11_report_p2",
        "Report Page 2 - Category and Time Analysis with YoY matrix"),
}

done, missing = [], []
for src, (dest, why) in MAP.items():
    sp = os.path.join(S, src)
    dp = os.path.join(S, dest + ".png")
    if not os.path.exists(sp):
        missing.append(src)
        continue
    if os.path.exists(dp):
        os.remove(dp)
    shutil.move(sp, dp)
    done.append((dest, why, os.path.getsize(dp) / 1024))

print("Renamed:")
for d, why, kb in done:
    print(f"  {d + '.png':<28} {kb:>5.0f} KB   {why}")
if missing:
    print("\nNot found:", missing)

print("\nCurrent screenshot inventory")
print("-" * 70)
have = sorted(f[:-4] for f in os.listdir(S) if f.endswith(".png"))
q1 = [h for h in have if h.startswith("qp1_")]
q2 = [h for h in have if h.startswith("qp2_")]
other = [h for h in have if not h.startswith(("qp1_", "qp2_"))]
print(f"QP1 ({len(q1)}/12): " + ", ".join(q1))
print(f"QP2 ({len(q2)}/14): " + ", ".join(q2))
if other:
    print(f"Unclassified: {other}")
