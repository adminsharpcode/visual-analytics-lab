"""
Writes code/ready_to_paste/*.m with <PATH> replaced by the real data folder,
so each query can be pasted straight into the Advanced Editor.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
SRC = os.path.join(BASE, "code", "Step2_PowerQuery_M.txt")
OUT = os.path.join(BASE, "code", "ready_to_paste")
os.makedirs(OUT, exist_ok=True)

text = open(SRC, encoding="utf-8").read().replace("<PATH>", DATA)

# each query block starts at a "QUERY n : Name" header
blocks = re.split(r"-{50,}\nQUERY \d+ : (\w+)", text)
# blocks = [preamble, name1, body1, name2, body2, ...]
written = []
for i in range(1, len(blocks) - 1, 2):
    name = blocks[i].strip()
    body = blocks[i + 1]
    m = re.search(r"^let\b.*?\n(?:.*\n)*?^in\s*\n\s*\S+", body,
                  re.M)
    if not m:
        continue
    q = m.group(0).rstrip()
    p = os.path.join(OUT, f"{name}.m")
    with open(p, "w", encoding="utf-8") as f:
        f.write(q + "\n")
    written.append((name, len(q.splitlines())))

print("ready-to-paste M queries ->", OUT)
for n, ln in written:
    print(f"  {n}.m  ({ln} lines)")
