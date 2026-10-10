/**
 * ============================================================================
 * Apache ECharts Multi-Perspective Visual Analytics Engine
 * Subject: Visual Analytics Lab (MACSE603)
 * Student: Vedant Nimkar | 26MML0045
 * Enterprise-Grade Interactive Analytics Architecture
 * Features: Multi-dimensional Filtering, 6 GPU Charts, Cross-filtering, SKU Table
 * ============================================================================
 */

// Comprehensive Master Dataset (Star-Schema Verified)
const ENTERPRISE_DATA = {
  // Monthly time-series data across years (2023, 2024, 2025)
  monthly: [
    { month: '2023-01', year: '2023', revenue: 240500, profit: 129870, units: 620, Bikes: 172000, Components: 37000, Clothing: 19000, Accessories: 12500 },
    { month: '2023-03', year: '2023', revenue: 310200, profit: 167500, units: 790, Bikes: 222000, Components: 48000, Clothing: 24500, Accessories: 15700 },
    { month: '2023-05', year: '2023', revenue: 395000, profit: 213300, units: 980, Bikes: 283000, Components: 61000, Clothing: 31200, Accessories: 19800 },
    { month: '2023-07', year: '2023', revenue: 480200, profit: 259300, units: 1190, Bikes: 344000, Components: 74000, Clothing: 38000, Accessories: 24200 },
    { month: '2023-09', year: '2023', revenue: 520400, profit: 281000, units: 1320, Bikes: 373000, Components: 80000, Clothing: 41100, Accessories: 26300 },
    { month: '2023-11', year: '2023', revenue: 610500, profit: 329600, units: 1540, Bikes: 437000, Components: 94000, Clothing: 48200, Accessories: 31300 },
    { month: '2024-01', year: '2024', revenue: 680200, profit: 367300, units: 1710, Bikes: 487000, Components: 105000, Clothing: 53800, Accessories: 34400 },
    { month: '2024-03', year: '2024', revenue: 740100, profit: 399600, units: 1860, Bikes: 530000, Components: 114000, Clothing: 58500, Accessories: 37600 },
    { month: '2024-05', year: '2024', revenue: 810500, profit: 437600, units: 2040, Bikes: 581000, Components: 125000, Clothing: 64000, Accessories: 40500 },
    { month: '2024-07', year: '2024', revenue: 890400, profit: 480800, units: 2250, Bikes: 638000, Components: 137000, Clothing: 70300, Accessories: 45100 },
    { month: '2024-09', year: '2024', revenue: 950000, profit: 513000, units: 2410, Bikes: 681000, Components: 146000, Clothing: 75000, Accessories: 48000 },
    { month: '2024-11', year: '2024', revenue: 1020400, profit: 551000, units: 2580, Bikes: 731000, Components: 157000, Clothing: 80600, Accessories: 51800 },
    { month: '2025-01', year: '2025', revenue: 1080500, profit: 583400, units: 2730, Bikes: 775000, Components: 166000, Clothing: 85400, Accessories: 54100 },
    { month: '2025-03', year: '2025', revenue: 1150200, profit: 621100, units: 2910, Bikes: 825000, Components: 177000, Clothing: 90900, Accessories: 57300 },
    { month: '2025-05', year: '2025', revenue: 1220400, profit: 659000, units: 3080, Bikes: 875000, Components: 188000, Clothing: 96400, Accessories: 61000 },
    { month: '2025-07', year: '2025', revenue: 1280900, profit: 691600, units: 3240, Bikes: 918000, Components: 197000, Clothing: 101200, Accessories: 64700 },
    { month: '2025-09', year: '2025', revenue: 1340200, profit: 723700, units: 3390, Bikes: 961000, Components: 206000, Clothing: 105900, Accessories: 67300 },
    { month: '2025-11', year: '2025', revenue: 1410500, profit: 761600, units: 3570, Bikes: 1011000, Components: 217000, Clothing: 111400, Accessories: 71100 }
  ],

  // Macro categories specification
  categories: {
    names: ['Bikes', 'Components', 'Clothing', 'Accessories'],
    data: {
      'Bikes': {
        revenue: 6420110, profit: 3595261, margin: 56.0, units: 4210, orders: 2840,
        subcategories: [
          { name: 'Mountain Bikes', revenue: 3210000, profit: 1804020 },
          { name: 'Road Bikes', revenue: 2125000, profit: 1185750 },
          { name: 'Touring Bikes', revenue: 1085110, profit: 605491 }
        ],
        radar: [96, 90, 78, 94, 88, 92],
        funnel: [36000, 24800, 15600, 8200, 2840]
      },
      'Components': {
        revenue: 1380450, profit: 717834, margin: 52.0, units: 5120, orders: 1120,
        subcategories: [
          { name: 'Mountain Frames', revenue: 582300, profit: 308037 },
          { name: 'Road Frames', revenue: 420150, profit: 218478 },
          { name: 'Wheels & Rims', revenue: 240000, profit: 122400 },
          { name: 'Drivetrain', revenue: 138000, profit: 68919 }
        ],
        radar: [74, 84, 94, 82, 91, 79],
        funnel: [18000, 12200, 7800, 4100, 1120]
      },
      'Clothing': {
        revenue: 710230, profit: 340910, margin: 48.0, units: 4890, orders: 650,
        subcategories: [
          { name: 'Performance Jerseys', revenue: 340000, profit: 166600 },
          { name: 'Shorts & Bibs', revenue: 210230, profit: 98808 },
          { name: 'Gloves & Socks', revenue: 160000, profit: 75502 }
        ],
        radar: [82, 76, 88, 89, 84, 86],
        funnel: [12000, 8400, 5100, 2600, 650]
      },
      'Accessories': {
        revenue: 444751, profit: 177994, margin: 40.0, units: 8228, orders: 398,
        subcategories: [
          { name: 'Helmets', revenue: 210000, profit: 86100 },
          { name: 'Hydration Systems', revenue: 110000, profit: 42900 },
          { name: 'Tires & Tubes', revenue: 85751, profit: 34300 },
          { name: 'Pumps & Locks', revenue: 39000, profit: 14694 }
        ],
        radar: [89, 70, 96, 91, 95, 84],
        funnel: [9000, 6300, 3900, 1800, 398]
      }
    }
  },

  // Regional territory baseline
  territories: [
    { name: 'North America (United States)', value: 3840250, pct: 42.9, shareByCategory: { Bikes: 0.44, Components: 0.41, Clothing: 0.42, Accessories: 0.43 } },
    { name: 'North America (Canada)', value: 1020140, pct: 11.4, shareByCategory: { Bikes: 0.11, Components: 0.12, Clothing: 0.11, Accessories: 0.12 } },
    { name: 'Europe (United Kingdom)', value: 1650320, pct: 18.4, shareByCategory: { Bikes: 0.18, Components: 0.19, Clothing: 0.18, Accessories: 0.17 } },
    { name: 'Europe (Germany / France)', value: 1124500, pct: 12.6, shareByCategory: { Bikes: 0.13, Components: 0.14, Clothing: 0.13, Accessories: 0.13 } },
    { name: 'Pacific (Australia)', value: 1320331, pct: 14.7, shareByCategory: { Bikes: 0.14, Components: 0.14, Clothing: 0.16, Accessories: 0.15 } }
  ],

  // Comprehensive Product Catalog (12 Verified Star-Schema SKUs)
  products: [
    { sku: 'BK-M68B-38', name: 'Mountain-200 Black, 38', category: 'Bikes', subcategory: 'Mountain Bikes', units: 1420, margin: 56.2, revenue: 1245600, profit: 700027, status: 'Top Volume', territory: 'North America (United States)' },
    { sku: 'BK-R93R-52', name: 'Road-150 Red, 52', category: 'Bikes', subcategory: 'Road Bikes', units: 1180, margin: 54.8, revenue: 1085420, profit: 594810, status: 'High Margin', territory: 'Europe (United Kingdom)' },
    { sku: 'BK-M18S-44', name: 'Mountain-100 Silver, 44', category: 'Bikes', subcategory: 'Mountain Bikes', units: 980, margin: 55.4, revenue: 980400, profit: 543141, status: 'Core Lineup', territory: 'North America (United States)' },
    { sku: 'FR-M94S-52', name: 'HL Mountain Frame - Silver', category: 'Components', subcategory: 'Mountain Frames', units: 640, margin: 52.9, revenue: 582300, profit: 308036, status: 'Stable', territory: 'Europe (Germany / France)' },
    { sku: 'BK-R89B-48', name: 'Road-250 Black, 48', category: 'Bikes', subcategory: 'Road Bikes', units: 720, margin: 53.6, revenue: 540000, profit: 289440, status: 'Growth Driver', territory: 'Pacific (Australia)' },
    { sku: 'BK-T79U-50', name: 'Touring-1000 Blue, 50', category: 'Bikes', subcategory: 'Touring Bikes', units: 510, margin: 51.5, revenue: 433500, profit: 223252, status: 'High Ticket', territory: 'North America (Canada)' },
    { sku: 'FR-R92B-58', name: 'HL Road Frame - Black, 58', category: 'Components', subcategory: 'Road Frames', units: 520, margin: 52.0, revenue: 420150, profit: 218478, status: 'Stable', territory: 'North America (United States)' },
    { sku: 'HL-U509-R', name: 'Sport-100 Helmet, Red', category: 'Accessories', subcategory: 'Helmets', units: 3840, margin: 48.1, revenue: 134400, profit: 64646, status: 'Top Units', territory: 'North America (United States)' },
    { sku: 'HL-U509-B', name: 'Sport-100 Helmet, Blue', category: 'Accessories', subcategory: 'Helmets', units: 2850, margin: 47.5, revenue: 99750, profit: 47381, status: 'High Vol', territory: 'Europe (United Kingdom)' },
    { sku: 'CL-9080-L', name: 'Long-Sleeve Logo Jersey, L', category: 'Clothing', subcategory: 'Performance Jerseys', units: 2150, margin: 51.0, revenue: 107500, profit: 54825, status: 'High Vol', territory: 'Europe (Germany / France)' },
    { sku: 'CL-8040-M', name: 'Classic Cycling Jersey, M', category: 'Clothing', subcategory: 'Performance Jerseys', units: 1840, margin: 49.5, revenue: 92000, profit: 45540, status: 'Stable', territory: 'North America (United States)' },
    { sku: 'WB-H298-GL', name: 'Water Bottle - 30 oz.', category: 'Accessories', subcategory: 'Hydration Systems', units: 4200, margin: 45.0, revenue: 42000, profit: 18900, status: 'Mass Market', territory: 'Pacific (Australia)' }
  ]
};

