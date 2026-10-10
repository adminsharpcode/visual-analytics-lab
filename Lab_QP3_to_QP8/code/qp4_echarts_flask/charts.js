/**
 * ============================================================================
 * Apache ECharts Multi-Perspective Analytics Suite
 * Subject: Visual Analytics Lab (MACSE603)
 * Student: Vedant Nimkar | 26MML0045
 * Experiment 10: Interactive ECharts (Line, Bar, Donut, Scatter, Radar, Funnel)
 * ============================================================================
 */

// Fallback embedded analytical dataset (mirrors verified star-schema database)
const FALLBACK_DATA = {
  monthly: {
    months: ["2023-01","2023-03","2023-05","2023-07","2023-09","2023-11","2024-01","2024-03","2024-05","2024-07","2024-09","2024-11","2025-01","2025-03","2025-05","2025-07","2025-09","2025-11"],
    revenue: [240500, 310200, 395000, 480200, 520400, 610500, 680200, 740100, 810500, 890400, 950000, 1020400, 1080500, 1150200, 1220400, 1280900, 1340200, 1410500],
    profit: [129870, 167500, 213300, 259300, 281000, 329600, 367300, 399600, 437600, 480800, 513000, 551000, 583400, 621100, 659000, 691600, 723700, 761600],
    units: [620, 790, 980, 1190, 1320, 1540, 1710, 1860, 2040, 2250, 2410, 2580, 2730, 2910, 3080, 3240, 3390, 3570]
  },
  categories: {
    categories: ["Bikes", "Components", "Clothing", "Accessories"],
    revenue: [6420110, 1380450, 710230, 444751],
    profit: [3595261, 717834, 340910, 177994],
    units: [4210, 5120, 4890, 8228]
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
    { name: "Touring-1000 Blue, 50", value: [510, 51.5, 433500, "Bikes"] },
    { name: "Sport-100 Helmet, Red", value: [3840, 48.1, 134400, "Accessories"] },
    { name: "Long-Sleeve Logo Jersey, L", value: [2150, 51.0, 107500, "Clothing"] },
    { name: "Classic Jersey, M", value: [1840, 49.5, 92000, "Clothing"] },
    { name: "Water Bottle - 30 oz.", value: [4200, 45.0, 42000, "Accessories"] }
  ]
};

// Global ECharts Instances
let lineChart, barChart, donutChart, scatterChart, radarChart, funnelChart;

const THEME = {
  backgroundColor: 'transparent',
  textStyle: { fontFamily: "'Plus Jakarta Sans', sans-serif", color: '#94a3b8' },
  grid: { top: 38, right: 28, bottom: 38, left: 56, containLabel: true }
};

// Initialize All 6 Charts
async function initCharts() {
  const lineDom = document.getElementById('echart-line');
  const barDom = document.getElementById('echart-bar');
  const donutDom = document.getElementById('echart-donut');
  const scatterDom = document.getElementById('echart-scatter');
  const radarDom = document.getElementById('echart-radar');
  const funnelDom = document.getElementById('echart-funnel');

  if (lineDom) lineChart = echarts.init(lineDom, 'dark');
  if (barDom) barChart = echarts.init(barDom, 'dark');
  if (donutDom) donutChart = echarts.init(donutDom, 'dark');
  if (scatterDom) scatterChart = echarts.init(scatterDom, 'dark');
  if (radarDom) radarChart = echarts.init(radarDom, 'dark');
  if (funnelDom) funnelChart = echarts.init(funnelDom, 'dark');

  // Try fetching dynamic backend data, else fallback to verified dataset
  let monthlyData = FALLBACK_DATA.monthly;
  let categoryData = FALLBACK_DATA.categories;
  let territoryData = FALLBACK_DATA.territories;

  try {
    const resM = await fetch('http://127.0.0.1:5000/api/sales/monthly');
    if (resM.ok) monthlyData = await resM.json();

    const resC = await fetch('http://127.0.0.1:5000/api/sales/by-category');
    if (resC.ok) categoryData = await resC.json();

    const resT = await fetch('http://127.0.0.1:5000/api/sales/by-territory');
    if (resT.ok) territoryData = await resT.json();
  } catch (e) {
    console.info('Using high-fidelity embedded analytical dataset.');
  }

  renderLineChart(monthlyData);
  renderBarChart(categoryData);
  renderDonutChart(territoryData);
  renderScatterChart(FALLBACK_DATA.products);
  renderRadarChart();
  renderFunnelChart();

  window.addEventListener('resize', () => {
    lineChart && lineChart.resize();
    barChart && barChart.resize();
    donutChart && donutChart.resize();
    scatterChart && scatterChart.resize();
    radarChart && radarChart.resize();
    funnelChart && funnelChart.resize();
  });
}

