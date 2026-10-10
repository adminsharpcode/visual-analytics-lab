"""
Shared rendering library for Visual Analytics Lab Assessments 3 to 8.
Author: Vedant Nimkar | Reg No: 26MML0045 | Subject: MACSE603
"""

import base64
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import time
import uuid
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(BASE, "figures")
SHOT = os.path.join(BASE, "screenshots")

AUTHOR = "Vedant Nimkar"
REG = "26MML0045"
SUBJECT = "Visual Analytics Lab"
CODE_NO = "MACSE603"

EDGE = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

_fig_n = [0]
_shot_n = [0]


def reset_counters():
    _fig_n[0] = 0
    _shot_n[0] = 0


def fig(name, caption):
    """Embeds an analytical figure or diagram from figures/."""
    _fig_n[0] += 1
    if name.endswith(".png"): name = name[:-4]
    p1 = os.path.join(FIG, f"{name}.png")
    p2 = os.path.join(SHOT, f"{name}.png")
    p = p1 if os.path.exists(p1) else p2
    if os.path.exists(p) and os.path.getsize(p) > 2000:
        return (f'\n<figure>\n<img src="{os.path.relpath(p, BASE).replace(chr(92), "/")}" alt="fig">\n'
                f'<figcaption><b>Figure {_fig_n[0]}.</b> {caption}</figcaption>\n'
                f'</figure>\n')
    return (f'\n<div class="shot"><div class="shot-t">[FIGURE: {name}]</div>'
            f'<div class="shot-b">{caption}</div></div>\n')


def shot(name, caption):
    """Embeds a captured screenshot from screenshots/ or falls back to figures/."""
    _shot_n[0] += 1
    if name.endswith(".png"): name = name[:-4]
    p1 = os.path.join(SHOT, f"{name}.png")
    p2 = os.path.join(FIG, f"{name}.png")
    p = p1 if os.path.exists(p1) and os.path.getsize(p1) > 2000 else (p2 if os.path.exists(p2) and os.path.getsize(p2) > 2000 else None)
    if p:
        rel = os.path.relpath(p, BASE).replace(chr(92), "/")
        return (f'\n<figure class="sc">\n'
                f'<img src="{rel}" alt="screenshot">\n'
                f'<figcaption><b>Screenshot {_shot_n[0]}.</b> {caption}</figcaption>\n'
                f'</figure>\n')
    return (f'\n<div class="shot">\n'
            f'<div class="shot-t">[SCREENSHOT SLOT &bull; {name}.png]</div>\n'
            f'<div class="shot-b">{caption}</div>\n'
            f'<div class="shot-c">Capture with: <code>.\\capture_qp3_to_qp8.ps1 -Step {name}</code></div>\n'
            f'</div>\n')


CSS = """
<style>
  @page { size: A4; margin: 15mm 14mm 14mm 14mm; }
  body { font-family: "Segoe UI", Calibri, Arial, sans-serif; color: #1c1c1c;
         font-size: 9.8pt; line-height: 1.5; }
  .cover { page-break-after: always; height: 95vh; position: relative;
           display: flex; flex-direction: column; justify-content: center;
           align-items: center; text-align: center; }
  .cover .bt { position: absolute; top: 0; left: -14mm; right: -14mm; height: 11mm;
      background: linear-gradient(90deg, #10245c, #3366cc 60%, #6fa3ff); }
  .cover .bb { position: absolute; bottom: 0; left: -14mm; right: -14mm;
      height: 7mm; background: linear-gradient(90deg, #6fa3ff, #3366cc 60%, #10245c); }
  .cover .k { color: #3366cc; font-size: 12pt; letter-spacing: 2px;
      text-transform: uppercase; font-weight: 600; margin-bottom: 14px; }
  .cover .asmt { display: inline-block; background: #10245c; color: #fff;
      font-size: 11.5pt; font-weight: 700; letter-spacing: 1px; padding: 6px 22px;
      border-radius: 16px; margin-bottom: 22px; }
  .cover h1 { font-size: 28pt; color: #10245c; border: none; margin: 0 0 8px;
      page-break-before: auto; }
  .cover .st { font-size: 13.5pt; color: #334155; font-weight: 500; margin: 0 0 10px;
      max-width: 160mm; }
  .cover .who { font-size: 16pt; font-weight: 700; color: #10245c; margin-top: 32px; }
  .cover .reg { font-size: 12.5pt; color: #555; margin-top: 5px; }
  .cover .sub { font-size: 11pt; color: #666; margin-top: 22px; }
  .cover .tools { margin-top: 22px; font-size: 9.5pt; color: #22336b; font-weight: 500; }
  h1 { font-size: 16pt; color: #10245c; border-bottom: 3px solid #3366cc;
       padding-bottom: 5px; margin: 0 0 12px; page-break-before: always; }
  h2 { font-size: 12.5pt; color: #10245c; border-bottom: 1px solid #c8d4ee;
       padding-bottom: 3px; margin-top: 18px; page-break-after: avoid; }
  h3 { font-size: 10.8pt; color: #22336b; margin-top: 13px; page-break-after: avoid; }
  .meta { background: #f3f7ff; border: 1px solid #c8d4ee; border-left: 4px solid #3366cc;
          padding: 9px 13px; font-size: 9.6pt; border-radius: 4px; margin-bottom: 15px; }
  .note { background: #fdf8ec; border-left: 4px solid #e0a020; padding: 9px 13px;
          font-size: 9pt; margin-top: 12px; border-radius: 4px; }
  .ok { background: #eef8f1; border-left: 4px solid #1e7a4f; padding: 9px 13px;
        font-size: 9pt; margin-top: 12px; border-radius: 4px; }
  table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 8.8pt;
          page-break-inside: avoid; }
  th, td { border: 1px solid #b8c4dc; padding: 5px 8px; text-align: left; vertical-align: top; }
  th { background: #eaf0fb; color: #10245c; font-weight: 600; }
  code { background: #f1f3f7; padding: 1px 4px; border-radius: 3px;
         font-family: Consolas, monospace; font-size: 8.5pt; color: #b03060; }
  pre { background: #0f172a; border-left: 3px solid #3366cc; padding: 10px 14px;
        border-radius: 5px; page-break-inside: avoid; white-space: pre-wrap; word-wrap: break-word; }
  pre code { background: none; padding: 0; color: #e2e8f0; font-size: 8pt; line-height: 1.45; }
  figure { margin: 12px 0; page-break-inside: avoid; text-align: center; }
  figure img { max-width: 98%; border: 1px solid #dfe4ee; border-radius: 6px; padding: 4px; background: #fff; }
  figure.sc img { border: 2px solid #3366cc; padding: 2px; max-width: 99%; }
  figcaption { font-size: 8.5pt; color: #555; margin-top: 5px; text-align: left; }
  .shot { border: 2px dashed #9fb3d9; background: #f8faff; border-radius: 6px;
          padding: 15px; text-align: center; margin: 12px 0; page-break-inside: avoid; }
  .shot-t { font-size: 8.8pt; font-weight: 700; color: #3366cc; letter-spacing: 1px; }
  .shot-b { font-size: 9pt; color: #475569; margin-top: 5px; }
  .shot-c { font-size: 8pt; color: #64748b; margin-top: 6px; }
  hr { border: none; border-top: 1px solid #d5dbe8; margin: 18px 0 15px; }
  strong { color: #0d1b3e; }
  ul, ol { padding-left: 20px; }
  li { margin: 2px 0; }
</style>
"""


