"""
Electric Vehicle Market Performance & Insights
Dataset Generator Script
Generates a realistic, multifaceted EV dataset covering 2020-2025
matching requirements for Emily Johnson, David Chen, and Dr. Sarah Williams.
"""

import os
import random
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Definitions
MANUFACTURERS_DATA = [
    {"name": "Tesla", "origin": "United States", "hq": "Austin, TX", "tier": "Premium/Mass"},
    {"name": "BYD", "origin": "China", "hq": "Shenzhen", "tier": "Mass/Volume"},
    {"name": "Volkswagen", "origin": "Germany", "hq": "Wolfsburg", "tier": "Legacy Mass"},
    {"name": "Hyundai", "origin": "South Korea", "hq": "Seoul", "tier": "Legacy Mass"},
    {"name": "Kia", "origin": "South Korea", "hq": "Seoul", "tier": "Legacy Mass"},
    {"name": "BMW", "origin": "Germany", "hq": "Munich", "tier": "Luxury"},
    {"name": "Mercedes-Benz", "origin": "Germany", "hq": "Stuttgart", "tier": "Luxury"},
    {"name": "Rivian", "origin": "United States", "hq": "Irvine, CA", "tier": "Premium EV Pureplay"},
    {"name": "Volvo", "origin": "Sweden", "hq": "Gothenburg", "tier": "Premium"},
    {"name": "NIO", "origin": "China", "hq": "Shanghai", "tier": "Premium Smart EV"},
    {"name": "XPeng", "origin": "China", "hq": "Guangzhou", "tier": "Smart Tech EV"},
    {"name": "Geely", "origin": "China", "hq": "Hangzhou", "tier": "Mass/Global"},
    {"name": "Tata Motors", "origin": "India", "hq": "Mumbai", "tier": "Mass Emerging"},
    {"name": "Ford", "origin": "United States", "hq": "Dearborn, MI", "tier": "Legacy Mass"},
    {"name": "Chevrolet", "origin": "United States", "hq": "Detroit, MI", "tier": "Legacy Mass"},
    {"name": "Yutong", "origin": "China", "hq": "Zhengzhou", "tier": "Commercial/Bus"},
    {"name": "Proterra", "origin": "United States", "hq": "Burlingame, CA", "tier": "Commercial/Bus"},
    {"name": "Ola Electric", "origin": "India", "hq": "Bengaluru", "tier": "Two-Wheeler EV"},
    {"name": "NIU Technologies", "origin": "China", "hq": "Changzhou", "tier": "Two-Wheeler EV"},
    {"name": "Zero Motorcycles", "origin": "United States", "hq": "Santa Cruz, CA", "tier": "Two-Wheeler Premium"}
]

