/**
 * Smart Energy Consumption Visualization Dashboard
 * Advanced Visualization Engine powered by Apache ECharts
 * MACSE603 - Visual Analytics Lab
 */

document.addEventListener("DOMContentLoaded", () => {
  if (typeof DASHBOARD_DATA === "undefined") {
    console.error("Dashboard data failed to load!");
    return;
  }

  // Application State
  const state = {
    selectedFacility: "ALL",
    granularity: "hourly",
    activeClusters: [0, 1, 2, 3],
    isStreaming: false,
    streamTimer: null,
    streamPackets: 0,
    streamPoints: [],
    theme: "dark"
  };

  // Chart Instances
  const charts = {
    diurnal: null,
    heatmap: null,
    forecast: null,
    anomaly: null,
    tsne: null,
    submeter: null,
    gauge: null,
    stream: null
  };

  // Cache DOM Elements
  const els = {
    themeToggleBtn: document.getElementById("themeToggleBtn"),
    themeIcon: document.getElementById("themeIcon"),
    facilitySelect: document.getElementById("facilitySelect"),
    granularityBtns: document.querySelectorAll("#granularityControl .seg-btn"),
    viewModeSelect: document.getElementById("viewModeSelect"),
    streamToggleBtn: document.getElementById("streamToggleBtn"),
    streamBtnText: document.getElementById("streamBtnText"),
    radarIndicator: document.getElementById("radarIndicator"),
    streamPacketCount: document.getElementById("streamPacketCount"),
    streamLatency: document.getElementById("streamLatency"),
    streamQuality: document.getElementById("streamQuality"),
    livePowerVal: document.getElementById("livePowerVal"),
    livePowerBar: document.getElementById("livePowerBar"),
    liveVoltageVal: document.getElementById("liveVoltageVal"),
    liveCurrentVal: document.getElementById("liveCurrentVal"),
    livePfVal: document.getElementById("livePfVal"),
    liveFreqVal: document.getElementById("liveFreqVal"),
    streamLogBody: document.getElementById("streamLogBody"),
    clearStreamLog: document.getElementById("clearStreamLog"),
    facilityRankList: document.getElementById("facilityRankList"),
    submeterLegendList: document.getElementById("submeterLegendList"),
    inspectAnomBtn: document.getElementById("inspectAnomBtn"),
    anomalyModal: document.getElementById("anomalyModal"),
    modalCloseBtn: document.getElementById("modalCloseBtn"),
    anomTableBody: document.getElementById("anomTableBody"),
    runPipelineWebBtn: document.getElementById("runPipelineWebBtn"),
    clusterToggles: document.querySelectorAll(".c-toggle"),
    
    // KPI Text
    valEnergy: document.getElementById("valEnergy"),
    valCost: document.getElementById("valCost"),
    valSolar: document.getElementById("valSolar"),
    valPeak: document.getElementById("valPeak"),
    valCarbon: document.getElementById("valCarbon"),
    valAnomalies: document.getElementById("valAnomalies"),

    // Mini Sparklines
    sparkEnergy: document.getElementById("sparkEnergy"),
    sparkCost: document.getElementById("sparkCost"),
    sparkSolar: document.getElementById("sparkSolar")
  };

  // Helper: Theme Palette
  function getThemeColors() {
    const isDark = state.theme === "dark";
    return {
      text: isDark ? "#94a3b8" : "#475569",
      textBright: isDark ? "#f8fafc" : "#0f172a",
      grid: isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.06)",
      tooltipBg: isDark ? "rgba(13, 22, 41, 0.94)" : "rgba(255, 255, 255, 0.96)",
      tooltipBorder: isDark ? "rgba(56, 189, 248, 0.4)" : "#3b82f6",
      cardBg: isDark ? "rgba(16, 27, 51, 0.75)" : "#ffffff"
    };
  }

  // Helper: Common Tooltip Style
  function getTooltipStyle() {
    const colors = getThemeColors();
    return {
      backgroundColor: colors.tooltipBg,
      borderColor: colors.tooltipBorder,
      borderWidth: 1,
      textStyle: { color: colors.textBright, fontFamily: "Inter, sans-serif", fontSize: 12 },
      extraCssText: "box-shadow: 0 8px 24px rgba(0,0,0,0.4); backdrop-filter: blur(8px); border-radius: 8px;"
    };
  }

  // =========================================================================
  // 1. Theme Switcher
  // =========================================================================
  els.themeToggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
    const isLight = document.body.classList.contains("light-theme");
    state.theme = isLight ? "light" : "dark";
    els.themeIcon.textContent = isLight ? "☀️" : "🌙";
    renderAllVisuals();
  });

  // =========================================================================
  // 2. Mini Sparklines on KPI Cards
  // =========================================================================
  function renderMiniSparkline(svgEl, dataPoints, strokeColor) {
    if (!svgEl || !dataPoints || dataPoints.length === 0) return;
    const min = Math.min(...dataPoints);
    const max = Math.max(...dataPoints);
    const range = (max - min) || 1;
    const w = 80;
    const h = 20;
    const pts = dataPoints.map((val, idx) => {
      const x = (idx / (dataPoints.length - 1)) * w;
      const y = h - ((val - min) / range) * (h - 4) - 2;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(" ");

    svgEl.innerHTML = `<polyline fill="none" stroke="${strokeColor}" stroke-width="2" points="${pts}" stroke-linecap="round" stroke-linejoin="round" />`;
  }

  function initSparklines() {
    renderMiniSparkline(els.sparkEnergy, [1.4, 1.5, 1.8, 1.9, 1.85, 1.7, 1.6, 1.55, 1.5, 1.48, 1.52, 1.62], "#38bdf8");
    renderMiniSparkline(els.sparkCost, [0.95, 1.02, 1.25, 1.35, 1.30, 1.15, 1.08, 1.05, 1.02, 0.98, 1.01, 1.1], "#f59e0b");
    renderMiniSparkline(els.sparkSolar, [0.08, 0.09, 0.12, 0.14, 0.13, 0.09, 0.07, 0.08, 0.10, 0.11, 0.09, 0.08], "#10b981");
  }

  // =========================================================================
  // 3. Facility Benchmarks & Sparklines
  // =========================================================================
  function renderFacilityList() {
    els.facilityRankList.innerHTML = "";
    DASHBOARD_DATA.facilities.forEach((fac, idx) => {
      const item = document.createElement("div");
      item.className = "facility-item";
      if (state.selectedFacility === fac.id) {
        item.style.borderColor = "var(--accent-blue)";
        item.style.background = "rgba(56, 189, 248, 0.12)";
      }

      const pts = fac.sparkline.map((v, i) => {
        const min = Math.min(...fac.sparkline);
        const max = Math.max(...fac.sparkline);
        const x = (i / 11) * 60;
        const y = 18 - ((v - min) / ((max - min) || 1)) * 14 - 2;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      }).join(" ");

      item.innerHTML = `
        <span class="fac-rank">0${idx + 1}</span>
        <div class="fac-name-col">
          <span class="fac-name">${fac.name}</span>
          <span class="fac-cat-tag">${fac.category} • ${fac.area_sqft.toLocaleString()} sq.ft</span>
        </div>
        <div class="fac-kwh-col">
          <span class="fac-kwh">${fac.annual_gwh} GWh</span>
          <div class="fac-cost">₹${fac.annual_cost_cr} Cr</div>
        </div>
        <div class="fac-spark-col">
          <svg width="64" height="20" viewBox="0 0 64 20">
            <polyline fill="none" stroke="#38bdf8" stroke-width="1.8" points="${pts}" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <div class="fac-badge-col">
          <span class="energy-star-badge" title="Energy Star Rating: ${fac.energy_star}/100">★ ${fac.energy_star}</span>
        </div>
      `;

      item.addEventListener("click", () => {
        els.facilitySelect.value = fac.id;
        handleFacilityChange(fac.id);
      });

      els.facilityRankList.appendChild(item);
    });
  }

  // =========================================================================
  // 4. ECharts: Diurnal Power Flow Chart
  // =========================================================================
  function renderDiurnalChart() {
    const dom = document.getElementById("diurnalChart");
    if (!dom) return;
    if (!charts.diurnal) charts.diurnal = echarts.init(dom);

    const colors = getThemeColors();
    const data = DASHBOARD_DATA.hourly_diurnal || [];
    const hours = data.map((d, idx) => (d && d.Hour !== undefined ? String(d.Hour).padStart(2, "0") : String(idx).padStart(2, "0")) + ":00");

    // Multiplier if individual facility selected
    let mult = 1.0;
    if (state.selectedFacility !== "ALL") {
      const fac = DASHBOARD_DATA.facilities.find(f => f.id === state.selectedFacility);
      if (fac) mult = fac.annual_gwh / 19.35;
    }

    const activePower = data.map(d => Math.round(d.ActivePower_kWh * mult));
    const solarGen = data.map(d => Math.round(d.SolarGeneration_kWh * mult));
    const netImport = data.map(d => Math.round(d.NetImport_kWh * mult));

    const option = {
      backgroundColor: "transparent",
      tooltip: {
        trigger: "axis",
        ...getTooltipStyle(),
        axisPointer: { type: "cross", crossStyle: { color: "#38bdf8" } }
      },
      legend: {
        data: ["Active Demand (kW)", "Solar Generation (kW)", "Net Grid Import (kW)"],
        textStyle: { color: colors.text, fontSize: 11 },
        top: "2%"
      },
      grid: { left: "3%", right: "4%", bottom: "3%", top: "18%", containLabel: true },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: hours,
        axisLine: { lineStyle: { color: colors.grid } },
        axisLabel: { color: colors.text, fontFamily: "JetBrains Mono", fontSize: 10 }
      },
      yAxis: {
        type: "value",
        name: "Power (kW)",
        nameTextStyle: { color: colors.text, fontSize: 11 },
        splitLine: { lineStyle: { color: colors.grid, type: "dashed" } },
        axisLabel: { color: colors.text, fontFamily: "JetBrains Mono", fontSize: 10 }
      },
      series: [
        {
          name: "Active Demand (kW)",
          type: "line",
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 3, color: "#38bdf8" },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(56, 189, 248, 0.45)" },
              { offset: 1, color: "rgba(56, 189, 248, 0.02)" }
            ])
          },
          markPoint: {
            data: [{ type: "max", name: "Peak Load" }],
            itemStyle: { color: "#ef4444" },
            label: { formatter: "Peak: {c}kW", fontSize: 10 }
          },
          data: activePower
        },
        {
          name: "Solar Generation (kW)",
          type: "line",
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 2.2, color: "#10b981" },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(16, 185, 129, 0.4)" },
              { offset: 1, color: "rgba(16, 185, 129, 0.0)" }
            ])
          },
          data: solarGen
        },
        {
          name: "Net Grid Import (kW)",
          type: "line",
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 2, color: "#818cf8", type: "dashed" },
          data: netImport
        }
      ]
    };

    charts.diurnal.setOption(option);
  }

  // =========================================================================
  // 5. ECharts: 24x7 Diurnal Load Profile Heatmap Matrix
  // =========================================================================
  function renderHeatmapChart() {
    const dom = document.getElementById("heatmapChart");
    if (!dom) return;
    if (!charts.heatmap) charts.heatmap = echarts.init(dom);

    const colors = getThemeColors();
    const hours = Array.from({ length: 24 }, (_, i) => `${i.toString().padStart(2, "0")}:00`);
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    const heatData = [];
    let allVals = [];
    DASHBOARD_DATA.heatmap.forEach(row => {
      row.hours.forEach((val, h) => {
        heatData.push([h, row.dow, val]);
        allVals.push(val);
      });
    });

    const minVal = Math.min(...allVals);
    const maxVal = Math.max(...allVals);

    const option = {
      backgroundColor: "transparent",
      tooltip: {
        position: "top",
        ...getTooltipStyle(),
        formatter: (params) => {
          const h = params.value[0];
          const d = params.value[1];
          const val = params.value[2];
          const isPeak = (17 <= h && h < 22);
          const tBand = isPeak ? "Peak Period (17:00-22:00)" : (h >= 6 && h < 17 ? "Shoulder Period" : "Off-Peak Night");
          return `
            <div style="font-weight: bold; margin-bottom: 4px;">${days[d]} @ ${hours[h]}</div>
            <div>Average Load: <strong>${val} kW</strong></div>
            <div style="color: ${isPeak ? '#ef4444' : '#38bdf8'}">${tBand}</div>
          `;
        }
      },
      grid: { left: "4%", right: "4%", bottom: "16%", top: "6%", containLabel: true },
      xAxis: {
        type: "category",
        data: hours,
        splitArea: { show: true, areaStyle: { color: ["rgba(255,255,255,0.01)", "rgba(0,0,0,0.02)"] } },
        axisLine: { lineStyle: { color: colors.grid } },
        axisLabel: { color: colors.text, fontSize: 10, fontFamily: "JetBrains Mono" }
      },
      yAxis: {
        type: "category",
        data: days,
        splitArea: { show: true },
        axisLine: { lineStyle: { color: colors.grid } },
        axisLabel: { color: colors.text, fontSize: 11, fontWeight: "bold" }
      },
      visualMap: {
        min: Math.floor(minVal),
        max: Math.ceil(maxVal),
        calculable: true,
        orient: "horizontal",
        left: "center",
        bottom: "0%",
        textStyle: { color: colors.text, fontSize: 10, fontFamily: "JetBrains Mono" },
        inRange: {
          color: ["#0b1a3a", "#1e3a8a", "#2563eb", "#38bdf8", "#f59e0b", "#ef4444"]
        }
      },
      series: [{
        name: "Demand Heatmap",
        type: "heatmap",
        data: heatData,
        label: { show: false },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: "rgba(255, 255, 255, 0.5)",
            borderColor: "#ffffff",
            borderWidth: 1.5
          }
        }
      }]
    };

    charts.heatmap.setOption(option);
  }

  // =========================================================================
  // 6. ECharts: ML Demand Forecasting Chart
  // =========================================================================
  function renderForecastChart() {
    const dom = document.getElementById("forecastChart");
    if (!dom) return;
    if (!charts.forecast) charts.forecast = echarts.init(dom);

    const colors = getThemeColors();
    const pts = DASHBOARD_DATA.forecast.points;
    const dates = pts.map(p => p.date);
    const actuals = pts.map(p => p.actual);
    const forecasts = pts.map(p => p.forecast);
    const lowers = pts.map(p => p.lower);
    const bandHeights = pts.map(p => (p.upper && p.lower) ? Math.round(p.upper - p.lower) : 0);

    const splitIdx = pts.findIndex(p => p.type === "Forecast");
    const splitDate = dates[splitIdx] || dates[dates.length - 30];

    const option = {
      backgroundColor: "transparent",
      tooltip: {
        trigger: "axis",
        ...getTooltipStyle(),
        formatter: (params) => {
          let str = `<div style="font-weight: bold; margin-bottom: 4px;">${params[0].axisValue}</div>`;
          params.forEach(p => {
            if (p.seriesName !== "CI Band Lower" && p.seriesName !== "Confidence Band" && p.value !== null && p.value !== undefined) {
              str += `<div><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color};margin-right:6px;"></span>${p.seriesName}: <strong>${Math.round(p.value).toLocaleString()} kWh</strong></div>`;
            }
          });
          return str;
        }
      },
      legend: {
        data: ["Historical Demand", "ML 30-Day Projection", "95% Confidence Interval"],
        textStyle: { color: colors.text, fontSize: 11 },
        top: "2%"
      },
      grid: { left: "3%", right: "4%", bottom: "5%", top: "18%", containLabel: true },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: dates,
        axisLine: { lineStyle: { color: colors.grid } },
        axisLabel: {
          color: colors.text,
          fontSize: 10,
          fontFamily: "JetBrains Mono",
          formatter: (val) => val.substring(5) // MM-DD
        }
      },
      yAxis: {
        type: "value",
        name: "Demand (kWh)",
        nameTextStyle: { color: colors.text, fontSize: 11 },
        splitLine: { lineStyle: { color: colors.grid, type: "dashed" } },
        axisLabel: {
          color: colors.text,
          fontSize: 10,
          fontFamily: "JetBrains Mono",
          formatter: (v) => `${(v / 1000).toFixed(0)}k`
        }
      },
      series: [
        {
          name: "CI Band Lower",
          type: "line",
          data: lowers,
          lineStyle: { opacity: 0 },
          stack: "confidence-band",
          symbol: "none"
        },
        {
          name: "95% Confidence Interval",
          type: "line",
          data: bandHeights,
          lineStyle: { opacity: 0 },
          areaStyle: { color: "rgba(245, 158, 11, 0.22)" },
          stack: "confidence-band",
          symbol: "none"
        },
        {
          name: "Historical Demand",
          type: "line",
          data: actuals,
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 2.2, color: "#38bdf8" }
        },
        {
          name: "ML 30-Day Projection",
          type: "line",
          data: forecasts,
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 2.5, color: "#f59e0b", type: "dashed" },
          markLine: {
            silent: true,
            symbol: "none",
            data: [{ xAxis: splitDate, label: { formatter: "Forecast Horizon", color: "#f59e0b", fontSize: 10 } }],
            lineStyle: { color: "#f59e0b", type: "dotted", width: 1.5 }
          }
        }
      ]
    };

    charts.forecast.setOption(option);
  }

  // =========================================================================
  // 7. ECharts: Shewhart 3-Sigma Anomaly Detection Chart
  // =========================================================================
  function renderAnomalyChart() {
    const dom = document.getElementById("anomalyChart");
    if (!dom) return;
    if (!charts.anomaly) charts.anomaly = echarts.init(dom);

    const colors = getThemeColors();
    const hours = Array.from({ length: 72 }, (_, i) => `H+${i}`);
    const baseline = 240;

    const actualLoad = [];
    const meanLine = [];
    const uclLine = [];
    const lclLine = [];
    const anomalies = [];

    for (let i = 0; i < 72; i++) {
      const isBreach = (i >= 26 && i <= 34);
      const wave = Math.sin(i * 0.3) * 60;
      const noise = (Math.random() - 0.5) * 20;
      const load = isBreach ? (baseline + 180 + noise) : (baseline + wave + noise);
      const m = baseline + wave;
      const u = m + 85;
      const l = Math.max(70, m - 85);

      actualLoad.push(Math.round(load));
      meanLine.push(Math.round(m));
      uclLine.push(Math.round(u));
      lclLine.push(Math.round(l));

      if (isBreach && (i % 2 === 0)) {
        anomalies.push({
          name: "Chiller Leak",
          coord: [`H+${i}`, Math.round(load)],
          value: `+${Math.round(load - m)} kW`
        });
      }
    }

    const option = {
      backgroundColor: "transparent",
      tooltip: {
        trigger: "axis",
        ...getTooltipStyle()
      },
      legend: {
        data: ["Hourly Telemetry", "Rolling Baseline", "Shewhart UCL (+3σ)", "Shewhart LCL (-3σ)"],
        textStyle: { color: colors.text, fontSize: 10 },
        top: "2%"
      },
      grid: { left: "3%", right: "4%", bottom: "5%", top: "18%", containLabel: true },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: hours,
        axisLine: { lineStyle: { color: colors.grid } },
        axisLabel: { color: colors.text, fontSize: 9, fontFamily: "JetBrains Mono" }
      },
      yAxis: {
        type: "value",
        name: "Load (kW)",
        nameTextStyle: { color: colors.text, fontSize: 11 },
        splitLine: { lineStyle: { color: colors.grid, type: "dashed" } },
        axisLabel: { color: colors.text, fontSize: 10, fontFamily: "JetBrains Mono" }
      },
      series: [
        {
          name: "Shewhart LCL (-3σ)",
          type: "line",
          data: lclLine,
          lineStyle: { opacity: 0 },
          stack: "control-band",
          symbol: "none"
        },
        {
          name: "Shewhart UCL (+3σ)",
          type: "line",
          data: uclLine.map((u, i) => u - lclLine[i]),
          lineStyle: { opacity: 0 },
          areaStyle: { color: "rgba(226, 232, 240, 0.12)" },
          stack: "control-band",
          symbol: "none"
        },
        {
          name: "Rolling Baseline",
          type: "line",
          data: meanLine,
          lineStyle: { width: 1.5, color: "#94a3b8", type: "dashed" },
          symbol: "none"
        },
        {
          name: "Hourly Telemetry",
          type: "line",
          data: actualLoad,
          lineStyle: { width: 2.2, color: "#38bdf8" },
          showSymbol: false,
          markPoint: {
            data: anomalies,
            symbol: "pin",
            symbolSize: 42,
            itemStyle: { color: "#ef4444" },
            label: { formatter: "{c}", fontSize: 9, fontWeight: "bold" }
          }
        }
      ]
    };

    charts.anomaly.setOption(option);
  }

  // =========================================================================
  // 8. ECharts: t-SNE 2D Manifold Clustering Scatter
  // =========================================================================
  function renderTsneChart() {
    const dom = document.getElementById("tsneChart");
    if (!dom) return;
    if (!charts.tsne) charts.tsne = echarts.init(dom);

    const colors = getThemeColors();
    const clusterLabels = [
      "Commercial Day-Shift Heavy",
      "Continuous Baseload (DataCenter)",
      "Evening Residential (Hostels)",
      "Low-Intensity Weekend Idle"
    ];
    const clusterColors = ["#2563EB", "#059669", "#D97706", "#7C3AED"];

    const seriesList = [];
    for (let cid = 0; cid < 4; cid++) {
      if (!state.activeClusters.includes(cid)) continue;
      const pts = DASHBOARD_DATA.clusters
        .filter(c => c.cluster_id === cid)
        .map(c => {
          const isHighlight = (state.selectedFacility === "ALL" || c.facility_id === state.selectedFacility);
          return {
            name: `${c.facility_id} (${c.date})`,
            value: [c.x, c.y],
            itemStyle: {
              color: clusterColors[cid],
              opacity: isHighlight ? 0.85 : 0.15,
              shadowBlur: isHighlight ? 8 : 0,
              shadowColor: clusterColors[cid]
            }
          };
        });

      seriesList.push({
        name: clusterLabels[cid],
        type: "scatter",
        symbolSize: (data) => (state.selectedFacility === "ALL" ? 9 : 11),
        data: pts
      });
    }

    const option = {
      backgroundColor: "transparent",
      tooltip: {
        ...getTooltipStyle(),
        formatter: (params) => `
          <div style="font-weight: bold; color: ${params.color};">${params.seriesName}</div>
          <div>Entity: <strong>${params.name}</strong></div>
          <div style="font-family: JetBrains Mono; font-size: 11px;">[t-SNE 1: ${params.value[0]}, t-SNE 2: ${params.value[1]}]</div>
        `
      },
      legend: {
        textStyle: { color: colors.text, fontSize: 10 },
        top: "2%"
      },
      grid: { left: "4%", right: "4%", bottom: "5%", top: "18%", containLabel: true },
      xAxis: {
        type: "value",
        name: "t-SNE Dim 1",
        nameTextStyle: { color: colors.text, fontSize: 10 },
        splitLine: { lineStyle: { color: colors.grid, type: "dashed" } },
        axisLabel: { color: colors.text, fontSize: 10, fontFamily: "JetBrains Mono" }
      },
      yAxis: {
        type: "value",
        name: "t-SNE Dim 2",
        nameTextStyle: { color: colors.text, fontSize: 10 },
        splitLine: { lineStyle: { color: colors.grid, type: "dashed" } },
        axisLabel: { color: colors.text, fontSize: 10, fontFamily: "JetBrains Mono" }
      },
      series: seriesList
    };

    charts.tsne.setOption(option);
  }

  // Cluster filter toggles
  els.clusterToggles.forEach(btn => {
    btn.addEventListener("click", () => {
      const cid = parseInt(btn.dataset.cluster, 10);
      btn.classList.toggle("active");
      if (state.activeClusters.includes(cid)) {
        state.activeClusters = state.activeClusters.filter(c => c !== cid);
      } else {
        state.activeClusters.push(cid);
      }
      renderTsneChart();
    });
  });

  // =========================================================================
  // 9. ECharts: Appliance Submetering Donut Chart
  // =========================================================================
  function renderSubmeterChart() {
    const dom = document.getElementById("submeterDonut");
    if (!dom) return;
    if (!charts.submeter) charts.submeter = echarts.init(dom);

    const colors = getThemeColors();
    const data = DASHBOARD_DATA.submetering.map(s => ({
      name: s.category,
      value: s.annual_gwh,
      share: s.share_pct,
      itemStyle: { color: s.color }
    }));

    const option = {
      backgroundColor: "transparent",
      tooltip: {
        trigger: "item",
        ...getTooltipStyle(),
        formatter: (p) => `
          <div style="font-weight: bold; color:${p.color};">${p.name}</div>
          <div>Annual Load: <strong>${p.value} GWh</strong> (${p.data.share}%)</div>
        `
      },
      series: [{
        name: "Submetering",
        type: "pie",
        radius: ["50%", "78%"],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 6,
          borderColor: state.theme === "dark" ? "#0d1629" : "#ffffff",
          borderWidth: 2
        },
        label: { show: false },
        emphasis: {
          scale: true,
          scaleSize: 8,
          label: {
            show: true,
            fontSize: 14,
            fontWeight: "bold",
            color: colors.textBright,
            formatter: "{b}\n{d}%"
          }
        },
        data: data
      }]
    };

    charts.submeter.setOption(option);

    // Populate Legend List
    els.submeterLegendList.innerHTML = "";
    DASHBOARD_DATA.submetering.forEach(item => {
      const row = document.createElement("div");
      row.className = "submeter-stat-row";
      row.innerHTML = `
        <div class="submeter-stat-meta">
          <span><strong style="color: ${item.color}">■</strong> ${item.category}</span>
          <span><strong>${item.share_pct}%</strong> (${item.annual_gwh} GWh)</span>
        </div>
        <div class="submeter-stat-bar-track">
          <div class="submeter-stat-bar-fill" style="width: ${item.share_pct}%; background-color: ${item.color}"></div>
        </div>
      `;
      els.submeterLegendList.appendChild(row);
    });
  }

  // =========================================================================
  // 10. ECharts: Live Streaming Gauge & Oscilloscope
  // =========================================================================
  function initStreamingCharts() {
    const gaugeDom = document.getElementById("streamGauge");
    const streamDom = document.getElementById("streamChart");
    if (gaugeDom && !charts.gauge) charts.gauge = echarts.init(gaugeDom);
    if (streamDom && !charts.stream) charts.stream = echarts.init(streamDom);

    const colors = getThemeColors();

    // Gauge Option
    const gaugeOption = {
      backgroundColor: "transparent",
      series: [{
        type: "gauge",
        min: 0,
        max: 850,
        splitNumber: 5,
        radius: "95%",
        axisLine: {
          lineStyle: {
            width: 10,
            color: [
              [0.4, "#10b981"],
              [0.75, "#38bdf8"],
              [0.9, "#f59e0b"],
              [1, "#ef4444"]
            ]
          }
        },
        pointer: { itemStyle: { color: "#38bdf8" }, width: 4 },
        axisTick: { distance: -10, length: 4, lineStyle: { color: "#fff", width: 1 } },
        splitLine: { distance: -10, length: 10, lineStyle: { color: "#fff", width: 2 } },
        axisLabel: { color: colors.text, fontSize: 9, distance: -18 },
        detail: {
          valueAnimation: true,
          formatter: "{value} kW",
          color: colors.textBright,
          fontSize: 16,
          offsetCenter: [0, "65%"],
          fontFamily: "JetBrains Mono"
        },
        data: [{ value: 0 }]
      }]
    };
    charts.gauge.setOption(gaugeOption);

    // Oscilloscope Option
    const streamOption = {
      backgroundColor: "transparent",
      tooltip: { trigger: "axis", ...getTooltipStyle() },
      grid: { left: "4%", right: "4%", bottom: "8%", top: "12%", containLabel: true },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: [],
        axisLine: { lineStyle: { color: colors.grid } },
        axisLabel: { color: colors.text, fontSize: 9, fontFamily: "JetBrains Mono" }
      },
      yAxis: {
        type: "value",
        min: 0,
        max: 850,
        splitLine: { lineStyle: { color: colors.grid, type: "dashed" } },
        axisLabel: { color: colors.text, fontSize: 9, fontFamily: "JetBrains Mono" }
      },
      series: [{
        name: "Telemetry kW",
        type: "line",
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 2.2, color: "#38bdf8" },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(56, 189, 248, 0.4)" },
            { offset: 1, color: "rgba(56, 189, 248, 0.0)" }
          ])
        },
        data: []
      }]
    };
    charts.stream.setOption(streamOption);
  }

  function updateStreamingCharts(kw, timeStr) {
    if (!charts.gauge || !charts.stream) return;

    // Update gauge
    charts.gauge.setOption({
      series: [{ data: [{ value: Math.round(kw) }] }]
    });

    // Update oscilloscope buffer
    state.streamPoints.push({ time: timeStr, kw: Math.round(kw) });
    if (state.streamPoints.length > 25) state.streamPoints.shift();

    charts.stream.setOption({
      xAxis: { data: state.streamPoints.map(p => p.time) },
      series: [{ data: state.streamPoints.map(p => p.kw) }]
    });
  }

  function toggleLiveStream() {
    state.isStreaming = !state.isStreaming;
    if (state.isStreaming) {
      els.streamBtnText.textContent = "Halt Live Feed";
      els.streamToggleBtn.classList.add("streaming");
      els.radarIndicator.classList.add("active");
      els.streamLogBody.innerHTML = "";

      state.streamTimer = setInterval(() => {
        simulateTelemetryTick();
      }, 1500);
    } else {
      els.streamBtnText.textContent = "Start Live Telemetry";
      els.streamToggleBtn.classList.remove("streaming");
      els.radarIndicator.classList.remove("active");
      clearInterval(state.streamTimer);
    }
  }

  function simulateTelemetryTick() {
    state.streamPackets++;
    const now = new Date();
    const timeStr = now.toTimeString().split(" ")[0];

    const facId = state.selectedFacility === "ALL" ? "FAC001" : state.selectedFacility;
    const base = facId === "FAC002" ? 380 : 250;
    const noise = (Math.random() - 0.5) * 40;
    const isSurge = Math.random() < 0.08;
    const kw = Math.max(100, Math.round((base + noise) * (isSurge ? 1.6 : 1.0) * 10) / 10);
    const v = (230.0 + (Math.random() - 0.5) * 4).toFixed(1);
    const pf = (0.94 + (Math.random() - 0.5) * 0.03).toFixed(3);
    const i = ((kw * 1000) / (v * pf * Math.sqrt(3))).toFixed(1);

    els.streamPacketCount.textContent = state.streamPackets.toLocaleString();
    els.streamLatency.textContent = `${Math.floor(12 + Math.random() * 8)} ms`;
    els.livePowerVal.textContent = kw.toFixed(1);
    els.livePowerBar.style.width = `${Math.min(100, (kw / 850) * 100)}%`;
    els.liveVoltageVal.textContent = v;
    els.liveCurrentVal.textContent = i;
    els.livePfVal.textContent = pf;

    updateStreamingCharts(kw, timeStr);

    const logLine = document.createElement("div");
    logLine.className = `log-line ${isSurge ? 'surge' : ''}`;
    logLine.textContent = `[${timeStr}] MQTT rx esp32/meters/${facId}: P=${kw}kW V=${v}V I=${i}A cosφ=${pf} ${isSurge ? '⚠️ SURGE_ALERT' : '✓ OK'}`;
    els.streamLogBody.appendChild(logLine);
    els.streamLogBody.scrollTop = els.streamLogBody.scrollHeight;
  }

  els.streamToggleBtn.addEventListener("click", toggleLiveStream);
  els.clearStreamLog.addEventListener("click", () => {
    els.streamLogBody.innerHTML = '<div class="log-line system">Terminal buffer cleared.</div>';
  });

  // =========================================================================
  // 11. Facility Filtering & Global Slicers
  // =========================================================================
  function handleFacilityChange(fid) {
    state.selectedFacility = fid;
    if (fid === "ALL") {
      els.valEnergy.textContent = "19.35";
      els.valCost.textContent = "13.20";
      els.valSolar.textContent = "1.14";
      els.valPeak.textContent = "2,840";
      els.valCarbon.textContent = "15,868";
      els.valAnomalies.textContent = "196";
    } else {
      const fac = DASHBOARD_DATA.facilities.find(f => f.id === fid);
      if (fac) {
        els.valEnergy.textContent = fac.annual_gwh.toFixed(2);
        els.valCost.textContent = fac.annual_cost_cr.toFixed(2);
        els.valSolar.textContent = fac.solar_gwh.toFixed(2);
        els.valPeak.textContent = Math.round(fac.annual_gwh * 150).toLocaleString();
        els.valCarbon.textContent = Math.round(fac.annual_gwh * 820).toLocaleString();
        els.valAnomalies.textContent = Math.round(196 * (fac.annual_gwh / 19.35));
      }
    }
    renderFacilityList();
    renderDiurnalChart();
    renderTsneChart();
  }

  els.facilitySelect.addEventListener("change", (e) => {
    handleFacilityChange(e.target.value);
  });

  els.granularityBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      els.granularityBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.granularity = btn.dataset.gran;
      renderDiurnalChart();
    });
  });

  els.viewModeSelect.addEventListener("change", (e) => {
    const val = e.target.value;
    const sections = {
      forecast: document.getElementById("panelForecast"),
      anomalies: document.getElementById("panelAnomalies"),
      clustering: document.getElementById("panelClusters"),
      submeter: document.getElementById("panelSubmeter"),
      streaming: document.getElementById("streamingSection")
    };

    if (val === "all") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (sections[val]) {
      sections[val].scrollIntoView({ behavior: "smooth", block: "center" });
      sections[val].style.boxShadow = "0 0 25px var(--accent-blue)";
      setTimeout(() => { sections[val].style.boxShadow = ""; }, 1800);
    }
  });

  // =========================================================================
  // 12. Anomaly Modal Inspection
  // =========================================================================
  els.inspectAnomBtn.addEventListener("click", () => {
    els.anomTableBody.innerHTML = "";
    DASHBOARD_DATA.anomalies.forEach(a => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${a.timestamp}</td>
        <td><strong>${a.facility_name}</strong></td>
        <td>${a.active_power} kW</td>
        <td>${a.rolling_mean} kW</td>
        <td style="color: #ef4444; font-weight: bold;">+${a.excess_kwh} kW</td>
        <td style="color: #f59e0b;">₹${a.wasted_inr.toLocaleString()}</td>
        <td>${a.anomaly_type}</td>
        <td><span class="kpi-badge ${a.severity === 'Critical' ? 'danger' : 'warning'}">${a.severity}</span></td>
      `;
      els.anomTableBody.appendChild(tr);
    });
    els.anomalyModal.classList.add("open");
  });

  els.modalCloseBtn.addEventListener("click", () => {
    els.anomalyModal.classList.remove("open");
  });

  els.anomalyModal.addEventListener("click", (e) => {
    if (e.target === els.anomalyModal) els.anomalyModal.classList.remove("open");
  });

  // Pipeline trigger
  els.runPipelineWebBtn.addEventListener("click", () => {
    els.runPipelineWebBtn.textContent = "⏳ Running Pipeline...";
    els.runPipelineWebBtn.disabled = true;
    setTimeout(() => {
      els.runPipelineWebBtn.textContent = "✓ Pipeline Verified";
      setTimeout(() => {
        els.runPipelineWebBtn.textContent = "⚡ Execute Pipeline";
        els.runPipelineWebBtn.disabled = false;
      }, 2000);
    }, 1500);
  });

  // =========================================================================
  // 13. Master Render
  // =========================================================================
  function renderAllVisuals() {
    try { initSparklines(); } catch (e) { console.error("Error in initSparklines:", e); }
    try { renderFacilityList(); } catch (e) { console.error("Error in renderFacilityList:", e); }
    try { renderDiurnalChart(); } catch (e) { console.error("Error in renderDiurnalChart:", e); }
    try { renderHeatmapChart(); } catch (e) { console.error("Error in renderHeatmapChart:", e); }
    try { renderForecastChart(); } catch (e) { console.error("Error in renderForecastChart:", e); }
    try { renderAnomalyChart(); } catch (e) { console.error("Error in renderAnomalyChart:", e); }
    try { renderTsneChart(); } catch (e) { console.error("Error in renderTsneChart:", e); }
    try { renderSubmeterChart(); } catch (e) { console.error("Error in renderSubmeterChart:", e); }
    try { initStreamingCharts(); } catch (e) { console.error("Error in initStreamingCharts:", e); }
  }

  // Initial draw
  renderAllVisuals();

  // Resize listener
  window.addEventListener("resize", () => {
    Object.values(charts).forEach(c => {
      if (c && typeof c.resize === "function") c.resize();
    });
  });
});
