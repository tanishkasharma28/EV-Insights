"""
Electric Vehicle Market Performance & Insights
Flask Web Application Backend
Integrates Tableau Embeds, Persona Dashboards, Story Mode, and Interactive SQL Explorer.
"""

import os
import sqlite3
import json
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database", "ev_market.db")
BENCHMARK_PATH = os.path.join(BASE_DIR, "docs", "performance_benchmark_results.json")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Global Executive KPIs (Latest Year: 2025)
    c.execute("""
        SELECT 
            SUM(annual_sales_units) AS total_units,
            ROUND(SUM(total_revenue_usd) / 1e9, 2) AS total_rev_bn,
            ROUND(AVG(driving_range_km), 0) AS avg_range,
            ROUND(AVG(customer_rating), 2) AS avg_rating,
            COUNT(DISTINCT manufacturer) AS total_mfg,
            ROUND(SUM(total_co2_abated_thousand_mt) / 1e3, 2) AS total_co2_mn_mt
        FROM vw_ev_master_analytics
        WHERE year = 2025;
    """)
    kpis = dict(c.fetchone())
    
    # Category Breakdown
    c.execute("""
        SELECT vehicle_category, SUM(annual_sales_units) as sales, ROUND(SUM(total_revenue_usd)/1e9, 2) as rev
        FROM vw_ev_master_analytics
        WHERE year = 2025
        GROUP BY vehicle_category
        ORDER BY sales DESC;
    """)
    category_summary = [dict(row) for row in c.fetchall()]
    
    # Available filter options
    c.execute("SELECT DISTINCT year FROM vw_ev_master_analytics ORDER BY year DESC;")
    years = [row[0] for row in c.fetchall()]
    
    conn.close()
    return render_template("index.html", kpis=kpis, categories=category_summary, years=years)

@app.route("/scenario/emily")
def scenario_emily():
    """Emily Johnson - EV Market Strategy Director"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT vehicle_category FROM models ORDER BY vehicle_category;")
    categories = [row[0] for row in c.fetchall()]
    c.execute("SELECT DISTINCT year FROM vw_ev_master_analytics ORDER BY year DESC;")
    years = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template("scenario_emily.html", categories=categories, years=years)

@app.route("/scenario/david")
def scenario_david():
    """David Chen - Automotive Business Intelligence Manager"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT manufacturer_name FROM manufacturers ORDER BY manufacturer_name;")
    manufacturers = [row[0] for row in c.fetchall()]
    c.execute("SELECT DISTINCT manufacturing_country FROM ev_market_records ORDER BY manufacturing_country;")
    countries = [row[0] for row in c.fetchall()]
    c.execute("SELECT DISTINCT year FROM vw_ev_master_analytics ORDER BY year DESC;")
    years = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template("scenario_david.html", manufacturers=manufacturers, countries=countries, years=years)

