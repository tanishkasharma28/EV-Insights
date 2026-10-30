# Electric Vehicle Market Performance & Insights

[![Python Version](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask_3.1-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Visualization](https://img.shields.io/badge/BI-Tableau_Desktop-E97627?logo=tableau&logoColor=white)](https://www.tableau.com/)
[![Frontend](https://img.shields.io/badge/UI-Bootstrap_5_%7C_Chart.js-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

---

### Mentor Evaluation & Submission Links

> [!IMPORTANT]
> **Please use the links below to evaluate and review the project:**
> - **GitHub Repository:** [https://github.com/your-username/electric-vehicle-market-insights](https://github.com/your-username/electric-vehicle-market-insights)
> - **Live Web Application Demo:** [https://ev-market-performance-insights.onrender.com](https://ev-market-performance-insights.onrender.com)
> - **Tableau Public Dashboard & Story:** [https://public.tableau.com/views/EVMarketPerformanceInsights/ExecutiveDashboard](https://public.tableau.com/views/EVMarketPerformanceInsights/ExecutiveDashboard)
> - **End-to-End Explanation Video:** [https://youtu.be/your-video-id](https://youtu.be/your-video-id)

---

## Project Overview
The electric vehicle (EV) industry is experiencing rapid global growth driven by sustainability mandates, battery chemistry advancements, and expanding charging infrastructure. 

**Electric Vehicle Market Performance & Insights** is an end-to-end data analytics and business intelligence solution designed to evaluate market trends, OEM competitive positioning, battery innovations, and decarbonization metrics.

The platform is designed around three distinct industry scenarios:
1. **Scenario 1: Emily Johnson — EV Market Strategy Director**  
   *Focus:* Vehicle category sales contributions, top-selling model rankings, range-vs-price quadrant positioning, and consumer sentiment across product segments.
2. **Scenario 2: David Chen — Automotive Business Intelligence Manager**  
   *Focus:* OEM global market share rankings, geographical manufacturing clusters, export flow analysis, battery chemistry adoption mix, and dollar-cost-per-kilometer competitive advantages.
3. **Scenario 3: Dr. Sarah Williams — Sustainable Mobility Research Analyst**  
   *Focus:* Battery innovations (LFP, NMC, NCA, Sodium-Ion, Solid-State), range evolution (2020–2025), charging speed parity, cycle life durability, and fleet-wide CO2 abatement.

---

## Key Features

- **2,500-Record Multi-Year Dataset:** Panel data spanning 2020–2025 across 20 global automakers, 6 vehicle categories, and 5 battery chemistries.
- **Normalized SQLite Database:** Normalized tables (`manufacturers`, `models`, `battery_technologies`, `ev_market_records`), 7 B-tree indexes, and 4 specialized analytical views.
- **12 Unique Visualizations:** Categorical sales donut, top 10 ranked bar chart, range vs price scatter matrix, satisfaction box plots, OEM share diverging bars, geographic hub choropleth, battery tech stacked bar, cost-per-km efficiency benchmark, range trajectory multi-line, fast-charging scatter, fleet CO2 area chart, and durability bubble matrix.
- **3 Scenario Dashboards & 5-Scene Story:** Interactive dashboards tailored to Emily, David, and Dr. Sarah, plus a guided 5-scene story walking through the EV revolution from 2020 to 2030.
- **Interactive SQL Console:** In-browser query playground allowing mentors to execute live SELECT queries against the database with execution latency timers.
- **Performance Testing Suite:** Benchmark framework verifying sub-3.2ms query latency, high index selectivity, and low calculation overhead.
- **Tableau Public / Desktop Embedding:** Integrated Tableau embed frame supporting custom Tableau Public URLs and downloadable data sources.

---

## Project Directory Structure

```
ev-market-performance-insights/
├── data/
│   ├── raw/
│   │   └── ev_market_raw.csv                # Raw generated synthetic dataset
│   ├── processed/
│   │   └── ev_market_cleaned.csv            # Preprocessed and validated dataset
│   ├── database/
│   │   └── ev_market.db                     # Normalized SQLite database with indexes & views
│   └── tableau/
│       └── ev_market_tableau_ready.csv      # Tableau-ready extract with calculated metrics
├── sql/
│   ├── schema.sql                           # DDL schema, tables, indexes, and views
│   └── analytical_queries.sql               # 12 analytical SQL queries for the 3 scenarios
├── scripts/
│   ├── generate_dataset.py                  # Realistic panel dataset generator
│   ├── setup_database.py                    # Schema creation and DB ingestion script
│   └── performance_benchmark.py             # Performance benchmark test suite
├── web_app/
│   ├── app.py                               # Flask backend application & REST APIs
│   ├── templates/
│   │   ├── base.html                        # Base template with responsive navigation
│   │   ├── index.html                       # Global overview & executive KPIs
│   │   ├── scenario_emily.html              # Emily Johnson strategy dashboard
│   │   ├── scenario_david.html              # David Chen BI intelligence dashboard
│   │   ├── scenario_sarah.html              # Dr. Sarah Williams research dashboard
│   │   ├── story.html                       # 5-Scene interactive story mode
│   │   ├── tableau_embed.html               # Tableau embed & connection guide
│   │   ├── sql_explorer.html                # Interactive SQL query playground
│   │   ├── performance.html                 # Performance testing benchmarks report
│   │   └── documentation.html               # Step-by-step documentation & links
│   └── static/
│       ├── css/
│       │   └── custom.css                   # Custom modern dark theme styling
│       └── js/
│           └── dashboard.js                 # Dynamic Chart.js and SQL runner engine
├── docs/
│   ├── Project_Documentation.md             # Complete step-by-step project procedure
│   ├── Tableau_Design_Guide.md              # 12 viz specifications & 10+ calculated fields
│   ├── Video_Demonstration_Script.md        # Script for recording presentation video
│   └── performance_benchmark_results.json   # Exported benchmark latency metrics
├── requirements.txt                         # Python dependencies
└── README.md                                # Root documentation & guide
```

---

## Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/electric-vehicle-market-insights.git
cd electric-vehicle-market-insights
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Generate Data & Initialize Database (Already pre-built)
```bash
# Optional: regenerate dataset
python scripts/generate_dataset.py

# Optional: rebuild SQLite database and views
python scripts/setup_database.py

# Optional: run performance benchmark suite
python scripts/performance_benchmark.py
```

### 4. Launch the Web Application
```bash
python web_app/app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## Tableau Connection & Calculated Fields Guide

1. Open Tableau Desktop / Tableau Public.
2. Select **Connect -> Text File** and open `data/tableau/ev_market_tableau_ready.csv`.
3. Utilize the pre-configured calculated fields:
   - **Energy Efficiency:** `[Driving Range Km] / [Battery Capacity Kwh]`
   - **Cost per KM:** `[Price Usd] / [Driving Range Km]`
   - **LOD Category Share:** `{FIXED [Year], [Category]: SUM([Sales])} / {FIXED [Year]: SUM([Sales])}`
   - **Charging Speed (km/min):** `([Driving Range Km] * 0.8) / [Fast Charge Time Min]`
   - **CO2 Abatement Intensity:** `([CO2 Saved Annual Mt] * 1000) / [Battery Carbon Footprint Kg]`
4. Publish the workbook to Tableau Public and paste the share URL into the web application's **Tableau Embed** tab!

---

## Performance Benchmark Summary

| Metric | Benchmark Result | Performance Target | Status |
|--------|------------------|--------------------|--------|
| **Total Rows Rendered** | 2,500 records (32 attributes) | > 1,000 records | PASS |
| **Indexed Query Latency** | 0.55 ms – 2.44 ms | < 10.0 ms | OPTIMAL |
| **Multi-Criteria Filter Latency** | 0.25 ms – 1.12 ms | < 5.0 ms | OPTIMAL |
| **Calculated Field Overhead** | 0.29 ms – 0.35 ms | < 1.0 ms | OPTIMAL |
| **SQL Master View Rows** | 2,500 rows | 2,500 rows | 100% PASS |

---

## License & Attribution
Developed for the **Electric Vehicle Market Performance & Insights** Capstone Analytics Track.
Designed with Python, SQLite, Tableau BI, Flask, and Bootstrap.
