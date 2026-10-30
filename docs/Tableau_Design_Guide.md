# Tableau Visualizations, Dashboard & Story Design Guide
**Project:** Electric Vehicle Market Performance & Insights  
**Audience:** Emily Johnson (Market Strategy Director), David Chen (BI Manager), Dr. Sarah Williams (Sustainable Mobility Analyst)

---

## 1. Database Connection & Data Source Setup

### Connecting to the Data Source:
1. **Option A: Live SQLite ODBC Connection**
   - In Tableau Desktop, select **To a Server** -> **Other Databases (ODBC)**.
   - Select the SQLite3 ODBC Driver (or DSN `EV_Market_Analytics`).
   - Connect to `data/database/ev_market.db`.
   - Select the denormalized master view: `vw_ev_master_analytics`.
2. **Option B: High-Performance Tableau Data Extract (.hyper / .csv)**
   - In Tableau Desktop / Tableau Public, click **To a File** -> **Text File**.
   - Navigate to `data/tableau/ev_market_tableau_ready.csv`.
   - Verify data types:
     - `year` -> Date / Integer
     - `manufacturing_country` -> Geographic Role (Country/Region)
     - `annual_sales_units`, `price_usd`, `driving_range_km` -> Measures (Continuous)
     - `customer_rating` -> Measure (Continuous Number)

---

## 2. Calculated Fields & Level of Detail (LOD) Formulas

Tableau Calculated Fields created for advanced analytical insights:

| # | Field Name | Tableau Formula Syntax | Business Purpose |
|---|------------|------------------------|------------------|
| 1 | **Energy Efficiency (km/kWh)** | `[Driving Range Km] / [Battery Capacity Kwh]` | Measures how many kilometers the vehicle travels per 1 kWh of battery energy. |
| 2 | **Cost per KM of Range** | `[Price Usd] / [Driving Range Km]` | Measures vehicle consumer value ratio (dollar capital cost per unit of driving freedom). |
| 3 | **Charging Recovery Rate (km/min)** | `([Driving Range Km] * 0.8) / [Fast Charge Time Min]` | Speed at which driving range is replenished during 10-80% DC fast charging. |
| 4 | **Category Sales Share (LOD)** | `{FIXED [Year], [Vehicle Category]: SUM([Annual Sales Units])} / {FIXED [Year]: SUM([Annual Sales Units])}` | Exact category share percentage of total global EV sales within the active year. |
| 5 | **Manufacturer Global Share** | `SUM([Annual Sales Units]) / TOTAL(SUM([Annual Sales Units]))` | Dynamic window table calculation calculating OEM market share across applied filters. |
| 6 | **Value-to-Satisfaction Index** | `[Customer Rating] / ([Cost Per Km Range Usd] / 100)` | Custom composite KPI evaluating whether customer satisfaction matches the price efficiency. |
| 7 | **CO2 Abatement Intensity** | `([Co2 Saved Per Vehicle Annual Mt] * 1000) / [Battery Carbon Footprint Kg]` | Lifecycle sustainability index comparing yearly emissions avoided to battery manufacturing footprint. |
| 8 | **Range Tier Category** | `IF [Driving Range Km] < 200 THEN "Urban (<200km)" ELSEIF [Driving Range Km] <= 350 THEN "Standard (200-350km)" ELSEIF [Driving Range Km] <= 500 THEN "Long-Range (350-500km)" ELSEIF [Driving Range Km] <= 650 THEN "Extended (500-650km)" ELSE "Ultra-Long (>650km)" END` | Categorical classification for consumer purchase decision modeling. |
| 9 | **Price Segment** | `IF [Price Usd] < 25000 THEN "Budget (<$25K)" ELSEIF [Price Usd] <= 45000 THEN "Mass ($25K-$45K)" ELSEIF [Price Usd] <= 75000 THEN "Upper-Mid ($45K-$75K)" ELSEIF [Price Usd] <= 150000 THEN "Premium ($75K-$150K)" ELSE "Commercial/Luxury (>$150K)" END` | Pricing tiers for scenario filtering. |
| 10 | **YoY Sales Growth %** | `(ZN(SUM([Annual Sales Units])) - LOOKUP(ZN(SUM([Annual Sales Units])), -1)) / ABS(LOOKUP(ZN(SUM([Annual Sales Units])), -1))` | Table calculation computing year-over-year volume growth rate. |

---

## 3. Catalog of 12 Unique Visualizations