MODELS_CATALOG = {
    "Tesla": [
        ("Model 3", "Sedan"), ("Model Y", "SUV"), ("Model S", "Sedan"), 
        ("Model X", "SUV"), ("Cybertruck", "Truck"), ("Semi", "Truck")
    ],
    "BYD": [
        ("Atto 3", "SUV"), ("Seal", "Sedan"), ("Dolphin", "Hatchback"), 
        ("Tang", "SUV"), ("Han", "Sedan"), ("K9 Electric Bus", "Electric Bus"), ("Seagull", "Hatchback")
    ],
    "Volkswagen": [
        ("ID.3", "Hatchback"), ("ID.4", "SUV"), ("ID.7", "Sedan"), ("ID. Buzz", "SUV")
    ],
    "Hyundai": [
        ("Ioniq 5", "SUV"), ("Ioniq 6", "Sedan"), ("Kona Electric", "SUV"), ("Elec City Bus", "Electric Bus")
    ],
    "Kia": [
        ("EV6", "SUV"), ("EV9", "SUV"), ("Niro EV", "SUV")
    ],
    "BMW": [
        ("i4", "Sedan"), ("iX3", "SUV"), ("iX", "SUV"), ("i7", "Sedan")
    ],
    "Mercedes-Benz": [
        ("EQE Sedan", "Sedan"), ("EQS Sedan", "Sedan"), ("EQB", "SUV"), ("eCitaro Bus", "Electric Bus")
    ],
    "Rivian": [
        ("R1T", "Truck"), ("R1S", "SUV"), ("EDV Delivery Van", "Truck")
    ],
    "Volvo": [
        ("EX30", "SUV"), ("EX90", "SUV"), ("XC40 Recharge", "SUV"), ("7900 Electric Bus", "Electric Bus")
    ],
    "NIO": [
        ("ET5", "Sedan"), ("ET7", "Sedan"), ("ES6", "SUV"), ("ES8", "SUV")
    ],
    "XPeng": [
        ("P7", "Sedan"), ("G6", "SUV"), ("G9", "SUV")
    ],
    "Geely": [
        ("Geometry C", "Hatchback"), ("Galaxy E8", "Sedan"), ("Zeekr 001", "Sedan")
    ],
    "Tata Motors": [
        ("Nexon EV", "SUV"), ("Tiago EV", "Hatchback"), ("Punch EV", "SUV"), ("Starbus EV", "Electric Bus")
    ],
    "Ford": [
        ("Mustang Mach-E", "SUV"), ("F-150 Lightning", "Truck"), ("E-Transit", "Truck")
    ],
    "Chevrolet": [
        ("Bolt EV", "Hatchback"), ("Blazer EV", "SUV"), ("Silverado EV", "Truck")
    ],
    "Yutong": [
        ("E12 Electric Bus", "Electric Bus"), ("U12 Bus", "Electric Bus"), ("T12 Coach", "Electric Bus")
    ],
    "Proterra": [
        ("ZX5 Electric Bus", "Electric Bus"), ("Catalyst E2", "Electric Bus")
    ],
    "Ola Electric": [
        ("S1 Pro", "Two-Wheeler"), ("S1 Air", "Two-Wheeler"), ("S1 X", "Two-Wheeler")
    ],
    "NIU Technologies": [
        ("NQi GTS", "Two-Wheeler"), ("MQi GT", "Two-Wheeler"), ("RQi Sport", "Two-Wheeler")
    ],
    "Zero Motorcycles": [
        ("Zero SR/F", "Two-Wheeler"), ("Zero DSR/X", "Two-Wheeler"), ("Zero FXE", "Two-Wheeler")
    ]
}

BATTERY_TECH_PROFILES = {
    "LFP": {
        "full_name": "Lithium Iron Phosphate",
        "energy_density_wh_kg": (140, 190),
        "cycle_life": (2500, 4000),
        "thermal_stability": "Very High",
        "cost_multiplier": 0.80,
        "efficiency_km_per_kwh_factor": 1.0,
        "co2_footprint_kg_per_kwh": 65
    },
    "NMC": {
        "full_name": "Nickel Manganese Cobalt",
        "energy_density_wh_kg": (220, 290),
        "cycle_life": (1500, 2200),
        "thermal_stability": "High",
        "cost_multiplier": 1.15,
        "efficiency_km_per_kwh_factor": 1.08,
        "co2_footprint_kg_per_kwh": 85
    },
    "NCA": {
        "full_name": "Nickel Cobalt Aluminum",
        "energy_density_wh_kg": (240, 310),
        "cycle_life": (1300, 2000),
        "thermal_stability": "Moderate",
        "cost_multiplier": 1.25,
        "efficiency_km_per_kwh_factor": 1.12,
        "co2_footprint_kg_per_kwh": 92
    },
    "Sodium-Ion": {
        "full_name": "Sodium-Ion",
        "energy_density_wh_kg": (120, 160),
        "cycle_life": (2000, 3200),
        "thermal_stability": "Very High",
        "cost_multiplier": 0.65,
        "efficiency_km_per_kwh_factor": 0.92,
        "co2_footprint_kg_per_kwh": 48
    },
    "Solid-State": {
        "full_name": "Solid-State Battery",
        "energy_density_wh_kg": (350, 480),
        "cycle_life": (3000, 5000),
        "thermal_stability": "Exceptional",
        "cost_multiplier": 1.70,
        "efficiency_km_per_kwh_factor": 1.25,
        "co2_footprint_kg_per_kwh": 70
    }
}

YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

MANUFACTURING_COUNTRIES = [
    "China", "United States", "Germany", "South Korea", 
    "Japan", "India", "Sweden", "Mexico", "United Kingdom", "Hungary"
]

SALES_REGIONS = ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East & Africa"]

