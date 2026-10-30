/**
 * Electric Vehicle Market Performance & Insights
 * Dynamic Dashboard Visualizations & SQL Runner Engine
 */

// Global Chart instances to allow smooth re-rendering on filter changes
let charts = {};

// Helper to destroy chart before re-creating
function destroyChart(id) {
    if (charts[id]) {
        charts[id].destroy();
        delete charts[id];
    }
}

// -------------------------------------------------------------
// SCENARIO 1: EMILY JOHNSON (MARKET STRATEGY DIRECTOR)
// -------------------------------------------------------------
function loadEmilyDashboard() {
    const year = document.getElementById("emilyYearSelect") ? document.getElementById("emilyYearSelect").value : "2025";
    const category = document.getElementById("emilyCategorySelect") ? document.getElementById("emilyCategorySelect").value : "All";

    fetch(`/api/scenario/emily?year=${year}&category=${encodeURIComponent(category)}`)
        .then(res => res.json())
        .then(data => {
            // Update KPIs
            if (data.kpis) {
                if (document.getElementById("emilyKpiSales")) {
                    document.getElementById("emilyKpiSales").innerText = (data.kpis.total_sales || 0).toLocaleString() + " units";
                }
                if (document.getElementById("emilyKpiRevenue")) {
                    document.getElementById("emilyKpiRevenue").innerText = "$" + (data.kpis.total_rev_bn || 0) + "B";
                }
                if (document.getElementById("emilyKpiRange")) {
                    document.getElementById("emilyKpiRange").innerText = (data.kpis.avg_range || 0) + " km";
                }
                if (document.getElementById("emilyKpiRating")) {
                    document.getElementById("emilyKpiRating").innerText = (data.kpis.avg_rating || 0) + " / 5.0";
                }
            }

            // Viz 1: Category Sales Share (Doughnut)
            destroyChart("chartCategorySales");
            const ctxCat = document.getElementById("chartCategorySales");
            if (ctxCat && data.cat_sales) {
                charts["chartCategorySales"] = new Chart(ctxCat, {
                    type: 'doughnut',
                    data: {
                        labels: data.cat_sales.map(c => c.vehicle_category),
                        datasets: [{
                            data: data.cat_sales.map(c => c.total_sales),
                            backgroundColor: ['#38bdf8', '#818cf8', '#34d399', '#fbbf24', '#f43f5e', '#a855f7'],
                            borderColor: '#131b2e',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom', labels: { color: '#94a3b8' } }
                        }
                    }
                });
            }

            // Viz 2: Top 10 Best-Selling Models (Ranked Horizontal Bar)
            destroyChart("chartTopModels");
            const ctxTop = document.getElementById("chartTopModels");
            if (ctxTop && data.top_models) {
                charts["chartTopModels"] = new Chart(ctxTop, {
                    type: 'bar',
                    data: {
                        labels: data.top_models.map(m => `${m.manufacturer} ${m.model_name}`),
                        datasets: [{
                            label: 'Annual Units Sold',
                            data: data.top_models.map(m => m.annual_sales_units),
                            backgroundColor: '#0284c7',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            y: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            }

            // Viz 3: Driving Range vs Price Quadrant (Scatter)
            destroyChart("chartRangeVsPrice");
            const ctxScatter = document.getElementById("chartRangeVsPrice");
            if (ctxScatter && data.scatter) {
                charts["chartRangeVsPrice"] = new Chart(ctxScatter, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'EV Models',
                            data: data.scatter.map(s => ({
                                x: s.driving_range_km,
                                y: s.price_usd,
                                model: `${s.manufacturer} ${s.model_name}`,
                                cat: s.vehicle_category
                            })),
                            backgroundColor: 'rgba(56, 189, 248, 0.7)',
                            borderColor: '#38bdf8',
                            pointHoverRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { 
                                title: { display: true, text: 'Driving Range (km)', color: '#94a3b8' },
                                grid: { color: 'rgba(255,255,255,0.05)' }, 
                                ticks: { color: '#94a3b8' } 
                            },
                            y: { 
                                title: { display: true, text: 'Price (USD $)', color: '#94a3b8' },
                                grid: { color: 'rgba(255,255,255,0.05)' }, 
                                ticks: { color: '#94a3b8' } 
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        const p = ctx.raw;
                                        return `${p.model} (${p.cat}): ${p.x} km | $${p.y.toLocaleString()}`;
                                    }
                                }
                            }
                        }
                    }
                });
            }

            // Viz 4: Customer Satisfaction Ratings
            destroyChart("chartRatings");
            const ctxRatings = document.getElementById("chartRatings");
            if (ctxRatings && data.ratings) {
                charts["chartRatings"] = new Chart(ctxRatings, {
                    type: 'bar',
                    data: {
                        labels: data.ratings.map(r => r.vehicle_category),
                        datasets: [{
                            label: 'Avg Customer Rating',
                            data: data.ratings.map(r => r.avg_rating),
                            backgroundColor: '#10b981',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { min: 3.0, max: 5.0, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            x: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            }
        });
}

// -------------------------------------------------------------
// SCENARIO 2: DAVID CHEN (AUTOMOTIVE BI MANAGER)
// -------------------------------------------------------------
function loadDavidDashboard() {
    const year = document.getElementById("davidYearSelect") ? document.getElementById("davidYearSelect").value : "2025";
    const country = document.getElementById("davidCountrySelect") ? document.getElementById("davidCountrySelect").value : "All";

    fetch(`/api/scenario/david?year=${year}&country=${encodeURIComponent(country)}`)
        .then(res => res.json())
        .then(data => {
            // Viz 5: Manufacturer Market Share
            destroyChart("chartMfgShare");
            const ctxShare = document.getElementById("chartMfgShare");
            if (ctxShare && data.mfg_share) {
                charts["chartMfgShare"] = new Chart(ctxShare, {
                    type: 'bar',
                    data: {
                        labels: data.mfg_share.map(m => m.manufacturer),
                        datasets: [{
                            label: 'Sales Units',
                            data: data.mfg_share.map(m => m.total_sales),
                            backgroundColor: '#3b82f6',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            y: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            }

            // Viz 6: Manufacturing Hubs
            destroyChart("chartMfgCountry");
            const ctxCountry = document.getElementById("chartMfgCountry");
            if (ctxCountry && data.mfg_countries) {
                charts["chartMfgCountry"] = new Chart(ctxCountry, {
                    type: 'bar',
                    data: {
                        labels: data.mfg_countries.map(c => c.manufacturing_country),
                        datasets: [{
                            label: 'Vehicles Produced',
                            data: data.mfg_countries.map(c => c.total_produced),
                            backgroundColor: '#8b5cf6',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            x: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            }

            // Viz 8: Cost per KM Benchmark
            destroyChart("chartCostPerKm");
            const ctxCost = document.getElementById("chartCostPerKm");
            if (ctxCost && data.cost_per_km) {
                charts["chartCostPerKm"] = new Chart(ctxCost, {
                    type: 'bar',
                    data: {
                        labels: data.cost_per_km.map(c => c.manufacturer),
                        datasets: [{
                            label: 'Cost per KM ($/km)',
                            data: data.cost_per_km.map(c => c.avg_cost_per_km),
                            backgroundColor: '#f59e0b',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            x: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            }
        });
}

// -------------------------------------------------------------
// SCENARIO 3: DR. SARAH WILLIAMS (SUSTAINABLE MOBILITY)
// -------------------------------------------------------------
function loadSarahDashboard() {
    const tech = document.getElementById("sarahTechSelect") ? document.getElementById("sarahTechSelect").value : "All";

    fetch(`/api/scenario/sarah?tech=${encodeURIComponent(tech)}`)
        .then(res => res.json())
        .then(data => {
            // Viz 9: Driving Range Trajectory (2020-2025)
            destroyChart("chartRangeEvolution");
            const ctxEvo = document.getElementById("chartRangeEvolution");
            if (ctxEvo && data.range_evolution) {
                // Group by tech
                const years = [2020, 2021, 2022, 2023, 2024, 2025];
                const techGroups = {};
                data.range_evolution.forEach(item => {
                    if (!techGroups[item.battery_technology]) {
                        techGroups[item.battery_technology] = {};
                    }
                    techGroups[item.battery_technology][item.year] = item.avg_range;
                });

                const colors = {
                    'LFP': '#34d399',
                    'NMC': '#38bdf8',
                    'NCA': '#fbbf24',
                    'Sodium-Ion': '#f43f5e',
                    'Solid-State': '#a855f7'
                };

                const datasets = Object.keys(techGroups).map(t => ({
                    label: t,
                    data: years.map(yr => techGroups[t][yr] || null),
                    borderColor: colors[t] || '#fff',
                    backgroundColor: colors[t] || '#fff',
                    tension: 0.3,
                    fill: false
                }));

                charts["chartRangeEvolution"] = new Chart(ctxEvo, {
                    type: 'line',
                    data: { labels: years, datasets: datasets },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { title: { display: true, text: 'Average Driving Range (km)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
                    }
                });
            }

            // Viz 11: CO2 Abatement by Category
            destroyChart("chartCo2Abatement");
            const ctxCo2 = document.getElementById("chartCo2Abatement");
            if (ctxCo2 && data.co2_by_cat) {
                charts["chartCo2Abatement"] = new Chart(ctxCo2, {
                    type: 'bar',
                    data: {
                        labels: data.co2_by_cat.map(c => c.vehicle_category),
                        datasets: [{
                            label: 'Total CO2 Abated (Thousand MT)',
                            data: data.co2_by_cat.map(c => c.total_co2_abated_k_mt),
                            backgroundColor: '#10b981',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            x: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            }

            // Viz 12: Durability Cycle Life
            destroyChart("chartDurability");
            const ctxDur = document.getElementById("chartDurability");
            if (ctxDur && data.durability) {
                charts["chartDurability"] = new Chart(ctxDur, {
                    type: 'bar',
                    data: {
                        labels: data.durability.map(d => `${d.battery_technology} (${d.thermal_stability})`),
                        datasets: [{
                            label: 'Average Cycle Life (Cycles)',
                            data: data.durability.map(d => d.avg_cycles),
                            backgroundColor: '#06b6d4',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            y: { grid: { display: false }, ticks: { color: '#f8fafc' } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            }
        });
}

// -------------------------------------------------------------
// INTERACTIVE SQL QUERY RUNNER
// -------------------------------------------------------------
function runSqlQuery() {
    const queryEditor = document.getElementById("sqlQueryEditor");
    const resultContainer = document.getElementById("sqlResultsContainer");
    const statusText = document.getElementById("sqlStatusText");

    if (!queryEditor || !queryEditor.value.trim()) return;

    statusText.innerHTML = '<span class="text-info"><i class="fa-solid fa-spinner fa-spin me-1"></i> Executing query against ev_market.db...</span>';

    fetch("/api/execute-sql", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryEditor.value })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            statusText.innerHTML = `<span class="text-danger"><i class="fa-solid fa-triangle-exclamation me-1"></i> Error: ${data.error}</span>`;
            resultContainer.innerHTML = '';
            return;
        }

        statusText.innerHTML = `<span class="text-success"><i class="fa-solid fa-check me-1"></i> Success: ${data.row_count} rows fetched in ${data.execution_time_ms} ms</span>`;

        if (!data.columns || data.columns.length === 0) {
            resultContainer.innerHTML = '<p class="text-muted">Query executed successfully (no rows returned).</p>';
            return;
        }

        let html = '<div class="table-responsive"><table class="table table-custom"><thead><tr>';
        data.columns.forEach(col => {
            html += `<th>${col}</th>`;
        });
        html += '</tr></thead><tbody>';

        data.rows.forEach(row => {
            html += '<tr>';
            data.columns.forEach(col => {
                html += `<td>${row[col] !== null ? row[col] : '<span class="text-muted">NULL</span>'}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table></div>';
        resultContainer.innerHTML = html;
    })
    .catch(err => {
        statusText.innerHTML = `<span class="text-danger">Failed to execute: ${err}</span>`;
    });
}

function loadPrebuiltSql(queryType) {
    const queryEditor = document.getElementById("sqlQueryEditor");
    if (!queryEditor) return;

    const queries = {
        "emily_sales": "SELECT vehicle_category, SUM(annual_sales_units) AS total_units, ROUND(SUM(total_revenue_usd)/1e9, 2) AS revenue_billion_usd, ROUND(AVG(customer_rating), 2) AS avg_rating FROM vw_ev_master_analytics WHERE year = 2025 GROUP BY vehicle_category ORDER BY total_units DESC;",
        "emily_top10": "SELECT manufacturer, model_name, vehicle_category, battery_technology, driving_range_km, price_usd, annual_sales_units FROM vw_ev_master_analytics WHERE year = 2025 ORDER BY annual_sales_units DESC LIMIT 10;",
        "david_market_share": "SELECT manufacturer, COUNT(DISTINCT model_name) AS models_count, SUM(annual_sales_units) AS total_sales, ROUND((SUM(annual_sales_units) * 100.0) / (SELECT SUM(annual_sales_units) FROM vw_ev_master_analytics WHERE year = 2025), 2) AS global_market_share_pct FROM vw_ev_master_analytics WHERE year = 2025 GROUP BY manufacturer ORDER BY total_sales DESC LIMIT 10;",
        "david_hubs": "SELECT manufacturing_country, primary_sales_region, COUNT(*) AS models_built, SUM(annual_sales_units) AS units_produced FROM vw_ev_master_analytics WHERE year = 2025 GROUP BY manufacturing_country, primary_sales_region ORDER BY units_produced DESC LIMIT 12;",
        "sarah_battery_evo": "SELECT year, battery_technology, ROUND(AVG(driving_range_km), 1) AS avg_range_km, ROUND(AVG(efficiency_km_per_kwh), 2) AS avg_efficiency, ROUND(AVG(fast_charge_time_min), 1) AS avg_fast_charge_min FROM vw_ev_master_analytics GROUP BY year, battery_technology ORDER BY battery_technology, year ASC;",
        "sarah_co2": "SELECT vehicle_category, SUM(annual_sales_units) AS fleet_size, ROUND(SUM(total_co2_abated_thousand_mt), 1) AS total_co2_abated_k_mt FROM vw_ev_master_analytics WHERE year = 2025 GROUP BY vehicle_category ORDER BY total_co2_abated_k_mt DESC;"
    };

    if (queries[queryType]) {
        queryEditor.value = queries[queryType];
        runSqlQuery();
    }
}

// -------------------------------------------------------------
// STORY MODE CONTROLLER (5 SCENES)
// -------------------------------------------------------------
let currentStoryScene = 1;
const totalStoryScenes = 5;

function showStoryScene(sceneIndex) {
    if (sceneIndex < 1 || sceneIndex > totalStoryScenes) return;
    currentStoryScene = sceneIndex;

    // Hide all scenes
    for (let i = 1; i <= totalStoryScenes; i++) {
        const el = document.getElementById(`storyScene${i}`);
        if (el) el.style.display = (i === currentStoryScene) ? 'block' : 'none';

        const dot = document.getElementById(`storyDot${i}`);
        if (dot) {
            if (i === currentStoryScene) dot.classList.add('active');
            else dot.classList.remove('active');
        }
    }

    // Scroll smoothly to top of story card
    const storyCard = document.getElementById("storyContainer");
    if (storyCard) storyCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function nextStoryScene() {
    if (currentStoryScene < totalStoryScenes) {
        showStoryScene(currentStoryScene + 1);
    }
}

function prevStoryScene() {
    if (currentStoryScene > 1) {
        showStoryScene(currentStoryScene - 1);
    }
}
