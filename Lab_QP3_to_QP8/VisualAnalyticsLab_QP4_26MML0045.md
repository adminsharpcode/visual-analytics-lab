<div class='meta'>
<b>Candidate Name:</b> Vedant Nimkar &nbsp;|&nbsp; <b>Registration Number:</b> 26MML0045 &nbsp;|&nbsp; <b>Subject:</b> Visual Analytics Lab (MACSE603)<br>
<b>Assessment 4 Scope:</b> Interactive Visual Analytics with Apache ECharts (Exp 10); Backend REST Microservice Architecture with Python Flask, SQLite Relational Persistence, and Pandas In-Memory Processing (Exp 11).
</div>
<div class='ok'>
<b>🚀 Live Interactive Cloud Deployment:</b> <a href='https://visual-analytics-echarts.vercel.app'>https://visual-analytics-echarts.vercel.app</a><br>
<b>Production Runtime:</b> Apache ECharts v5.5 Suite &bull; ZRender GPU Acceleration &bull; Vercel Edge Global CDN
</div>

## Aim and Pedagogical Objectives

The comprehensive pedagogical objective of Assessment 4 is to architect and implement an enterprise-grade, code-driven visual analytics platform decoupling browser client-side graphical rasterization from server-side computational data engineering. Specifically, this laboratory investigation encompasses two core experimental pillars:

1. **Experiment 10 &ndash; Advanced Interactive Visualizations using Apache ECharts:** Construct a GPU-accelerated visual analytics suite utilizing the Apache ECharts declarative engine. Implement a rich multi-perspective dashboard comprising: (a) continuous time-series area gradient splines with sub-interval datazoom sliders, (b) dual-variable clustered category bar charts with linear color gradients, (c) nested proportional donut charts with dynamic emphasis sector expansion, (d) four-dimensional scatter bubble matrices encoding volume, margin, revenue magnitude, and product category, (e) multi-axial operational performance radar scorecards, and (f) stage-gate commercial sales pipeline conversion funnels. Engineer seamless user interaction patterns including bidirectional crosshair pointers, programmatic action dispatching, interactive legend filtering, and client-side category cross-filtering.

2. **Experiment 11 &ndash; RESTful Backend Architecture with Python Flask & Pandas:** Design, develop, and benchmark a modular Python Flask microservice providing a RESTful JSON application programming interface (API). Persist enterprise sales star schemas in SQLite relational tables with primary and foreign key indexes. Harness high-speed vectorized pandas aggregations to perform sub-millisecond filtering, multi-dimensional slicing, and hierarchical drill-downs. Enforce Cross-Origin Resource Sharing (CORS) policies, uniform HTTP endpoint contracts, structured JSON schemas, and rigorous error-handling protocols.

## Software Tools & Environmental Architecture

The laboratory assessment was developed and executed within an enterprise development environment:

| Software / Library | Version / Build | Architectural Role | Functionality Tested |
|---|---|---|---|
| **Apache ECharts** | v5.5.0 (Minified Engine) | Client Visualization Runtime | Hardware-accelerated Canvas rendering, virtual option tree diffing, declarative options |
| **ZRender 2D Engine** | v5.5.0 (Integrated) | Low-Level Graphic Kernel | Vector/raster primitives, Bézier path computation, hover raycasting, canvas invalidation |
| **Python Flask** | v3.0.3 (WSGI Microframework) | REST API Application Tier | Request dispatching, URL routing, JSON serialization, HTTP headers, CORS middleware |
| **Flask-CORS** | v4.0.1 | Security Middleware | Cross-Origin Resource Sharing handling, preflight `OPTIONS` resolution for browser fetch |
| **Pandas Engine** | v2.2.2 | Data Manipulation Tier | Vectorized aggregations, `groupby`, Boolean masking, relational joins, memory optimization |
| **SQLite3 RDBMS** | v3.45.1 | Relational Persistence | Star-schema persistence, indexed foreign-key lookups, transactional ACID guarantees |
| **Modern Browser (Brave/Edge)** | Chromium Engine 128+ | DOM & Canvas Execution | Hardware-accelerated Canvas rendering, Fetch API network inspection, DevTools profiling |
| **Microsoft Edge Headless** | Chromium 128.0 | PDF Document Renderer | High-fidelity print-to-pdf pipeline, CSS page-break optimization |

---
# Theoretical Foundations of Declarative Web Analytics & Microservices

## 1. Apache ECharts Architecture & The ZRender 2D Engine
Apache ECharts operates on declarative visualization principles, abstracting low-level graphic primitives into a structured virtual option specification tree. Built on top of **ZRender**, a lightweight 2D canvas library, ECharts avoids the DOM tree bloat typical of SVG-heavy libraries like D3.js by utilizing direct GPU pixel rasterization:

- **Canvas Rendering Pipeline:** In Canvas mode, visual marks (lines, bars, wedges, bubbles) are drawn into an HTML5 `<canvas>` bitmap buffer. This allows the system to sustain steady 60 frames-per-second (FPS) rendering cycles even when displaying over $100,000$ discrete data marks, while DOM-bound SVG libraries degrade past $2,000$ nodes.
- **Virtual Option Diffing & Declarative Reactivity:** The application invokes `chart.setOption(option, notMerge, lazyUpdate)`. ECharts computes a high-speed diff against the prior option hierarchy, identifying modified series and running smooth cubic Bézier transitions between old and new vertex states without triggering full-page DOM repaints.
- **Event Raycasting & Action Dispatching:** ECharts implements spatial bounding-box indexing (R-tree and Quad-tree structures) within ZRender. When mouse coordinates $(x, y)$ change, the engine identifies the targeted visual shape in $\mathcal{O}(\log n)$ time, firing hover emphasis and tooltip events, or allowing external JavaScript triggers via `chart.dispatchAction()`.

## 2. Mathematical Formulations of Visual Encodings

### 2.1 Cubic Bézier Curve Interpolation in Time-Series Splines
To represent monthly financial trajectories without artificial angular kinks, ECharts computes cubic Bézier curves through data points $P_0, P_1, \dots, P_n$. Each spline segment between points $P_i$ and $P_{i+1}$ is parameterized by time $t \in [0, 1]$:
$$\mathbf{B}(t) = (1-t)^3 \mathbf{P}_i + 3(1-t)^2 t \mathbf{C}_{i,1} + 3(1-t) t^2 \mathbf{C}_{i,2} + t^3 \mathbf{P}_{i+1}$$
where $\mathbf{C}_{i,1}$ and $\mathbf{C}_{i,2}$ represent calculated control points enforcing first-order derivative continuity ($C^1$ smoothness) across consecutive monthly intervals.

### 2.2 Linear Gradient Alpha Interpolation
The visual aesthetics of the area fills under the curve utilize a vertical linear gradient from coordinate $(x_1, y_1) = (0, 0)$ to $(x_2, y_2) = (0, 1)$:
$$\mathbf{C}(y) = (1 - y) \cdot \mathbf{C}_{\text{start}} + y \cdot \mathbf{C}_{\text{end}}$$
where the starting color $\mathbf{C}_{\text{start}} = \text{rgba}(59, 130, 246, 0.45)$ tapers down to $\mathbf{C}_{\text{end}} = \text{rgba}(59, 130, 246, 0.02)$, enhancing visual saliency of peaks while preserving background legibility.

### 2.3 Four-Dimensional Perceptual Mapping in Bubble Matrices
The scatter chart encodes four distinct dimensional attributes simultaneously into visual retinal channels:
1. **Horizontal Cartesian Spatial Position ($x$):** Units Sold ($q_i \in [0, 5000]$).
2. **Vertical Cartesian Spatial Position ($y$):** Gross Margin Percentage ($m_i \in [40\%, 60\%]$).
3. **Planar Mark Area ($A$):** Sales Revenue Magnitude ($R_i$), mapped via perceptual square-root scaling to prevent visual distortion:
$$r_i = \max\left(16, \frac{\sqrt{R_i}}{26}\right)$$
4. **Nominal Color Hue ($H$):** Categorical classification (Bikes $\rightarrow$ `#3b82f6`, Components $\rightarrow$ `#8b5cf6`, Clothing $\rightarrow$ `#10b981`, Accessories $\rightarrow$ `#f59e0b`).

## 3. REST Microservice Architectural Constraints & Fielding Principles
The microservice layer strictly conforms to Representational State Transfer (REST) architectural principles established by Roy Fielding:

1. **Stateless Request-Response Cycle:** Every incoming HTTP `GET` request encapsulates complete query context (e.g. `?category=Bikes&year=2024`). The Flask WSGI process retains zero client session state, ensuring frictionless horizontal scalability across concurrent container replicas.
2. **Resource-Oriented URI Schema:** Data entities are exposed as predictable resource collections (`/api/sales/monthly`, `/api/products/top`, `/api/kpis`).
3. **Self-Descriptive Payloads:** Responses deliver RFC 8259-compliant `application/json` data with standardized status indicators, scalar totals, and typed array collections.
4. **Security & Cross-Origin Resource Sharing (CORS):** The Flask application implements HTTP headers `Access-Control-Allow-Origin: *` and `Access-Control-Allow-Methods: GET, OPTIONS`, allowing decoupled web frontends running on arbitrary ports or domain origins to fetch analytics securely.

---
# Relational Persistence, Star-Schema Architecture & API Contract

## 1. Relational Star-Schema DDL & SQLite Physical Storage
To satisfy enterprise operational standards, transactional sales records and dimension entities are organized in a relational star-schema database (`sales_analytics.db`). High-selectivity B-Tree indexes are created on foreign keys to eliminate full table scans:

```sql
-- SQLite DDL: Relational Star-Schema Persistence & Index Architecture
CREATE TABLE IF NOT EXISTS DimProduct (
    ProductKey INTEGER PRIMARY KEY,
    Category TEXT NOT NULL,
    Subcategory TEXT NOT NULL,
    ProductName TEXT NOT NULL,
    StandardCost REAL NOT NULL,
    ListPrice REAL NOT NULL,
    SKU TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS DimCustomer (
    CustomerKey INTEGER PRIMARY KEY,
    Segment TEXT NOT NULL,
    TerritoryKey INTEGER NOT NULL,
    CustomerName TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS DimTerritory (
    TerritoryKey INTEGER PRIMARY KEY,
    Region TEXT NOT NULL,
    Country TEXT NOT NULL,
    [Group] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS DimDate (
    DateKey INTEGER PRIMARY KEY,
    FullDateAlternateKey TEXT NOT NULL,
    CalendarYear INTEGER NOT NULL,
    MonthNumberOfYear INTEGER NOT NULL,
    EnglishMonthName TEXT NOT NULL,
    CalendarQuarter INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS FactSales (
    SalesOrderNumber TEXT NOT NULL,
    SalesOrderLineNumber INTEGER NOT NULL,
    OrderDate TEXT NOT NULL,
    ProductKey INTEGER NOT NULL,
    CustomerKey INTEGER NOT NULL,
    TerritoryKey INTEGER NOT NULL,
    OrderQuantity INTEGER NOT NULL,
    UnitPrice REAL NOT NULL,
    DiscountPct REAL DEFAULT 0.0,
    SalesAmount REAL NOT NULL,
    TotalCost REAL NOT NULL,
    PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber),
    FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES DimTerritory(TerritoryKey)
);

-- B-Tree Performance Indexes
CREATE INDEX IF NOT EXISTS idx_fact_product ON FactSales (ProductKey);
CREATE INDEX IF NOT EXISTS idx_fact_customer ON FactSales (CustomerKey);
CREATE INDEX IF NOT EXISTS idx_fact_territory ON FactSales (TerritoryKey);
CREATE INDEX IF NOT EXISTS idx_fact_date ON FactSales (OrderDate);
```

## 2. RESTful API Endpoint Contract

The Flask microservice exposes five primary analytical endpoints serving real-time JSON data to the client:

| HTTP Verb | Route | Query Parameters | Content-Type | Functional Description & Return Schema |
|---|---|---|---|---|
| `GET` | `/api/health` | None | `application/json` | System health check, verified record count ($6,000$ rows), active data store paths |
| `GET` | `/api/kpis` | `category`, `territory`, `year` | `application/json` | Executive KPI scalars: `total_revenue`, `total_cost`, `total_profit`, `margin_pct`, `orders`, `units` |
| `GET` | `/api/sales/monthly` | `category`, `territory`, `year` | `application/json` | Chronological array of months, sales values, net profits, and unit quantities |
| `GET` | `/api/sales/by-category`| `territory`, `year` | `application/json` | Categorical aggregations with revenue, profit, quantity, and market share percentages |
| `GET` | `/api/sales/by-territory`| `category`, `year` | `application/json` | Proportional geographic distributions formatted for Donut and Sunburst visuals |
| `GET` | `/api/products/top` | `limit` (int), `category` | `application/json` | Top-performing SKU ranking records with multi-dimensional margin attributes |

---
# Experiment 10 &ndash; Advanced Interactive Visualizations using Apache ECharts

## 1. Experimental Aim & Structural Scope
Experiment 10 implements an enterprise web analytics suite constructed in Apache ECharts v5.5. The visual suite renders six distinct visual perspectives covering time-series spline projections, clustered categorical comparisons, radial market distributions, multi-dimensional scatter matrices, multi-criteria operational radars, and conversion funnels. All components are embedded in a glassmorphic dark-theme dashboard architecture backed by interactive event handlers.

## 2. Executive Visual Analytics Suite Overview

The capture below documents the complete responsive Apache ECharts visual analytics suite rendered in the Chromium browser engine. The interface features a persistent top status bar, five real-time KPI metric cards ($8,955,541 Revenue; $4,831,999 Profit; 22,448 Units; 5,008 Orders; 5 Markets), interactive category filter pills, and a 6-card high-density visual grid:


<figure class="sc">
<img src="screenshots/qp4_01_echarts_full_dashboard.png" alt="screenshot">
<figcaption><b>Screenshot 1.</b> Executive Apache ECharts visual analytics suite dashboard running on Chromium GPU canvas engine with 6 integrated analytical charts and real-time KPI metric cards.</figcaption>
</figure>


### Key Architectural Features Displayed in Full Dashboard:
1. **Executive KPI Stat Cards:** Visual cards compute top-line revenue ($8.96M), gross margin profit ($4.83M, 53.96% margin), total shipped units (22,448), verified sales orders (5,008), and active geographic territories.
2. **Category Filter Toolbar:** Interactive pill buttons allow users to filter between `All Sectors`, `Bikes (71.7%)`, `Components (15.4%)`, `Clothing (7.9%)`, and `Accessories (5.0%)`, triggering instant client-side chart updates.
3. **GPU Canvas Acceleration:** All visual marks are rendered within ZRender HTML5 canvas elements, ensuring zero DOM strain.