// 1. Line Chart: Monthly Revenue & Profit Time-Series
function renderLineChart(data) {
  if (!lineChart) return;
  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross', lineStyle: { color: '#60a5fa', width: 1.5, type: 'dashed' } },
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#3b82f6',
      borderWidth: 1,
      textStyle: { color: '#f8fafc', fontSize: 12 },
      valueFormatter: (value) => '$' + Number(value).toLocaleString()
    },
    legend: {
      data: ['Monthly Revenue', 'Gross Profit'],
      textStyle: { color: '#cbd5e1' },
      top: 0
    },
    grid: THEME.grid,
    xAxis: {
      type: 'category',
      data: data.months,
      axisLine: { lineStyle: { color: '#334155' } },
      axisLabel: { color: '#94a3b8', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#334155' } },
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: {
        color: '#94a3b8',
        formatter: (v) => '$' + (v / 1000) + 'k'
      }
    },
    dataZoom: [
      { type: 'inside', start: 0, end: 100 },
      { type: 'slider', start: 0, end: 100, height: 18, bottom: 0, borderColor: '#334155', textStyle: { color: '#94a3b8' } }
    ],
    series: [
      {
        name: 'Monthly Revenue',
        type: 'line',
        smooth: true,
        showSymbol: true,
        symbolSize: 6,
        data: data.revenue,
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
        data: data.profit,
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
  lineChart.setOption(option);
}

// 2. Bar Chart: Product Category Breakdown
function renderBarChart(data) {
  if (!barChart) return;
  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(59, 130, 246, 0.1)' } },
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#8b5cf6',
      borderWidth: 1,
      textStyle: { color: '#f8fafc' },
      valueFormatter: (v) => '$' + Number(v).toLocaleString()
    },
    legend: {
      data: ['Revenue', 'Profit'],
      textStyle: { color: '#cbd5e1' },
      top: 0
    },
    grid: THEME.grid,
    xAxis: {
      type: 'category',
      data: data.categories,
      axisLabel: { color: '#f8fafc', fontWeight: 600 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: { formatter: (v) => '$' + (v / 1000000).toFixed(1) + 'M' }
    },
    series: [
      {
        name: 'Revenue',
        type: 'bar',
        barWidth: '28%',
        data: data.revenue,
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
        barWidth: '28%',
        data: data.profit,
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
  barChart.setOption(option);
}

// 3. Donut Chart: Territory Proportions
function renderDonutChart(data) {
  if (!donutChart) return;
  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#ec4899',
      borderWidth: 1,
      textStyle: { color: '#f8fafc' },
      formatter: '{b}<br/><b>${c}</b> ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: { color: '#94a3b8', fontSize: 11 },
      top: 'middle'
    },
    series: [
      {
        name: 'Territory Revenue',
        type: 'pie',
        radius: ['52%', '75%'],
        center: ['65%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#090d16',
          borderWidth: 3
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          scale: true,
          scaleSize: 10,
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
            color: '#ffffff'
          }
        },
        color: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899'],
        data: data
      }
    ]
  };
  donutChart.setOption(option);
}

// 4. Scatter Bubble Chart: Volume vs Margin %
function renderScatterChart(products) {
  if (!scatterChart) return;
  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#f59e0b',
      borderWidth: 1,
      textStyle: { color: '#f8fafc' },
      formatter: (param) => {
        const item = param.data;
        return `<b>${item.name}</b><br/>Units Sold: ${item.value[0].toLocaleString()}<br/>Gross Margin: ${item.value[1]}%<br/>Total Sales: $${Number(item.value[2]).toLocaleString()}`;
      }
    },
    grid: THEME.grid,
    xAxis: {
      name: 'Units Sold',
      nameLocation: 'middle',
      nameGap: 28,
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: { color: '#94a3b8' }
    },
    yAxis: {
      name: 'Margin %',
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } },
      axisLabel: { color: '#94a3b8', formatter: '{value}%' },
      min: 40,
      max: 60
    },
    series: [
      {
        name: 'Products',
        type: 'scatter',
        data: products,
        symbolSize: (data) => Math.max(16, Math.sqrt(data[2]) / 26),
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
  scatterChart.setOption(option);
}

// 5. Radar Chart: Multi-Criteria Operational Performance Scorecard
function renderRadarChart() {
  if (!radarChart) return;
  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#10b981',
      borderWidth: 1,
      textStyle: { color: '#f8fafc' }
    },
    legend: {
      data: ['Bikes Portfolio', 'Components & Gear'],
      textStyle: { color: '#cbd5e1' },
      top: 0
    },
    radar: {
      center: ['50%', '58%'],
      radius: '60%',
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
      axisName: { color: '#94a3b8', fontSize: 11 },
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
            value: [94, 88, 76, 92, 85, 90],
            name: 'Bikes Portfolio',
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: { width: 2, color: '#3b82f6' },
            itemStyle: { color: '#60a5fa' },
            areaStyle: { color: 'rgba(59, 130, 246, 0.3)' }
          },
          {
            value: [72, 82, 95, 84, 92, 78],
            name: 'Components & Gear',
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: { width: 2, color: '#10b981' },
            itemStyle: { color: '#34d399' },
            areaStyle: { color: 'rgba(16, 185, 129, 0.25)' }
          }
        ]
      }
    ]
  };
  radarChart.setOption(option);
}