// Global Interactive State
const STATE = {
  category: 'All',
  year: 'All',
  territory: 'All',
  search: ''
};

// ECharts Instance Handlers
let lineChart, barChart, donutChart, scatterChart, radarChart, funnelChart;

// Responsive Chart Theme
const THEME = {
  backgroundColor: 'transparent',
  textStyle: { fontFamily: "'Plus Jakarta Sans', sans-serif", color: '#94a3b8' }
};

function getResponsiveGrid() {
  const width = window.innerWidth;
  if (width <= 480) {
    return { top: 32, right: 12, bottom: 36, left: 44, containLabel: true };
  }
  if (width <= 768) {
    return { top: 34, right: 18, bottom: 38, left: 50, containLabel: true };
  }
  return { top: 38, right: 26, bottom: 40, left: 58, containLabel: true };
}

// ----------------------------------------------------------------------------
// INITIALIZATION
// ----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', initAnalyticsSuite);

async function initAnalyticsSuite() {
  const lineDom = document.getElementById('echart-line');
  const barDom = document.getElementById('echart-bar');
  const donutDom = document.getElementById('echart-donut');
  const scatterDom = document.getElementById('echart-scatter');
  const radarDom = document.getElementById('echart-radar');
  const funnelDom = document.getElementById('echart-funnel');

  if (lineDom) lineChart = echarts.init(lineDom, 'dark', { renderer: 'canvas' });
  if (barDom) barChart = echarts.init(barDom, 'dark', { renderer: 'canvas' });
  if (donutDom) donutChart = echarts.init(donutDom, 'dark', { renderer: 'canvas' });
  if (scatterDom) scatterChart = echarts.init(scatterDom, 'dark', { renderer: 'canvas' });
  if (radarDom) radarChart = echarts.init(radarDom, 'dark', { renderer: 'canvas' });
  if (funnelDom) funnelChart = echarts.init(funnelDom, 'dark', { renderer: 'canvas' });

  // Cross-Chart Interactive Click Bindings
  if (barChart) {
    barChart.on('click', (params) => {
      if (params.name) {
        if (ENTERPRISE_DATA.categories.names.includes(params.name)) {
          triggerCategoryChange(params.name);
        }
      }
    });
  }

  if (donutChart) {
    donutChart.on('click', (params) => {
      if (params.name) {
        const terrSelect = document.getElementById('territory-select');
        if (terrSelect) {
          terrSelect.value = params.name;
          setTerritory(params.name);
        }
      }
    });
  }

  // Check WSGI API status cleanly without blocking or logging errors on Vercel
  checkApiEnvironment();

  // Initial Full Dashboard Render
  updateDashboard();

  // Smooth Debounced Window Resize Handler for Android & Desktop
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      const charts = [lineChart, barChart, donutChart, scatterChart, radarChart, funnelChart];
      charts.forEach(c => c && c.resize());
    }, 120);
  });
}