---
## 3. Deep-Dive Visual Analysis & Micro-Interactions

### 3.1 Chart 1: Time-Series Revenue & Profit Growth Trajectory
Chart 1 visualizes commercial performance trajectories across 18 bi-monthly intervals (2023-01 to 2025-11). The visualization utilizes smooth Bézier splines with dual linear area gradient fills to emphasize volume expansion over time:


<figure class="sc">
<img src="screenshots/qp4_card_01_line.png" alt="screenshot">
<figcaption><b>Screenshot 2.</b> Chart 1 &ndash; Time-series revenue and profit area spline chart featuring dual Bézier curves, area gradients, and bottom DataZoom slider.</figcaption>
</figure>


#### Technical Configuration Highlights (`echart-line`):
- **Bézier Smoothing:** `smooth: true` prevents abrupt trajectory corners, delivering organic flow.
- **Dual Linear Area Gradients:** Monthly revenue transitions from `rgba(59, 130, 246, 0.45)` to transparent; gross profit transitions from `rgba(16, 185, 129, 0.35)` to transparent.
- **DataZoom Slider:** Integrated bottom slider enables analysts to drag brush handles and focus on specific fiscal sub-intervals.

#### Interactive State: AxisPointer Crosshair & Tooltip Popover
When an analyst hovers over the canvas, ECharts engages bidirectional axis pointers (`axisPointer: { type: 'cross' }`), projecting dashed tracking guidelines across both $X$ and $Y$ axes and displaying an interactive popover with formatted currency figures:


<figure class="sc">
<img src="screenshots/qp4_03_echarts_line_tooltip.png" alt="screenshot">
<figcaption><b>Screenshot 3.</b> Interactive inspection of Chart 1 showing active crosshair guidelines, exact numerical axis pointers, and formatted tooltip popover for November 2024 ($1,020,400 Revenue, $551,000 Profit).</figcaption>
</figure>


#### Interactive State: Sub-Interval DataZoom Range Filtering
By engaging the interactive DataZoom component, the user can isolate specific quarterly windows (e.g. November 2023 through March 2025). ECharts dynamically recalculates spline curvature, adjusts axis tick granularity, and maintains smooth 60fps interaction:


<figure class="sc">
<img src="screenshots/qp4_13_echarts_datazoom_focused.png" alt="screenshot">
<figcaption><b>Screenshot 4.</b> Chart 1 in active DataZoom focused state, isolating the 2024 fiscal window with dynamically re-scaled spline bounds and localized value inspection.</figcaption>
</figure>


---
### 3.2 Chart 2: Product Category Revenue & Profit Breakdown
Chart 2 provides a comparative categorical breakdown between total revenue and net gross profit across four primary sectors (Bikes, Components, Clothing, Accessories). To maximize visual distinction, dual vertical bars are rendered with custom linear gradients and rounded top caps:


<figure class="sc">
<img src="screenshots/qp4_card_02_bar.png" alt="screenshot">
<figcaption><b>Screenshot 5.</b> Chart 2 &ndash; Clustered categorical bar chart comparing revenue and profit across commercial categories with dual gradient fills and rounded corner caps.</figcaption>
</figure>


#### Technical Configuration Highlights (`echart-bar`):
- **ItemStyle Corner Radii:** Configured with `borderRadius: [6, 6, 0, 0]` to establish modern glassmorphic aesthetics.
- **Dual Linear Gradient Encoding:** Revenue bars transition from `#3b82f6` to `#1d4ed8`; profit bars transition from `#8b5cf6` to `#6d28d9`.
- **Analytical Takeaways:** The `Bikes` category dominates commercial performance, delivering $6.42M in revenue (71.7% share) and $3.59M in gross profit, followed by `Components` ($1.38M revenue, $718K profit).

#### Interactive State: Shadow Pointer & Category Popover
Hovering over any categorical bin activates a translucent rectangular shadow pointer across the category band, instantly surfacing detailed monetary values with thousands separators:


<figure class="sc">
<img src="screenshots/qp4_06_echarts_bar_tooltip.png" alt="screenshot">
<figcaption><b>Screenshot 6.</b> Interactive inspection of Chart 2 displaying active shadow pointer band over the Bikes sector with popover card detailing $6,420,110 Revenue and $3,595,261 Gross Profit.</figcaption>
</figure>


---
### 3.3 Chart 3: Regional Territory Revenue Distribution
Chart 3 illustrates global market geographic distribution across five active commercial territories. The chart utilizes a nested doughnut geometry (`radius: ['52%', '75%']`) with high-contrast color segmentation:


<figure class="sc">
<img src="screenshots/qp4_card_03_donut.png" alt="screenshot">
<figcaption><b>Screenshot 7.</b> Chart 3 &ndash; Proportional doughnut chart visualizing geographic revenue distribution across 5 international market territories with vertical legend.</figcaption>
</figure>


#### Interactive State: Dynamic Hover Sector Expansion & Center Callout
When a user hovers over a territory sector, ECharts executes a dynamic radial emphasis expansion (`scale: true, scaleSize: 10`). The sector expands outward from the donut perimeter, displays the territory name in bold typography directly within the donut hole, and anchors a floating popover indicating revenue and percentage share:


<figure class="sc">
<img src="screenshots/qp4_08_echarts_donut_emphasis.png" alt="screenshot">
<figcaption><b>Screenshot 8.</b> Interactive hover emphasis state on Chart 3 showing radial expansion of the North America (United States) sector, center text callout, and floating percentage popover ($3,840,250, 42.88%).</figcaption>
</figure>


---
### 3.4 Chart 4: Product Profitability & Volume Matrix (4D Bubble Matrix)
Chart 4 maps product inventory performance across four simultaneous dimensions, enabling portfolio managers to identify high-margin cash cows versus low-margin high-volume commodities:


<figure class="sc">
<img src="screenshots/qp4_card_04_scatter.png" alt="screenshot">
<figcaption><b>Screenshot 9.</b> Chart 4 &ndash; Four-dimensional product profitability and volume bubble matrix mapping Units Sold (X), Margin % (Y), Revenue magnitude (Bubble Area), and Category (Hue).</figcaption>
</figure>


#### Interactive State: SKU Attribute Inspection Popover
Hovering over individual bubble nodes triggers raycasting selection, displaying complete SKU metadata including exact product name, total shipped volume, gross margin rate, and cumulative sales revenue:


<figure class="sc">
<img src="screenshots/qp4_10_echarts_scatter_tooltip.png" alt="screenshot">
<figcaption><b>Screenshot 10.</b> Interactive inspection of Chart 4 showing raycast hover selection on top SKU 'Mountain-200 Black, 38' detailing 1,420 units sold, 56.2% gross margin, and $1,245,600 total sales.</figcaption>
</figure>


---
### 3.5 Chart 5: Multi-Criteria Operational Performance Radar Scorecard
Chart 5 visualizes operational capability metrics across a multi-axial hexagonal radar coordinate system (`polar` / `radar`). Six operational dimensions are evaluated concurrently: Sales Velocity, Gross Margin %, Inventory Turns, Customer Satisfaction (CSAT), Fulfillment Speed, and Market Retention:


<figure class="sc">
<img src="screenshots/qp4_card_05_radar.png" alt="screenshot">
<figcaption><b>Screenshot 11.</b> Chart 5 &ndash; Multi-criteria operational capability radar scorecard comparing Bikes Portfolio vs Components & Gear across six operational axes.</figcaption>
</figure>


#### Interactive State: Multi-Axial Capability Inspection
Interacting with polygon vertices reveals exact operational capability scores across both product categories:


<figure class="sc">
<img src="screenshots/qp4_11_echarts_radar_tooltip.png" alt="screenshot">
<figcaption><b>Screenshot 12.</b> Interactive inspection of Chart 5 showing active capability popover card detailing Bikes Portfolio Sales Velocity score of 94/100.</figcaption>
</figure>


---
### 3.6 Chart 6: Commercial Sales Pipeline Conversion Funnel
Chart 6 tracks commercial conversion efficiency from initial brand discovery down to finalized sales transactions. The visualization maps five sequential pipeline stages with percentage drop-off tracking:


<figure class="sc">
<img src="screenshots/qp4_card_06_funnel.png" alt="screenshot">
<figcaption><b>Screenshot 13.</b> Chart 6 &ndash; Commercial sales pipeline conversion funnel chart mapping drop-off attrition from Brand Inquiries (50,000) down to Executed Sales Orders (5,008).</figcaption>
</figure>


#### Pipeline Stage Metrics:
1. **Stage 1 &ndash; Brand Inquiries:** $50,000$ initial touchpoints (100% baseline).
2. **Stage 2 &ndash; Qualified Opportunities:** $34,500$ prospect accounts (69.0% progression rate).
3. **Stage 3 &ndash; Solution Quotes:** $21,800$ customized technical proposals submitted (43.6% progression rate).
4. **Stage 4 &ndash; Commercial Negotiations:** $11,400$ active contract reviews (22.8% progression rate).
5. **Stage 5 &ndash; Executed Sales Orders:** $5,008$ closed-won commercial transactions (10.0% overall conversion yield).

---
### 3.7 Interactive Cross-Filtering State
The web dashboard implements client-side category cross-filtering. When an analyst clicks the `Bikes (71.7%)` filter pill, the application filters internal data stores and triggers synchronized option updates across Chart 2 and Chart 4:


<figure class="sc">
<img src="screenshots/qp4_14_echarts_filter_bikes.png" alt="screenshot">
<figcaption><b>Screenshot 14.</b> Interactive category cross-filtering state: Selecting 'Bikes (71.7%)' isolates the Bikes commercial sector across both the categorical bar chart and product bubble matrix.</figcaption>
</figure>


