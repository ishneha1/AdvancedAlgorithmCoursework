"""
Smart Energy Grid Load Distribution (Nepal) - Functional Approach
Pure functions for energy allocation with detailed comments

Uses functional paradigm with immutable data structures and composition.
Greedy strategy: prioritize renewable sources (Solar > Hydro > Diesel).
"""


def get_sample_demand():
    """Return sample hourly district demand."""
    return {
        "06": {"A": 20, "B": 15, "C": 25},
        "07": {"A": 22, "B": 16, "C": 28},
        "08": {"A": 25, "B": 18, "C": 30},
        "12": {"A": 28, "B": 20, "C": 32},
        "18": {"A": 30, "B": 22, "C": 35},
        "19": {"A": 35, "B": 25, "C": 40},
        "20": {"A": 32, "B": 24, "C": 38},
        "23": {"A": 26, "B": 19, "C": 28},
    }


def get_energy_sources():
    """Return energy sources with specifications.
    Format: (name, capacity_kwh, start_hour, end_hour, cost_per_kwh)
    """
    return [
        ("Solar", 50, 6, 18, 1.0),
        ("Hydro", 40, 0, 24, 1.5),
        ("Diesel", 60, 17, 23, 3.0),
    ]


def is_source_available(source, hour):
    """Pure function: check if source is available at given hour."""
    name, capacity, start_h, end_h, cost = source
    return start_h <= hour < end_h


def get_available_sources_for_hour(all_sources, hour):
    """Pure function: return sources available at given hour, sorted by cost."""
    available = [s for s in all_sources if is_source_available(s, hour)]
    return sorted(available, key=lambda x: x[4])  # Sort by cost


def check_demand_satisfaction(energy_used, total_demand, flexibility_range=(0.9, 1.1)):
    """
    Pure function: check if demand is met within flexibility range.
    Default ±10% flexibility: between 90% and 110%.
    """
    if total_demand == 0:
        return True
    ratio = energy_used / total_demand
    lower, upper = flexibility_range
    return lower <= ratio <= upper


def allocate_energy_by_source(available_sources, district_demands):
    """
    Pure function: allocate energy from available sources to districts.
    Returns: allocation dict with district->source breakdown.
    """
    allocation = {d: {} for d in district_demands.keys()}
    total_hour_demand = sum(district_demands.values())
    
    remaining_need = total_hour_demand
    energy_used = 0
    cost = 0
    
    # Allocate from each source in order (greedy by cost)
    for source_name, capacity, start_h, end_h, cost_per_kwh in available_sources:
        if remaining_need <= 0.01:
            break
        
        source_used = 0
        # Proportionally allocate to each district
        for district, demand in district_demands.items():
            if remaining_need <= 0.01:
                break
            proportion = demand / total_hour_demand if total_hour_demand > 0 else 0
            to_allocate = min(proportion * capacity, demand - allocation[district].get('total', 0))
            
            if source_name not in allocation[district]:
                allocation[district][source_name] = 0
            allocation[district][source_name] += to_allocate
            source_used += to_allocate
        
        remaining_need -= source_used
        energy_used += source_used
        cost += source_used * cost_per_kwh
    
    return allocation, energy_used, cost


def calculate_hour_metrics(allocation, total_demand, cost, hour):
    """
    Pure function: compute metrics for an hour.
    Returns dict with all hour statistics.
    """
    energy_used = sum(
        sum(sources.values()) for sources in allocation.values()
    )
    demand_met_pct = (energy_used / total_demand * 100) if total_demand > 0 else 0
    is_satisfied = check_demand_satisfaction(energy_used, total_demand)
    
    return {
        "hour": hour,
        "allocation": allocation,
        "energy_used": energy_used,
        "total_demand": total_demand,
        "demand_met_pct": demand_met_pct,
        "is_satisfied": is_satisfied,
        "cost_rs": cost
    }


def process_all_hours(demand_dict, sources):
    """
    Main orchestration function: process all hours and collect results.
    Uses pure functions above.
    """
    results = {
        "hourly": [],
        "summary": {
            "total_cost": 0,
            "total_energy": 0,
            "renewable_energy": 0,
            "diesel_log": []
        }
    }
    
    for hour_str in sorted(demand_dict.keys()):
        hour = int(hour_str)
        district_demand = demand_dict[hour_str]
        total_demand = sum(district_demand.values())
        
        # Get available sources
        available = get_available_sources_for_hour(sources, hour)
        
        # Allocate energy
        allocation, energy_used, hour_cost = allocate_energy_by_source(
            available, district_demand
        )
        
        # Calculate metrics
        metrics = calculate_hour_metrics(allocation, total_demand, hour_cost, hour)
        
        # Track renewable vs non-renewable
        for dist_alloc in allocation.values():
            for source_name, amount in dist_alloc.items():
                if source_name in ["Solar", "Hydro"]:
                    results["summary"]["renewable_energy"] += amount
                elif source_name == "Diesel":
                    results["summary"]["diesel_log"].append({
                        "hour": hour,
                        "amount": amount,
                        "reason": "Backup power source"
                    })
        
        results["hourly"].append(metrics)
        results["summary"]["total_cost"] += hour_cost
        results["summary"]["total_energy"] += energy_used
    
    return results


def format_output_table(results):
    """Format and print detailed allocation table."""
    print("\n" + "="*110)
    print("ENERGY GRID ALLOCATION - FUNCTIONAL APPROACH")
    print("="*110)
    print(f"{'Hour':<6} {'District':<10} {'Solar':<10} {'Hydro':<10} {'Diesel':<10} {'Total':<10} {'Demand':<10} {'% Met':<8} {'Status':<10}")
    print("-"*110)
    
    for hour_data in results["hourly"]:
        hour = hour_data["hour"]
        allocation = hour_data["allocation"]
        satisfied = "✓ OK" if hour_data["is_satisfied"] else "✗ FAIL"
        
        for i, (district, sources) in enumerate(allocation.items()):
            solar = sources.get("Solar", 0)
            hydro = sources.get("Hydro", 0)
            diesel = sources.get("Diesel", 0)
            total_alloc = sum(sources.values())
            
            if i == 0:
                print(f"{hour:<6} {district:<10} {solar:<10.2f} {hydro:<10.2f} {diesel:<10.2f} {total_alloc:<10.2f} {hour_data['total_demand']:<10.1f} {hour_data['demand_met_pct']:<8.1f} {satisfied:<10}")
            else:
                print(f"{'':6} {district:<10} {solar:<10.2f} {hydro:<10.2f} {diesel:<10.2f} {total_alloc:<10.2f}")
    
    print("="*110)


def print_summary(results):
    """Print cost and performance summary."""
    summary = results["summary"]
    total_energy = summary["total_energy"]
    renewable = summary["renewable_energy"]
    
    print("\nSUMMARY REPORT")
    print("-"*50)
    print(f"Total Cost: Rs. {summary['total_cost']:.2f}")
    print(f"Total Energy: {total_energy:.2f} kWh")
    print(f"Renewable %: {(renewable/total_energy*100):.1f}%")
    print(f"Diesel Uses: {len(summary['diesel_log'])} times")
    
    if summary["diesel_log"]:
        print("\nDiesel Log:")
        for log in summary["diesel_log"]:
            print(f"  Hour {log['hour']}: {log['amount']:.2f} kWh")


if __name__ == "__main__":
    demand = get_sample_demand()
    sources = get_energy_sources()
    results = process_all_hours(demand, sources)
    format_output_table(results)
    print_summary(results)
