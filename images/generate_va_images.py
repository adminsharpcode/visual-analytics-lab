"""
Generate the visual-analytics concept imagery used in the presentation.
All figures are synthetic illustrations of the proposed dashboard visuals.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)

NAVY = "#10245C"
BLUE = "#3366CC"
SKY = "#6FA3FF"
GREEN = "#1E7A4F"
AMBER = "#E0A020"
RED = "#C0392B"
GREY = "#5A5A5A"

ENERGY_CMAP = LinearSegmentedColormap.from_list(
    "energy", ["#0B1A3A", "#10245C", "#3366CC", "#6FA3FF",
               "#FFD27F", "#F5A623", "#D64545"])

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#B8C4DC",
    "axes.labelcolor": NAVY,
    "text.color": "#1C1C1C",
    "xtick.color": GREY,
    "ytick.color": GREY,
})


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=190, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote", name)


# ------------------------------------------------------------ 1 heatmap
def load_profile_heatmap():
    """Hour-of-day x day-of-week consumption fingerprint."""
    hours = np.arange(24)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    base = (1.4 + 0.9 * np.exp(-((hours - 8) ** 2) / 7)
            + 1.7 * np.exp(-((hours - 19.5) ** 2) / 9)
            + 0.35 * np.exp(-((hours - 13) ** 2) / 14))
    grid = np.zeros((7, 24))
    for d in range(7):
        weekend = d >= 5
        shape = base.copy()
        if weekend:
            shape = (1.5 + 1.1 * np.exp(-((hours - 11) ** 2) / 18)
                     + 1.5 * np.exp(-((hours - 20) ** 2) / 12))
        grid[d] = shape * (1 + 0.05 * rng.standard_normal(24))
    grid[2, 19] *= 1.55          # injected anomaly

    fig, ax = plt.subplots(figsize=(9.6, 3.5))
    im = ax.imshow(grid, aspect="auto", cmap=ENERGY_CMAP,
                   interpolation="nearest")
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}" for h in range(0, 24, 2)], fontsize=9)
    ax.set_yticks(range(7))
    ax.set_yticklabels(days, fontsize=10)
    ax.set_xlabel("Hour of day", fontsize=10.5, weight="bold")
    ax.set_title("Load-Profile Heatmap  -  consumption fingerprint (kWh)",
                 fontsize=13, weight="bold", color=NAVY, pad=11)
    cb = fig.colorbar(im, ax=ax, pad=0.015)
    cb.set_label("kWh", fontsize=9.5)
    cb.ax.tick_params(labelsize=8)

    ax.add_patch(Rectangle((18.5, 1.5), 1, 1, fill=False, edgecolor="white",
                           lw=2.2))
    ax.annotate("anomaly", xy=(19, 2), xytext=(21.4, 0.35), fontsize=9.5,
                color="white", weight="bold",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.6))
    for sp in ax.spines.values():
        sp.set_visible(False)
    save(fig, "heatmap_load_profile.png")


# ------------------------------------------------------------ 2 forecast
def forecast_chart():
    n_hist, n_fut = 96, 30
    t = np.arange(n_hist)
    trend = 210 + 0.42 * t
    seasonal = 26 * np.sin(2 * np.pi * t / 7) + 11 * np.sin(2 * np.pi * t / 30)
    hist = trend + seasonal + rng.normal(0, 8, n_hist)

    tf = np.arange(n_hist, n_hist + n_fut)
    fut = (210 + 0.42 * tf + 26 * np.sin(2 * np.pi * tf / 7)
           + 11 * np.sin(2 * np.pi * tf / 30))
    band = 11 + 0.75 * np.arange(n_fut)

    fig, ax = plt.subplots(figsize=(9.6, 3.5))
    ax.plot(t, hist, color=NAVY, lw=1.9, label="Actual consumption")
    ax.plot(tf, fut, color=BLUE, lw=2.2, ls="--", label="Forecast")
    ax.fill_between(tf, fut - 2 * band, fut + 2 * band, color=SKY,
                    alpha=0.30, label="95% interval")
    ax.fill_between(tf, fut - band, fut + band, color=SKY, alpha=0.45)
    ax.axvline(n_hist - 0.5, color=AMBER, lw=1.7, ls=":")
    ax.text(n_hist + 0.6, ax.get_ylim()[1] * 0.98, "today", fontsize=9.5,
            color=AMBER, weight="bold", va="top")
    ax.set_xlabel("Day index", fontsize=10.5, weight="bold")
    ax.set_ylabel("kWh", fontsize=10.5, weight="bold")
    ax.set_title("Demand Forecast with Uncertainty Band  -  Prophet-style "
                 "decomposition", fontsize=13, weight="bold", color=NAVY,
                 pad=11)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left", ncol=3)
    ax.grid(axis="y", color="#E4E9F4", lw=0.9)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "forecast_band.png")


# ------------------------------------------------------------ 3 anomaly
def anomaly_timeline():
    n = 150
    t = np.arange(n)
    sig = (170 + 20 * np.sin(2 * np.pi * t / 24)
           + 9 * np.sin(2 * np.pi * t / 7) + rng.normal(0, 5.5, n))
    spikes = [28, 63, 97, 128]
    for i, sp in enumerate(spikes):
        sig[sp] += 62 + 11 * i
    mu, sd = sig.mean(), sig.std()
    upper, lower = mu + 2.2 * sd, mu - 2.2 * sd
    flags = np.where((sig > upper) | (sig < lower))[0]

    fig, ax = plt.subplots(figsize=(9.6, 3.3))
    ax.fill_between(t, lower, upper, color="#EAF0FB",
                    label="Expected band (±2.2σ)")
    ax.plot(t, sig, color=NAVY, lw=1.6, label="Consumption")
    ax.scatter(flags, sig[flags], s=118, color=RED, zorder=5,
               edgecolor="white", lw=1.6, label="Anomaly flagged")
    for f in flags:
        ax.annotate(f"+{sig[f]-mu:.0f}", xy=(f, sig[f]),
                    xytext=(0, 11), textcoords="offset points",
                    ha="center", fontsize=8.5, color=RED, weight="bold")
    ax.axhline(mu, color=GREY, lw=1.0, ls="--")
    ax.set_xlabel("Time interval", fontsize=10.5, weight="bold")
    ax.set_ylabel("kWh", fontsize=10.5, weight="bold")
    ax.set_title("Automated Anomaly Detection  -  statistical control band",
                 fontsize=13, weight="bold", color=NAVY, pad=11)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left", ncol=3)
    ax.grid(axis="y", color="#EEF1F8", lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "anomaly_timeline.png")


# ------------------------------------------------------------ 4 clusters
def tsne_clusters():
    """t-SNE-style 2D map of daily load shapes."""
    specs = [
        ("Morning-peak homes", (-4.6, 3.4), 0.95, BLUE),
        ("Evening-peak homes", (4.3, 2.6), 1.05, NAVY),
        ("Flat / always-on", (0.4, -3.9), 0.85, GREEN),
        ("Night-shift users", (-4.9, -3.2), 0.80, AMBER),
        ("Irregular / anomalous", (4.9, -4.3), 1.35, RED),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    for name, (cx, cy), sd, col in specs:
        k = 70 if name != "Irregular / anomalous" else 34
        x = rng.normal(cx, sd, k)
        y = rng.normal(cy, sd, k)
        ax.scatter(x, y, s=44, color=col, alpha=0.62, edgecolor="white",
                   lw=0.5, label=name)
        ax.scatter([cx], [cy], s=290, facecolor="none", edgecolor=col,
                   lw=2.1, ls="--")
        ax.annotate(name, xy=(cx, cy), xytext=(0, -0.05),
                    textcoords="offset points", ha="center", fontsize=9,
                    weight="bold", color=col)
    ax.set_title("Load-Shape Clustering  -  t-SNE projection of daily "
                 "profiles", fontsize=12.5, weight="bold", color=NAVY, pad=11)
    ax.set_xlabel("t-SNE dimension 1", fontsize=10, weight="bold")
    ax.set_ylabel("t-SNE dimension 2", fontsize=10, weight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(color="#F0F3FA", lw=0.9)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_color("#D5DBE8")
    save(fig, "tsne_clusters.png")


# ------------------------------------------------------------ 5 sparkline grid
def sparkline_ranking():
    """Top-N consumers with sparklines - small-multiples pattern."""
    names = ["Block A - Tower 3", "Campus Lab Wing", "Cold Storage Unit",
             "Admin Building", "Hostel Cluster B", "Workshop Bay"]
    vals = [4820, 4310, 3990, 2760, 2440, 1880]
    deltas = [+12.4, -3.1, +21.8, +1.2, -6.7, +4.9]

    fig, axes = plt.subplots(len(names), 1, figsize=(8.6, 3.9))
    fig.suptitle("Top-N High-Consumption Entities  -  ranking with "
                 "sparklines and deltas", fontsize=12.5, weight="bold",
                 color=NAVY, y=1.04)
    mx = max(vals)
    for ax, nm, v, d in zip(axes, names, vals, deltas):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(0.0, 0.5, nm, fontsize=10, va="center", weight="bold",
                color=NAVY)
        ax.add_patch(FancyBboxPatch((0.30, 0.24), 0.30 * (v / mx), 0.52,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=BLUE, edgecolor="none",
                                    alpha=0.85))
        ax.text(0.615, 0.5, f"{v:,} kWh", fontsize=9.5, va="center",
                color="#1C1C1C")
        spark = np.cumsum(rng.normal(0, 1, 26)) + 6
        sx = np.linspace(0.72, 0.90, spark.size)
        sy = 0.26 + 0.48 * (spark - spark.min()) / (np.ptp(spark) + 1e-9)
        ax.plot(sx, sy, color=GREY, lw=1.25)
        ax.scatter([sx[-1]], [sy[-1]], s=17, color=RED, zorder=4)
        col = RED if d > 0 else GREEN
        arrow = "\u25b2" if d > 0 else "\u25bc"
        ax.text(0.945, 0.5, f"{arrow} {abs(d):.1f}%", fontsize=9.5,
                va="center", color=col, weight="bold")
    save(fig, "topn_sparklines.png")


# ------------------------------------------------------------ 6 architecture
def architecture_flow():
    fig, ax = plt.subplots(figsize=(11.2, 3.5))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 3.5)
    ax.axis("off")

    stages = [
        ("Smart Meters\nIoT / ESP32\nBilling Data", "#0B1A3A"),
        ("MQTT Gateway\nCloud Store", "#10245C"),
        ("ETL\nPower Query\nCleaning", BLUE),
        ("Star Schema\n+ DAX\nMeasures", "#4A7FD4"),
        ("ML Layer\nForecast\nAnomaly", GREEN),
        ("Power BI\nDashboard", AMBER),
    ]
    x = 0.15
    w, h = 1.62, 1.5
    for i, (label, col) in enumerate(stages):
        ax.add_patch(FancyBboxPatch(
            (x, 1.15), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            facecolor=col, edgecolor="none"))
        ax.text(x + w / 2, 1.15 + h / 2, label, ha="center", va="center",
                fontsize=9.3, color="white", weight="bold", linespacing=1.5)
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch(
                (x + w + 0.05, 1.9), (x + w + 0.30, 1.9),
                arrowstyle="-|>", mutation_scale=17, lw=2.1, color="#8895B5"))
        x += w + 0.35

    ax.text(5.6, 3.15, "End-to-End Data Flow", ha="center", fontsize=13.5,
            weight="bold", color=NAVY)
    ax.text(5.6, 0.62, "Data quality gates applied at every hand-off  -  "
                       "unit standardisation, missing-value treatment, "
                       "outlier handling, refresh validation",
            ha="center", fontsize=9.6, color=GREY, style="italic")
    save(fig, "architecture_flow.png")


if __name__ == "__main__":
    print("Generating imagery...")
    load_profile_heatmap()
    forecast_chart()
    anomaly_timeline()
    tsne_clusters()
    sparkline_ranking()
    architecture_flow()
    print("Done.")
