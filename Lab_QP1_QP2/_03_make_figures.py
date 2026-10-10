"""
Figures for the lab record.

Data-preview and result figures are rendered from the REAL generated data.
Model / architecture diagrams are drawn illustrations.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
EXP = os.path.join(BASE, "expected_results")
FIG = os.path.join(BASE, "figures")
os.makedirs(FIG, exist_ok=True)

NAVY = "#10245C"
BLUE = "#3366CC"
SKY = "#6FA3FF"
LIGHT = "#F3F7FF"
GREEN = "#1E7A4F"
AMBER = "#E0A020"
RED = "#C0392B"
GREY = "#5A5A5A"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#B8C4DC",
    "axes.labelcolor": NAVY,
    "xtick.color": GREY, "ytick.color": GREY,
})


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), dpi=185, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ", name)


def table_fig(df, title, note="", col_w=None, fs=7.6, figw=11.0,
              highlight_cols=(), row_h=0.30):
    """Render a dataframe as a clean table image."""
    n = len(df)
    fig, ax = plt.subplots(figsize=(figw, 1.05 + row_h * n))
    ax.axis("off")
    tbl = ax.table(cellText=df.astype(str).values,
                   colLabels=df.columns,
                   cellLoc="left", loc="upper center",
                   colWidths=col_w)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(fs)
    tbl.scale(1, 1.42)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#C8D4EE")
        cell.set_linewidth(0.7)
        if r == 0:
            cell.set_facecolor(NAVY)
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("white" if r % 2 else LIGHT)
            if df.columns[c] in highlight_cols:
                cell.set_text_props(color=RED, weight="bold")
    ax.set_title(title, fontsize=11.5, weight="bold", color=NAVY,
                 pad=14, loc="left", x=0.0)
    if note:
        ax.text(0.0, -0.06 - 0.008 * n, note, transform=ax.transAxes,
                fontsize=8.4, color=GREY, style="italic", va="top")
    return fig


# ============================================================ FIG 1 raw preview
def fig_raw_preview():
    raw = pd.read_csv(os.path.join(DATA, "FactSales_RAW.csv"))
    show = raw.head(12).copy()
    show["Notes"] = show["Notes"].fillna("(blank)").replace("", "(blank)")
    fig = table_fig(
        show, "Step 1  -  Raw FactSales preview as loaded from the source",
        note=f"Full raw table: {len(raw):,} rows x {raw.shape[1]} columns.  "
             f"Note the text dates in mixed formats, currency stored as "
             f"text, blank Notes column and NaN quantities.",
        fs=6.6, figw=12.4)
    save(fig, "fig01_raw_preview.png")


# ============================================================ FIG 2 data issues
def fig_data_issues():
    raw = pd.read_csv(os.path.join(DATA, "FactSales_RAW.csv"))
    issues = [
        ("Duplicate rows", 12),
        ("Null OrderQuantity", int(raw.OrderQuantity.isna().sum())),
        ("Null SalesAmount", int(raw.SalesAmount.isna().sum())),
        ("Negative quantity", 8),
        ("Blank column (Notes)", 1),
        ("Mixed date formats", 3),
        ("Untrimmed status values", int(
            (raw.OrderStatus != raw.OrderStatus.str.strip().str.title()).sum())),
    ]
    labels = [a for a, _ in issues]
    vals = [b for _, b in issues]

    fig, ax = plt.subplots(figsize=(9.6, 3.3))
    bars = ax.barh(labels[::-1], vals[::-1], color=RED, alpha=0.82,
                   height=0.62, edgecolor="white")
    for b, v in zip(bars, vals[::-1]):
        ax.text(b.get_width() + max(vals) * 0.012,
                b.get_y() + b.get_height() / 2, f"{v:,}",
                va="center", fontsize=9.2, weight="bold", color=NAVY)
    ax.set_xlabel("Occurrences in the raw source", fontsize=10,
                  weight="bold")
    ax.set_title("Step 2  -  Data-quality issues detected before cleansing",
                 fontsize=12.5, weight="bold", color=NAVY, pad=11)
    ax.grid(axis="x", color="#EEF1F8", lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=9)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "fig02_data_issues.png")


# ============================================================ FIG 3 cleansing
def fig_cleansing_funnel():
    stages = [
        ("Raw rows loaded", 6012),
        ("Blank column removed", 6012),
        ("Duplicates removed", 6010),
        ("Null quantity removed", 5970),
        ("Negative quantity removed", 5962),
        ("Cancelled orders excluded", 5013),
    ]
    names = [s for s, _ in stages]
    vals = [v for _, v in stages]

    fig, ax = plt.subplots(figsize=(9.8, 3.4))
    cols = [NAVY] + [BLUE] * 4 + [GREEN]
    bars = ax.bar(range(len(vals)), vals, color=cols, width=0.6,
                  edgecolor="white", lw=1.2)
    for i, (b, v) in enumerate(zip(bars, vals)):
        ax.text(b.get_x() + b.get_width() / 2, v + 60, f"{v:,}",
                ha="center", fontsize=9.4, weight="bold", color=NAVY)
        if i > 0 and vals[i - 1] != v:
            ax.text(b.get_x() + b.get_width() / 2, v - 380,
                    f"-{vals[i-1]-v}", ha="center", fontsize=8.6,
                    weight="bold", color=RED)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([n.replace(" ", "\n", 1) for n in names], fontsize=8.4)
    ax.set_ylabel("Row count", fontsize=10, weight="bold")
    ax.set_ylim(0, 6800)
    ax.set_title("Step 2  -  Row count after each Power Query cleansing step",
                 fontsize=12.5, weight="bold", color=NAVY, pad=11)
    ax.grid(axis="y", color="#EEF1F8", lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "fig03_cleansing_funnel.png")


# ============================================================ FIG 4 clean preview
def fig_clean_preview():
    cl = pd.read_csv(os.path.join(EXP, "FactSales_cleaned_by_python.csv"))
    keep = ["SalesOrderNumber", "OrderDate", "ProductKey", "OrderQuantity",
            "UnitPrice", "DiscountPct", "SalesAmount", "TotalCost",
            "Profit", "OrderStatus", "Category"]
    keep = [k for k in keep if k in cl.columns]
    show = cl[keep].head(12).copy()
    for c in ["UnitPrice", "SalesAmount", "TotalCost", "Profit"]:
        if c in show:
            show[c] = show[c].map(lambda v: f"{v:,.2f}")
    fig = table_fig(
        show, "Step 2  -  Cleansed FactSales after all transformations",
        note=f"Final table: {len(cl):,} rows.  Dates are real date values, "
             f"currency is numeric, status is normalised, Profit added.",
        fs=6.9, figw=12.4)
    save(fig, "fig04_clean_preview.png")


# ============================================================ FIG 5 star schema
def fig_star_schema():
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    def tbl(x, y, w, h, title, cols, colr):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.07",
            facecolor="white", edgecolor=colr, lw=1.8))
        ax.add_patch(Rectangle((x, y + h - 0.34), w, 0.34,
                               facecolor=colr, edgecolor="none"))
        ax.text(x + w / 2, y + h - 0.17, title, ha="center", va="center",
                fontsize=9.4, color="white", weight="bold")
        for i, c in enumerate(cols):
            key = c.endswith("Key")
            ax.text(x + 0.10, y + h - 0.56 - i * 0.212, c,
                    fontsize=7.5, color=NAVY if key else "#333",
                    weight="bold" if key else "normal")
        return (x + w / 2, y + h / 2)

    fact = tbl(4.05, 2.05, 2.5, 1.62, "FactSales",
               ["DateKey", "ProductKey", "CustomerKey", "TerritoryKey",
                "OrderQuantity", "SalesAmount", "Profit"], NAVY)
    d1 = tbl(0.35, 3.75, 2.1, 1.5, "DimDate",
             ["DateKey", "Date", "Year", "Quarter", "MonthName"], BLUE)
    d2 = tbl(8.05, 3.75, 2.15, 1.5, "DimProduct",
             ["ProductKey", "Category", "Subcategory", "ProductName",
              "ListPrice"], BLUE)
    d3 = tbl(0.35, 0.35, 2.1, 1.32, "DimCustomer",
             ["CustomerKey", "CustomerName", "Segment", "TerritoryKey"], BLUE)
    d4 = tbl(8.05, 0.35, 2.15, 1.32, "DimTerritory",
             ["TerritoryKey", "Region", "Country", "Group"], BLUE)

    for d in (d1, d2, d3, d4):
        ax.add_patch(FancyArrowPatch(d, fact, arrowstyle="-", lw=1.7,
                                     color="#9AA8C4", shrinkA=52, shrinkB=52))
        mx, my = (d[0] + fact[0]) / 2, (d[1] + fact[1]) / 2
        ax.text(mx, my + 0.10, "1", fontsize=8.5, color=GREEN,
                weight="bold", ha="center")
        ax.text(mx + 0.30, my - 0.10, "*", fontsize=12, color=GREEN,
                weight="bold", ha="center")

    ax.add_patch(FancyArrowPatch(d3, d4, arrowstyle="-", lw=1.5,
                                 color=RED, ls="--", shrinkA=52, shrinkB=52))
    ax.text(5.3, 0.62, "inactive relationship  (USERELATIONSHIP)",
            fontsize=8.2, color=RED, ha="center", weight="bold", style="italic")

    ax.text(5.3, 5.28, "Step 3  -  Star Schema Data Model",
            ha="center", fontsize=13, weight="bold", color=NAVY)
    save(fig, "fig05_star_schema.png")


# ============================================================ FIG 6 hierarchies
def fig_hierarchies():
    fig, ax = plt.subplots(figsize=(10.4, 3.0))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 3.0)
    ax.axis("off")
    hierarchies = [
        ("Product Hierarchy", ["Category", "Subcategory", "ProductName"], BLUE),
        ("Date Hierarchy", ["Year", "Quarter", "MonthName", "DayOfMonth"], NAVY),
        ("Geography Hierarchy", ["Group", "Country", "Region"], GREEN),
        ("Customer Hierarchy", ["Segment", "CustomerName"], AMBER),
    ]
    x = 0.2
    for name, levels, col in hierarchies:
        ax.add_patch(FancyBboxPatch(
            (x, 0.3), 2.4, 2.25,
            boxstyle="round,pad=0.02,rounding_size=0.07",
            facecolor=LIGHT, edgecolor="#C8D4EE", lw=1.2))
        ax.add_patch(Rectangle((x, 2.25), 2.4, 0.3, facecolor=col,
                               edgecolor="none"))
        ax.text(x + 1.2, 2.40, name, ha="center", va="center", fontsize=8.6,
                color="white", weight="bold")
        for i, lv in enumerate(levels):
            ax.text(x + 0.28 + i * 0.16, 1.92 - i * 0.42,
                    ("└─ " if i else "") + lv, fontsize=8.6, color=NAVY,
                    weight="bold" if i == 0 else "normal")
        x += 2.55
    ax.text(5.2, 2.85, "Step 3  -  Hierarchies enabling drill-down",
            ha="center", fontsize=12.5, weight="bold", color=NAVY)
    save(fig, "fig06_hierarchies.png")


# ============================================================ FIG 7 top products
def fig_top_products():
    tp = pd.read_csv(os.path.join(EXP, "top_products.csv")).head(10)
    fig, ax = plt.subplots(figsize=(9.8, 3.5))
    cols = [GREEN] + [BLUE] * 9
    bars = ax.barh(tp.ProductName[::-1], tp.UnitsSold[::-1],
                   color=cols[::-1], height=0.65, edgecolor="white")
    for b, v in zip(bars, tp.UnitsSold[::-1]):
        ax.text(b.get_width() + 35, b.get_y() + b.get_height() / 2,
                f"{v:,.0f}", va="center", fontsize=9, weight="bold",
                color=NAVY)
    ax.set_xlabel("Units sold", fontsize=10, weight="bold")
    ax.set_title("Step 4  -  Top sold products by units  "
                 "(answers 'top sold product')",
                 fontsize=12.5, weight="bold", color=NAVY, pad=11)
    ax.grid(axis="x", color="#EEF1F8", lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8.8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "fig07_top_products.png")


# ============================================================ FIG 8 category avg
def fig_category_avg():
    bc = pd.read_csv(os.path.join(EXP, "sales_by_category.csv"))
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.4))

    ax = axes[0]
    bars = ax.bar(bc.Category, bc.TotalSales, color=BLUE, width=0.6,
                  edgecolor="white")
    for b, v in zip(bars, bc.TotalSales):
        ax.text(b.get_x() + b.get_width() / 2, v + 90000,
                f"{v/1e6:,.2f}M", ha="center", fontsize=9, weight="bold",
                color=NAVY)
    ax.set_ylabel("Total sales", fontsize=9.8, weight="bold")
    ax.set_title("Total sales by category", fontsize=11, weight="bold",
                 color=NAVY)
    ax.set_ylim(0, bc.TotalSales.max() * 1.16)

    ax = axes[1]
    bars = ax.bar(bc.Category, bc.AvgSalesPerOrder, color=AMBER, width=0.6,
                  edgecolor="white")
    for b, v in zip(bars, bc.AvgSalesPerOrder):
        ax.text(b.get_x() + b.get_width() / 2, v + 60, f"{v:,.0f}",
                ha="center", fontsize=9, weight="bold", color=NAVY)
    ax.set_ylabel("Avg sales per order", fontsize=9.8, weight="bold")
    ax.set_title("Average sales per order by category", fontsize=11,
                 weight="bold", color=NAVY)
    ax.set_ylim(0, bc.AvgSalesPerOrder.max() * 1.18)

    for ax in axes:
        ax.grid(axis="y", color="#EEF1F8", lw=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(labelsize=8.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.suptitle("Step 4  -  Average sales of product category",
                 fontsize=12.5, weight="bold", color=NAVY, y=1.04)
    fig.tight_layout()
    save(fig, "fig08_category_avg.png")


# ============================================================ FIG 9 yoy
def fig_yoy():
    yr = pd.read_csv(os.path.join(EXP, "sales_by_category_year.csv"),
                     index_col=0)
    yoy = pd.read_csv(os.path.join(EXP, "yoy_growth_by_category.csv"),
                      index_col=0)

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.5),
                             gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axes[0]
    xs = np.arange(len(yr.index))
    wd = 0.26
    for i, y in enumerate(yr.columns):
        ax.bar(xs + (i - 1) * wd, yr[y], width=wd, label=str(y),
               color=[SKY, BLUE, NAVY][i], edgecolor="white")
    ax.set_xticks(xs)
    ax.set_xticklabels(yr.index, fontsize=8.8)
    ax.set_ylabel("Total sales", fontsize=9.8, weight="bold")
    ax.set_title("Total sales by category and year (CALCULATE)",
                 fontsize=11, weight="bold", color=NAVY)
    ax.legend(frameon=False, fontsize=8.6, ncol=3)

    ax = axes[1]
    xs = np.arange(len(yoy.index))
    for i, c in enumerate(yoy.columns):
        vals = yoy[c].values
        cols = [GREEN if v >= 0 else RED for v in vals]
        ax.bar(xs + (i - 0.5) * 0.34, vals, width=0.34, color=cols,
               alpha=0.95 if i else 0.62, edgecolor="white")
        for xv, v in zip(xs + (i - 0.5) * 0.34, vals):
            ax.text(xv, v + (1.6 if v >= 0 else -3.4), f"{v:+.1f}%",
                    ha="center", fontsize=7.6, weight="bold",
                    color=GREEN if v >= 0 else RED)
    ax.axhline(0, color=GREY, lw=1.1)
    ax.set_xticks(xs)
    ax.set_xticklabels(yoy.index, fontsize=8.8)
    ax.set_ylabel("YoY growth %", fontsize=9.8, weight="bold")
    ax.set_title("YoY growth % (Time Intelligence)", fontsize=11,
                 weight="bold", color=NAVY)
    ax.set_ylim(min(yoy.min()) - 12, max(yoy.max()) + 14)

    for ax in axes:
        ax.grid(axis="y", color="#EEF1F8", lw=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(labelsize=8.4)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.suptitle("Step 5  -  CALCULATE and Time Intelligence results",
                 fontsize=12.5, weight="bold", color=NAVY, y=1.04)
    fig.tight_layout()
    save(fig, "fig09_yoy.png")


# ============================================================ FIG 10 ytd
def fig_ytd():
    m = pd.read_csv(os.path.join(EXP, "monthly_sales_ytd.csv"), index_col=0)
    fig, ax = plt.subplots(figsize=(10.2, 3.4))
    xs = np.arange(len(m))
    ax.bar(xs, m.Sales, color=SKY, width=0.66, label="Monthly sales",
           edgecolor="white")
    ax2 = ax.twinx()
    ax2.plot(xs, m.YTD, color=NAVY, lw=2.3, marker="o", ms=3.4,
             label="Sales YTD (resets each January)")
    ax.set_xticks(xs[::2])
    ax.set_xticklabels(m.index[::2], rotation=45, ha="right", fontsize=7.6)
    ax.set_ylabel("Monthly sales", fontsize=9.6, weight="bold", color=BLUE)
    ax2.set_ylabel("Cumulative YTD", fontsize=9.6, weight="bold", color=NAVY)
    for x in [11.5, 23.5]:
        ax.axvline(x, color=AMBER, ls=":", lw=1.5)
    ax.set_title("Step 5  -  TOTALYTD behaviour: cumulative total resetting "
                 "at each year boundary", fontsize=12.3, weight="bold",
                 color=NAVY, pad=11)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.8, loc="upper left")
    ax.grid(axis="y", color="#EEF1F8", lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top",):
        ax.spines[sp].set_visible(False)
        ax2.spines[sp].set_visible(False)
    save(fig, "fig10_ytd.png")


# ============================================================ FIG 11 mockup
def fig_report_mockup():
    fig, ax = plt.subplots(figsize=(11.0, 5.4))
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 11.0, 5.4, facecolor="#F7F9FC",
                           edgecolor="#C8D4EE", lw=1.4))
    ax.add_patch(Rectangle((0, 4.95), 11.0, 0.45, facecolor=NAVY,
                           edgecolor="none"))
    ax.text(0.22, 5.17, "Sales Analysis  -  Vedant Nimkar (26MML0045)",
            fontsize=10.5, color="white", weight="bold", va="center")

    kpis = [("Total Sales", "8.96M", BLUE), ("Quantity", "22,448", NAVY),
            ("Total Profit", "4.83M", GREEN), ("Margin %", "53.96%", AMBER),
            ("YoY Growth", "+5.59%", GREEN)]
    x = 1.62
    for name, val, col in kpis:
        ax.add_patch(FancyBboxPatch(
            (x, 4.05), 1.75, 0.72,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor="white", edgecolor="#C8D4EE", lw=1.1))
        ax.add_patch(Rectangle((x, 4.70), 1.75, 0.07, facecolor=col,
                               edgecolor="none"))
        ax.text(x + 0.12, 4.53, name, fontsize=7.2, color=GREY,
                weight="bold")
        ax.text(x + 0.12, 4.20, val, fontsize=13, color=NAVY, weight="bold")
        x += 1.85

    # slicer panel
    ax.add_patch(FancyBboxPatch((0.14, 0.20), 1.32, 4.55,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor="white", edgecolor="#C8D4EE"))
    ax.text(0.80, 4.55, "FILTERS", ha="center", fontsize=7.4, weight="bold",
            color=BLUE)
    for i, sl in enumerate(["Year", "Category", "Region", "Segment",
                            "OrderStatus"]):
        ax.add_patch(FancyBboxPatch(
            (0.26, 4.06 - i * 0.55), 1.08, 0.38,
            boxstyle="round,pad=0.01,rounding_size=0.05",
            facecolor=LIGHT, edgecolor="#C8D4EE", lw=0.8))
        ax.text(0.80, 4.25 - i * 0.55, sl, ha="center", va="center",
                fontsize=7.0, color=NAVY)

    panels = [
        (1.62, 2.10, 4.35, 1.80, "Sales trend  vs  Sales PY", "line"),
        (6.15, 2.10, 4.70, 1.80, "Sales by category / year", "bar"),
        (1.62, 0.20, 4.35, 1.75, "Top 10 products by units", "hbar"),
        (6.15, 0.20, 4.70, 1.75, "YoY matrix by category", "matrix"),
    ]
    rngl = np.random.default_rng(4)
    for px, py, pw, ph, title, kind in panels:
        ax.add_patch(FancyBboxPatch(
            (px, py), pw, ph, boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor="white", edgecolor="#C8D4EE", lw=1.1))
        ax.text(px + 0.12, py + ph - 0.17, title, fontsize=7.8,
                weight="bold", color=NAVY)
        ix, iy = px + 0.25, py + 0.18
        iw, ih = pw - 0.45, ph - 0.52
        if kind == "line":
            t = np.linspace(0, 1, 30)
            for c, off in [(NAVY, 0.0), (SKY, -0.22)]:
                yv = iy + ih * (0.45 + off + 0.3 * np.sin(t * 6)
                                + 0.05 * rngl.standard_normal(30))
                ax.plot(ix + t * iw, np.clip(yv, iy, iy + ih), color=c,
                        lw=1.5)
        elif kind == "bar":
            for k in range(12):
                bx = ix + k * (iw / 12) + 0.02
                bh = ih * (0.25 + 0.7 * rngl.random())
                ax.add_patch(Rectangle((bx, iy), iw / 12 - 0.05, bh,
                                       facecolor=[SKY, BLUE, NAVY][k % 3],
                                       edgecolor="none"))
        elif kind == "hbar":
            for k in range(6):
                by = iy + k * (ih / 6) + 0.02
                bw = iw * (0.30 + 0.65 * rngl.random())
                ax.add_patch(Rectangle((ix, by), bw, ih / 6 - 0.06,
                                       facecolor=BLUE if k else GREEN,
                                       edgecolor="none"))
        else:
            for r in range(4):
                for c in range(4):
                    cw, ch = iw / 4, ih / 4
                    val = rngl.random()
                    fc = "white" if (r == 0 or c == 0) else (
                        "#DFF3E6" if val > 0.4 else "#FBE3E1")
                    ax.add_patch(Rectangle((ix + c * cw, iy + r * ch),
                                           cw, ch, facecolor=fc,
                                           edgecolor="#DDE4F0", lw=0.6))

    ax.text(5.5, -0.22, "Illustration of the Step 6 report layout - not a "
                        "screenshot of Power BI Desktop",
            ha="center", fontsize=8, color=GREY, style="italic")
    save(fig, "fig11_report_mockup.png")


if __name__ == "__main__":
    print("Generating figures...")
    fig_raw_preview()
    fig_data_issues()
    fig_cleansing_funnel()
    fig_clean_preview()
    fig_star_schema()
    fig_hierarchies()
    fig_top_products()
    fig_category_avg()
    fig_yoy()
    fig_ytd()
    fig_report_mockup()
    print("Done ->", FIG)
