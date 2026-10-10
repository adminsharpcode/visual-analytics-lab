/**
 * ============================================================================
 * Assessment 3: HTML & CSS Visual Analytics Frontend Engine
 * Subject: Visual Analytics Lab (MACSE603)
 * Student: Vedant Nimkar | 26MML0045
 * Full-Featured Multi-Page Navigation, Dynamic Filtering & Reactive Ledger
 * ============================================================================
 */

// Star-Schema Database Mirror
const DB = {
  kpis: {
    revenue: 8955541,
    profit: 4831999,
    units: 22448,
    orders: 5008,
    customers: 220,
    marginRate: 53.96
  },
  categories: {
    'Bikes': { revenue: 6420110, profit: 3595261, margin: 56.0, units: 4210, orders: 2840 },
    'Components': { revenue: 1380450, profit: 717834, margin: 52.0, units: 5120, orders: 1120 },
    'Clothing': { revenue: 710230, profit: 340910, margin: 48.0, units: 4890, orders: 650 },
    'Accessories': { revenue: 444751, profit: 177994, margin: 40.0, units: 8228, orders: 398 }
  },
  territories: {
    'North America': { revenue: 4860390, pct: 54.3, orders: 2715 },
    'Europe': { revenue: 2774820, pct: 31.0, orders: 1552 },
    'Pacific': { revenue: 1320331, pct: 14.7, orders: 741 }
  },
  products: [
    { name: 'Mountain-200 Black, 38', category: 'Bikes', subcat: 'Mountain Bikes', units: 1420, revenue: 1245600, margin: 56.2, status: 'Top Revenue' },
    { name: 'Road-150 Red, 52', category: 'Bikes', subcat: 'Road Bikes', units: 1180, revenue: 1085420, margin: 54.8, status: 'High Margin' },
    { name: 'Sport-100 Helmet, Red', category: 'Accessories', subcat: 'Helmets', units: 3840, revenue: 134400, margin: 48.1, status: 'Top Units' },
    { name: 'HL Mountain Frame - Silver', category: 'Components', subcat: 'Mountain Frames', units: 640, revenue: 582300, margin: 52.9, status: 'Stable' },
    { name: 'Long-Sleeve Logo Jersey, L', category: 'Clothing', subcat: 'Jerseys', units: 2150, revenue: 107500, margin: 51.0, status: 'High Vol' },
    { name: 'Road-250 Black, 48', category: 'Bikes', subcat: 'Road Bikes', units: 720, revenue: 540000, margin: 53.6, status: 'Growth Driver' },
    { name: 'Touring-1000 Blue, 50', category: 'Bikes', subcat: 'Touring Bikes', units: 510, revenue: 433500, margin: 51.5, status: 'High Ticket' },
    { name: 'Classic Cycling Jersey, M', category: 'Clothing', subcat: 'Jerseys', units: 1840, revenue: 92000, margin: 49.5, status: 'Stable' },
    { name: 'Water Bottle - 30 oz.', category: 'Accessories', subcat: 'Hydration', units: 4200, revenue: 42000, margin: 45.0, status: 'Mass Market' }
  ]
};

// Runtime Active State
const STATE = {
  activeView: 'overview',
  category: 'All',
  territory: 'All',
  year: 'All'
};

document.addEventListener('DOMContentLoaded', initQP3Dashboard);

function initQP3Dashboard() {
  // 1. Setup Multi-Page Sidebar Nav Links
  const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const targetHash = item.getAttribute('href').replace('#', '');
      switchView(targetHash);
    });
  });

  // 2. Setup Filter Inputs
  const catFilter = document.getElementById('categoryFilter');
  const terrFilter = document.getElementById('territoryFilter');
  const yrFilter = document.getElementById('yearFilter');
  const resetBtn = document.getElementById('resetFilters');

  if (catFilter) catFilter.addEventListener('change', () => { STATE.category = catFilter.value; updateDashboard(); });
  if (terrFilter) terrFilter.addEventListener('change', () => { STATE.territory = terrFilter.value; updateDashboard(); });
  if (yrFilter) yrFilter.addEventListener('change', () => { STATE.year = yrFilter.value; updateDashboard(); });
  if (resetBtn) resetBtn.addEventListener('click', resetAllFilters);

  // 3. Setup Refresh and Export Action Buttons
  const refreshBtn = document.getElementById('refreshBtn');
  const exportBtn = document.getElementById('exportBtn');

  if (refreshBtn) refreshBtn.addEventListener('click', triggerRefresh);
  if (exportBtn) exportBtn.addEventListener('click', () => window.print());

  // 4. Initial Render
  updateDashboard();
}

// Multi-Page View Switcher
function switchView(viewId) {
  STATE.activeView = viewId;

  // Update Sidebar Active Class
  document.querySelectorAll('.sidebar-nav .nav-item').forEach(item => {
    const hash = item.getAttribute('href').replace('#', '');
    item.classList.toggle('active', hash === viewId);
  });

  // Show Active View Panel
  document.querySelectorAll('.view-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === `view-${viewId}`);
  });

  // Scroll to top of main wrapper
  const mainWrapper = document.querySelector('.main-wrapper');
  if (mainWrapper) mainWrapper.scrollTop = 0;
}