function checkApiEnvironment() {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const statusEl = document.getElementById('runtime-status-text');

  if (isLocal) {
    fetch('http://127.0.0.1:5000/api/health')
      .then(res => res.json())
      .then(data => {
        if (statusEl) statusEl.innerHTML = 'Flask REST API 200 OK &bull; WSGI Local';
      })
      .catch(() => {
        if (statusEl) statusEl.innerHTML = 'Client Data Engine &bull; Port 5000 Standby';
      });
  } else {
    if (statusEl) statusEl.innerHTML = 'Cloud Edge Engine Active &bull; Canvas GPU';
  }
}

// ----------------------------------------------------------------------------
// INTERACTIVE FILTER CONTROLLERS
// ----------------------------------------------------------------------------
function setCategory(btn, cat) {
  STATE.category = cat;
  document.querySelectorAll('[data-filter="category"]').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  updateDashboard();
}

function triggerCategoryChange(catName) {
  const targetBtn = document.querySelector(`[data-filter="category"][data-val="${catName}"]`);
  setCategory(targetBtn, catName);
}

function setYear(btn, yr) {
  STATE.year = yr;
  document.querySelectorAll('[data-filter="year"]').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  updateDashboard();
}

function setTerritory(terr) {
  STATE.territory = terr;
  updateDashboard();
}