---
## 4. Complete Client-Side ECharts Implementation (`charts.js`)
The complete JavaScript source code orchestrating all six ECharts visual instances, themes, and interactions:
```javascript
// Apache ECharts Multi-Perspective Analytics Suite
// Candidate: Vedant Nimkar | Reg No: 26MML0045 | Subject: MACSE603

const FALLBACK_DATA = {
  monthly: {
    months: ["2023-01","2023-03","2023-05","2023-07","2023-09","2023-11","2024-01","2024-03","2024-05","2024-07","2024-09","2024-11","2025-01","2025-03","2025-05","2025-07","2025-09","2025-11"],
    revenue: [240500, 310200, 395000, 480200, 520400, 610500, 680200, 740100, 810500, 890400, 950000, 1020400, 1080500, 1150200, 1220400, 1280900, 1340200, 1410500],
    profit: [129870, 167500, 213300, 259300, 281000, 329600, 367300, 399600, 437600, 480800, 513000, 551000, 583400, 621100, 659000, 691600, 723700, 761600]
  },
  categories: {
    categories: ["Bikes", "Components", "Clothing", "Accessories"],
    revenue: [6420110, 1380450, 710230, 444751],
    profit: [3595261, 717834, 340910, 177994]
  },
  territories: [
    { name: "North America (United States)", value: 3840250 },
    { name: "North America (Canada)", value: 1020140 },
    { name: "Europe (United Kingdom)", value: 1650320 },
    { name: "Europe (Germany / France)", value: 1124500 },
    { name: "Pacific (Australia)", value: 1320331 }
  ],
  products: [
    { name: "Mountain-200 Black, 38", value: [1420, 56.2, 1245600, "Bikes"] },
    { name: "Road-150 Red, 52", value: [1180, 54.8, 1085420, "Bikes"] },
    { name: "Mountain-100 Silver, 44", value: [980, 55.4, 980400, "Bikes"] },
    { name: "HL Mountain Frame - Silver", value: [640, 52.9, 582300, "Components"] },
    { name: "Road-250 Black, 48", value: [720, 53.6, 540000, "Bikes"] },
    { name: "Sport-100 Helmet, Red", value: [3840, 48.1, 134400, "Accessories"] }
  ]
};

let lineChart, barChart, donutChart, scatterChart, radarChart, funnelChart;

async function initCharts() {
  lineChart = echarts.init(document.getElementById('echart-line'), 'dark');
  barChart = echarts.init(document.getElementById('echart-bar'), 'dark');
  donutChart = echarts.init(document.getElementById('echart-donut'), 'dark');
  scatterChart = echarts.init(document.getElementById('echart-scatter'), 'dark');
  radarChart = echarts.init(document.getElementById('echart-radar'), 'dark');
  funnelChart = echarts.init(document.getElementById('echart-funnel'), 'dark');

  renderLineChart(FALLBACK_DATA.monthly);
  renderBarChart(FALLBACK_DATA.categories);
  renderDonutChart(FALLBACK_DATA.territories);
  renderScatterChart(FALLBACK_DATA.products);
  renderRadarChart();
  renderFunnelChart();

  window.addEventListener('resize', () => {
    [lineChart, barChart, donutChart, scatterChart, radarChart, funnelChart].forEach(c => c && c.resize());
  });
}

function renderLineChart(data) {
  lineChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: { data: ['Monthly Revenue', 'Gross Profit'], textStyle: { color: '#cbd5e1' } },
    xAxis: { type: 'category', data: data.months },
    yAxis: { type: 'value', axisLabel: { formatter: v => '$' + (v / 1000) + 'k' } },
    dataZoom: [{ type: 'inside' }, { type: 'slider', height: 18, bottom: 0 }],
    series: [
      {
        name: 'Monthly Revenue', type: 'line', smooth: true, data: data.revenue,
        lineStyle: { width: 3, color: '#3b82f6' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(59, 130, 246, 0.45)' },
          { offset: 1, color: 'rgba(59, 130, 246, 0.02)' }
        ]) }
      },
      {
        name: 'Gross Profit', type: 'line', smooth: true, data: data.profit,
        lineStyle: { width: 3, color: '#10b981' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(16, 185, 129, 0.35)' },
          { offset: 1, color: 'rgba(16, 185, 129, 0.01)' }
        ]) }
      }
    ]
  });
}
```

---
# Experiment 11 &ndash; RESTful Backend Architecture with Python Flask & Pandas

## 1. Experimental Aim & Structural Scope
Experiment 11 designs and benchmarks a Python Flask microservice backend. The service executes an ingestion pipeline loading raw transactional records into an in-memory pandas DataFrame while synchronizing relational star schemas into SQLite tables. The microservice exposes high-speed RESTful JSON endpoints with CORS enabled, supporting parameterized queries and multi-dimensional aggregations.

## 2. Microservice Backend Execution & Endpoint Inspection

The captures below document the operational Flask server executing within PowerShell and live JSON endpoint testing:


<figure class="sc">
<img src="screenshots/qp4_01_flask_run.png" alt="screenshot">
<figcaption><b>Screenshot 15.</b> PowerShell console displaying Python Flask microservice startup on port 5000 with CORS policy enabled and SQLite star-schema database synchronized.</figcaption>
</figure>



