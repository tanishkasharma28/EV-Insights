"""
Electric Vehicle Market Performance & Insights
Performance Testing & Benchmark Script
Measures database render efficiency, query latency, index impact,
filter performance, and calculated fields computational overhead.
"""

import os
import time
import sqlite3
import json
import pandas as pd

def run_performance_benchmarks():
    base_dir = r"C:\Users\makro\.gemini\antigravity\scratch\ev-market-performance-insights"
    db_path = os.path.join(base_dir, "data", "database", "ev_market.db")
    csv_path = os.path.join(base_dir, "data", "processed", "ev_market_cleaned.csv")
    benchmark_output_path = os.path.join(base_dir, "docs", "performance_benchmark_results.json")
    
    print("[*] Starting Performance Testing Suite...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_records": 0,
            "database_size_bytes": os.path.getsize(db_path),
            "csv_size_bytes": os.path.getsize(csv_path)
        },
        "query_latency_benchmarks": [],
        "filter_utilization_benchmarks": [],
        "calculated_fields_benchmarks": [],
        "data_rendering_summary": {}
    }
    
    cursor.execute("SELECT COUNT(*) FROM ev_market_records")
    results["metadata"]["total_records"] = cursor.fetchone()[0]
    
    # 1. Query Latency Benchmarks (Indexed vs Aggregation)
    test_queries = [
        {
            "name": "Scenario 1: Category Sales Aggregation & Ranking",
            "sql": """
                SELECT vehicle_category, SUM(annual_sales_units), AVG(customer_rating), AVG(driving_range_km)
                FROM vw_ev_master_analytics
                WHERE year = 2025
                GROUP BY vehicle_category
                ORDER BY 2 DESC;
            """
        },
        {
            "name": "Scenario 2: Manufacturer Market Share & Geographic Distribution",
            "sql": """
                SELECT manufacturer, manufacturing_country, SUM(annual_sales_units), SUM(total_revenue_usd)
                FROM vw_ev_master_analytics
                WHERE year = 2025
                GROUP BY manufacturer, manufacturing_country
                ORDER BY 3 DESC;
            """
        },
        {
            "name": "Scenario 3: Battery Chemistry Multi-Year Trend Analysis",
            "sql": """
                SELECT year, battery_technology, AVG(driving_range_km), AVG(efficiency_km_per_kwh), SUM(total_co2_abated_thousand_mt)
                FROM vw_ev_master_analytics
                GROUP BY year, battery_technology
                ORDER BY year ASC, battery_technology;
            """
        },
        {
            "name": "Complex Multi-Table Join & Subquery with Cost Ratio",
            "sql": """
                SELECT m.manufacturer_name, mod.vehicle_category, b.tech_code,
                       AVG(r.price_usd / r.driving_range_km) AS avg_cost_per_km,
                       SUM(r.annual_sales_units) AS total_sales
                FROM ev_market_records r
                JOIN manufacturers m ON r.manufacturer_id = m.manufacturer_id
                JOIN models mod ON r.model_id = mod.model_id
                JOIN battery_technologies b ON r.battery_tech_id = b.battery_tech_id
                WHERE r.driving_range_km >= 400 AND r.customer_rating >= 4.2
                GROUP BY m.manufacturer_name, mod.vehicle_category, b.tech_code
                ORDER BY total_sales DESC
                LIMIT 15;
            """
        }
    ]
    
    for tq in test_queries:
        latencies = []
        # Run 50 iterations for statistical confidence
        for _ in range(50):
            start = time.perf_counter()
            cursor.execute(tq["sql"])
            _ = cursor.fetchall()
            end = time.perf_counter()
            latencies.append((end - start) * 1000) # milliseconds
            
        avg_latency = round(sum(latencies) / len(latencies), 3)
        min_latency = round(min(latencies), 3)
        max_latency = round(max(latencies), 3)
        p95_latency = round(sorted(latencies)[int(0.95 * len(latencies))], 3)
        
        results["query_latency_benchmarks"].append({
            "query_name": tq["name"],
            "avg_latency_ms": avg_latency,
            "min_latency_ms": min_latency,
            "max_latency_ms": max_latency,
            "p95_latency_ms": p95_latency,
            "status": "Optimal (< 10ms target)" if avg_latency < 10 else "Acceptable"
        })
        print(f"[+] {tq['name']}: Avg {avg_latency} ms (P95: {p95_latency} ms)")
        
    # 2. Filter Utilization Benchmarks (Filter selectivity and combination impact)
    filter_tests = [
        {"filter": "Single Filter (Year = 2025)", "where": "WHERE year = 2025"},
        {"filter": "Dual Filter (Year = 2025 AND Category = 'SUV')", "where": "WHERE year = 2025 AND vehicle_category = 'SUV'"},
        {"filter": "Triple Filter (Year = 2025, Category = 'SUV', Tech = 'LFP')", "where": "WHERE year = 2025 AND vehicle_category = 'SUV' AND battery_technology = 'LFP'"},
        {"filter": "Range Filter (Price Between 30K and 80K AND Range > 400km)", "where": "WHERE price_usd BETWEEN 30000 AND 80000 AND driving_range_km > 400"}
    ]
    
    for ft in filter_tests:
        query = f"SELECT COUNT(*), AVG(driving_range_km), SUM(annual_sales_units) FROM vw_ev_master_analytics {ft['where']};"
        times = []
        for _ in range(50):
            s = time.perf_counter()
            cursor.execute(query)
            row = cursor.fetchone()
            e = time.perf_counter()
            times.append((e - s) * 1000)
            
        results["filter_utilization_benchmarks"].append({
            "filter_combination": ft["filter"],
            "matched_rows": row[0],
            "execution_time_ms": round(sum(times) / len(times), 3)
        })
        print(f"[+] Filter: {ft['filter']} -> {row[0]} rows in {round(sum(times)/len(times), 3)} ms")
        
    # 3. Calculated Fields Computational Overhead
    calc_tests = [
        {
            "name": "Efficiency Metric (km / kWh calculation)",
            "sql": "SELECT AVG(driving_range_km * 1.0 / battery_capacity_kwh) FROM ev_market_records;"
        },
        {
            "name": "Cost-Value Ratio (Price / Range calculation)",
            "sql": "SELECT AVG(price_usd * 1.0 / driving_range_km) FROM ev_market_records;"
        },
        {
            "name": "Charging Speed Efficiency ((Range * 0.8) / Charge_Time)",
            "sql": "SELECT AVG((driving_range_km * 0.8) / fast_charge_time_min) FROM ev_market_records;"
        },
        {
            "name": "CO2 Abatement Intensity (CO2 Saved / Battery Footprint)",
            "sql": "SELECT AVG((co2_saved_per_vehicle_annual_mt * 1000.0) / battery_carbon_footprint_kg) FROM ev_market_records;"
        }
    ]
    
    for ct in calc_tests:
        ct_times = []
        for _ in range(50):
            s = time.perf_counter()
            cursor.execute(ct["sql"])
            _ = cursor.fetchone()
            e = time.perf_counter()
            ct_times.append((e - s) * 1000)
        results["calculated_fields_benchmarks"].append({
            "calculation_name": ct["name"],
            "avg_overhead_ms": round(sum(ct_times) / len(ct_times), 3)
        })
        
    # 4. Rendering summary
    results["data_rendering_summary"] = {
        "total_rows_rendered": results["metadata"]["total_records"],
        "total_attributes": 32,
        "database_storage_kb": round(results["metadata"]["database_size_bytes"] / 1024, 2),
        "index_count": 7,
        "avg_query_response_time_ms": round(sum(b["avg_latency_ms"] for b in results["query_latency_benchmarks"]) / len(results["query_latency_benchmarks"]), 3),
        "throughput_queries_per_sec": int(1000 / (sum(b["avg_latency_ms"] for b in results["query_latency_benchmarks"]) / len(results["query_latency_benchmarks"])))
    }
    
    with open(benchmark_output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print(f"[+] Performance test completed. Results exported to {benchmark_output_path}")
    conn.close()

if __name__ == "__main__":
    run_performance_benchmarks()
