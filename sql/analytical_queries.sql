-- ====================================================================
-- ELECTRIC VEHICLE MARKET PERFORMANCE & INSIGHTS
-- Comprehensive Analytical SQL Queries
-- Designed for: Emily Johnson, David Chen, Dr. Sarah Williams
-- ====================================================================

-- --------------------------------------------------------------------
-- SECTION 1: SCENARIO 1 - EMILY JOHNSON (EV MARKET STRATEGY DIRECTOR)
-- --------------------------------------------------------------------

-- 1.1 Category Contribution to Annual Sales Volume & Revenue (Latest Year: 2025)
SELECT 
    vehicle_category,
    SUM(annual_sales_units) AS total_sales_units,
    ROUND(SUM(total_revenue_usd) / 1e9, 2) AS total_revenue_billion_usd,
    ROUND(AVG(driving_range_km), 1) AS avg_driving_range_km,
    ROUND(AVG(customer_rating), 2) AS avg_customer_satisfaction,
    ROUND((SUM(annual_sales_units) * 100.0) / (SELECT SUM(annual_sales_units) FROM vw_ev_master_analytics WHERE year = 2025), 2) AS category_market_share_pct
FROM vw_ev_master_analytics
WHERE year = 2025
GROUP BY vehicle_category
ORDER BY total_sales_units DESC;

-- 1.2 Top 10 Best-Selling EV Models in 2025
SELECT 
    manufacturer,
    model_name,
    vehicle_category,
    battery_technology,
    driving_range_km,
    price_usd,
    annual_sales_units,
    customer_rating
FROM vw_ev_master_analytics
WHERE year = 2025
ORDER BY annual_sales_units DESC
LIMIT 10;

-- 1.3 High-Growth Segment Analysis: Year-over-Year (YoY) Sales Growth by Category
WITH CategoryYearlySales AS (
    SELECT 
        year,
        vehicle_category,
        SUM(annual_sales_units) AS yearly_sales
    FROM vw_ev_master_analytics
    GROUP BY year, vehicle_category
)
SELECT 
    c1.year,
    c1.vehicle_category,
    c1.yearly_sales AS current_year_sales,
    c2.yearly_sales AS previous_year_sales,
    ROUND(((c1.yearly_sales - c2.yearly_sales) * 100.0) / c2.yearly_sales, 2) AS yoy_growth_pct
FROM CategoryYearlySales c1
LEFT JOIN CategoryYearlySales c2 
    ON c1.vehicle_category = c2.vehicle_category 
    AND c1.year = c2.year + 1
WHERE c1.year >= 2021
ORDER BY c1.year DESC, yoy_growth_pct DESC;

-- 1.4 Customer Satisfaction & Value Analysis Across Price Tiers
SELECT 
    price_tier,
    COUNT(*) AS total_models_analyzed,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
    ROUND(AVG(cost_per_km_range_usd), 2) AS avg_cost_per_km_range,
    ROUND(AVG(driving_range_km), 0) AS avg_range_km
FROM vw_ev_master_analytics
GROUP BY price_tier
ORDER BY avg_customer_rating DESC;


-- --------------------------------------------------------------------
-- SECTION 2: SCENARIO 2 - DAVID CHEN (AUTOMOTIVE BI MANAGER)
-- --------------------------------------------------------------------

-- 2.1 Manufacturer Global Market Share & Sales Ranking (2025)
SELECT 
    manufacturer,
    manufacturer_country,
    COUNT(DISTINCT model_name) AS distinct_models_in_portfolio,
    SUM(annual_sales_units) AS total_sales_units,
    ROUND(SUM(total_revenue_usd) / 1e9, 2) AS total_revenue_billion_usd,
    ROUND((SUM(annual_sales_units) * 100.0) / (SELECT SUM(annual_sales_units) FROM vw_ev_master_analytics WHERE year = 2025), 2) AS global_market_share_pct,
    ROUND(AVG(customer_rating), 2) AS brand_customer_rating
FROM vw_ev_master_analytics
WHERE year = 2025
GROUP BY manufacturer, manufacturer_country
ORDER BY total_sales_units DESC;