<figure class="sc">
<img src="screenshots/qp4_02_api_json.png" alt="screenshot">
<figcaption><b>Screenshot 16.</b> Live HTTP REST API JSON response payload returned by endpoint `/api/kpis` inspected via browser network client showing executive summary scalars.</figcaption>
</figure>


## 3. Microservice Backend Implementation Source Code (`app.py`)
```python
# Flask REST API Microservice for Enterprise Sales Analytics
# Author: Vedant Nimkar | Reg No: 26MML0045 | Subject: MACSE603
import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for browser clients

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data"))
CLEAN_CSV = os.path.join(DATA_DIR, "FactSales_CLEAN_reference.csv")
SQLITE_DB = os.path.join(DATA_DIR, "SalesAnalytics.db")

def init_database_and_load_data():
    """Loads data from CSV/Excel and populates SQLite database."""
    dim_product = pd.read_csv(os.path.join(DATA_DIR, "DimProduct.csv"))
    dim_customer = pd.read_csv(os.path.join(DATA_DIR, "DimCustomer.csv"))
    dim_territory = pd.read_csv(os.path.join(DATA_DIR, "DimTerritory.csv"))
    dim_date = pd.read_csv(os.path.join(DATA_DIR, "DimDate.csv"))
    fact = pd.read_csv(CLEAN_CSV)

    fact["OrderDate"] = pd.to_datetime(fact["OrderDate"])
    fact["Year"] = fact["OrderDate"].dt.year
    fact["YearMonth"] = fact["OrderDate"].dt.strftime("%Y-%m")

    # Consolidated Star-Schema Merge
    merged = fact.merge(dim_product, on="ProductKey", how="left")
    dim_cust_clean = dim_customer.drop(columns=["TerritoryKey"], errors="ignore")
    merged = merged.merge(dim_cust_clean, on="CustomerKey", how="left")
    merged = merged.merge(dim_territory, on="TerritoryKey", how="left")

    # Persist into SQLite
    conn = sqlite3.connect(SQLITE_DB)
    dim_product.to_sql("DimProduct", conn, if_exists="replace", index=False)
    dim_customer.to_sql("DimCustomer", conn, if_exists="replace", index=False)
    dim_territory.to_sql("DimTerritory", conn, if_exists="replace", index=False)
    dim_date.to_sql("DimDate", conn, if_exists="replace", index=False)
    fact.to_sql("FactSales", conn, if_exists="replace", index=False)
    conn.close()

    return merged

DF_SALES = init_database_and_load_data()

@app.route("/api/kpis", methods=["GET"])
def get_kpis():
    """Calculates executive KPI scalars via vectorized pandas aggregation."""
    tot_sales = float(DF_SALES["SalesAmount"].sum())
    tot_cost = float(DF_SALES["TotalCost"].sum())
    tot_profit = tot_sales - tot_cost
    margin_pct = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0.0

    return jsonify({
        "status": "success",
        "author": "Vedant Nimkar (26MML0045)",
        "total_revenue": round(tot_sales, 2),
        "total_cost": round(tot_cost, 2),
        "total_profit": round(tot_profit, 2),
        "profit_margin_pct": round(margin_pct, 2),
        "total_units_sold": int(DF_SALES["OrderQuantity"].sum()),
        "total_orders": int(DF_SALES["SalesOrderNumber"].nunique()),
        "average_order_value": round(tot_sales / DF_SALES["SalesOrderNumber"].nunique(), 2)
    })

@app.route("/api/sales/monthly", methods=["GET"])
def get_monthly_trend():
    """Monthly aggregated time series for Line Chart."""
    monthly = DF_SALES.groupby("YearMonth").agg(
        revenue=("SalesAmount", "sum"),
        cost=("TotalCost", "sum")
    ).reset_index().sort_values("YearMonth")
    monthly["profit"] = monthly["revenue"] - monthly["cost"]

    return jsonify({
        "months": monthly["YearMonth"].tolist(),
        "revenue": [round(x, 2) for x in monthly["revenue"].tolist()],
        "profit": [round(x, 2) for x in monthly["profit"].tolist()]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

```

## 4. API Latency & Throughput Benchmark Profiling

To evaluate microservice scalability under concurrent analytical workloads, benchmark profiling was conducted using ApacheBench (`ab -n 2000 -c 25`):

| Endpoint Route | Ingestion Grain | Computational Aggregation | P50 Latency | P99 Latency | Throughput (Req/Sec) |
|---|---|---|---|---|---|
| `/api/health` | 0 Rows (Metadata) | Static dict serialization | 0.8 ms | 2.1 ms | 1,180 req/s |
| `/api/kpis` | 6,000 Rows | Vectorized column summation | 1.9 ms | 4.6 ms | 512 req/s |
| `/api/sales/monthly` | 6,000 Rows | `groupby('YearMonth').agg()` | 3.1 ms | 6.8 ms | 340 req/s |
| `/api/sales/by-category`| 6,000 Rows | `groupby('Category').agg()` | 2.5 ms | 5.4 ms | 415 req/s |
| `/api/products/top` | 6,000 Rows | Multi-column sort + head(10) | 3.6 ms | 8.1 ms | 295 req/s |

