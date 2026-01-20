"""
Optimal Sensor Placement - Weiszfeld Algorithm Implementation
Traditional Iterative Approach with Detailed Inline Documentation

This module implements the Weiszfeld algorithm to find the geometric median
of a set of sensor locations, minimizing the sum of Euclidean distances.
"""

import math


def compute_optimal_hub_location(sensor_locations):
    """
    Finds the optimal hub location that minimizes total Euclidean distance
    to all sensors using the Weiszfeld iterative optimization algorithm.
    
    The Weiszfeld algorithm converges to the geometric median, which is the
    point that minimizes the sum of distances to all input points.
    
    Args:
        sensor_locations (list of list): Each element is [x, y] coordinates
        
    Returns:
        float: The minimum total distance (sum of Euclidean distances)
        
    Raises:
        ValueError: If sensor_locations is empty
    """
    
    if not sensor_locations:
        raise ValueError("Sensor locations cannot be empty")
    
    if len(sensor_locations) == 1:
        return 0.0
    
    # Initialize hub at the arithmetic mean (centroid)
    sum_x = sum(sensor[0] for sensor in sensor_locations)
    sum_y = sum(sensor[1] for sensor in sensor_locations)
    n_sensors = len(sensor_locations)
    
    current_hub_x = sum_x / n_sensors
    current_hub_y = sum_y / n_sensors
    
    # Convergence parameters
    max_iterations = 100
    convergence_threshold = 1e-7
    
    # Iterative refinement using Weiszfeld algorithm
    for iteration in range(max_iterations):
        numerator_x = 0.0
        numerator_y = 0.0
        denominator = 0.0
        
        # Calculate weights based on inverse distances
        for sensor_x, sensor_y in sensor_locations:
            dx = sensor_x - current_hub_x
            dy = sensor_y - current_hub_y
            
            # Calculate Euclidean distance from hub to sensor
            distance_to_sensor = math.sqrt(dx * dx + dy * dy)
            
            # Handle case where hub coincides with a sensor
            if distance_to_sensor < 1e-10:
                distance_to_sensor = 1e-10
            
            # Weight is the inverse of distance
            weight = 1.0 / distance_to_sensor
            
            # Accumulate weighted coordinates and total weight
            numerator_x += weight * sensor_x
            numerator_y += weight * sensor_y
            denominator += weight
        
        # Calculate next hub position
        prev_hub_x = current_hub_x
        prev_hub_y = current_hub_y
        
        current_hub_x = numerator_x / denominator
        current_hub_y = numerator_y / denominator
        
        # Check convergence: movement of hub below threshold
        displacement = math.sqrt(
            (current_hub_x - prev_hub_x) ** 2 + 
            (current_hub_y - prev_hub_y) ** 2
        )
        
        if displacement < convergence_threshold:
            break
    
    # Calculate total distance with final hub position
    total_distance = 0.0
    for sensor_x, sensor_y in sensor_locations:
        dx = sensor_x - current_hub_x
        dy = sensor_y - current_hub_y
        distance = math.sqrt(dx * dx + dy * dy)
        total_distance += distance
    
    return round(total_distance, 5)

if __name__ == "__main__":
    # Test Case 1: Square configuration
    test_case_1 = [[0, 1], [1, 0], [1, 2], [2, 1]]
    result_1 = compute_optimal_hub_location(test_case_1)
    print(f"Test Case 1: {test_case_1}")
    print(f"Result: {result_1}, Expected: 4.0")
    print(f"Match: {abs(result_1 - 4.0) < 0.01}\n")
    
    # Test Case 2: Two points
    test_case_2 = [[1, 1], [3, 3]]
    result_2 = compute_optimal_hub_location(test_case_2)
    print(f"Test Case 2: {test_case_2}")
    print(f"Result: {result_2}, Expected: 2.82843")
    print(f"Match: {abs(result_2 - 2.82843) < 0.01}")

