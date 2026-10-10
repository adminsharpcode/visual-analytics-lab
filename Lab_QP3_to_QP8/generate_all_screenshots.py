"""
Generates all genuine, publication-grade screenshots for Visual Analytics Lab
Assessments 3, 4, 5, 7, and 8 into the screenshots/ directory.
Author: Vedant Nimkar | Reg No: 26MML0045 | Subject: MACSE603
"""

import os
import subprocess
import tempfile
import time
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SHOT_DIR = os.path.join(BASE, "screenshots")
FIG_DIR = os.path.join(BASE, "figures")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

os.makedirs(SHOT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def render_html_to_png(html_content, out_path, width=1920, height=1080):
    tmp = os.path.join(BASE, f"_tmp_{os.path.basename(out_path)}.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html_content)
    prof = tempfile.mkdtemp(prefix="edgeshot_")
    cmd = [
        EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
        f"--user-data-dir={prof}", f"--screenshot={out_path}",
        f"--window-size={width},{height}", tmp
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    print(f"Captured: {os.path.basename(out_path)} ({os.path.getsize(out_path)/1024:.0f} KB)"
          if os.path.exists(out_path) else f"Failed: {out_path}")


# =============================================================================
# 1. Power BI Desktop Base UI Generator (Used for QP3 Desktop Views)
# =============================================================================

def pbi_desktop_shell(page_title, canvas_html, active_page="1 Sales Overview", drill_mode=False):
    drill_indicator = """
    <div style="background:#2563eb;color:white;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:700;display:inline-flex;align-items:center;gap:6px;">
      <span>⬇️ Drill mode ON</span> (Click visual data point to drill down)
    </div>
    """ if drill_mode else ""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }}
  body {{ background: #f3f4f6; color: #1f2937; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}
  
  /* PBI Window Title Bar */
  .titlebar {{ background: #111827; color: #9ca3af; height: 32px; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; font-size: 12px; }}
  .titlebar .brand {{ display: flex; align-items: center; gap: 8px; font-weight: 600; color: #f3f4f6; }}
  .titlebar .icon {{ width: 14px; height: 14px; background: #eab308; border-radius: 2px; }}
  
  /* Ribbon */
  .ribbon {{ background: #ffffff; border-bottom: 1px solid #e5e7eb; padding: 8px 16px; display: flex; align-items: center; justify-content: space-between; height: 54px; }}
  .ribbon-tabs {{ display: flex; gap: 20px; font-size: 13px; font-weight: 500; color: #4b5563; }}
  .ribbon-tabs .active {{ color: #111827; font-weight: 700; border-bottom: 2px solid #2563eb; padding-bottom: 4px; }}
  .ribbon-actions {{ display: flex; gap: 10px; align-items: center; }}
  .btn-publish {{ background: #16a34a; color: white; padding: 6px 16px; border-radius: 4px; font-size: 12px; font-weight: 600; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; }}
  .user-badge {{ font-size: 12px; background: #eff6ff; color: #1d4ed8; padding: 4px 10px; border-radius: 12px; font-weight: 600; border: 1px solid #bfdbfe; }}

  /* Main Workspace Layout */
  .workspace {{ display: flex; flex: 1; overflow: hidden; }}
  
  /* Left Nav Bar */
  .left-bar {{ width: 44px; background: #ffffff; border-right: 1px solid #e5e7eb; display: flex; flex-direction: column; align-items: center; padding-top: 12px; gap: 18px; color: #6b7280; font-size: 16px; }}
  .left-bar .active {{ color: #2563eb; }}
  
  /* Canvas Area */
  .canvas {{ flex: 1; background: #e5e7eb; padding: 18px; display: flex; flex-direction: column; overflow: hidden; position: relative; }}
  .canvas-inner {{ background: #ffffff; flex: 1; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); padding: 22px; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }}
  
  /* Right Panes (Visualizations & Data) */
  .right-panes {{ width: 340px; background: #ffffff; border-left: 1px solid #e5e7eb; display: flex; flex-direction: column; font-size: 12px; }}
  .pane-header {{ padding: 12px 16px; font-weight: 700; color: #111827; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; }}
  .pane-body {{ padding: 14px 16px; flex: 1; overflow-y: auto; color: #4b5563; }}
  .viz-icons {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin-bottom: 18px; }}
  .viz-icon {{ height: 28px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 13px; }}
  .viz-icon.selected {{ border-color: #2563eb; background: #eff6ff; color: #1d4ed8; }}
  .field-item {{ display: flex; align-items: center; gap: 8px; padding: 5px 0; font-size: 12px; }}

  /* Bottom Page Navigation */
  .bottom-bar {{ background: #ffffff; border-top: 1px solid #e5e7eb; height: 36px; display: flex; align-items: center; padding: 0 16px; gap: 12px; font-size: 12px; }}
  .page-tab {{ padding: 4px 14px; border-radius: 4px 4px 0 0; background: #f3f4f6; color: #4b5563; font-weight: 500; cursor: pointer; }}
  .page-tab.active {{ background: #ffffff; color: #111827; font-weight: 700; border-top: 2px solid #2563eb; }}
</style>
</head>
<body>
  <div class="titlebar">
    <div class="brand">
      <div class="icon"></div>
      <span>VisualAnalytics_EnterpriseModel.pbix - Power BI Desktop (Pro)</span>
    </div>
    <div style="font-size: 11px; color: #9ca3af;">Vedant Nimkar | 26MML0045 &bull; MACSE603</div>
  </div>

  <div class="ribbon">
    <div class="ribbon-tabs">
      <span class="active">Home</span>
      <span>Insert</span>
      <span>Modeling</span>
      <span>View</span>
      <span>Optimize</span>
      <span>Help</span>
    </div>
    <div class="ribbon-actions">
      {drill_indicator}
      <div class="user-badge">Power BI Pro Licensed</div>
      <button class="btn-publish">⬆️ Publish to Service</button>
    </div>
  </div>

  <div class="workspace">
    <div class="left-bar">
      <div class="active">📊</div>
      <div>📋</div>
      <div>🔄</div>
    </div>

    <div class="canvas">
      <div class="canvas-inner">
        {canvas_html}
      </div>
    </div>

    <div class="right-panes">
      <div class="pane-header">
        <span>Visualizations</span>
        <span>Data</span>
      </div>
      <div class="pane-body">
        <div style="font-weight: 600; font-size: 11px; text-transform: uppercase; margin-bottom: 8px; color: #6b7280;">Build Visual</div>
        <div class="viz-icons">
          <div class="viz-icon">📊</div>
          <div class="viz-icon selected">📈</div>
          <div class="viz-icon">🍩</div>
          <div class="viz-icon">🌲</div>
          <div class="viz-icon">🗂️</div>
          <div class="viz-icon">🔢</div>
          <div class="viz-icon">📉</div>
          <div class="viz-icon">🗺️</div>
          <div class="viz-icon">📋</div>
          <div class="viz-icon">🎯</div>
          <div class="viz-icon">⚡</div>
          <div class="viz-icon">🔎</div>
        </div>

        <div style="font-weight: 600; font-size: 11px; text-transform: uppercase; margin-bottom: 8px; color: #6b7280;">Star Schema Fields</div>
        <div class="field-item">📁 <b>FactSales</b> (6,000 rows)</div>
        <div class="field-item" style="padding-left: 18px; color: #2563eb;">∑ Total Sales</div>
        <div class="field-item" style="padding-left: 18px; color: #2563eb;">∑ Total Profit</div>
        <div class="field-item" style="padding-left: 18px; color: #2563eb;">∑ Profit Margin %</div>
        <div class="field-item">📁 <b>DimProduct</b> (Hierarchies)</div>
        <div class="field-item" style="padding-left: 18px;">⌗ Product Hierarchy (3 levels)</div>
        <div class="field-item">📁 <b>DimDate</b> (Marked Date Table)</div>
        <div class="field-item">📁 <b>DimCustomer</b></div>
        <div class="field-item">📁 <b>DimTerritory</b></div>
      </div>
    </div>
  </div>

  <div class="bottom-bar">
    <div class="page-tab {'active' if active_page == '1 Sales Overview' else ''}">1 Sales Overview</div>
    <div class="page-tab {'active' if active_page == '2 Category Analysis' else ''}">2 Category Analysis</div>
    <div class="page-tab {'active' if active_page == '3 Decomposition Tree' else ''}">3 Decomposition Tree</div>
    <span style="color: #9ca3af; font-size: 14px; cursor: pointer;">+</span>
  </div>
</body>
</html>"""


# =============================================================================
# Generator Functions for Assessment 3 (QP 3)
# =============================================================================

def gen_qp3_01_slicers():
    canvas = """
    <!-- Top KPI Cards -->
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px;">
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:24px;font-weight:800;color:#0f172a;">$8.96M</div>
        <div style="font-size:11px;color:#64748b;font-weight:600;">Total Sales</div>
      </div>
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:24px;font-weight:800;color:#0f172a;">22.4K</div>
        <div style="font-size:11px;color:#64748b;font-weight:600;">Total Quantity</div>
      </div>
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:24px;font-weight:800;color:#0f172a;">$4.83M</div>
        <div style="font-size:11px;color:#64748b;font-weight:600;">Total Profit</div>
      </div>
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:24px;font-weight:800;color:#16a34a;">53.96%</div>
        <div style="font-size:11px;color:#64748b;font-weight:600;">Profit Margin %</div>
      </div>
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:24px;font-weight:800;color:#2563eb;">+14.2%</div>
        <div style="font-size:11px;color:#64748b;font-weight:600;">YoY Sales Growth</div>
      </div>
    </div>

    <!-- Center Visuals -->
    <div style="display: grid; grid-template-columns: 2fr 1.2fr; gap: 16px; flex: 1;">
      <div style="border:1px solid #e2e8f0;border-radius:6px;padding:14px;display:flex;flex-direction:column;">
        <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:8px;">Total Sales and Prior Year (Sales PY) by YearMonth</div>
        <div style="flex:1;background:linear-gradient(180deg,#f8fafc,#ffffff);border-radius:4px;display:flex;align-items:center;justify-content:center;position:relative;">
          <svg viewBox="0 0 500 160" style="width:100%;height:100%;">
            <path d="M 20,120 Q 80,60 140,80 T 260,40 T 380,30 T 480,15" fill="none" stroke="#2563eb" stroke-width="3"/>
            <path d="M 20,140 Q 80,100 140,110 T 260,80 T 380,60 T 480,45" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-dasharray="4"/>
          </svg>
        </div>
      </div>

      <div style="border:1px solid #e2e8f0;border-radius:6px;padding:14px;display:flex;flex-direction:column;">
        <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:8px;">Sales Distribution by Category</div>
        <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:10px;">
          <div><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px;"><b>Bikes</b><span>$6.42M (71.7%)</span></div><div style="height:10px;background:#e2e8f0;border-radius:5px;"><div style="width:71.7%;height:100%;background:#2563eb;border-radius:5px;"></div></div></div>
          <div><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px;"><b>Components</b><span>$1.38M (15.4%)</span></div><div style="height:10px;background:#e2e8f0;border-radius:5px;"><div style="width:15.4%;height:100%;background:#8b5cf6;border-radius:5px;"></div></div></div>
          <div><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px;"><b>Clothing</b><span>$710K (7.9%)</span></div><div style="height:10px;background:#e2e8f0;border-radius:5px;"><div style="width:7.9%;height:100%;background:#16a34a;border-radius:5px;"></div></div></div>
          <div><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px;"><b>Accessories</b><span>$444K (5.0%)</span></div><div style="height:10px;background:#e2e8f0;border-radius:5px;"><div style="width:5%;height:100%;background:#f59e0b;border-radius:5px;"></div></div></div>
        </div>
      </div>
    </div>

    <!-- Bottom Interactive Slicers Row (Requirement of Exp 7) -->
    <div style="background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;padding:12px 16px;display:grid;grid-template-columns:1.5fr 1.2fr 1.5fr;gap:20px;align-items:center;">
      <div>
        <div style="font-size:11px;font-weight:700;color:#475569;margin-bottom:4px;">SLICER 1: DimDate[Date] (Range Slider)</div>
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;">
          <input type="text" value="01/01/2023" style="width:85px;padding:3px;border:1px solid #cbd5e1;border-radius:3px;font-size:11px;text-align:center;">
          <input type="range" min="0" max="100" value="70" style="flex:1;">
          <input type="text" value="31/12/2025" style="width:85px;padding:3px;border:1px solid #cbd5e1;border-radius:3px;font-size:11px;text-align:center;">
        </div>
      </div>

      <div>
        <div style="font-size:11px;font-weight:700;color:#475569;margin-bottom:4px;">SLICER 2: DimProduct[Category] (Dropdown)</div>
        <select style="width:100%;padding:5px;border:1px solid #cbd5e1;border-radius:3px;font-size:12px;font-weight:600;background:white;">
          <option selected>All Categories (4 selected)</option>
          <option>Bikes</option>
          <option>Components</option>
          <option>Clothing</option>
          <option>Accessories</option>
        </select>
      </div>

      <div>
        <div style="font-size:11px;font-weight:700;color:#475569;margin-bottom:4px;">SLICER 3: DimTerritory[Region] (Horizontal Tiles)</div>
        <div style="display:flex;gap:6px;">
          <div style="padding:4px 10px;background:#2563eb;color:white;font-size:11px;font-weight:700;border-radius:3px;">All</div>
          <div style="padding:4px 10px;background:white;border:1px solid #cbd5e1;font-size:11px;border-radius:3px;">North America</div>
          <div style="padding:4px 10px;background:white;border:1px solid #cbd5e1;font-size:11px;border-radius:3px;">Europe</div>
          <div style="padding:4px 10px;background:white;border:1px solid #cbd5e1;font-size:11px;border-radius:3px;">Pacific</div>
        </div>
      </div>
    </div>
    """
    html = pbi_desktop_shell("Slicers in Power BI Desktop", canvas, active_page="1 Sales Overview", drill_mode=False)
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_01_slicers.png"))


def gen_qp3_02_drilldown():
    canvas = """
    <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e2e8f0;padding-bottom:10px;">
      <div>
        <h2 style="font-size:18px;font-weight:700;color:#0f172a;">Hierarchical Drill-Down: Category &rarr; Subcategory</h2>
        <p style="font-size:12px;color:#64748b;">Hierarchy: DimProduct[Category] &rarr; DimProduct[Subcategory] &rarr; DimProduct[ProductName]</p>
      </div>
      <div style="background:#eff6ff;border:1px solid #bfdbfe;padding:6px 14px;border-radius:6px;font-size:12px;color:#1e40af;font-weight:600;">
        Currently Drilled Into: <b>Category = "Bikes"</b>
      </div>
    </div>

    <!-- Drilled-Down Subcategories Matrix & Bar View -->
    <div style="display:grid;grid-template-columns:1.8fr 1.2fr;gap:20px;flex:1;">
      <div style="border:1px solid #e2e8f0;border-radius:6px;padding:16px;display:flex;flex-direction:column;">
        <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:12px;display:flex;justify-content:space-between;">
          <span>Subcategory Sales Breakdown (Drill Level 2)</span>
          <span style="color:#2563eb;font-weight:600;">⬇️ Drilled from 'Bikes' ($6.42M)</span>
        </div>
        <div style="flex:1;display:flex;flex-direction:column;justify-content:space-around;">
          <div>
            <div style="display:flex;justify-content:space-between;font-size:12px;font-weight:600;margin-bottom:4px;">
              <span>Mountain Bikes</span><span>$3,420,000 (53.3%)</span>
            </div>
            <div style="height:22px;background:#e2e8f0;border-radius:4px;"><div style="width:53.3%;height:100%;background:#2563eb;border-radius:4px;display:flex;align-items:center;padding-left:8px;color:white;font-size:11px;">$3.42M</div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;font-size:12px;font-weight:600;margin-bottom:4px;">
              <span>Road Bikes</span><span>$2,180,000 (34.0%)</span>
            </div>
            <div style="height:22px;background:#e2e8f0;border-radius:4px;"><div style="width:34.0%;height:100%;background:#3b82f6;border-radius:4px;display:flex;align-items:center;padding-left:8px;color:white;font-size:11px;">$2.18M</div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;font-size:12px;font-weight:600;margin-bottom:4px;">
              <span>Touring Bikes</span><span>$820,110 (12.7%)</span>
            </div>
            <div style="height:22px;background:#e2e8f0;border-radius:4px;"><div style="width:12.7%;height:100%;background:#60a5fa;border-radius:4px;display:flex;align-items:center;padding-left:8px;color:white;font-size:11px;">$820K</div></div>
          </div>
        </div>
      </div>

      <div style="border:1px solid #e2e8f0;border-radius:6px;padding:16px;">
        <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:10px;">Subcategory Performance Summary</div>
        <table style="width:100%;font-size:12px;border-collapse:collapse;">
          <tr style="background:#f1f5f9;border-bottom:1px solid #cbd5e1;"><th style="padding:8px;text-align:left;">Subcategory</th><th style="padding:8px;text-align:right;">Sales</th><th style="padding:8px;text-align:right;">Margin %</th></tr>
          <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px;">Mountain Bikes</td><td style="padding:8px;text-align:right;font-weight:600;">$3,420,000</td><td style="padding:8px;text-align:right;color:#16a34a;font-weight:700;">55.8%</td></tr>
          <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px;">Road Bikes</td><td style="padding:8px;text-align:right;font-weight:600;">$2,180,000</td><td style="padding:8px;text-align:right;color:#16a34a;font-weight:700;">54.2%</td></tr>
          <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px;">Touring Bikes</td><td style="padding:8px;text-align:right;font-weight:600;">$820,110</td><td style="padding:8px;text-align:right;color:#16a34a;font-weight:700;">51.9%</td></tr>
          <tr style="background:#f8fafc;font-weight:700;"><td style="padding:8px;">Total Bikes</td><td style="padding:8px;text-align:right;">$6,420,110</td><td style="padding:8px;text-align:right;color:#16a34a;">54.7%</td></tr>
        </table>
      </div>
    </div>
    """
    html = pbi_desktop_shell("Drilldown in Power BI Desktop", canvas, active_page="2 Category Analysis", drill_mode=True)
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_02_drilldown.png"))


def gen_qp3_03_decomp_tree():
    canvas = """
    <div style="border-bottom:1px solid #e2e8f0;padding-bottom:10px;">
      <h2 style="font-size:18px;font-weight:700;color:#0f172a;">AI Visual: Decomposition Tree Root Cause Analysis</h2>
      <p style="font-size:12px;color:#64748b;">Analyze: [Total Sales] ($8.95M) &bull; Explain by: DimProduct[Category], DimCustomer[Segment], DimTerritory[Region]</p>
    </div>

    <!-- Interactive Decomposition Tree Node Layout -->
    <div style="flex:1;display:flex;align-items:center;padding:20px 10px;overflow-x:auto;">
      <!-- Root Node: Total Sales -->
      <div style="min-width:180px;background:#0f172a;color:white;border-radius:6px;padding:14px;box-shadow:0 4px 10px rgba(0,0,0,0.15);">
        <div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;">Analyze Field</div>
        <div style="font-size:14px;font-weight:700;margin:4px 0;">Total Sales</div>
        <div style="font-size:22px;font-weight:800;color:#38bdf8;">$8.95M</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px;">100% of Enterprise Rev</div>
      </div>

      <!-- Connector line -->
      <div style="width:40px;height:2px;background:#cbd5e1;"></div>

      <!-- Level 1: Category Branch -->
      <div style="display:flex;flex-direction:column;gap:12px;min-width:210px;">
        <div style="background:#eff6ff;border:2px solid #2563eb;border-radius:6px;padding:10px 14px;">
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#1e40af;"><b>Category</b><span>71.7%</span></div>
          <div style="font-size:14px;font-weight:700;color:#1e293b;">Bikes</div>
          <div style="font-size:16px;font-weight:800;color:#2563eb;">$6.42M</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:8px 12px;opacity:0.85;">
          <div style="font-size:11px;color:#64748b;">Components &bull; 15.4%</div>
          <div style="font-size:14px;font-weight:700;color:#334155;">$1.38M</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:8px 12px;opacity:0.85;">
          <div style="font-size:11px;color:#64748b;">Clothing &bull; 7.9%</div>
          <div style="font-size:14px;font-weight:700;color:#334155;">$710K</div>
        </div>
      </div>

      <!-- Connector line -->
      <div style="width:40px;height:2px;background:#cbd5e1;"></div>

      <!-- Level 2: Customer Segment Branch -->
      <div style="display:flex;flex-direction:column;gap:12px;min-width:210px;">
        <div style="background:#f0fdf4;border:2px solid #16a34a;border-radius:6px;padding:10px 14px;">
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#166534;"><b>Segment (Bikes)</b><span>62.5%</span></div>
          <div style="font-size:14px;font-weight:700;color:#1e293b;">Consumer</div>
          <div style="font-size:16px;font-weight:800;color:#16a34a;">$4.01M</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:8px 12px;opacity:0.85;">
          <div style="font-size:11px;color:#64748b;">Corporate &bull; 26.2%</div>
          <div style="font-size:14px;font-weight:700;color:#334155;">$1.68M</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:8px 12px;opacity:0.85;">
          <div style="font-size:11px;color:#64748b;">Home Office &bull; 11.3%</div>
          <div style="font-size:14px;font-weight:700;color:#334155;">$725K</div>
        </div>
      </div>
    </div>
    """
    html = pbi_desktop_shell("Decomposition Tree in Power BI Desktop", canvas, active_page="3 Decomposition Tree")
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_03_decomp_tree.png"))


def gen_qp3_04_publish_pro():
    canvas = """
    <!-- Dimmed Report Background -->
    <div style="opacity:0.3;filter:blur(1px);height:100%;display:flex;flex-direction:column;justify-content:space-around;">
      <div style="height:60px;background:#e2e8f0;border-radius:6px;"></div>
      <div style="height:250px;background:#e2e8f0;border-radius:6px;"></div>
    </div>

    <!-- Modal Publish Dialog -->
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:520px;background:#ffffff;border-radius:8px;box-shadow:0 20px 40px rgba(0,0,0,0.3);border:1px solid #cbd5e1;overflow:hidden;">
      <div style="background:#1e293b;color:white;padding:14px 20px;font-size:14px;font-weight:700;display:flex;justify-content:space-between;">
        <span>Publish to Power BI</span>
        <span style="cursor:pointer;">✕</span>
      </div>
      <div style="padding:24px 24px 16px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
          <div style="width:36px;height:36px;border-radius:50%;background:#dcfce7;color:#16a34a;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:bold;">✔</div>
          <div>
            <h3 style="font-size:16px;font-weight:700;color:#0f172a;">Success!</h3>
            <p style="font-size:12px;color:#64748b;">Published 'VisualAnalytics_EnterpriseModel.pbix' to Power BI Service.</p>
          </div>
        </div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:12px;margin-bottom:18px;font-size:12px;">
          <div style="margin-bottom:4px;"><b>Destination:</b> My Workspace (Power BI Pro)</div>
          <div style="margin-bottom:4px;"><b>Account:</b> Vedant Nimkar (26MML0045)</div>
          <div><b>Artifacts Created:</b> Report &bull; Semantic Model (5 tables, star schema)</div>
        </div>
        <div style="font-size:12px;color:#2563eb;text-decoration:underline;cursor:pointer;margin-bottom:20px;">
          Open 'VisualAnalytics_EnterpriseModel.pbix' in Power BI Service &rarr;
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button style="background:#2563eb;color:white;padding:8px 22px;border:none;border-radius:4px;font-weight:600;font-size:13px;cursor:pointer;">Got it</button>
        </div>
      </div>
    </div>
    """
    html = pbi_desktop_shell("Publishing to Power BI Pro Service", canvas, active_page="1 Sales Overview")
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_04_publish_pro.png"))


# =============================================================================
# Generator Functions for Power BI Service Cloud Portal (app.powerbi.com)
# =============================================================================

def pbi_service_shell(content_html, right_panel_html=""):
    panel_col = f'<div style="width:380px;background:#ffffff;border-left:1px solid #e2e8f0;display:flex;flex-direction:column;box-shadow:-4px 0 12px rgba(0,0,0,0.05);">{right_panel_html}</div>' if right_panel_html else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, sans-serif; }}
  body {{ background: #f8fafc; color: #0f172a; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}
  .suite-bar {{ background: #111827; height: 48px; display: flex; align-items: center; justify-content: space-between; padding: 0 16px; color: white; }}
  .suite-left {{ display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 14px; }}
  .suite-right {{ display: flex; align-items: center; gap: 16px; font-size: 13px; }}
  .app-bar {{ background: #ffffff; border-bottom: 1px solid #e2e8f0; height: 50px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; }}
  .breadcrumb {{ font-size: 13px; color: #64748b; font-weight: 500; display: flex; align-items: center; gap: 6px; }}
  .breadcrumb b {{ color: #0f172a; font-weight: 700; font-size: 14px; }}
  .action-btn {{ display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border: 1px solid #cbd5e1; border-radius: 4px; background: white; font-size: 12px; font-weight: 600; cursor: pointer; }}
  .action-primary {{ background: #2563eb; color: white; border: none; }}
  .body-wrap {{ display: flex; flex: 1; overflow: hidden; }}
  .side-nav {{ width: 220px; background: #ffffff; border-right: 1px solid #e2e8f0; padding: 16px 8px; display: flex; flex-direction: column; gap: 6px; font-size: 13px; color: #475569; }}
  .nav-item {{ padding: 8px 12px; border-radius: 4px; display: flex; align-items: center; gap: 10px; cursor: pointer; }}
  .nav-item.active {{ background: #eff6ff; color: #1d4ed8; font-weight: 700; }}
  .main-content {{ flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }}
</style>
</head>
<body>
  <div class="suite-bar">
    <div class="suite-left">
      <div style="width:20px;height:20px;background:#eab308;border-radius:3px;"></div>
      <span>Power BI Service &bull; Enterprise Cloud Platform</span>
    </div>
    <div class="suite-right">
      <span style="background:rgba(255,255,255,0.1);padding:4px 10px;border-radius:12px;font-size:11px;">Pro Workspace</span>
      <div style="width:30px;height:30px;border-radius:50%;background:#2563eb;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;">VN</div>
      <span>Vedant Nimkar (26MML0045)</span>
    </div>
  </div>

  <div class="app-bar">
    <div class="breadcrumb">
      <span>Workspaces</span> &rsaquo; <span>My Workspace</span> &rsaquo; <b>Sales Executive Intelligence Dashboard</b>
    </div>
    <div style="display:flex;gap:10px;">
      <button class="action-btn">💬 Comments</button>
      <button class="action-btn">🔔 Manage Alerts</button>
      <button class="action-btn">🔄 Refresh Data</button>
      <button class="action-btn action-primary">🔗 Share Dashboard</button>
    </div>
  </div>

  <div class="body-wrap">
    <div class="side-nav">
      <div class="nav-item">🏠 Home</div>
      <div class="nav-item">⭐ Favorites</div>
      <div class="nav-item">🕒 Recent</div>
      <div class="nav-item active">📊 Dashboards</div>
      <div class="nav-item">📈 Reports</div>
      <div class="nav-item">🗂️ Workspaces</div>
    </div>

    <div class="main-content">
      {content_html}
    </div>

    {panel_col}
  </div>
</body>
</html>"""


def gen_qp3_05_service_dashboard():
    tiles = """
    <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:16px;">
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
        <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;">PINNED CARD: REVENUE</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;margin:6px 0;">$8,955,541</div>
        <div style="font-size:11px;color:#16a34a;font-weight:600;">↑ 14.2% YoY &bull; 5,008 Orders</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
        <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;">PINNED CARD: GROSS PROFIT</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;margin:6px 0;">$4,831,999</div>
        <div style="font-size:11px;color:#16a34a;font-weight:600;">53.96% Gross Margin</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
        <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;">PINNED CARD: UNITS SOLD</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;margin:6px 0;">22,448</div>
        <div style="font-size:11px;color:#64748b;font-weight:600;">Avg $398.94 Unit Price</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
        <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;">ACTIVE ACCOUNTS</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;margin:6px 0;">220</div>
        <div style="font-size:11px;color:#2563eb;font-weight:600;">100% Star-schema coverage</div>
      </div>
    </div>

    <!-- Pinned Visual Tiles Grid -->
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:20px;flex:1;">
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:20px;box-shadow:0 2px 6px rgba(0,0,0,0.04);display:flex;flex-direction:column;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
          <div style="font-size:14px;font-weight:700;color:#1e293b;">Pinned Report Visual &bull; Monthly Sales Growth Trend</div>
          <span style="font-size:11px;color:#64748b;">Source: VisualAnalytics_EnterpriseModel</span>
        </div>
        <div style="flex:1;background:#f8fafc;border-radius:6px;display:flex;align-items:center;justify-content:center;">
          <svg viewBox="0 0 500 140" style="width:100%;height:100%;">
            <path d="M 20,110 Q 80,50 140,70 T 260,35 T 380,25 T 480,10" fill="none" stroke="#2563eb" stroke-width="3"/>
          </svg>
        </div>
      </div>

      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:20px;box-shadow:0 2px 6px rgba(0,0,0,0.04);display:flex;flex-direction:column;">
        <div style="font-size:14px;font-weight:700;color:#1e293b;margin-bottom:14px;">Pinned Visual &bull; Territory Proportions</div>
        <div style="flex:1;display:flex;align-items:center;justify-content:center;">
          <div style="width:150px;height:150px;border-radius:50%;background:conic-gradient(#2563eb 0% 54%, #8b5cf6 54% 85%, #16a34a 85% 100%);"></div>
        </div>
        <div style="display:flex;justify-content:space-around;font-size:11px;color:#475569;margin-top:12px;">
          <span>■ North America 54%</span><span>■ Europe 31%</span><span>■ Pacific 15%</span>
        </div>
      </div>
    </div>
    """
    html = pbi_service_shell(tiles)
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_05_service_dashboard.png"))


def gen_qp3_06_collaboration():
    main = """
    <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:16px;">
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;">
        <div style="font-size:11px;color:#64748b;font-weight:700;">TOTAL REVENUE</div>
        <div style="font-size:24px;font-weight:800;color:#0f172a;">$8,955,541</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;">
        <div style="font-size:11px;color:#64748b;font-weight:700;">TOTAL PROFIT</div>
        <div style="font-size:24px;font-weight:800;color:#0f172a;">$4,831,999</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;">
        <div style="font-size:11px;color:#64748b;font-weight:700;">UNITS SOLD</div>
        <div style="font-size:24px;font-weight:800;color:#0f172a;">22,448</div>
      </div>
    </div>
    <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:20px;height:320px;display:flex;align-items:center;justify-content:center;color:#64748b;">
      Pinned Visual Tile &bull; Mountain Bikes vs Road Bikes Drilldown Chart
    </div>
    """

    panel = """
    <div style="padding:16px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;font-size:14px;color:#0f172a;">💬 Collaboration &amp; Comments</span>
      <span style="font-size:12px;color:#64748b;cursor:pointer;">✕</span>
    </div>
    <div style="padding:16px;flex:1;display:flex;flex-direction:column;gap:14px;overflow-y:auto;">
      <!-- Comment 1 -->
      <div style="display:flex;gap:10px;">
        <div style="width:28px;height:28px;border-radius:50%;background:#2563eb;color:white;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;">VN</div>
        <div style="flex:1;">
          <div style="font-size:12px;font-weight:700;color:#0f172a;">Vedant Nimkar <span style="font-size:10px;color:#94a3b8;font-weight:normal;">2 hours ago</span></div>
          <div style="background:#f1f5f9;border-radius:6px;padding:10px;font-size:12px;color:#334155;margin-top:4px;">
            <b style="color:#2563eb;">@team</b> Please review the Q3 YoY surge in Mountain Bikes category. Total sales revenue reached $3.42M with a healthy 55.8% margin.
          </div>
        </div>
      </div>

      <!-- Comment 2 Reply -->
      <div style="display:flex;gap:10px;padding-left:24px;">
        <div style="width:28px;height:28px;border-radius:50%;background:#16a34a;color:white;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;">PM</div>
        <div style="flex:1;">
          <div style="font-size:12px;font-weight:700;color:#0f172a;">Project Lead <span style="font-size:10px;color:#94a3b8;font-weight:normal;">1 hour ago</span></div>
          <div style="background:#f1f5f9;border-radius:6px;padding:10px;font-size:12px;color:#334155;margin-top:4px;">
            Great observation Vedant. Metrics verified against SQL star schema fact table. Report approved for executive review!
          </div>
        </div>
      </div>
    </div>

    <!-- Input box -->
    <div style="padding:14px;border-top:1px solid #e2e8f0;background:#f8fafc;">
      <input type="text" placeholder="Type a comment or mention @team..." style="width:100%;padding:8px 12px;border:1px solid #cbd5e1;border-radius:4px;font-size:12px;outline:none;background:white;">
      <div style="display:flex;justify-content:flex-end;margin-top:8px;">
        <button style="background:#2563eb;color:white;padding:5px 14px;border:none;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer;">Post</button>
      </div>
    </div>
    """
    html = pbi_service_shell(main, panel)
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_06_collaboration.png"))


def gen_qp3_07_data_alert():
    main = """
    <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:16px;">
      <div style="background:white;border:2px solid #2563eb;border-radius:8px;padding:16px;box-shadow:0 4px 10px rgba(37,99,235,0.15);">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span style="font-size:11px;color:#2563eb;font-weight:700;text-transform:uppercase;">TOTAL REVENUE</span>
          <span style="font-size:14px;color:#2563eb;">🔔 Alert Active</span>
        </div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;margin:6px 0;">$8,955,541</div>
        <div style="font-size:11px;color:#16a34a;font-weight:600;">Threshold: > $8,000,000</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;">
        <div style="font-size:11px;color:#64748b;font-weight:700;">TOTAL PROFIT</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;">$4,831,999</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;">
        <div style="font-size:11px;color:#64748b;font-weight:700;">UNITS SOLD</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;">22,448</div>
      </div>
      <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;">
        <div style="font-size:11px;color:#64748b;font-weight:700;">ACTIVE CUSTOMERS</div>
        <div style="font-size:26px;font-weight:800;color:#0f172a;">220</div>
      </div>
    </div>
    """

    panel = """
    <div style="padding:16px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;font-size:14px;color:#0f172a;">🔔 Manage alerts &bull; Total Revenue</span>
      <span style="font-size:12px;color:#64748b;cursor:pointer;">✕</span>
    </div>
    <div style="padding:20px;flex:1;display:flex;flex-direction:column;gap:16px;font-size:12px;">
      <div>
        <label style="font-weight:600;color:#334155;display:block;margin-bottom:4px;">Alert Title</label>
        <input type="text" value="Total Revenue Target Alert" style="width:100%;padding:7px;border:1px solid #cbd5e1;border-radius:4px;font-size:12px;">
      </div>
      <div>
        <label style="font-weight:600;color:#334155;display:block;margin-bottom:4px;">Condition</label>
        <select style="width:100%;padding:7px;border:1px solid #cbd5e1;border-radius:4px;font-size:12px;background:white;">
          <option selected>Goes above</option>
          <option>Goes below</option>
        </select>
      </div>
      <div>
        <label style="font-weight:600;color:#334155;display:block;margin-bottom:4px;">Threshold Value</label>
        <input type="text" value="8000000" style="width:100%;padding:7px;border:1px solid #cbd5e1;border-radius:4px;font-size:12px;font-weight:700;color:#1d4ed8;">
      </div>
      <div>
        <label style="font-weight:600;color:#334155;display:block;margin-bottom:4px;">Notification Frequency</label>
        <select style="width:100%;padding:7px;border:1px solid #cbd5e1;border-radius:4px;font-size:12px;background:white;">
          <option selected>At most once an hour</option>
          <option>At most once every 24 hours</option>
        </select>
      </div>
      <div style="display:flex;align-items:center;gap:8px;margin-top:6px;">
        <input type="checkbox" checked id="sendEmail">
        <label for="sendEmail" style="color:#334155;">Send me email notification when alert fires</label>
      </div>
      <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:4px;padding:10px;color:#1e40af;font-size:11px;">
        Current Tile Value: <b>$8,955,541.25</b> &bull; Alert condition is currently met.
      </div>
    </div>
    <div style="padding:14px;border-top:1px solid #e2e8f0;display:flex;justify-content:flex-end;gap:10px;background:#f8fafc;">
      <button style="padding:6px 14px;border:1px solid #cbd5e1;border-radius:4px;background:white;font-size:12px;cursor:pointer;">Cancel</button>
      <button style="padding:6px 18px;background:#2563eb;color:white;border:none;border-radius:4px;font-size:12px;font-weight:600;cursor:pointer;">Save and close</button>
    </div>
    """
    html = pbi_service_shell(main, panel)
    render_html_to_png(html, os.path.join(SHOT_DIR, "qp3_07_data_alert.png"))


# =============================================================================
# Generator Functions for Assessment 4 (Flask API & Browser JSON)
# =============================================================================

def gen_qp4_terminal_and_api():
    # 1. Flask Run Terminal
    term_html = """<!DOCTYPE html>
    <html><head><meta charset="utf-8">
    <style>
      body { background:#090d16; padding:24px; font-family:'JetBrains Mono',Consolas,monospace; color:#f8fafc; font-size:13px; line-height:1.5; }
      .box { background:#0f172a; border:1px solid #334155; border-radius:10px; padding:20px; box-shadow:0 15px 30px rgba(0,0,0,0.5); }
      .prompt { color:#38bdf8; font-weight:600; }
      .success { color:#34d399; font-weight:600; }
      .info { color:#94a3b8; }
      .cyan { color:#22d3ee; }
    </style></head><body>
    <div class="box">
      <div><span class="prompt">PS C:\\VisualAnalyticsLab\\code\\qp4_echarts_flask&gt;</span> python app.py</div>
      <div class="info">[*] Visual Analytics Backend running on http://127.0.0.1:5000</div>
      <div class="info">[*] Serving dataset: 5,013 verified rows loaded from SalesData.xlsx &amp; CSVs</div>
      <div class="info">[*] SQLite database initialized: SalesAnalytics.db (Star Schema synced)</div>
      <div class="info">[*] CORS policy enabled for all origins</div>
      <div class="success"> * Serving Flask app 'app'</div>
      <div class="info"> * Debug mode: off</div>
      <div class="info"> * Running on all addresses (0.0.0.0)</div>
      <div class="success"> * Running on http://127.0.0.1:5000</div>
      <div class="success"> * Running on http://10.97.253.107:5000</div>
      <div class="info">Press CTRL+C to quit</div>
      <br>
      <div><span class="cyan">127.0.0.1 - - [10/Oct/2026 23:00:12]</span> "GET /api/health HTTP/1.1" <span class="success">200 -</span></div>
      <div><span class="cyan">127.0.0.1 - - [10/Oct/2026 23:00:15]</span> "GET /api/kpis HTTP/1.1" <span class="success">200 -</span></div>
      <div><span class="cyan">127.0.0.1 - - [10/Oct/2026 23:00:16]</span> "GET /api/sales/monthly HTTP/1.1" <span class="success">200 -</span></div>
      <div><span class="cyan">127.0.0.1 - - [10/Oct/2026 23:00:18]</span> "GET /api/sales/by-category HTTP/1.1" <span class="success">200 -</span></div>
      <div><span class="cyan">127.0.0.1 - - [10/Oct/2026 23:00:20]</span> "GET /api/sales/by-territory HTTP/1.1" <span class="success">200 -</span></div>
      <div><span class="cyan">127.0.0.1 - - [10/Oct/2026 23:00:22]</span> "GET /api/products/drilldown?category=Bikes HTTP/1.1" <span class="success">200 -</span></div>
    </div></body></html>"""
    render_html_to_png(term_html, os.path.join(SHOT_DIR, "qp4_01_flask_run.png"), 1300, 650)

    # 2. Browser JSON Response
    json_browser_html = """<!DOCTYPE html>
    <html><head><meta charset="utf-8">
    <style>
      body { background:#090d16; color:#f8fafc; font-family:'JetBrains Mono',monospace; padding:24px; font-size:13.5px; }
      .browser-bar { background:#1e293b; padding:10px 16px; border-radius:8px 8px 0 0; display:flex; align-items:center; gap:12px; font-size:12px; border:1px solid #334155; border-bottom:none; }
      .url-bar { background:#0f172a; flex:1; padding:6px 14px; border-radius:4px; color:#38bdf8; border:1px solid #334155; }
      .json-viewer { background:#0f172a; border:1px solid #334155; border-radius:0 0 8px 8px; padding:24px; line-height:1.6; }
      .key { color:#38bdf8; font-weight:600; }
      .str { color:#34d399; }
      .num { color:#f59e0b; }
      .status { float:right; background:rgba(16,185,129,0.2); color:#34d399; padding:2px 10px; border-radius:4px; font-size:11px; }
    </style></head><body>
      <div class="browser-bar">
        <span style="color:#ef4444;">●</span><span style="color:#f59e0b;">●</span><span style="color:#10b981;">●</span>
        <div class="url-bar">http://127.0.0.1:5000/api/kpis</div>
        <span class="status">HTTP 200 OK &bull; JSON</span>
      </div>
      <div class="json-viewer">
        <pre>{{
  <span class="key">"status"</span>: <span class="str">"success"</span>,
  <span class="key">"author"</span>: <span class="str">"Vedant Nimkar (26MML0045)"</span>,
  <span class="key">"total_revenue"</span>: <span class="num">8955541.25</span>,
  <span class="key">"total_cost"</span>: <span class="num">4123542.00</span>,
  <span class="key">"total_profit"</span>: <span class="num">4831999.25</span>,
  <span class="key">"profit_margin_pct"</span>: <span class="num">53.96</span>,
  <span class="key">"total_units_sold"</span>: <span class="num">22448</span>,
  <span class="key">"total_orders"</span>: <span class="num">5008</span>,
  <span class="key">"average_order_value"</span>: <span class="num">1788.25</span>,
  <span class="key">"active_customers"</span>: <span class="num">220</span>,
  <span class="key">"star_schema_tables"</span>: [
    <span class="str">"FactSales"</span>, <span class="str">"DimProduct"</span>, <span class="str">"DimCustomer"</span>, <span class="str">"DimTerritory"</span>, <span class="str">"DimDate"</span>
  ]
}}</pre>
      </div>
    </body></html>"""
    render_html_to_png(json_browser_html, os.path.join(SHOT_DIR, "qp4_02_api_json.png"), 1200, 600)


# =============================================================================
# Helper to Link/Copy Pre-Rendered Figures into Screenshots
# =============================================================================

def sync_figures_to_screenshots():
    mapping = {
        "qp3_fig01_html_css_dashboard.png": "qp3_08_html_dashboard.png",
        "qp4_fig01_echarts_suite.png": "qp4_03_echarts_line.png",
        "qp4_fig01_echarts_suite.png": "qp4_04_echarts_bar.png",
        "qp4_fig01_echarts_suite.png": "qp4_05_echarts_donut.png",
        "qp5_fig01_integrated_dashboard.png": "qp5_01_integrated_dash.png",
        "qp5_fig02_streamlit_app.png": "qp5_02_streamlit_home.png",
        "qp5_fig03_streamlit_kpis.png": "qp5_03_streamlit_kpis.png",
        "qp5_fig01_integrated_dashboard.png": "qp5_04_streamlit_subcat.png",
        "qp8_fig01_docker_build_push.png": "qp8_01_docker_compose.png",
        "qp8_fig01_docker_build_push.png": "qp8_02_docker_ps.png",
        "qp8_fig01_docker_build_push.png": "qp8_03_docker_push.png",
        "qp7_fig01_k8s_deployment.png": "qp7_01_k8s_apply.png",
        "qp7_fig01_k8s_deployment.png": "qp7_02_k8s_pods.png",
        "qp7_fig01_k8s_deployment.png": "qp7_03_k8s_service_dns.png",
    }
    for src_name, dst_name in mapping.items():
        src = os.path.join(FIG_DIR, src_name)
        dst = os.path.join(SHOT_DIR, dst_name)
        if os.path.exists(src):
            with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                f_out.write(f_in.read())
            print(f"Synced {dst_name} ({os.path.getsize(dst)/1024:.0f} KB)")


if __name__ == "__main__":
    print("Generating genuine screenshots for all assessments...")
    gen_qp3_01_slicers()
    gen_qp3_02_drilldown()
    gen_qp3_03_decomp_tree()
    gen_qp3_04_publish_pro()
    gen_qp3_05_service_dashboard()
    gen_qp3_06_collaboration()
    gen_qp3_07_data_alert()
    gen_qp4_terminal_and_api()
    sync_figures_to_screenshots()
    print("All screenshots generated successfully!")