-- 2.2 Geographical Manufacturing Hubs vs Primary Sales Regions
SELECT 
    manufacturing_country,
    primary_sales_region,
    COUNT(*) AS factory_allocations,
    SUM(annual_sales_units) AS units_produced_for_market,
    ROUND(SUM(total_revenue_usd) / 1e9, 2) AS export_value_billion_usd
FROM vw_ev_master_analytics
WHERE year = 2025
GROUP BY manufacturing_country, primary_sales_region
ORDER BY units_produced_for_market DESC;

-- 2.3 Manufacturer Battery Chemistry Strategy Breakdown (Percentage Deployment)
SELECT 
    manufacturer,
    battery_technology,
    COUNT(*) AS trims_deployed,
    SUM(annual_sales_units) AS total_sales_with_tech,
    ROUND(AVG(driving_range_km), 0) AS avg_delivered_range_km
FROM vw_ev_master_analytics
WHERE year = 2025 AND manufacturer IN ('Tesla', 'BYD', 'Volkswagen', 'Hyundai', 'BMW', 'Tata Motors')
GROUP BY manufacturer, battery_technology
ORDER BY manufacturer, total_sales_with_tech DESC;

-- 2.4 Competitive Pricing Efficiency: Cost per KM of Driving Range by Manufacturer
SELECT 
    manufacturer,
    ROUND(AVG(cost_per_km_range_usd), 2) AS avg_cost_per_km,
    ROUND(AVG(price_usd), 0) AS avg_selling_price_usd,
    ROUND(AVG(driving_range_km), 0) AS avg_driving_range_km,
    ROUND(AVG(customer_rating), 2) AS avg_rating
FROM vw_ev_master_analytics
WHERE year = 2025
GROUP BY manufacturer
ORDER BY avg_cost_per_km ASC;


-- --------------------------------------------------------------------
-- SECTION 3: SCENARIO 3 - DR. SARAH WILLIAMS (SUSTAINABLE MOBILITY ANALYST)
-- --------------------------------------------------------------------

-- 3.1 Battery Innovation Evolution: Range, Efficiency & Charging Speed (2020 - 2025)
SELECT 
    year,
    battery_technology,
    COUNT(*) AS models_tested,
    ROUND(AVG(battery_capacity_kwh), 1) AS avg_capacity_kwh,
    ROUND(AVG(driving_range_km), 1) AS avg_driving_range_km,
    ROUND(AVG(efficiency_km_per_kwh), 2) AS avg_efficiency_km_per_kwh,
    ROUND(AVG(fast_charge_time_min), 1) AS avg_fast_charge_min,
    ROUND(AVG(battery_cycle_life_cycles), 0) AS avg_lifespan_cycles
FROM vw_ev_master_analytics
GROUP BY year, battery_technology
ORDER BY battery_technology, year ASC;

-- 3.2 Decarbonization Assessment: Annual CO2 Abatement by Vehicle Category
SELECT 
    vehicle_category,
    SUM(annual_sales_units) AS total_fleet_deployed,
    ROUND(AVG(co2_saved_per_vehicle_annual_mt), 2) AS avg_co2_offset_per_vehicle_mt,
    ROUND(SUM(total_co2_abated_thousand_mt), 1) AS cumulative_co2_abated_k_mt,
    ROUND(AVG(energy_consumption_kwh_per_100km), 1) AS avg_grid_draw_kwh_per_100km
FROM vw_ev_master_analytics
GROUP BY vehicle_category
ORDER BY cumulative_co2_abated_k_mt DESC;

-- 3.3 Battery Lifecycle & Carbon Footprint vs Durability Trade-off
SELECT 
    battery_technology,
    thermal_stability,
    ROUND(AVG(battery_carbon_footprint_kg), 0) AS avg_embedded_co2_kg,
    ROUND(AVG(battery_cycle_life_cycles), 0) AS avg_cycle_life_cycles,
    ROUND(AVG(driving_range_km), 0) AS avg_range_km,
    ROUND(AVG(battery_carbon_footprint_kg) / AVG(battery_cycle_life_cycles), 2) AS co2_kg_per_lifecycle_cycle
FROM vw_ev_master_analytics
GROUP BY battery_technology, thermal_stability
ORDER BY co2_kg_per_lifecycle_cycle ASC;