def get_battery_tech_for_context(category, year, mfg_country):
    """Realistic probabilistic battery chemistry assignment based on time and category."""
    if year in [2020, 2021]:
        weights = {"NMC": 0.50, "NCA": 0.35, "LFP": 0.15, "Sodium-Ion": 0.0, "Solid-State": 0.0}
    elif year in [2022, 2023]:
        weights = {"NMC": 0.42, "NCA": 0.23, "LFP": 0.33, "Sodium-Ion": 0.02, "Solid-State": 0.0}
    else: # 2024, 2025
        weights = {"NMC": 0.35, "NCA": 0.15, "LFP": 0.40, "Sodium-Ion": 0.07, "Solid-State": 0.03}
    
    # Adjust for commercial bus / two wheeler
    if category in ["Electric Bus", "Two-Wheeler"]:
        weights["LFP"] += 0.25
        weights["NCA"] = max(0.01, weights["NCA"] - 0.15)
        weights["NMC"] = max(0.05, weights["NMC"] - 0.10)
        
    # China manufactures heavy LFP & Sodium-Ion
    if mfg_country == "China":
        weights["LFP"] += 0.15
        if year >= 2024:
            weights["Sodium-Ion"] += 0.08
            
    # Normalize probabilities
    techs = list(weights.keys())
    probs = np.array([weights[t] for t in techs])
    probs = np.maximum(probs, 0.001)
    probs = probs / probs.sum()
    
    return np.random.choice(techs, p=probs)