@app.route("/scenario/sarah")
def scenario_sarah():
    """Dr. Sarah Williams - Sustainable Mobility Research Analyst"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT tech_code, full_name FROM battery_technologies ORDER BY tech_code;")
    technologies = [dict(row) for row in c.fetchall()]
    c.execute("SELECT DISTINCT year FROM vw_ev_master_analytics ORDER BY year DESC;")
    years = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template("scenario_sarah.html", technologies=technologies, years=years)

@app.route("/tableau")
def tableau_embed():
    """Tableau Desktop / Tableau Public Embed Integration"""
    return render_template("tableau_embed.html")

@app.route("/story")
def story():
    """5-Scene Interactive Story Walkthrough"""
    return render_template("story.html")

@app.route("/sql-explorer")
def sql_explorer():
    """Interactive SQL Query Console against ev_market.db"""
    return render_template("sql_explorer.html")

@app.route("/performance")
def performance():
    """Performance Testing & Benchmark Metrics"""
    benchmark_data = {}
    if os.path.exists(BENCHMARK_PATH):
        with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
            benchmark_data = json.load(f)
    return render_template("performance.html", benchmarks=benchmark_data)

@app.route("/documentation")
def documentation():
    """Full Step-by-Step Project Documentation & Evaluation Links"""
    return render_template("documentation.html")


# ====================================================================
# API ENDPOINTS FOR DYNAMIC DASHBOARDS & CHART VISUALIZATIONS
# ====================================================================

@app.route("/api/scenario/emily")
def api_scenario_emily():
    year = request.args.get("year", "2025")
    category = request.args.get("category", "All")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    where_clauses = ["year = ?"]
    params = [int(year)]
    
    if category != "All":
        where_clauses.append("vehicle_category = ?")
        params.append(category)
        
    where_str = " AND ".join(where_clauses)
    
    # 1. Sales & Revenue by Category
    c.execute(f"""
        SELECT vehicle_category, SUM(annual_sales_units) as total_sales, ROUND(SUM(total_revenue_usd)/1e9, 2) as total_rev
        FROM vw_ev_master_analytics
        WHERE year = ?
        GROUP BY vehicle_category
        ORDER BY total_sales DESC;
    """, (int(year),))
    cat_sales = [dict(r) for r in c.fetchall()]
    
    # 2. Top 10 Best-Selling Models
    c.execute(f"""
        SELECT manufacturer, model_name, vehicle_category, annual_sales_units, price_usd, driving_range_km, customer_rating
        FROM vw_ev_master_analytics
        WHERE {where_str}
        ORDER BY annual_sales_units DESC
        LIMIT 10;
    """, params)
    top_models = [dict(r) for r in c.fetchall()]
    
    # 3. Driving Range vs Price Distribution (Scatter)
    c.execute(f"""
        SELECT model_name, manufacturer, vehicle_category, driving_range_km, price_usd, annual_sales_units, customer_rating
        FROM vw_ev_master_analytics
        WHERE {where_str}
        ORDER BY annual_sales_units DESC
        LIMIT 80;
    """, params)
    scatter_data = [dict(r) for r in c.fetchall()]
    
    # 4. Customer Satisfaction by Segment
    c.execute(f"""
        SELECT vehicle_category, ROUND(AVG(customer_rating), 2) as avg_rating, ROUND(MIN(customer_rating), 2) as min_rating, ROUND(MAX(customer_rating), 2) as max_rating
        FROM vw_ev_master_analytics
        WHERE year = ?
        GROUP BY vehicle_category
        ORDER BY avg_rating DESC;
    """, (int(year),))
    ratings_by_cat = [dict(r) for r in c.fetchall()]
    
    # Executive KPIs
    c.execute(f"""
        SELECT 
            SUM(annual_sales_units) as total_sales,
            ROUND(SUM(total_revenue_usd)/1e9, 2) as total_rev_bn,
            ROUND(AVG(driving_range_km), 0) as avg_range,
            ROUND(AVG(customer_rating), 2) as avg_rating
        FROM vw_ev_master_analytics
        WHERE {where_str};
    """, params)
    summary_kpi = dict(c.fetchone())
    
    conn.close()
    return jsonify({
        "kpis": summary_kpi,
        "cat_sales": cat_sales,
        "top_models": top_models,
        "scatter": scatter_data,
        "ratings": ratings_by_cat
    })

@app.route("/api/scenario/david")
def api_scenario_david():
    year = request.args.get("year", "2025")
    country = request.args.get("country", "All")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    where_clauses = ["year = ?"]
    params = [int(year)]
    
    if country != "All":
        where_clauses.append("manufacturing_country = ?")
        params.append(country)
        
    where_str = " AND ".join(where_clauses)
    
    # 1. Manufacturer Market Share & Sales
    c.execute(f"""
        SELECT manufacturer, SUM(annual_sales_units) as total_sales, ROUND(SUM(total_revenue_usd)/1e9, 2) as total_rev, ROUND(AVG(customer_rating), 2) as avg_rating
        FROM vw_ev_master_analytics
        WHERE {where_str}
        GROUP BY manufacturer
        ORDER BY total_sales DESC
        LIMIT 10;
    """, params)
    mfg_share = [dict(r) for r in c.fetchall()]
    
    # 2. Manufacturing Country Production Distribution
    c.execute(f"""
        SELECT manufacturing_country, SUM(annual_sales_units) as total_produced, ROUND(SUM(total_revenue_usd)/1e9, 2) as total_value
        FROM vw_ev_master_analytics
        WHERE year = ?
        GROUP BY manufacturing_country
        ORDER BY total_produced DESC;
    """, (int(year),))
    mfg_countries = [dict(r) for r in c.fetchall()]
    
    # 3. Battery Chemistry Mix by Top Manufacturers
    c.execute(f"""
        SELECT manufacturer, battery_technology, SUM(annual_sales_units) as units
        FROM vw_ev_master_analytics
        WHERE year = ? AND manufacturer IN ('Tesla', 'BYD', 'Volkswagen', 'Hyundai', 'BMW', 'Tata Motors')
        GROUP BY manufacturer, battery_technology
        ORDER BY manufacturer, units DESC;
    """, (int(year),))
    tech_mix = [dict(r) for r in c.fetchall()]
    
    # 4. Cost-per-Kilometer Value Benchmark
    c.execute(f"""
        SELECT manufacturer, ROUND(AVG(cost_per_km_range_usd), 2) as avg_cost_per_km, ROUND(AVG(driving_range_km), 0) as avg_range
        FROM vw_ev_master_analytics
        WHERE year = ?
        GROUP BY manufacturer
        ORDER BY avg_cost_per_km ASC
        LIMIT 12;
    """, (int(year),))
    cost_per_km = [dict(r) for r in c.fetchall()]
    
    conn.close()
    return jsonify({
        "mfg_share": mfg_share,
        "mfg_countries": mfg_countries,
        "tech_mix": tech_mix,
        "cost_per_km": cost_per_km
    })

@app.route("/api/scenario/sarah")
def api_scenario_sarah():
    tech = request.args.get("tech", "All")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    where_str = "1=1"
    params = []
    if tech != "All":
        where_str = "battery_technology = ?"
        params.append(tech)
        
    # 1. Driving Range Evolution (2020-2025)
    c.execute(f"""
        SELECT year, battery_technology, ROUND(AVG(driving_range_km), 1) as avg_range, ROUND(AVG(efficiency_km_per_kwh), 2) as avg_efficiency
        FROM vw_ev_master_analytics
        WHERE {where_str}
        GROUP BY year, battery_technology
        ORDER BY year ASC, battery_technology;
    """, params)
    range_evolution = [dict(r) for r in c.fetchall()]
    
    # 2. Charging Speed (kW) vs Battery Capacity (kWh)
    c.execute(f"""
        SELECT battery_technology, max_charging_power_kw, battery_capacity_kwh, fast_charge_time_min, model_name
        FROM vw_ev_master_analytics
        WHERE year = 2025 AND {where_str}
        LIMIT 60;
    """, params)
    charging_matrix = [dict(r) for r in c.fetchall()]
    
    # 3. Decarbonization: Cumulative CO2 Abated by Category
    c.execute(f"""
        SELECT vehicle_category, ROUND(SUM(total_co2_abated_thousand_mt), 1) as total_co2_abated_k_mt, SUM(annual_sales_units) as total_sales
        FROM vw_ev_master_analytics
        WHERE year = 2025
        GROUP BY vehicle_category
        ORDER BY total_co2_abated_k_mt DESC;
    """)
    co2_by_cat = [dict(r) for r in c.fetchall()]
    
    # 4. Battery Durability & Degradation Resilience
    c.execute(f"""
        SELECT battery_technology, thermal_stability, ROUND(AVG(battery_cycle_life_cycles), 0) as avg_cycles, ROUND(AVG(battery_carbon_footprint_kg), 0) as avg_carbon_kg
        FROM vw_ev_master_analytics
        GROUP BY battery_technology, thermal_stability
        ORDER BY avg_cycles DESC;
    """)
    durability = [dict(r) for r in c.fetchall()]
    
    conn.close()
    return jsonify({
        "range_evolution": range_evolution,
        "charging_matrix": charging_matrix,
        "co2_by_cat": co2_by_cat,
        "durability": durability
    })

@app.route("/api/execute-sql", methods=["POST"])
def execute_sql():
    """Safe read-only execution of queries against SQLite for interactive mentor testing."""
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Empty SQL query provided."}), 400
        
    # Security: allow only read-only statements
    lower_query = query.lower()
    forbidden = ["drop", "delete", "insert", "update", "alter", "truncate", "create", "replace"]
    if any(lower_query.startswith(cmd) or f" {cmd} " in lower_query for cmd in forbidden):
        return jsonify({"error": "Read-only access permitted. DDL/DML write statements are disabled."}), 403
        
    try:
        start_time = time.perf_counter()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(100) # Limit to 100 rows for display
        execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        results = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return jsonify({
            "columns": columns,
            "rows": results,
            "row_count": len(results),
            "execution_time_ms": execution_time_ms
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("[*] Starting Electric Vehicle Market Performance & Insights Flask Server...")
    print("[*] Accessible locally at: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