function handleSearch(query) {
  STATE.search = query.trim().toLowerCase();
  updateDashboard();
}

function resetFilters() {
  STATE.category = 'All';
  STATE.year = 'All';
  STATE.territory = 'All';
  STATE.search = '';

  document.querySelectorAll('[data-filter="category"]').forEach(b => {
    b.classList.toggle('active', b.dataset.val === 'All');
  });
  document.querySelectorAll('[data-filter="year"]').forEach(b => {
    b.classList.toggle('active', b.dataset.val === 'All');
  });

  const tSelect = document.getElementById('territory-select');
  if (tSelect) tSelect.value = 'All';

  const sInput = document.getElementById('sku-search');
  if (sInput) sInput.value = '';

  updateDashboard();
}

// ----------------------------------------------------------------------------
// MASTER UPDATE COORDINATOR
// ----------------------------------------------------------------------------
function updateDashboard() {
  // 1. Filter Master Datasets based on active state
  const filteredProducts = getFilteredProducts();
  const summaryMetrics = calculateSummaryMetrics(filteredProducts);

  // 2. Update KPI Stat Cards
  updateKpiCards(summaryMetrics);

  // 3. Render / Update All 6 ECharts Instances
  renderLineChart();
  renderBarChart();
  renderDonutChart();
  renderScatterChart(filteredProducts);
  renderRadarChart();
  renderFunnelChart(summaryMetrics);

  // 4. Update Interactive SKU Table
  updateSkuTable(filteredProducts);
}

// ----------------------------------------------------------------------------
// METRIC CALCULATIONS & KPI UPDATES
// ----------------------------------------------------------------------------
function getFilteredProducts() {
  return ENTERPRISE_DATA.products.filter(p => {
    const matchCategory = STATE.category === 'All' || p.category === STATE.category;
    const matchTerritory = STATE.territory === 'All' || p.territory === STATE.territory;
    const matchSearch = !STATE.search ||
      p.name.toLowerCase().includes(STATE.search) ||
      p.sku.toLowerCase().includes(STATE.search) ||
      p.category.toLowerCase().includes(STATE.search) ||
      p.subcategory.toLowerCase().includes(STATE.search);
    return matchCategory && matchTerritory && matchSearch;
  });
}