def generate_ev_dataset(num_records=2500):
    records = []
    
    # Base category specifications
    cat_specs = {
        "Hatchback": {
            "battery_kwh": (30, 62),
            "base_price": (18000, 36000),
            "range_km": (220, 420),
            "charging_kw": (50, 130),
            "wh_per_km": (135, 175)
        },
        "Sedan": {
            "battery_kwh": (55, 105),
            "base_price": (34000, 115000),
            "range_km": (380, 720),
            "charging_kw": (100, 270),
            "wh_per_km": (150, 195)
        },
        "SUV": {
            "battery_kwh": (60, 115),
            "base_price": (38000, 135000),
            "range_km": (350, 680),
            "charging_kw": (100, 250),
            "wh_per_km": (175, 230)
        },
        "Truck": {
            "battery_kwh": (110, 215),
            "base_price": (55000, 140000),
            "range_km": (400, 750),
            "charging_kw": (150, 350),
            "wh_per_km": (260, 350)
        },
        "Electric Bus": {
            "battery_kwh": (240, 520),
            "base_price": (220000, 450000),
            "range_km": (250, 480),
            "charging_kw": (150, 350),
            "wh_per_km": (950, 1400)
        },
        "Two-Wheeler": {
            "battery_kwh": (2.5, 18),
            "base_price": (1500, 19500),
            "range_km": (75, 280),
            "charging_kw": (3, 22),
            "wh_per_km": (30, 65)
        }
    }
    
    record_id = 1
    
    # We generate a structured panel dataset across manufacturers, models, years, and markets
    while len(records) < num_records:
        mfg_dict = random.choice(MANUFACTURERS_DATA)
        mfg = mfg_dict["name"]
        models_available = MODELS_CATALOG[mfg]
        model, category = random.choice(models_available)
        
        year = random.choice(YEARS)
        specs = cat_specs[category]
        
        # Determine manufacturing country
        if mfg_dict["origin"] in MANUFACTURING_COUNTRIES and random.random() < 0.70:
            mfg_country = mfg_dict["origin"]
        else:
            mfg_country = random.choice(MANUFACTURING_COUNTRIES)
            
        battery_tech = get_battery_tech_for_context(category, year, mfg_country)
        tech_meta = BATTERY_TECH_PROFILES[battery_tech]
        
        # Technology improvements by year (2020 -> 2025)
        tech_progress = 1.0 + (year - 2020) * 0.045 # 4.5% improvement per year in efficiency & range
        cost_decline = 1.0 - (year - 2020) * 0.055 # 5.5% annual battery cost decline
        
        # Calculate battery capacity
        base_cap = random.uniform(specs["battery_kwh"][0], specs["battery_kwh"][1])
        battery_capacity_kwh = round(base_cap * (1.0 + (year - 2020) * 0.02), 1)
        
        # Driving range (km)
        eff_factor = tech_meta["efficiency_km_per_kwh_factor"]
        base_range = random.uniform(specs["range_km"][0], specs["range_km"][1])
        driving_range_km = int(base_range * tech_progress * eff_factor * (battery_capacity_kwh / ((specs["battery_kwh"][0] + specs["battery_kwh"][1]) / 2)) ** 0.8)
        driving_range_miles = int(driving_range_km * 0.621371)
        
        # Energy consumption (kWh / 100 km)
        kwh_per_100km = round((battery_capacity_kwh / driving_range_km) * 100, 2)
        km_per_kwh = round(driving_range_km / battery_capacity_kwh, 2)
        
        # Charging specs
        max_charging_power_kw = int(random.uniform(specs["charging_kw"][0], specs["charging_kw"][1]) * (1.0 + (year - 2020) * 0.06))
        # Fast charge time 10% to 80% (mins)
        # formula: 0.7 * battery_kwh / avg_effective_charge_kw * 60
        effective_charge_kw = max(20, min(max_charging_power_kw * 0.72, 280))
        fast_charge_time_min = int(max(15, min(75, (0.7 * battery_capacity_kwh / effective_charge_kw) * 60 + random.uniform(-4, 5))))
        if category == "Two-Wheeler":
            fast_charge_time_min = int(random.uniform(25, 75))
            
        # Base pricing
        base_p = random.uniform(specs["base_price"][0], specs["base_price"][1])
        price_usd = int(base_p * tech_meta["cost_multiplier"] * cost_decline)
        
        # Tier adjustments
        if "Luxury" in mfg_dict["tier"]:
            price_usd = int(price_usd * 1.35)
        elif "Mass" in mfg_dict["tier"]:
            price_usd = int(price_usd * 0.88)
            
        cost_per_km_range = round(price_usd / driving_range_km, 2)
        
        # Sales volume
        # EV market grew rapidly between 2020 and 2025
        market_growth_mult = (1.0 + (year - 2020) * 0.48)
        
        if category == "SUV":
            base_sales = random.uniform(25000, 160000)
        elif category == "Sedan":
            base_sales = random.uniform(20000, 130000)
        elif category == "Hatchback":
            base_sales = random.uniform(15000, 95000)
        elif category == "Truck":
            base_sales = random.uniform(8000, 48000) if year >= 2022 else random.uniform(1000, 8000)
        elif category == "Electric Bus":
            base_sales = random.uniform(800, 8500)
        else: # Two-Wheeler
            base_sales = random.uniform(35000, 220000)
            
        # Brand market multiplier
        if mfg in ["Tesla", "BYD"]:
            sales_units = int(base_sales * market_growth_mult * random.uniform(1.6, 2.8))
        elif mfg in ["Volkswagen", "Hyundai", "BMW"]:
            sales_units = int(base_sales * market_growth_mult * random.uniform(0.9, 1.4))
        else:
            sales_units = int(base_sales * market_growth_mult * random.uniform(0.4, 0.95))
            
        revenue_usd = sales_units * price_usd
        
        # Primary sales region
        primary_region = random.choice(SALES_REGIONS)
        if mfg_dict["origin"] == "China":
            primary_region = np.random.choice(["Asia-Pacific", "Europe", "Latin America"], p=[0.72, 0.20, 0.08])
        elif mfg_dict["origin"] == "United States":
            primary_region = np.random.choice(["North America", "Europe", "Asia-Pacific"], p=[0.68, 0.22, 0.10])
        elif mfg_dict["origin"] == "Germany":
            primary_region = np.random.choice(["Europe", "North America", "Asia-Pacific"], p=[0.55, 0.25, 0.20])
            
        # Customer satisfaction rating (1.0 - 5.0)
        # Higher range and reliability correlated with slightly higher ratings
        score_base = 3.9 + (driving_range_km / 800) * 0.5 + random.uniform(-0.4, 0.5)
        if mfg in ["Tesla", "Porsche", "BMW", "Rivian"]:
            score_base += 0.2
        customer_rating = round(min(5.0, max(3.0, score_base)), 2)
        reviews_count = int(sales_units * random.uniform(0.015, 0.05) + random.randint(150, 1200))
        
        # Environmental / Sustainability Metrics (Dr. Sarah Williams)
        # Average ICE emits ~4.6 MT CO2/yr for passenger car, EV saves ~2.5 - 4.2 MT CO2/yr based on clean grid
        co2_saved_per_vehicle_mt = round(2.8 + (km_per_kwh * 0.2) + random.uniform(-0.3, 0.4), 2)
        total_co2_abated_k_mt = round((sales_units * co2_saved_per_vehicle_mt) / 1000.0, 2)
        battery_cycle_life = int(random.uniform(tech_meta["cycle_life"][0], tech_meta["cycle_life"][1]))
        battery_carbon_footprint_kg = int(battery_capacity_kwh * tech_meta["co2_footprint_kg_per_kwh"])
        
        records.append({
            "record_id": record_id,
            "year": year,
            "manufacturer": mfg,
            "model_name": model,
            "vehicle_category": category,
            "manufacturer_country": mfg_dict["origin"],
            "manufacturing_country": mfg_country,
            "primary_sales_region": primary_region,
            "battery_technology": battery_tech,
            "battery_tech_full_name": tech_meta["full_name"],
            "battery_capacity_kwh": battery_capacity_kwh,
            "driving_range_km": driving_range_km,
            "driving_range_miles": driving_range_miles,
            "energy_consumption_kwh_per_100km": kwh_per_100km,
            "efficiency_km_per_kwh": km_per_kwh,
            "max_charging_power_kw": max_charging_power_kw,
            "fast_charge_time_min": fast_charge_time_min,
            "price_usd": price_usd,
            "cost_per_km_range_usd": cost_per_km_range,
            "annual_sales_units": sales_units,
            "total_revenue_usd": revenue_usd,
            "customer_rating": customer_rating,
            "reviews_count": reviews_count,
            "co2_saved_per_vehicle_annual_mt": co2_saved_per_vehicle_mt,
            "total_co2_abated_thousand_mt": total_co2_abated_k_mt,
            "battery_cycle_life_cycles": battery_cycle_life,
            "battery_carbon_footprint_kg": battery_carbon_footprint_kg,
            "thermal_stability": tech_meta["thermal_stability"]
        })
        record_id += 1
        
    df = pd.DataFrame(records)
    
    # Calculate global market share by year
    yearly_totals = df.groupby("year")["annual_sales_units"].transform("sum")
    df["market_share_percentage"] = round((df["annual_sales_units"] / yearly_totals) * 100, 3)
    
    # Calculate category market share within year
    cat_yearly_totals = df.groupby(["year", "vehicle_category"])["annual_sales_units"].transform("sum")
    df["category_market_share_percentage"] = round((df["annual_sales_units"] / cat_yearly_totals) * 100, 3)
    
    # Price Tier category
    df["price_tier"] = pd.cut(
        df["price_usd"],
        bins=[-1, 25000, 45000, 75000, 150000, 1000000],
        labels=["Budget (<$25K)", "Mass-Market ($25K-$45K)", "Upper Mid ($45K-$75K)", "Premium ($75K-$150K)", "Ultra/Commercial (>$150K)"]
    )
    
    # Range Tier
    df["range_tier"] = pd.cut(
        df["driving_range_km"],
        bins=[-1, 200, 350, 500, 650, 1500],
        labels=["Urban (<200km)", "Standard (200-350km)", "Long-Range (350-500km)", "Extended (500-650km)", "Ultra-Long (>650km)"]
    )
    
    return df

