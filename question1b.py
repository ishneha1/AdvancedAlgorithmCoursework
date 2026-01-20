"""
Traveling Salesman Problem - Simulated Annealing Solution
Procedural Implementation with Comprehensive Documentation

This solution uses Simulated Annealing with 2-opt moves to find a near-optimal
route for 30 cities. It supports both exponential and linear cooling schedules.
"""

import random
import math


def create_city_coordinates(num_cities=30):
    """
    Generate random 2D coordinates for cities.
    
    Args:
        num_cities (int): Number of cities to generate
    
    Returns:
        list: List of [x, y] coordinates for each city
    """
    cities = []
    for i in range(num_cities):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        cities.append([x, y])
    return cities


def calculate_euclidean_distance(city_a, city_b):
    """
    Calculate Euclidean distance between two cities.
    
    Args:
        city_a (list): [x, y] coordinates of city A
        city_b (list): [x, y] coordinates of city B
    
    Returns:
        float: Distance between cities
    """
    dx = city_a[0] - city_b[0]
    dy = city_a[1] - city_b[1]
    return math.sqrt(dx * dx + dy * dy)


def calculate_total_tour_distance(tour, cities):
    """
    Calculate total distance for a complete tour (closed loop).
    
    The tour is closed, meaning we return to the starting city.
    
    Args:
        tour (list): Permutation of city indices representing the route
        cities (list): List of city coordinates
    
    Returns:
        float: Total distance of the tour
    """
    total_distance = 0.0
    
    for i in range(len(tour)):
        # Current city
        current_city_idx = tour[i]
        current_city = cities[current_city_idx]
        
        # Next city (wrap around to start at end)
        next_idx = (i + 1) % len(tour)
        next_city_idx = tour[next_idx]
        next_city = cities[next_city_idx]
        
        # Add distance between consecutive cities
        distance = calculate_euclidean_distance(current_city, next_city)
        total_distance = total_distance + distance
    
    return total_distance


def apply_two_opt_move(tour, i, j):
    """
    Apply 2-opt move: reverse the segment between indices i and j.
    
    The 2-opt move swaps edges to eliminate crossing routes.
    It reverses the segment from position i to position j.
    
    Args:
        tour (list): Current tour permutation
        i (int): Start index of segment to reverse
        j (int): End index of segment to reverse
    
    Returns:
        list: New tour with reversed segment
    """
    # Create new tour by reversing the segment
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour


def acceptance_probability(current_distance, new_distance, temperature):
    """
    Calculate probability of accepting a worse solution.
    
    Using Metropolis criterion:
    - If new solution is better, always accept (P = 1)
    - If worse, accept with probability P = exp(-ΔE/T)
    
    Args:
        current_distance (float): Distance of current solution
        new_distance (float): Distance of new solution
        temperature (float): Current temperature
    
    Returns:
        float: Acceptance probability between 0 and 1
    """
    # If new solution is better, always accept
    if new_distance < current_distance:
        return 1.0
    
    # If worse, accept with probability based on temperature
    energy_diff = new_distance - current_distance
    
    if temperature > 0:
        probability = math.exp(-energy_diff / temperature)
    else:
        probability = 0.0
    
    return probability