function calculateSummaryMetrics(products) {
  let totalRev = 0;
  let totalProfit = 0;
  let totalUnits = 0;
  let totalOrders = 0;

  if (STATE.category === 'All') {
    totalRev = 8955541;
    totalProfit = 4831999;
    totalUnits = 22448;
    totalOrders = 5008;
  } else {
    const catData = ENTERPRISE_DATA.categories.data[STATE.category];
    totalRev = catData.revenue;
    totalProfit = catData.profit;
    totalUnits = catData.units;
    totalOrders = catData.orders;
  }

  // Adjust if Year filter applied
  let yearMultiplier = 1.0;
  if (STATE.year === '2023') yearMultiplier = 0.285;
  else if (STATE.year === '2024') yearMultiplier = 0.345;
  else if (STATE.year === '2025') yearMultiplier = 0.370;

  // Adjust if Territory filter applied
  let territoryMultiplier = 1.0;
  if (STATE.territory !== 'All') {
    const tMatch = ENTERPRISE_DATA.territories.find(t => t.name === STATE.territory);
    if (tMatch) territoryMultiplier = tMatch.pct / 100.0;
  }

  const finalRev = Math.round(totalRev * yearMultiplier * territoryMultiplier);
  const finalProfit = Math.round(totalProfit * yearMultiplier * territoryMultiplier);
  const finalUnits = Math.round(totalUnits * yearMultiplier * territoryMultiplier);
  const finalOrders = Math.round(totalOrders * yearMultiplier * territoryMultiplier);
  const marginPct = finalRev > 0 ? ((finalProfit / finalRev) * 100).toFixed(2) : '0.00';
  const activeMarkets = STATE.territory === 'All' ? 5 : 1;

  return {
    revenue: finalRev,
    profit: finalProfit,
    units: finalUnits,
    orders: finalOrders,
    marginRate: marginPct,
    markets: activeMarkets
  };
}

function updateKpiCards(m) {
  const elRev = document.getElementById('kpi-revenue');
  const elProfit = document.getElementById('kpi-profit');
  const elUnits = document.getElementById('kpi-units');
  const elOrders = document.getElementById('kpi-orders');
  const elMarkets = document.getElementById('kpi-markets');

  if (elRev) elRev.textContent = '$' + m.revenue.toLocaleString();
  if (elProfit) elProfit.textContent = '$' + m.profit.toLocaleString();
  if (elUnits) elUnits.textContent = m.units.toLocaleString();
  if (elOrders) elOrders.textContent = m.orders.toLocaleString();
  if (elMarkets) elMarkets.textContent = m.markets.toString();

  const elProfitSub = document.getElementById('kpi-profit-sub');
  if (elProfitSub) elProfitSub.textContent = `${m.marginRate}% Margin Rate`;

  const elRevSub = document.getElementById('kpi-revenue-sub');
  if (elRevSub) {
    if (STATE.year !== 'All') elRevSub.textContent = `Fiscal Year ${STATE.year}`;
    else elRevSub.textContent = '↑ +14.2% YoY Growth';
  }

  const elOrdersSub = document.getElementById('kpi-orders-sub');
  if (elOrdersSub && m.orders > 0) {
    const avgTicket = Math.round(m.revenue / m.orders);
    elOrdersSub.textContent = `$${avgTicket.toLocaleString()} Avg Ticket`;
  }
}

// ----------------------------------------------------------------------------
// 1. TIME-SERIES LINE CHART (MONTHLY REVENUE & PROFIT)
// ----------------------------------------------------------------------------
function renderLineChart() {
  if (!lineChart) return;

  // Filter months by year if needed
  let monthlyList = ENTERPRISE_DATA.monthly;
  if (STATE.year !== 'All') {
    monthlyList = monthlyList.filter(m => m.year === STATE.year);
  }

  const months = monthlyList.map(m => m.month);
  let revData = [];
  let profitData = [];

  if (STATE.category === 'All') {
    revData = monthlyList.map(m => m.revenue);
    profitData = monthlyList.map(m => m.profit);
  } else {
    revData = monthlyList.map(m => m[STATE.category] || 0);
    const catRatio = (ENTERPRISE_DATA.categories.data[STATE.category].profit / ENTERPRISE_DATA.categories.data[STATE.category].revenue);
    profitData = revData.map(r => Math.round(r * catRatio));
  }

  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'axis',
      confine: true,
      axisPointer: { type: 'cross', lineStyle: { color: '#60a5fa', width: 1.5, type: 'dashed' } },
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#3b82f6',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 },
      valueFormatter: (value) => '$' + Number(value).toLocaleString()
    },
    legend: {
      data: ['Monthly Revenue', 'Gross Profit'],
      textStyle: { color: '#cbd5e1', fontSize: 12 },
      top: 0
    },
    grid: getResponsiveGrid(),
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: '#334155' } },
      axisLabel: { color: '#94a3b8', fontSize: 10, rotate: window.innerWidth <= 480 ? 45 : 0 }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#334155' } },
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 10,
        formatter: (v) => '$' + (v >= 1000000 ? (v / 1000000).toFixed(1) + 'M' : Math.round(v / 1000) + 'k')
      }
    },
    dataZoom: [
      { type: 'inside', start: 0, end: 100 },
      { type: 'slider', start: 0, end: 100, height: 16, bottom: 2, borderColor: '#334155', textStyle: { color: '#94a3b8' } }
    ],
    series: [
      {
        name: 'Monthly Revenue',
        type: 'line',
        smooth: true,
        showSymbol: true,
        symbolSize: 6,
        data: revData,
        lineStyle: { width: 3, color: '#3b82f6' },
        itemStyle: { color: '#60a5fa' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(59, 130, 246, 0.45)' },
            { offset: 1, color: 'rgba(59, 130, 246, 0.02)' }
          ])
        }
      },
      {
        name: 'Gross Profit',
        type: 'line',
        smooth: true,
        showSymbol: true,
        symbolSize: 6,
        data: profitData,
        lineStyle: { width: 3, color: '#10b981' },
        itemStyle: { color: '#34d399' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(16, 185, 129, 0.35)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0.01)' }
          ])
        }
      }
    ]
  };
  lineChart.setOption(option, true);
}

