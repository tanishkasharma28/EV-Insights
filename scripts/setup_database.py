"""
Electric Vehicle Market Performance & Insights
Database Ingestion & SQL Setup Script
Creates normalized tables, analytical views, and indexes in SQLite.
"""

import os
import sqlite3
import pandas as pd

def setup_database():
    base_dir = r"C:\Users\makro\.gemini\antigravity\scratch\ev-market-performance-insights"
    csv_path = os.path.join(base_dir, "data", "processed", "ev_market_cleaned.csv")
    db_path = os.path.join(base_dir, "data", "database", "ev_market.db")
    sql_schema_path = os.path.join(base_dir, "sql", "schema.sql")
    sql_queries_path = os.path.join(base_dir, "sql", "analytical_queries.sql")
    
    print(f"[*] Reading cleaned data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create Schema
    schema_sql = """
    PRAGMA foreign_keys = ON;

    DROP VIEW IF EXISTS vw_executive_sales_summary;
    DROP VIEW IF EXISTS vw_manufacturer_competitive_intel;
    DROP VIEW IF EXISTS vw_battery_innovation_sustainability;
    DROP VIEW IF EXISTS vw_ev_master_analytics;

    DROP TABLE IF EXISTS ev_market_records;
    DROP TABLE IF EXISTS models;
    DROP TABLE IF EXISTS manufacturers;
    DROP TABLE IF EXISTS battery_technologies;

    -- 1. Manufacturers Table
    CREATE TABLE manufacturers (
        manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer_name TEXT NOT NULL UNIQUE,
        country_of_origin TEXT NOT NULL
    );

    -- 2. Battery Technologies Table
    CREATE TABLE battery_technologies (
        battery_tech_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tech_code TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        thermal_stability TEXT NOT NULL
    );

    -- 3. Vehicle Models Table
    CREATE TABLE models (
        model_id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer_id INTEGER NOT NULL,
        model_name TEXT NOT NULL,
        vehicle_category TEXT NOT NULL,
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id),
        UNIQUE(manufacturer_id, model_name)
    );

    -- 4. Main Market Performance Records Table
    CREATE TABLE ev_market_records (
        record_id INTEGER PRIMARY KEY,
        year INTEGER NOT NULL,
        manufacturer_id INTEGER NOT NULL,
        model_id INTEGER NOT NULL,
        battery_tech_id INTEGER NOT NULL,
        manufacturing_country TEXT NOT NULL,
        primary_sales_region TEXT NOT NULL,
        battery_capacity_kwh REAL NOT NULL,
        driving_range_km INTEGER NOT NULL,
        driving_range_miles INTEGER NOT NULL,
        energy_consumption_kwh_per_100km REAL NOT NULL,
        efficiency_km_per_kwh REAL NOT NULL,
        max_charging_power_kw INTEGER NOT NULL,
        fast_charge_time_min INTEGER NOT NULL,
        price_usd INTEGER NOT NULL,
        cost_per_km_range_usd REAL NOT NULL,
        annual_sales_units INTEGER NOT NULL,
        total_revenue_usd REAL NOT NULL,
        customer_rating REAL NOT NULL,
        reviews_count INTEGER NOT NULL,
        co2_saved_per_vehicle_annual_mt REAL NOT NULL,
        total_co2_abated_thousand_mt REAL NOT NULL,
        battery_cycle_life_cycles INTEGER NOT NULL,
        battery_carbon_footprint_kg INTEGER NOT NULL,
        price_tier TEXT,
        range_tier TEXT,
        market_share_percentage REAL,
        category_market_share_percentage REAL,
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id),
        FOREIGN KEY (model_id) REFERENCES models(model_id),
        FOREIGN KEY (battery_tech_id) REFERENCES battery_technologies(battery_tech_id)
    );

    -- Performance Indexes for Accelerated BI & SQL Queries
    CREATE INDEX idx_ev_year ON ev_market_records(year);
    CREATE INDEX idx_ev_mfg ON ev_market_records(manufacturer_id);
    CREATE INDEX idx_ev_cat ON models(vehicle_category);
    CREATE INDEX idx_ev_tech ON ev_market_records(battery_tech_id);
    CREATE INDEX idx_ev_mfg_country ON ev_market_records(manufacturing_country);
    CREATE INDEX idx_ev_sales ON ev_market_records(annual_sales_units DESC);
    CREATE INDEX idx_ev_rating ON ev_market_records(customer_rating DESC);
    """
    
    cursor.executescript(schema_sql)
    print("[+] Created normalized tables and performance indexes.")
    
    # 2. Populate lookup tables
    # Manufacturers
    mfg_df = df[["manufacturer", "manufacturer_country"]].drop_duplicates()
    for _, row in mfg_df.iterrows():
        cursor.execute("INSERT INTO manufacturers (manufacturer_name, country_of_origin) VALUES (?, ?)", 
                       (row["manufacturer"], row["manufacturer_country"]))
    
    # Battery Tech
    tech_df = df[["battery_technology", "battery_tech_full_name", "thermal_stability"]].drop_duplicates()
    for _, row in tech_df.iterrows():
        cursor.execute("INSERT INTO battery_technologies (tech_code, full_name, thermal_stability) VALUES (?, ?, ?)",
                       (row["battery_technology"], row["battery_tech_full_name"], row["thermal_stability"]))
                       
    # Models
    cursor.execute("SELECT manufacturer_id, manufacturer_name FROM manufacturers")
    mfg_map = {name: mid for mid, name in cursor.fetchall()}
    
    cursor.execute("SELECT battery_tech_id, tech_code FROM battery_technologies")
    tech_map = {code: tid for tid, code in cursor.fetchall()}
    
    models_df = df[["manufacturer", "model_name", "vehicle_category"]].drop_duplicates()
    for _, row in models_df.iterrows():
        mid = mfg_map[row["manufacturer"]]
        cursor.execute("INSERT INTO models (manufacturer_id, model_name, vehicle_category) VALUES (?, ?, ?)",
                       (mid, row["model_name"], row["vehicle_category"]))
                       
    cursor.execute("SELECT model_id, manufacturer_id, model_name FROM models")
    model_map = {(mid, name): mod_id for mod_id, mid, name in cursor.fetchall()}
    
    # 3. Populate Main Records
    record_tuples = []
    for _, row in df.iterrows():
        mid = mfg_map[row["manufacturer"]]
        mod_id = model_map[(mid, row["model_name"])]
        tid = tech_map[row["battery_technology"]]
        
        record_tuples.append((
            int(row["record_id"]),
            int(row["year"]),
            mid,
            mod_id,
            tid,
            row["manufacturing_country"],
            row["primary_sales_region"],
            float(row["battery_capacity_kwh"]),
            int(row["driving_range_km"]),
            int(row["driving_range_miles"]),
            float(row["energy_consumption_kwh_per_100km"]),
            float(row["efficiency_km_per_kwh"]),
            int(row["max_charging_power_kw"]),
            int(row["fast_charge_time_min"]),
            int(row["price_usd"]),
            float(row["cost_per_km_range_usd"]),
            int(row["annual_sales_units"]),
            float(row["total_revenue_usd"]),
            float(row["customer_rating"]),
            int(row["reviews_count"]),
            float(row["co2_saved_per_vehicle_annual_mt"]),
            float(row["total_co2_abated_thousand_mt"]),
            int(row["battery_cycle_life_cycles"]),
            int(row["battery_carbon_footprint_kg"]),
            str(row["price_tier"]),
            str(row["range_tier"]),
            float(row["market_share_percentage"]),
            float(row["category_market_share_percentage"])
        ))
        
    cursor.executemany("""
    INSERT INTO ev_market_records VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """, record_tuples)
    
    print(f"[+] Inserted {len(record_tuples)} records into ev_market_records.")
    
    # 4. Create Analytical Views for Scenarios and Tableau
    views_sql = """
    -- Denormalized Master View for Tableau and Web BI
    CREATE VIEW vw_ev_master_analytics AS
    SELECT 
        r.record_id,
        r.year,
        m.manufacturer_name AS manufacturer,
        m.country_of_origin AS manufacturer_country,
        mod.model_name,
        mod.vehicle_category,
        b.tech_code AS battery_technology,
        b.full_name AS battery_tech_full_name,
        b.thermal_stability,
        r.manufacturing_country,
        r.primary_sales_region,
        r.battery_capacity_kwh,
        r.driving_range_km,
        r.driving_range_miles,
        r.energy_consumption_kwh_per_100km,
        r.efficiency_km_per_kwh,
        r.max_charging_power_kw,
        r.fast_charge_time_min,
        r.price_usd,
        r.cost_per_km_range_usd,
        r.annual_sales_units,
        r.total_revenue_usd,
        r.customer_rating,
        r.reviews_count,
        r.co2_saved_per_vehicle_annual_mt,
        r.total_co2_abated_thousand_mt,
        r.battery_cycle_life_cycles,
        r.battery_carbon_footprint_kg,
        r.price_tier,
        r.range_tier,
        r.market_share_percentage,
        r.category_market_share_percentage
    FROM ev_market_records r
    JOIN manufacturers m ON r.manufacturer_id = m.manufacturer_id
    JOIN models mod ON r.model_id = mod.model_id
    JOIN battery_technologies b ON r.battery_tech_id = b.battery_tech_id;

    -- Scenario 1 View: Emily Johnson (Market Strategy & Category Trends)
    CREATE VIEW vw_executive_sales_summary AS
    SELECT 
        year,
        vehicle_category,
        COUNT(record_id) AS total_model_trims,
        SUM(annual_sales_units) AS total_units_sold,
        ROUND(SUM(total_revenue_usd) / 1000000.0, 2) AS total_revenue_million_usd,
        ROUND(AVG(driving_range_km), 1) AS avg_driving_range_km,
        ROUND(AVG(price_usd), 2) AS avg_price_usd,
        ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
        ROUND(AVG(efficiency_km_per_kwh), 2) AS avg_efficiency_km_per_kwh
    FROM vw_ev_master_analytics
    GROUP BY year, vehicle_category;

    -- Scenario 2 View: David Chen (Competitive Intelligence & Regional Manufacturing)
    CREATE VIEW vw_manufacturer_competitive_intel AS
    SELECT 
        year,
        manufacturer,
        manufacturing_country,
        COUNT(DISTINCT model_name) AS models_offered,
        SUM(annual_sales_units) AS total_units_sold,
        ROUND(SUM(total_revenue_usd) / 1000000.0, 2) AS total_revenue_million_usd,
        ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
        ROUND(AVG(cost_per_km_range_usd), 2) AS avg_cost_per_km_range
    FROM vw_ev_master_analytics
    GROUP BY year, manufacturer, manufacturing_country;

    -- Scenario 3 View: Dr. Sarah Williams (Battery Innovations & Decarbonization)
    CREATE VIEW vw_battery_innovation_sustainability AS
    SELECT 
        year,
        battery_technology,
        COUNT(record_id) AS deployment_count,
        ROUND(AVG(battery_capacity_kwh), 1) AS avg_battery_capacity_kwh,
        ROUND(AVG(driving_range_km), 1) AS avg_driving_range_km,
        ROUND(AVG(fast_charge_time_min), 1) AS avg_fast_charge_min,
        ROUND(AVG(energy_consumption_kwh_per_100km), 2) AS avg_kwh_per_100km,
        ROUND(AVG(battery_cycle_life_cycles), 0) AS avg_cycle_life,
        ROUND(SUM(total_co2_abated_thousand_mt), 2) AS total_co2_abated_thousand_mt
    FROM vw_ev_master_analytics
    GROUP BY year, battery_technology;
    """
    
    cursor.executescript(views_sql)
    print("[+] Created analytical views (Emily, David, Dr. Sarah, Master).")
    
    conn.commit()
    
    # Save the full schema DDL to sql/schema.sql
    with open(sql_schema_path, "w", encoding="utf-8") as f:
        f.write(schema_sql + "\n" + views_sql)
    print(f"[+] Saved DDL schema to {sql_schema_path}")
    
    # Verify views with test queries
    cursor.execute("SELECT COUNT(*) FROM vw_ev_master_analytics")
    print(f"[+] Verification: Master view row count = {cursor.fetchone()[0]}")
    
    conn.close()

if __name__ == "__main__":
    setup_database()