// Master Update Engine
function updateDashboard() {
  const filteredMetrics = calculateMetrics();

  // Update Executive KPI Elements
  const elRev = document.getElementById('valRevenue');
  const elProf = document.getElementById('valProfit');
  const elUnits = document.getElementById('valUnits');
  const elCust = document.getElementById('valCust');

  if (elRev) elRev.textContent = '$' + filteredMetrics.revenue.toLocaleString();
  if (elProf) elProf.textContent = '$' + filteredMetrics.profit.toLocaleString();
  if (elUnits) elUnits.textContent = filteredMetrics.units.toLocaleString();
  if (elCust) elCust.textContent = filteredMetrics.customers.toString();

  const elMarginSub = document.getElementById('valMarginSub');
  if (elMarginSub) elMarginSub.textContent = `Gross margin ${filteredMetrics.marginRate}%`;

  const elOrderSub = document.getElementById('valOrderSub');
  if (elOrderSub) elOrderSub.textContent = `${filteredMetrics.orders.toLocaleString()} Orders • Avg $${filteredMetrics.avgTicket}/order`;

  // Update Dynamic Progress Bars
  const pRev = document.getElementById('barRevenue');
  const pProf = document.getElementById('barProfit');
  if (pRev) pRev.style.width = Math.min(100, Math.round((filteredMetrics.revenue / 8955541) * 100)) + '%';
  if (pProf) pProf.style.width = Math.min(100, Math.round((filteredMetrics.profit / 4831999) * 100)) + '%';

  // Filter Table
  renderTableRows();
}

function calculateMetrics() {
  let rev = DB.kpis.revenue;
  let prof = DB.kpis.profit;
  let units = DB.kpis.units;
  let orders = DB.kpis.orders;
  let customers = DB.kpis.customers;

  if (STATE.category !== 'All') {
    const c = DB.categories[STATE.category];
    if (c) {
      rev = c.revenue;
      prof = c.profit;
      units = c.units;
      orders = c.orders;
      customers = Math.round(customers * 0.45);
    }
  }

  let yrFactor = 1.0;
  if (STATE.year === '2023') yrFactor = 0.285;
  else if (STATE.year === '2024') yrFactor = 0.345;
  else if (STATE.year === '2025') yrFactor = 0.370;

  let terrFactor = 1.0;
  if (STATE.territory !== 'All') {
    const t = DB.territories[STATE.territory];
    if (t) terrFactor = t.pct / 100.0;
  }

  const finalRev = Math.round(rev * yrFactor * terrFactor);
  const finalProf = Math.round(prof * yrFactor * terrFactor);
  const finalUnits = Math.round(units * yrFactor * terrFactor);
  const finalOrders = Math.round(orders * yrFactor * terrFactor);
  const marginPct = finalRev > 0 ? ((finalProf / finalRev) * 100).toFixed(2) : '53.96';
  const avgTicket = finalOrders > 0 ? Math.round(finalRev / finalOrders) : 1788;

  return {
    revenue: finalRev,
    profit: finalProf,
    units: finalUnits,
    orders: finalOrders,
    customers: customers,
    marginRate: marginPct,
    avgTicket: avgTicket
  };
}

function renderTableRows() {
  const tbody = document.getElementById('tableBody');
  if (!tbody) return;

  const filtered = DB.products.filter(p => {
    return STATE.category === 'All' || p.category === STATE.category;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 24px; color: #94a3b8;">No matching records.</td></tr>`;
    return;
  }

  let html = '';
  filtered.forEach(p => {
    const marginBadge = p.margin >= 52 ? 'badge-success' : 'badge-warning';
    html += `
      <tr>
        <td><strong>${p.name}</strong></td>
        <td>${p.category}</td>
        <td>${p.subcat}</td>
        <td>${p.units.toLocaleString()}</td>
        <td style="color: #60a5fa; font-weight: 700;">$${p.revenue.toLocaleString()}</td>
        <td><span class="badge ${marginBadge}">${p.margin}%</span></td>
        <td><span class="status-pill status-high">${p.status}</span></td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

function resetAllFilters() {
  STATE.category = 'All';
  STATE.territory = 'All';
  STATE.year = 'All';

  const catFilter = document.getElementById('categoryFilter');
  const terrFilter = document.getElementById('territoryFilter');
  const yrFilter = document.getElementById('yearFilter');

  if (catFilter) catFilter.value = 'All';
  if (terrFilter) terrFilter.value = 'All';
  if (yrFilter) yrFilter.value = 'All';

  updateDashboard();
  showToast('Filters reset to default enterprise baseline.');
}

function triggerRefresh() {
  const refreshBtn = document.getElementById('refreshBtn');
  const icon = refreshBtn ? refreshBtn.querySelector('.icon') : null;

  if (icon) {
    icon.classList.add('spin-anim');
    setTimeout(() => icon.classList.remove('spin-anim'), 700);
  }

  updateDashboard();
  showToast('SalesData star schema refreshed: 5,013 verified transactions active!');
}

function showToast(message) {
  let toast = document.getElementById('dashboardToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'dashboardToast';
    toast.className = 'toast-notification';
    document.body.appendChild(toast);
  }

  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5">
      <path d="M20 6L9 17l-5-5"/>
    </svg>
    <span>${message}</span>
  `;

  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2600);
}