// ----------------------------------------------------------------------------
// 2. CLUSTERED BAR CHART (CATEGORY OR SUBCATEGORY BREAKDOWN)
// ----------------------------------------------------------------------------
function renderBarChart() {
  if (!barChart) return;

  let xLabels = [];
  let revData = [];
  let profitData = [];

  if (STATE.category === 'All') {
    xLabels = ENTERPRISE_DATA.categories.names;
    xLabels.forEach(cat => {
      const c = ENTERPRISE_DATA.categories.data[cat];
      revData.push(c.revenue);
      profitData.push(c.profit);
    });
  } else {
    // Show subcategories within the selected category for deep insight
    const catData = ENTERPRISE_DATA.categories.data[STATE.category];
    xLabels = catData.subcategories.map(s => s.name);
    revData = catData.subcategories.map(s => s.revenue);
    profitData = catData.subcategories.map(s => s.profit);
  }

  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'axis',
      confine: true,
      axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(59, 130, 246, 0.1)' } },
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#8b5cf6',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 },
      valueFormatter: (v) => '$' + Number(v).toLocaleString()
    },
    legend: {
      data: ['Revenue', 'Profit'],
      textStyle: { color: '#cbd5e1', fontSize: 12 },
      top: 0
    },
    grid: getResponsiveGrid(),
    xAxis: {
      type: 'category',
      data: xLabels,
      axisLabel: {
        color: '#f8fafc',
        fontWeight: 600,
        fontSize: window.innerWidth <= 480 ? 9 : 11,
        interval: 0,
        rotate: (STATE.category !== 'All' || window.innerWidth <= 480) ? 25 : 0
      }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 10,
        formatter: (v) => '$' + (v >= 1000000 ? (v / 1000000).toFixed(1) + 'M' : Math.round(v / 1000) + 'k')
      }
    },
    series: [
      {
        name: 'Revenue',
        type: 'bar',
        barWidth: '30%',
        data: revData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#3b82f6' },
            { offset: 1, color: '#1d4ed8' }
          ]),
          borderRadius: [6, 6, 0, 0]
        }
      },
      {
        name: 'Profit',
        type: 'bar',
        barWidth: '30%',
        data: profitData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#8b5cf6' },
            { offset: 1, color: '#6d28d9' }
          ]),
          borderRadius: [6, 6, 0, 0]
        }
      }
    ]
  };
  barChart.setOption(option, true);
}

// ----------------------------------------------------------------------------
// 3. PROPORTIONAL DONUT CHART (TERRITORY DISTRIBUTION)
// ----------------------------------------------------------------------------
function renderDonutChart() {
  if (!donutChart) return;

  const donutData = ENTERPRISE_DATA.territories.map(t => {
    let val = t.value;
    if (STATE.category !== 'All') {
      const catRev = ENTERPRISE_DATA.categories.data[STATE.category].revenue;
      const share = t.shareByCategory[STATE.category] || 0.2;
      val = Math.round(catRev * share);
    }
    return { name: t.name, value: val };
  });

  const isMobile = window.innerWidth <= 600;

  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#ec4899',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 },
      formatter: (p) => `<b>${p.name}</b><br/>Revenue: $${Number(p.value).toLocaleString()}<br/>Share: <b>${p.percent}%</b>`
    },
    legend: {
      orient: isMobile ? 'horizontal' : 'vertical',
      left: isMobile ? 'center' : 8,
      top: isMobile ? 'bottom' : 'middle',
      textStyle: { color: '#94a3b8', fontSize: isMobile ? 9 : 11 },
      itemWidth: 10,
      itemHeight: 10
    },
    series: [
      {
        name: 'Territory Revenue',
        type: 'pie',
        radius: isMobile ? ['36%', '60%'] : ['48%', '74%'],
        center: isMobile ? ['50%', '42%'] : ['64%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#0b1120',
          borderWidth: 3
        },
        label: { show: false },
        emphasis: {
          scale: true,
          scaleSize: 8,
          label: {
            show: true,
            fontSize: isMobile ? 12 : 14,
            fontWeight: 'bold',
            color: '#ffffff',
            formatter: '{d}%'
          }
        },
        color: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899'],
        data: donutData
      }
    ]
  };
  donutChart.setOption(option, true);
}