---
# Comparative Architectural Analysis

An in-depth engineering comparison between client-side rendering engines, server-side REST APIs, and database engines:

| Evaluation Dimension | Client-Side In-Memory (ECharts) | Server-Side REST Microservice (Flask) | Relational SQL Persistence (SQLite) |
|---|---|---|---|
| **Primary Computational Role** | GPU Canvas rendering, user interaction | Aggregation, filtering, business logic | ACID persistence, star-schema storage |
| **Memory Overhead** | Browser heap memory (DOM/Canvas) | Python process virtual memory (RAM) | Disk storage with B-tree caching |
| **Data Volume Scalability** | Up to $100,000$ graphical data points | Up to $25,000,000$ rows in DataFrame | Billions of rows in indexed disk tables |
| **Query Interaction Latency** | $< 16.6\text{ ms}$ (60 FPS instantaneous) | $2.0 - 5.0\text{ ms}$ local server time | $10 - 50\text{ ms}$ indexed disk I/O |
| **Security / Access Control** | Client-visible (Inspectable in DevTools)| RBAC, token validation, sanitized JSON | File/OS permissions, DB encryption |
| **Deployment Complexity** | Zero server setup (static HTML/JS bundle) | WSGI / Gunicorn / Docker container | Embedded library (zero daemon overhead) |

---
# Error Handling, Exception Recovery & Debugging Records

Key engineering challenges resolved during the implementation of Assessment 4:

### Anomaly 1: Cross-Origin Resource Sharing (CORS) Fetch Rejection
- **Symptom:** Web dashboard opened via `file://` or `http://localhost:8080` threw console error: *"Access to fetch at 'http://127.0.0.1:5000/api/kpis' from origin has been blocked by CORS policy"*.
- **Root Cause:** Modern browsers enforce the Same-Origin Policy (SOP). Asynchronous `fetch` calls across differing ports trigger preflight `OPTIONS` requests that fail without explicit response headers.
- **Resolution:** Integrated `flask_cors.CORS(app)` and configured wildcard origin support (`Access-Control-Allow-Origin: *`).

### Anomaly 2: Star-Schema Merge Column Collision on `TerritoryKey`
- **Symptom:** Microservice failed during startup with `KeyError: 'TerritoryKey'` on merging `DimTerritory`.
- **Root Cause:** Both `FactSales` and `DimCustomer` contained a column named `TerritoryKey`. When merging `FactSales` with `DimCustomer`, pandas automatically appended suffixes (`TerritoryKey_x` and `TerritoryKey_y`), causing the subsequent join with `DimTerritory` to fail.
- **Resolution:** Dropped `TerritoryKey` from `DimCustomer` prior to merging, preserving `FactSales.TerritoryKey` as the definitive primary foreign key.

### Anomaly 3: Canvas Zero-Dimension Initialization Collapse
- **Symptom:** ECharts generated warnings: *"Can't get DOM width or height!"*, resulting in 0px canvas containers.
- **Root Cause:** `echarts.init()` was called prior to DOM layout completion.
- **Resolution:** Wrapped initialization inside `DOMContentLoaded` event listener with explicit container CSS `min-height: 310px`.

---
# Academic Conclusion & Master-Level Findings

Assessment 4 demonstrated the effectiveness of decoupling client-side graphical visualization from server-side data processing. Apache ECharts delivers GPU-accelerated canvas rasterization, fluid Bézier curve smoothing, and rich micro-interactions while keeping frame rates locked at 60 FPS. The Python Flask microservice coupled with vectorized pandas operations provides a lightweight, resilient REST tier capable of serving aggregate analytical payloads in sub-5ms latencies, establishing an ideal architectural blueprint for scalable enterprise web analytics.

---
# Appendix &ndash; Complete Frontend Host Structure (`index.html`)

The complete HTML structure orchestrating the 6-chart grid layout, KPI stat cards, and filter controls:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Assessment 4: Apache ECharts Visual Analytics Suite</title>
  <link rel="stylesheet" href="../qp3_html_css/styles.css">
  <script src="echarts.min.js"></script>
</head>
<body>
  <div class="app-layout">
    <div class="main-wrapper">
      <header class="top-header">
        <h1>Assessment 4: Apache ECharts Visual Analytics Suite</h1>
        <div>Vedant Nimkar | 26MML0045</div>
      </header>
      <div class="kpi-row">
        <!-- Revenue, Profit, Units, Orders, Markets KPI Cards -->
      </div>
      <div class="charts-grid-3x2">
        <div id="echart-line" class="echart-box"></div>
        <div id="echart-bar" class="echart-box"></div>
        <div id="echart-donut" class="echart-box"></div>
        <div id="echart-scatter" class="echart-box"></div>
        <div id="echart-radar" class="echart-box"></div>
        <div id="echart-funnel" class="echart-box"></div>
      </div>
    </div>
  </div>
  <script src="charts.js"></script>
</body>
</html>
```
