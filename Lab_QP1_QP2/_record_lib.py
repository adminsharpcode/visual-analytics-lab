"""
Shared rendering helpers for the QP1 and QP2 lab records.

Screenshots are auto-embedded when screenshots/<name>.png exists; otherwise a
dashed placeholder slot is rendered so the document is still complete.
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
CODE = os.path.join(BASE, "code")
FIG = os.path.join(BASE, "figures")
SHOT = os.path.join(BASE, "screenshots")
EXP = os.path.join(BASE, "expected_results")

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


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fig(name, caption):
    """Generated figure from the real dataset or a drawn diagram."""
    _fig_n[0] += 1
    return (f'\n<figure>\n<img src="figures/{name}" alt="fig">\n'
            f'<figcaption><b>Figure {_fig_n[0]}.</b> {caption}</figcaption>\n'
            f'</figure>\n')


def shot(name, caption):
    """
    Embed a real Power BI screenshot. If it was never captured, emit nothing -
    the record only claims what actually exists.
    """
    path = os.path.join(SHOT, f"{name}.png")
    if not (os.path.exists(path) and os.path.getsize(path) > 2000):
        return ""
    _shot_n[0] += 1
    return (f'\n<figure class="sc">\n'
            f'<img src="screenshots/{name}.png" alt="screenshot">\n'
            f'<figcaption><b>Screenshot {_shot_n[0]}.</b> {caption}'
            f'</figcaption>\n</figure>\n')


def shot_status(prefix):
    """Return (captured, total) for a qp1_/qp2_ prefix."""
    import glob
    have = glob.glob(os.path.join(SHOT, f"{prefix}*.png"))
    return len(have)


CSS = """
<style>
  @page { size: A4; margin: 16mm 14mm 14mm 14mm; }
  body { font-family:"Segoe UI",Calibri,Arial,sans-serif; color:#1c1c1c;
         font-size:10pt; line-height:1.5; }
  .cover { page-break-after:always; height:96vh; position:relative;
           display:flex; flex-direction:column; justify-content:center;
           align-items:center; text-align:center; }
  .cover .bt { position:absolute; top:0; left:-14mm; right:-14mm; height:11mm;
     background:linear-gradient(90deg,#10245c,#3366cc 60%,#6fa3ff); }
  .cover .bb { position:absolute; bottom:0; left:-14mm; right:-14mm;
     height:7mm; background:linear-gradient(90deg,#6fa3ff,#3366cc 60%,#10245c); }
  .cover .k { color:#3366cc; font-size:12pt; letter-spacing:2px;
     text-transform:uppercase; font-weight:600; margin-bottom:14px; }
  .cover .asmt { display:inline-block; background:#10245c; color:#fff;
     font-size:11pt; font-weight:700; letter-spacing:1px; padding:6px 20px;
     border-radius:16px; margin-bottom:22px; }
  .cover h1 { font-size:30pt; color:#10245c; border:none; margin:0 0 8px;
     page-break-before:auto; }
  .cover .st { font-size:14pt; color:#444; font-weight:500; margin:0 0 10px;
     max-width:150mm; }
  .cover .who { font-size:16pt; font-weight:700; color:#10245c;
     margin-top:30px; }
  .cover .reg { font-size:12.5pt; color:#555; margin-top:5px; }
  .cover .sub { font-size:11pt; color:#666; margin-top:24px; }
  .cover .tools { margin-top:20px; font-size:9.5pt; color:#22336b; }
  h1 { font-size:16.5pt; color:#10245c; border-bottom:3px solid #3366cc;
       padding-bottom:5px; margin:0 0 12px; page-break-before:always; }
  h2 { font-size:12.5pt; color:#10245c; border-bottom:1px solid #c8d4ee;
       padding-bottom:3px; margin-top:19px; page-break-after:avoid; }
  h3 { font-size:10.8pt; color:#22336b; margin-top:13px;
       page-break-after:avoid; }
  .meta { background:#f3f7ff; border:1px solid #c8d4ee;
       border-left:4px solid #3366cc; padding:9px 13px; font-size:9.6pt;
       border-radius:4px; }
  .note { background:#fdf8ec; border-left:4px solid #e0a020; padding:9px 13px;
       font-size:9pt; margin-top:13px; border-radius:4px; }
  .ok { background:#eef8f1; border-left:4px solid #1e7a4f; padding:9px 13px;
       font-size:9pt; margin-top:13px; border-radius:4px; }
  table { border-collapse:collapse; width:100%; margin:8px 0; font-size:8.7pt;
       page-break-inside:avoid; }
  th,td { border:1px solid #b8c4dc; padding:4px 7px; text-align:left;
       vertical-align:top; }
  th { background:#eaf0fb; color:#10245c; }
  code { background:#f1f3f7; padding:1px 3px; border-radius:3px;
       font-family:Consolas,monospace; font-size:8.5pt; color:#b03060; }
  pre { background:#1e2430; border-left:3px solid #3366cc; padding:9px 12px;
       border-radius:5px; page-break-inside:avoid; white-space:pre-wrap;
       word-wrap:break-word; }
  pre code { background:none; padding:0; color:#d8dee9; font-size:7.9pt;
       line-height:1.44; }
  figure { margin:11px 0; page-break-inside:avoid; text-align:center; }
  figure img { max-width:97%; border:1px solid #dfe4ee; border-radius:5px;
       padding:4px; background:#fff; }
  figure.sc img { border:2px solid #3366cc; padding:2px; max-width:99%; }
  figcaption { font-size:8.5pt; color:#555; margin-top:5px;
       text-align:left; }
  .shot { border:2px dashed #9fb3d9; background:#f8faff; border-radius:6px;
       padding:15px; text-align:center; margin:11px 0;
       page-break-inside:avoid; }
  .shot-t { font-size:8.8pt; font-weight:700; color:#3366cc;
       letter-spacing:1px; }
  .shot-b { font-size:9pt; color:#555; margin-top:5px; }
  .shot-c { font-size:8pt; color:#888; margin-top:6px; }
  hr { border:none; border-top:1px solid #d5dbe8; margin:18px 0 15px; }
  strong { color:#0d1b3e; }
  ul,ol { padding-left:20px; }
  li { margin:2px 0; }
  blockquote { border-left:4px solid #6fa3ff; background:#f5f9ff;
       margin:9px 0; padding:7px 13px; font-size:9.3pt; }
</style>
"""


def cover(assessment, title, subtitle):
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
  <div class="tools">Power BI Desktop &nbsp;&middot;&nbsp; SQL Server
     &nbsp;&middot;&nbsp; Power Query (M) &nbsp;&middot;&nbsp; DAX
     &nbsp;&middot;&nbsp; Python</div>
  <div class="bb"></div>
</div>
"""


def _embed(html):
    def rep(m):
        pre, src, post = m.group(1), m.group(2), m.group(3)
        p = os.path.normpath(os.path.join(BASE, src))
        if not os.path.exists(p):
            print("   missing image:", src)
            return m.group(0)
        mime = mimetypes.guess_type(p)[0] or "image/png"
        with open(p, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        return f'{pre}data:{mime};base64,{b64}{post}'
    return re.sub(r'(<img[^>]*src=")([^"]+)("[^>]*>)', rep, html)


def render(md_text, cover_html, out_stem):
    """Markdown -> styled HTML -> PDF via Edge headless."""
    md_path = os.path.join(BASE, f"{out_stem}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    body = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "sane_lists",
                             "md_in_html", "attr_list"])
    body = _embed(body)
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>{out_stem}</title>{CSS}</head><body>"
            f"{cover_html}{body}</body></html>")

    tmp = os.path.join(BASE, f"_t_{uuid.uuid4().hex[:8]}.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    edge = next((e for e in EDGE if os.path.exists(e)), None)
    if not edge:
        print("Edge not found. HTML at", tmp)
        return None

    for suffix in ["", "_v2", "_v3"]:
        pdf = os.path.join(BASE, f"{out_stem}{suffix}.pdf")
        if os.path.exists(pdf):
            try:
                os.remove(pdf)
            except PermissionError:
                print(f"   {os.path.basename(pdf)} is open, trying next name")
                continue
        prof = tempfile.mkdtemp(prefix="edgepdf_")
        try:
            subprocess.run([edge, "--headless=new", "--disable-gpu",
                            "--no-first-run", "--no-pdf-header-footer",
                            f"--user-data-dir={prof}",
                            f"--print-to-pdf={pdf}", tmp],
                           capture_output=True, text=True, timeout=300)
        finally:
            time.sleep(0.4)
            shutil.rmtree(prof, ignore_errors=True)
        if os.path.exists(pdf) and os.path.getsize(pdf) > 2000:
            os.remove(tmp)
            print(f"   PDF -> {os.path.basename(pdf)} "
                  f"({os.path.getsize(pdf)/1024:.0f} KB)")
            return pdf
    print("   PDF failed. HTML at", tmp)
    return None