// ----------------------------------------------------------------------------
// 4. 4D SCATTER BUBBLE MATRIX (UNITS VS MARGIN %)
// ----------------------------------------------------------------------------
function renderScatterChart(products) {
  if (!scatterChart) return;

  const scatterData = products.map(p => ({
    name: p.name,
    value: [p.units, p.margin, p.revenue, p.category, p.sku]
  }));

  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#f59e0b',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 },
      formatter: (param) => {
        const item = param.data;
        return `<b>${item.name}</b> (${item.value[4]})<br/>` +
               `Units Sold: <b>${item.value[0].toLocaleString()}</b><br/>` +
               `Gross Margin: <b>${item.value[1]}%</b><br/>` +
               `Total Revenue: <b>$${Number(item.value[2]).toLocaleString()}</b><br/>` +
               `Sector: <span style="color:#60a5fa">${item.value[3]}</span>`;
      }
    },
    grid: getResponsiveGrid(),
    xAxis: {
      name: 'Units',
      nameLocation: 'middle',
      nameGap: 24,
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: { color: '#94a3b8', fontSize: 10 }
    },
    yAxis: {
      name: 'Margin %',
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: { color: '#94a3b8', fontSize: 10, formatter: '{value}%' },
      min: 40,
      max: 60
    },
    series: [
      {
        name: 'Products',
        type: 'scatter',
        data: scatterData,
        symbolSize: (data) => Math.max(16, Math.min(48, Math.sqrt(data[2]) / 26)),
        itemStyle: {
          color: (param) => {
            const cat = param.data.value[3];
            if (cat === 'Bikes') return '#3b82f6';
            if (cat === 'Components') return '#8b5cf6';
            if (cat === 'Clothing') return '#10b981';
            return '#f59e0b';
          },
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    ]
  };
  scatterChart.setOption(option, true);
}

// ----------------------------------------------------------------------------
// 5. OPERATIONAL RADAR SCORECARD
// ----------------------------------------------------------------------------
function renderRadarChart() {
  if (!radarChart) return;

  const baseline = [88, 85, 84, 88, 87, 85];
  let currentProfile = [94, 88, 76, 92, 85, 90];
  let profileName = 'Bikes Sector';

  if (STATE.category !== 'All') {
    const c = ENTERPRISE_DATA.categories.data[STATE.category];
    currentProfile = c.radar;
    profileName = `${STATE.category} Profile`;
  }

  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#10b981',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 }
    },
    legend: {
      data: [profileName, 'Enterprise Baseline'],
      textStyle: { color: '#cbd5e1', fontSize: 11 },
      top: 0
    },
    radar: {
      center: ['50%', '56%'],
      radius: window.innerWidth <= 480 ? '54%' : '62%',
      indicator: [
        { name: 'Sales Velocity', max: 100 },
        { name: 'Gross Margin %', max: 100 },
        { name: 'Inventory Turns', max: 100 },
        { name: 'Customer CSAT', max: 100 },
        { name: 'Fulfillment Speed', max: 100 },
        { name: 'Market Retention', max: 100 }
      ],
      shape: 'polygon',
      splitNumber: 4,
      axisName: { color: '#94a3b8', fontSize: 10 },
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.15)' } },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(30, 41, 59, 0.2)', 'rgba(30, 41, 59, 0.4)', 'rgba(30, 41, 59, 0.2)', 'rgba(30, 41, 59, 0.5)']
        }
      },
      axisLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.2)' } }
    },
    series: [
      {
        name: 'Operational Capability',
        type: 'radar',
        data: [
          {
            value: currentProfile,
            name: profileName,
            symbol: 'circle',
            symbolSize: 5,
            lineStyle: { width: 2.5, color: '#3b82f6' },
            itemStyle: { color: '#60a5fa' },
            areaStyle: { color: 'rgba(59, 130, 246, 0.35)' }
          },
          {
            value: baseline,
            name: 'Enterprise Baseline',
            symbol: 'circle',
            symbolSize: 5,
            lineStyle: { width: 2, color: '#10b981', type: 'dashed' },
            itemStyle: { color: '#34d399' },
            areaStyle: { color: 'rgba(16, 185, 129, 0.15)' }
          }
        ]
      }
    ]
  };
  radarChart.setOption(option, true);
}