def cover(assessment, title, subtitle, tools_str):
    return f"""
<div class="cover">
  <div class="bt"></div>
  <div class="k">{CODE_NO} &mdash; Laboratory Record</div>
  <div class="asmt">{assessment}</div>
  <h1>{SUBJECT}</h1>
  <div class="st">{title}</div>
  <div style="width:90px;height:3px;background:#3366cc;margin:16px auto;"></div>
  <div class="st" style="font-size:11pt;color:#666;">{subtitle}</div>
  <div class="who">{AUTHOR}</div>
  <div class="reg">Registration No.: {REG}</div>
  <div class="sub">M.Tech &mdash; Computer Science and Engineering</div>
  <div class="tools">{tools_str}</div>
  <div class="bb"></div>
</div>
"""


def _embed(html):
    def rep(m):
        pre, src, post = m.group(1), m.group(2), m.group(3)
        p = os.path.normpath(os.path.join(BASE, src))
        if not os.path.exists(p):
            return m.group(0)
        mime = mimetypes.guess_type(p)[0] or "image/png"
        with open(p, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        return f'{pre}data:{mime};base64,{b64}{post}'
    return re.sub(r'(<img[^>]*src=")([^"]+)("[^>]*>)', rep, html)


def render(md_text, cover_html, out_stem):
    """Converts Markdown -> HTML -> base64 embedded images -> PDF via Edge."""
    md_path = os.path.join(BASE, f"{out_stem}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    body = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "sane_lists", "md_in_html", "attr_list"])
    body = _embed(body)
    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{out_stem}</title>{CSS}</head><body>{cover_html}{body}</body></html>"

    tmp = os.path.join(BASE, f"_t_{uuid.uuid4().hex[:8]}.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    edge = next((e for e in EDGE if os.path.exists(e)), None)
    if not edge:
        print("Edge not found.")
        return None

    for suffix in ["", "_ready", "_v2"]:
        pdf = os.path.join(BASE, f"{out_stem}{suffix}.pdf")
        if os.path.exists(pdf):
            try:
                os.remove(pdf)
            except PermissionError:
                print(f"   {os.path.basename(pdf)} is open in viewer, trying next name...")
                continue
        prof = tempfile.mkdtemp(prefix="edgepdf_")
        try:
            subprocess.run([edge, "--headless=new", "--disable-gpu",
                            "--no-first-run", "--no-pdf-header-footer",
                            f"--user-data-dir={prof}",
                            f"--print-to-pdf={pdf}", tmp],
                           capture_output=True, text=True, timeout=120)
        finally:
            time.sleep(0.3)
            shutil.rmtree(prof, ignore_errors=True)

        if os.path.exists(pdf) and os.path.getsize(pdf) > 2000:
            if os.path.exists(tmp): os.remove(tmp)
            print(f"Generated PDF: {os.path.basename(pdf)} ({os.path.getsize(pdf)/1024:.0f} KB)")
            return pdf

    if os.path.exists(tmp): os.remove(tmp)
    return None