| Viz ID | Visualization Title | Chart Type | Dimensions & Measures | Persona Focus |
|--------|---------------------|------------|-----------------------|---------------|
| **Viz 1** | Annual Sales & Revenue Dominance by Category | Donut / Sunburst & Bar | Category, SUM(Sales Units), SUM(Revenue USD) | Emily Johnson |
| **Viz 2** | Top 10 Best-Selling EV Models | Ranked Horizontal Bar | Model Name, Manufacturer, Sales Units, Customer Rating | Emily Johnson |
| **Viz 3** | Driving Range vs Price Quadrant Analysis | Scatter Plot with Reference Lines | Driving Range (X), Price USD (Y), Color by Category, Size by Sales | Emily Johnson |
| **Viz 4** | Customer Satisfaction Distribution Across Segments | Box Plot & Violin Distribution | Category (Columns), Customer Rating (Rows), Jittered Model Points | Emily Johnson |
| **Viz 5** | Global OEM Market Share & Sales Ranking | Ranked Diverging Bar Chart | Manufacturer, Global Market Share %, YoY Growth Indicator | David Chen |
| **Viz 6** | Geographic Production Hubs vs Sales Markets | Filled Choropleth & Flow Map | Manufacturing Country, Sales Region, Export Volume | David Chen |
| **Viz 7** | OEM Battery Chemistry Portfolio Allocation | 100% Stacked Bar Chart | Manufacturer (Rows), Battery Tech (Color), Sales % (Columns) | David Chen |
| **Viz 8** | Cost-per-Kilometer Efficiency Benchmark | Sorted Horizontal Bar Chart | Manufacturer, Cost per KM Range USD, Color by Price Tier | David Chen |
| **Viz 9** | Battery Innovation & Driving Range Trajectory | Multi-Line Trend Chart (2020-2025) | Year (Columns), Avg Range KM (Rows), Color by Battery Tech | Dr. Sarah Williams |
| **Viz 10** | DC Fast-Charging Speed vs Battery Capacity | Dual-Axis Scatter Plot | Battery Capacity kWh (X), Peak Power kW (Y), Size by Fast Charge Time | Dr. Sarah Williams |
| **Viz 11** | Decarbonization Impact & CO2 Abatement | Stacked Area & KPI Cards | Year, Category, Cumulative Thousand MT CO2 Abated | Dr. Sarah Williams |
| **Viz 12** | Battery Degradation Resilience vs Carbon Intensity | Bubble Matrix Plot | Cycle Life Cycles (X), Embedded CO2 (Y), Thermal Stability (Color) | Dr. Sarah Williams |

---

## 4. Multi-Dashboard Architecture

### Dashboard 1: Executive EV Market Strategy (Persona: Emily Johnson)
- **Objective:** Enable the Market Strategy Director to optimize product portfolios and allocate capital across vehicle categories.
- **Components:**
  - 4 Executive KPI Cards: Total Fleet Sales, Total Industry Revenue, Category Leader (SUV), Avg Industry Rating.
  - Interactive Filter Panel: Year (2020-2025), Category, Price Tier.
  - Main Visualizations: Viz 1 (Sales by Category), Viz 2 (Top 10 Models), Viz 3 (Range vs Price Quadrant), Viz 4 (Customer Satisfaction).
  - Cross-filtering: Clicking a category filters model rankings and quadrant analysis dynamically.

### Dashboard 2: Automotive Competitive Intelligence (Persona: David Chen)
- **Objective:** Benchmark EV OEMs, monitor market share shifts, identify manufacturing geographic clusters, and price-to-range value propositions.
- **Components:**
  - 4 BI KPI Cards: Leading Manufacturer (BYD/Tesla), Total Active OEMs, Leading Export Hub (China), Cost/Range Benchmark.
  - Interactive Filter Panel: Manufacturer Multi-select, Region, Manufacturing Country.
  - Main Visualizations: Viz 5 (Global Market Share), Viz 6 (Geographic Hubs Map), Viz 7 (Battery Tech Strategy), Viz 8 (Cost per KM Efficiency).

### Dashboard 3: Sustainable Mobility & Battery Research (Persona: Dr. Sarah Williams)
- **Objective:** Evaluate battery chemistry shifts, clean energy impact, charging speed advancements, and lifecycle sustainability.
- **Components:**
  - 4 Tech KPI Cards: Clean Mobility Fleet Size, Total CO2 Abated (MT), Emerging Tech Adoption (Sodium-Ion / Solid-State), Avg Fast Charge Time.
  - Interactive Filter Panel: Battery Technology Selector, Year, Vehicle Category.
  - Main Visualizations: Viz 9 (Range Evolution Trend), Viz 10 (Fast Charging vs Capacity), Viz 11 (CO2 Abatement Impact), Viz 12 (Lifecycle Durability Matrix).

---

## 5. Story Mode: 5-Scene Narrative Walkthrough

- **Scene 1: The Global EV Inflection Point (2020–2025)**  
  Narrates the explosive market expansion from 2020 to 2025, reaching over 95 million annual sales globally, with transition from luxury novelty to mainstream adoption.
- **Scene 2: Emily's Strategic Lens — Category Domination & Consumer Value**  
  Deep dives into the commanding dominance of SUVs and Sedans, the surge in electric two-wheelers in emerging markets, and how consumer satisfaction directly aligns with driving range and affordability.
- **Scene 3: David's Intelligence Brief — The Battle for Market Share**  
  Deconstructs the intense rivalry between Tesla and BYD, China's manufacturing export supremacy, and legacy European and US OEMs' strategic pivot to cost-competitive models.
- **Scene 4: Dr. Sarah's Clean Frontier — Battery Tech Disruption**  
  Illustrates the rapid mainstream adoption of cobalt-free LFP chemistry, the high-range capabilities of NMC/NCA, and the cutting-edge emergence of Sodium-Ion and Solid-State batteries.
- **Scene 5: Strategic Synthesis & 2026–2030 Executive Action Plan**  
  Summarizes core recommendations: standardizing on high-cycle LFP for mass volume, accelerating 800V fast-charging architecture, diversifying battery supply chains, and targeting sub-$30K price points.

---

## 6. Tableau Public & Web Embedding Instructions
1. Save Tableau Workbook (`.twbx`) with packaged data source.
2. In Tableau Desktop, select **Server** -> **Tableau Public** -> **Save to Tableau Public**.
3. Copy the generated embed link.
4. Replace the `TABLEAU_PUBLIC_URL` parameter in the Flask web integration (`web_app/templates/tableau_embed.html`) or use the built-in dynamic embed controller.