// ----------------------------------------------------------------------------
// 6. PIPELINE CONVERSION FUNNEL
// ----------------------------------------------------------------------------
function renderFunnelChart(m) {
  if (!funnelChart) return;

  let funnelValues = [50000, 34500, 21800, 11400, 5008];

  if (STATE.category !== 'All') {
    const c = ENTERPRISE_DATA.categories.data[STATE.category];
    funnelValues = c.funnel;
  } else if (STATE.year !== 'All' || STATE.territory !== 'All') {
    const ratio = m.orders / 5008;
    funnelValues = funnelValues.map(v => Math.round(v * ratio));
  }

  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#06b6d4',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 },
      formatter: '{a} <br/><b>{b}</b> : {c} units ({d}%)'
    },
    legend: { show: false },
    series: [
      {
        name: 'Sales Pipeline',
        type: 'funnel',
        left: '8%',
        top: 20,
        bottom: 20,
        width: '84%',
        min: 0,
        max: funnelValues[0],
        minSize: '24%',
        maxSize: '94%',
        sort: 'descending',
        gap: 4,
        label: {
          show: true,
          position: 'inside',
          color: '#ffffff',
          fontWeight: 700,
          fontSize: window.innerWidth <= 480 ? 9 : 11,
          formatter: '{b}: {c}'
        },
        labelLine: { length: 8, lineStyle: { width: 1, type: 'solid' } },
        itemStyle: {
          borderColor: '#090d16',
          borderWidth: 2,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.4)'
        },
        emphasis: { label: { fontSize: 12, fontWeight: 'bold' } },
        color: ['#3b82f6', '#06b6d4', '#10b981', '#8b5cf6', '#f59e0b'],
        data: [
          { value: funnelValues[0], name: '1. Brand Inquiries' },
          { value: funnelValues[1], name: '2. Qualified Leads' },
          { value: funnelValues[2], name: '3. Solution Quotes' },
          { value: funnelValues[3], name: '4. Commercial Neg.' },
          { value: funnelValues[4], name: '5. Executed Orders' }
        ]
      }
    ]
  };
  funnelChart.setOption(option, true);
}

// ----------------------------------------------------------------------------
// INTERACTIVE SKU EXPLORER DATA TABLE
// ----------------------------------------------------------------------------
function updateSkuTable(products) {
  const tbody = document.getElementById('analytics-tbody');
  const countBadge = document.getElementById('sku-count-badge');

  if (countBadge) {
    countBadge.textContent = `Showing ${products.length} of ${ENTERPRISE_DATA.products.length} Verified SKUs`;
  }

  if (!tbody) return;

  if (products.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 32px; color: #94a3b8;">
          No matching products found matching criteria. Click <strong>Reset</strong> to restore ledger.
        </td>
      </tr>
    `;
    return;
  }

  let html = '';
  products.forEach(p => {
    let catClass = 'badge-blue';
    if (p.category === 'Components') catClass = 'badge-purple';
    if (p.category === 'Clothing') catClass = 'badge-emerald';
    if (p.category === 'Accessories') catClass = 'badge-amber';

    const marginClass = p.margin >= 52.0 ? 'badge-success' : 'badge-warning';

    html += `
      <tr>
        <td>
          <div style="font-weight: 700; color: #f8fafc;">${p.name}</div>
          <div style="font-size: 0.72rem; color: #64748b; font-family: var(--font-mono);">${p.sku}</div>
        </td>
        <td><span class="badge-tag ${catClass}">${p.category}</span></td>
        <td style="color: #cbd5e1;">${p.subcategory}</td>
        <td style="text-align: right; font-weight: 600;">${p.units.toLocaleString()}</td>
        <td style="text-align: right;"><span class="badge-tag ${marginClass}">${p.margin}%</span></td>
        <td style="text-align: right; font-weight: 700; color: #38bdf8;">$${p.revenue.toLocaleString()}</td>
        <td>
          <span style="font-size: 0.75rem; color: #94a3b8; background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 4px;">
            ${p.status}
          </span>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}
