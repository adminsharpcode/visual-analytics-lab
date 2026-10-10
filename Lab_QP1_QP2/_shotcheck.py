"""Sanity-check a captured screenshot: size, contrast, and whether it looks
like a real UI capture rather than a blank or solid frame."""
import os
import sys
import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SHOT = os.path.join(BASE, "screenshots")

names = sys.argv[1:] or sorted(
    os.path.splitext(f)[0] for f in os.listdir(SHOT) if f.endswith(".png"))

for n in names:
    p = os.path.join(SHOT, f"{n}.png")
    if not os.path.exists(p):
        print(f"{n:<22} MISSING")
        continue
    im = Image.open(p).convert("RGB")
    a = np.asarray(im)
    uniq = len(np.unique(a.reshape(-1, 3), axis=0))
    std = a.std()
    kb = os.path.getsize(p) / 1024
    verdict = ("BLANK/SOLID - recapture" if std < 8 or uniq < 60
               else "ok - real UI content")
    print(f"{n:<22} {im.size[0]}x{im.size[1]}  {kb:6.0f} KB  "
          f"std={std:5.1f}  colours={uniq:>7,}  {verdict}")