// 6. Funnel Chart: Sales Pipeline Conversion Funnel
function renderFunnelChart() {
  if (!funnelChart) return;
  const option = {
    backgroundColor: THEME.backgroundColor,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#06b6d4',
      borderWidth: 1,
      textStyle: { color: '#f8fafc' },
      formatter: '{a} <br/><b>{b}</b> : {c} units ({d}%)'
    },
    legend: {
      show: false
    },
    series: [
      {
        name: 'Sales Pipeline',
        type: 'funnel',
        left: '10%',
        top: 20,
        bottom: 20,
        width: '80%',
        min: 0,
        max: 50000,
        minSize: '28%',
        maxSize: '92%',
        sort: 'descending',
        gap: 4,
        label: {
          show: true,
          position: 'inside',
          color: '#ffffff',
          fontWeight: 700,
          fontSize: 11,
          formatter: '{b}: {c}'
        },
        labelLine: {
          length: 10,
          lineStyle: { width: 1, type: 'solid' }
        },
        itemStyle: {
          borderColor: '#090d16',
          borderWidth: 2,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.4)'
        },
        emphasis: {
          label: {
            fontSize: 13,
            fontWeight: 'bold'
          }
        },
        color: ['#3b82f6', '#06b6d4', '#10b981', '#8b5cf6', '#f59e0b'],
        data: [
          { value: 50000, name: '1. Brand Inquiries' },
          { value: 34500, name: '2. Qualified Opportunities' },
          { value: 21800, name: '3. Solution Quotes' },
          { value: 11400, name: '4. Commercial Negotiations' },
          { value: 5008, name: '5. Executed Sales Orders' }
        ]
      }
    ]
  };
  funnelChart.setOption(option);
}

// Category filter interaction
function applyCategoryFilter(cat) {
  const pills = document.querySelectorAll('.filter-pill');
  pills.forEach(p => p.classList.remove('active'));
  event.target.classList.add('active');

  if (cat === 'All') {
    renderBarChart(FALLBACK_DATA.categories);
    renderScatterChart(FALLBACK_DATA.products);
  } else {
    const idx = FALLBACK_DATA.categories.categories.indexOf(cat);
    if (idx !== -1) {
      renderBarChart({
        categories: [cat],
        revenue: [FALLBACK_DATA.categories.revenue[idx]],
        profit: [FALLBACK_DATA.categories.profit[idx]]
      });
      const filteredProds = FALLBACK_DATA.products.filter(p => p.value[3] === cat);
      renderScatterChart(filteredProds);
    }
  }
}

document.addEventListener('DOMContentLoaded', initCharts);