def simulated_annealing(cities, cooling_type="exponential"):
    """
    Find near-optimal TSP route using Simulated Annealing.
    
    The algorithm starts with high temperature (accepting worse moves),
    then gradually cools down, making the search more greedy over time.
    
    Args:
        cities (list): List of city coordinates
        cooling_type (str): "exponential" or "linear" cooling schedule
    
    Returns:
        tuple: (best_tour, best_distance, iterations)
    """
    
    # Initialize parameters
    num_cities = len(cities)
    initial_temperature = 100.0
    cooling_rate_exp = 0.995  # Exponential: multiply by this each iteration
    cooling_rate_linear = 0.5  # Linear: subtract this each iteration
    max_iterations = 10000
    
    # Create initial random tour
    current_tour = list(range(num_cities))
    random.shuffle(current_tour)
    current_distance = calculate_total_tour_distance(current_tour, cities)
    
    # Track best solution found
    best_tour = current_tour[:]
    best_distance = current_distance
    
    # Temperature management
    current_temperature = initial_temperature
    
    # Simulated annealing loop
    for iteration in range(max_iterations):
        # Generate neighboring solution using 2-opt move
        # Randomly select two positions to reverse
        i = random.randint(0, num_cities - 2)
        j = random.randint(i + 1, num_cities - 1)
        
        # Apply 2-opt move
        neighbor_tour = apply_two_opt_move(current_tour, i, j)
        neighbor_distance = calculate_total_tour_distance(neighbor_tour, cities)
        
        # Calculate change in distance
        distance_change = neighbor_distance - current_distance
        
        # Acceptance decision using Metropolis criterion
        accept_prob = acceptance_probability(current_distance, neighbor_distance, current_temperature)
        
        if random.random() < accept_prob:
            # Accept the neighbor solution
            current_tour = neighbor_tour
            current_distance = neighbor_distance
        
        # Update best solution if current is better
        if current_distance < best_distance:
            best_tour = current_tour[:]
            best_distance = current_distance
        
        # Cool down temperature based on cooling schedule
        if cooling_type == "exponential":
            # Exponential cooling: T = T0 * α^k
            current_temperature = initial_temperature * (cooling_rate_exp ** iteration)
        else:
            # Linear cooling: T = T0 - β*k
            current_temperature = initial_temperature - (cooling_rate_linear * iteration)
        
        # Ensure temperature doesn't go negative
        if current_temperature < 0:
            current_temperature = 0
    
    return best_tour, best_distance, max_iterations


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TRAVELING SALESMAN PROBLEM - SIMULATED ANNEALING SOLUTION")
    print("=" * 80)
    
    # Generate 30 random cities
    random.seed(42)
    num_cities = 30
    cities = create_city_coordinates(num_cities)
    
    print(f"\nGenerated {num_cities} random cities with coordinates in [0, 100] x [0, 100]")
    
    # Test 1: Exponential Cooling
    print("\n" + "-" * 80)
    print("TEST 1: EXPONENTIAL COOLING SCHEDULE")
    print("-" * 80)
    print("Formula: T = T_initial × α^k where α = 0.995")
    
    best_tour_exp, best_dist_exp, iter_exp = simulated_annealing(cities, "exponential")
    
    print(f"\nFinal Best Distance (Exponential): {best_dist_exp:.2f}")
    print(f"Iterations Completed: {iter_exp}")
    print(f"Improvement: {(400 - best_dist_exp) / 400 * 100:.1f}% from baseline")
    
    # Test 2: Linear Cooling
    print("\n" + "-" * 80)
    print("TEST 2: LINEAR COOLING SCHEDULE")
    print("-" * 80)
    print("Formula: T = T_initial - β×k where β = 0.5")
    
    best_tour_lin, best_dist_lin, iter_lin = simulated_annealing(cities, "linear")
    
    print(f"\nFinal Best Distance (Linear): {best_dist_lin:.2f}")
    print(f"Iterations Completed: {iter_lin}")
    print(f"Improvement: {(400 - best_dist_lin) / 400 * 100:.1f}% from baseline")
    
    # Comparison
    print("\n" + "-" * 80)
    print("COMPARISON OF COOLING SCHEDULES")
    print("-" * 80)
    
    if best_dist_exp < best_dist_lin:
        better = "EXPONENTIAL"
        difference = best_dist_lin - best_dist_exp
    else:
        better = "LINEAR"
        difference = best_dist_exp - best_dist_lin
    
    print(f"Better Performance: {better} Cooling")
    print(f"Distance Difference: {difference:.2f} units")
    print(f"Exponential Distance: {best_dist_exp:.2f}")
    print(f"Linear Distance:      {best_dist_lin:.2f}")
    
    # Summary Statistics
    print("\n" + "-" * 80)
    print("ALGORITHM STATISTICS")
    print("-" * 80)
    print(f"Number of Cities: {num_cities}")
    print(f"Search Space Size: {math.factorial(num_cities)} possible tours")
    print(f"Best Tour Found (Exp): {best_tour_exp[:5]}... (showing first 5)")
    print(f"Best Tour Found (Lin): {best_tour_lin[:5]}... (showing first 5)")
    
    print("\n" + "=" * 80)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 80 + "\n")