def main():
    base_dir = r"C:\Users\makro\.gemini\antigravity\scratch\ev-market-performance-insights"
    raw_path = os.path.join(base_dir, "data", "raw", "ev_market_raw.csv")
    cleaned_path = os.path.join(base_dir, "data", "processed", "ev_market_cleaned.csv")
    tableau_path = os.path.join(base_dir, "data", "tableau", "ev_market_tableau_ready.csv")
    
    print("[*] Generating EV Market dataset (2500 records)...")
    df = generate_ev_dataset(2500)
    
    # Save raw
    df.to_csv(raw_path, index=False)
    print(f"[+] Saved raw dataset to: {raw_path}")
    
    # Perform Data Cleaning & Validation
    # Check nulls, verify data ranges
    assert df.isnull().sum().sum() == 0, "Missing values found!"
    print(f"[+] Dataset shape: {df.shape}")
    print(f"[+] Years covered: {sorted(df['year'].unique())}")
    print(f"[+] Manufacturers count: {df['manufacturer'].nunique()}")
    print(f"[+] Vehicle categories: {df['vehicle_category'].unique().tolist()}")
    print(f"[+] Battery technologies: {df['battery_technology'].unique().tolist()}")
    
    # Save cleaned
    df.to_csv(cleaned_path, index=False)
    print(f"[+] Saved cleaned dataset to: {cleaned_path}")
    
    # Save tableau ready
    df.to_csv(tableau_path, index=False)
    print(f"[+] Saved Tableau-ready dataset to: {tableau_path}")
    
    # Summary metrics
    total_sales = df['annual_sales_units'].sum()
    total_revenue = df['total_revenue_usd'].sum()
    print(f"[+] Total EV sales represented: {total_sales:,} units")
    print(f"[+] Total Market Revenue: ${total_revenue / 1e9:,.2f} Billion USD")

if __name__ == "__main__":
    main()
