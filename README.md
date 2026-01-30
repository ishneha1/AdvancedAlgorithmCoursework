# Advanced Algorithm Coursework
# Implementation Guide - ST5003CEM Coursework
**Advanced Algorithms Implementations with Examples**  
**Submission Date:** 25 January 2026

---

## Table of Contents
1. [Weiszfeld Algorithm](#1-weiszfeld-algorithm)
2. [Traveling Salesman Problem](#2-traveling-salesman-problem)
3. [Tile Shatter Game](#3-tile-shatter-game)
4. [Min Service Centers](#4-minimum-service-centers)
5. [Energy Grid Distribution](#5-smart-energy-grid)
6. [Network Simulator](#6-emergency-network-simulator)
7. [Multithreaded Sorting](#7-multithreaded-sorting)
8. [Robot Delivery](#8-robot-delivery-pathfinding)

---

## 1. Weiszfeld Algorithm

**File:** `question1a.py`  
**Problem:** Find the point that minimizes sum of distances to all sensor locations.

### How to Run
```bash
python question1a.py
```

### Expected Output
```
Test Case 1: [[0, 1], [1, 0], [1, 2], [2, 1]]
Result: 4.0, Expected: 4.0
Match: True

Test Case 2: [[1, 1], [3, 3]]
Result: 2.82843, Expected: 2.82843
Match: True
```

### Code Structure
```python
def compute_optimal_hub_location(sensor_locations):
    # 1. Start at centroid
    # 2. Loop up to 100 iterations:
    #    - Calculate inverse distance weights
    #    - Compute new hub position
    #    - Check convergence
    # 3. Return total distance
```

### Custom Example
```python
# Your sensors
my_sensors = [[0, 0], [4, 0], [4, 4], [0, 4]]

result = compute_optimal_hub_location(my_sensors)
print(f"Minimum total distance: {result}")
```

### Key Parameters
- **Max Iterations:** 100 (sufficient for convergence)
- **Convergence Threshold:** 1e-7 (displacement)
- **Singularity Handling:** 1e-10 (avoid divide by zero)

### What It Outputs
- Single float value: total Euclidean distance from optimal hub to all sensors

### Input Used
- Test Case 1 sensors: [[0, 1], [1, 0], [1, 2], [2, 1]]
- Test Case 2 sensors: [[1, 1], [3, 3]]
- Note: These test cases are executed in `__main__` of `question1a.py`.

---

## 2. Traveling Salesman Problem

**File:** `question1b.py`  
**Problem:** Find near-optimal tour for 30 cities using Simulated Annealing.


### Expected Output
```
TEST 1: EXPONENTIAL COOLING SCHEDULE
Final Best Distance (Exponential): ~200-250
Iterations Completed: 10000

TEST 2: LINEAR COOLING SCHEDULE
Final Best Distance (Linear): ~200-250
Iterations Completed: 10000

COMPARISON OF COOLING SCHEDULES
Better Performance: [Exponential or Linear]
Distance Difference: X units
```

### Code Structure
```python
def simulated_annealing(cities, cooling_type="exponential"):
    # 1. Generate random initial tour
    # 2. Loop 10,000 iterations:
    #    - Generate neighbor via 2-opt swap
    #    - Calculate acceptance probability
    #    - Accept/reject based on Metropolis criterion
    #    - Cool temperature
    # 3. Return best tour found
```

### Custom Example
```python
# Generate 10 custom cities
my_cities = [[i*10, j*10] for i in range(5) for j in range(2)]

best_tour, best_dist, iters = simulated_annealing(my_cities)
print(f"Best distance: {best_dist:.2f}")
print(f"Tour: {best_tour}")
```

### Key Parameters
- **Initial Temperature:** 100.0
- **Exponential Cooling:** α = 0.995 per iteration
- **Linear Cooling:** β = 0.5 per iteration
- **Max Iterations:** 10,000

### What It Outputs
- Tuple: (best_tour, best_distance, iterations_completed)

### Input Used
- Random seed: `random.seed(42)` (ensures reproducible city coordinates)
- Number of cities generated: `num_cities = 30` (coordinates in [0,100] × [0,100])
- Cooling schedules tested: `"exponential"` and `"linear"`
- Max iterations: `10000`

---

## 3. Tile Shatter Game

**File:** `question2.py`  
**Problem:** Maximize points from shattering tiles optimally.


### Expected Output
```
Test Case 1: Multiple Tiles
Tile Multipliers: [3, 1, 5, 8]
Calculated Points: 167
Expected Points: 167
Test Status: PASS

Test Case 2: Two Tiles
Tile Multipliers: [1, 5]
Calculated Points: 10
Expected Points: 10
Test Status: PASS
```

### Code Structure
```python
def max_shatter_points(tile_multipliers):
    # 1. Add boundary sentinels (1) at start/end
    # 2. Create O(N²) DP table
    # 3. Fill by increasing range length:
    #    for each range [i, j]:
    #      for each possible last_tile k in (i, j):
    #        dp[i][j] = max(dp[i][j], 
    #          dp[i][k] + dp[k][j] + tiles[i]*tiles[k]*tiles[j])
    # 4. Return dp[0][n-1]
```

### Custom Example
```python
# Your tile multipliers
my_tiles = [2, 3, 4]

points = max_shatter_points(my_tiles)
print(f"Maximum points: {points}")
```

### Understanding the DP Table
```
For [3, 1, 5, 8]:
Boundaries added: [1, 3, 1, 5, 8, 1]

DP Table (partial):
       0    1    2    3    4    5
    0 [0    0    3   15  159  167]
    1 [0    0    0    5   49   78]
    2 [0    0    0    0   40   56]
    3 [0    0    0    0    0   40]
    4 [0    0    0    0    0    8]
    5 [0    0    0    0    0    0]
```

### Key Parameters
- **Range Length:** Increases from 2 to N (ensures subproblems solved first)
- **Last Tile Selection:** Tries all k in (i, j)

### What It Outputs
- Single integer: maximum total points achievable

### Input Used
- Test Case 1: `tile_multipliers = [3, 1, 5, 8]`
- Test Case 2: `tile_multipliers = [1, 5]`
- Note: These are executed in `__main__` of `question2.py` and validated against expected results.

---

## 4. Minimum Service Centers

**File:** `question3.py`  
**Problem:** Place minimum service centers to cover all binary tree nodes.


### Expected Output
```
Procedural Greedy Result: 2
Expected: 2

Test Case 2 (Balanced tree):
Procedural Greedy Result: 2
Expected: 2
Explanation: Centers at nodes 1 and 2 cover all nodes
  - Node 1 covers: 0, 1, 3, 4
  - Node 2 covers: 2, 5, 6
```

### Code Structure
```python
def min_service_centers(root):
    # 1. Post-order DFS traversal
    # 2. For each node evaluate children first:
    #    if any child not covered (state 0):
    #      place center here → return 1
    #    elif any child has center (state 1):
    #      this node covered → return 2
    #    else:
    #      this node not covered → return 0
    # 3. If root state = 0, add final center
```

### Custom Example
```python
# Build tree from level-order list
# None = missing node
level_list = [1, 2, 3, 4, None, 5, 6]

root = build_tree_from_level_list(level_list)
centers = min_service_centers(root)
print(f"Minimum centers needed: {centers}")
```

### Tree Building Visualization
```
Input:  [0, 0, None, 0, None, 0, None, None, 0]

Tree:        0
            / \
           0   X
          /
         0
        / \
       0   X
      /
     0

Result: 2 centers needed
```

### State Meanings
| State | Meaning | Placement Strategy |
|-------|---------|-------------------|
| 0 | Not covered | Parent must place center |
| 1 | Has center | Covers itself + neighbors |
| 2 | Covered | By child or parent center |

### What It Outputs
- Single integer: minimum number of centers required

### Input Used
- Test 1 level-order input: `[0, 0, None, 0, None, 0, None, None, 0]`
- Test 2 level-order input: `[0, 1, 2, 3, 4, 5, 6]`
- Note: Trees are built with `build_tree_from_level_list` and passed to `min_service_centers`.

---

## 5. Smart Energy Grid

**File:** `question4.py`  
**Problem:** Allocate renewable and diesel energy to districts for 24 hours.


### Expected Output
```
ENERGY GRID ALLOCATION - OPTIMIZED NEPAL GRID
===============================================
Hour  District  Solar      Hydro      Diesel     Total     Demand    % Met   Status
0     A         0.00       0.00       0.00       0.00      0.0       N/A     ✓ OK
6     A         20.00      0.00       0.00       20.00     20.0      100.0   ✓ OK
      B         0.00       15.00      0.00       15.00     15.0
      C         0.00       0.00       25.00      25.00     25.0
[... hourly breakdown ...]

SUMMARY REPORT
===============
Total Operational Cost: Rs. XXXX.XX
Total Energy Delivered: XXXX.XX kWh
Renewable Energy Contribution: XX.X%
Diesel Trigger Events: XX
```

### Code Structure
```python
def process_all_hours(demand_dict, sources):
    # For each hour:
    #   1. Get available sources (time-window check)
    #   2. Sort by cost (Solar < Hydro < Diesel)
    #   3. Allocate greedily:
    #      - Take from cheapest first
    #      - Don't exceed district demand
    #      - Don't exceed source capacity
    #   4. Track cost, renewable percentage
    # Return hourly results + summary
```

### Custom Example
```python
# Define custom demand
my_demand = {
    "09": {"A": 25, "B": 20, "C": 30},
    "15": {"A": 28, "B": 22, "C": 32},
}

sources = [
    ("Solar", 50, 6, 18, 1.0),
    ("Hydro", 40, 0, 24, 1.5),
    ("Diesel", 60, 17, 23, 3.0),
]

results = process_all_hours(my_demand, sources)
```

### Source Specifications
```python
# (name, capacity, start_hour, end_hour, cost_per_kwh)
("Solar", 50, 6, 18, 1.0)      # Day only
("Hydro", 40, 0, 24, 1.5)      # 24-hour baseline
("Diesel", 60, 17, 23, 3.0)    # Peak hours + backup
```

### Demand Tolerance
- Must satisfy: **90% ≤ (energy_used / demand) ≤ 110%**
- Ensures feasibility without excessive oversupply

### What It Outputs
```python
{
    "hourly": [
        {
            "hour": 6,
            "allocation": {"A": {"Solar": 20}, "B": {...}, ...},
            "energy_used": 60,
            "total_demand": 60,
            "demand_met_pct": 100.0,
            "is_satisfied": True,
            "cost_rs": 50.0
        },
        ...
    ],
    "summary": {
        "total_cost": 2850.0,
        "total_energy": 1950.0,
        "renewable_energy": 1400.0,
        "diesel_log": [...]
    }
}
```

### Input Used
- Sample demand from `get_sample_demand()`:
  ```python
  {
    "06": {"A": 20, "B": 15, "C": 25},
    "07": {"A": 22, "B": 16, "C": 28},
    "08": {"A": 25, "B": 18, "C": 30},
    "12": {"A": 28, "B": 20, "C": 32},
    "18": {"A": 30, "B": 22, "C": 35},
    "19": {"A": 35, "B": 25, "C": 40},
    "20": {"A": 32, "B": 24, "C": 38},
    "23": {"A": 26, "B": 19, "C": 28},
  }
  ```
- Energy sources from `get_energy_sources()`:
  ```python
  [
    ("Solar", 50, 6, 18, 1.0),
    ("Hydro", 40, 0, 24, 1.5),
    ("Diesel", 60, 17, 23, 3.0),
  ]
  ```
- Note: The main simulation calls `process_all_hours(get_sample_demand(), get_energy_sources())`.

---

---

## 6. Emergency Network Simulator

**File:** `question5a.py`  
**Problem:** Graph algorithms with interactive visualization (MST, paths, coloring).


### GUI Usage
1. **Select Source/Target nodes** from dropdowns
2. **Click operation buttons:**
   - **Q1: Compute MST** → Find minimum spanning tree
   - **Q2: Find Disjoint Paths** → Find 2 edge-disjoint paths
   - **Q3: Optimize BST** → Apply Day-Stout-Warren rebalancing
   - **Q4: Simulate Failure** → Disable a node
   - **Graph Coloring** → Apply Welsh-Powell algorithm
   - **Reset** → Clear all selections

### Visual Indicators
- **Green edges** = MST edges
- **Orange edges** = Path edges
- **Gray nodes** = Disabled nodes
- **Black edges** = Regular edges
- **Red labels** = Edge weights

### Operations Explained

#### Q1: Compute MST (Kruskal's Algorithm)
```
Purpose: Find minimum spanning tree connecting all nodes with minimum total weight
Output: Total weight, edge list
Time Complexity: O(E log E)
```

#### Q2: Find Disjoint Paths (Suurballe's Algorithm)
```
Purpose: Find 2 edge-disjoint paths from source to target
Output: Path 1 + Path 2 (no shared edges)
Time Complexity: O(V log V + E)
```

#### Q3: Optimize BST (Day-Stout-Warren)
```
Purpose: Rebalance binary search tree
Output: Height reduction message
Time Complexity: O(N)
```

#### Q4: Simulate Failure
```
Purpose: Mark a node as disabled (removes its edges)
Output: Network with disabled node
```

#### Graph Coloring (Welsh-Powell)
```
Purpose: Color graph with minimum colors
Output: Number of colors used
Time Complexity: O(V² + E)
```

### What It Displays
- Network graph visualization
- Edge weights on connections
- MST/path highlighting
- Status messages
- Node count and operation results

### Input Used
- Sample edges (u, v, weight) used in `_create_sample_network()`:
  ```python
  edges = [
    (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5),
    (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6),
    (4, 5, 3), (5, 6, 1), (6, 7, 4), (4, 7, 7)
  ]
  ```
- Node layout generated with `nx.spring_layout(self.graph, seed=42)` (seed ensures reproducible layout)

---

## 7. Multithreaded Sorting

**File:** `question5b.py`  
**Problem:** Sort array using multithreaded MergeSort with functional decomposition.

### GUI Usage
1. **Enter integers** in text field (comma or space separated):
   ```
   5 2 8 1 9
   OR
   5,2,8,1,9
   ```

2. **Click buttons:**
   - **Sort** → Execute multithreaded sort
   - **Generate Random** → Create 25 random numbers (random integers in the range 1–100)
   - **Clear** → Reset interface

3. **Observe thread log** showing:
   ```
   [HH:MM:SS] SYSTEM: Received 5 elements: [5, 2, 8, 1, 9]
   [HH:MM:SS] SYSTEM: Split into halves - Left: [5,2], Right: [8,1,9]
   [HH:MM:SS] THREAD_LEFT: Starting to sort left half
   [HH:MM:SS] THREAD_RIGHT: Starting to sort right half
   [HH:MM:SS] THREAD_MERGE: Waiting for sorting threads to complete
   [HH:MM:SS] THREAD_MERGE: All threads completed
   [HH:MM:SS] SYSTEM: Sorted result: [1, 2, 5, 8, 9]
   ```

### Code Structure
```python
def mergesort(arr):
    # Divide array at midpoint
    # Recursively sort left half
    # Recursively sort right half
    # Merge sorted halves
    return merged_array

# Threading:
thread_left = Thread(sort_left_half)
thread_right = Thread(sort_right_half)
thread_merge = Thread(merge_results)
thread_merge.join()  # Wait for completion
```

### Custom Example
```python
coordinator = SortingCoordinator()
data = [64, 34, 25, 12, 22, 11, 90]
coordinator.execute_sorting(data)
result = coordinator.wait_completion()
print(f"Sorted: {result}")
```

### Thread Safety
- **Lock-Protected Data Store:** Thread-safe variable access
- **Join Synchronization:** Merge thread waits for sorting threads
- **Timestamped Logging:** All operations logged with timestamps

### What It Displays
- Sorted array result
- Complete thread execution log
- Completion notification
- Status messages for each step

### Input Used
- Manual input example: `5 2 8 1 9` (space or comma separated)
- Generated test input: 25 random integers via `_generate_random()` (uses `random.randint(1, 100)`)
- Example programmatic use in `__main__`/tests: `data = [64, 34, 25, 12, 22, 11, 90]` passed to `execute_sorting`.

---

## 8. Robot Delivery Pathfinding

**File:** `question6.py`  
**Problem:** Find optimal path from Glogow (blue) to Plock (red) across Polish city network.

### Expected Output
```
================================================================================
DEPTH-FIRST SEARCH (DFS)
================================================================================
Step 1:
  Current City: Glogow
  Open Set: ['Poznan', 'Zielona_Gora']
  Closed Set: set()

Step 2:
  Current City: Zielona_Gora
  Open Set: ['Poznan', 'Szczecin']
  Closed Set: {'Glogow'}

[... continues until Plock found ...]

Found path: Glogow -> ... -> Plock
Total distance: X km
Nodes explored: Y

================================================================================
BREADTH-FIRST SEARCH (BFS)
================================================================================
[Similar step-by-step output with FIFO queue]

================================================================================
A* SEARCH
================================================================================
Step 1:
  Current City: Glogow
  g(n)=0, h(n)=380, f(n)=380
  Open Set: [(h1, counter, 'Poznan'), ...]
  Closed Set: set()

[... continues with f(n) calculations ...]

================================================================================
COMPARATIVE ANALYSIS REPORT
================================================================================
1. PATH COMPARISON:
   DFS Path: Glogow -> ... -> Plock (length: X cities)
   BFS Path: Glogow -> ... -> Plock (length: X cities)
   A* Path: Glogow -> ... -> Plock (length: X cities, OPTIMAL)

2. EFFICIENCY COMPARISON:
   DFS - Steps: X, Nodes Explored: Y
   BFS - Steps: X, Nodes Explored: Y
   A*  - Steps: X, Nodes Explored: Y (LOWEST)

3. PATH OPTIMALITY:
   Shortest path distance: X km (found by A*)
   All algorithms found paths: YES

4. TIME & SPACE COMPLEXITY:
   DFS: O(b^d) time, O(d) space
   BFS: O(b^d) time, O(b^d) space
   A*: O(b^d) time, O(b^d) space (best with heuristic)

5. ALGORITHM CHARACTERISTICS:
   DFS - Non-optimal, memory efficient
   BFS - Optimal (unweighted), explores breadth
   A* - Optimal (with heuristic), BEST FOR THIS TASK
```

### Code Structure
```python
# DFS - Stack based
open_set = [START]
while open_set:
    current = open_set.pop()  # LIFO
    for neighbor in CITY_GRAPH[current]:
        open_set.append(neighbor)

# BFS - Queue based
open_set = deque([START])
while open_set:
    current = open_set.popleft()  # FIFO
    for neighbor in CITY_GRAPH[current]:
        open_set.append(neighbor)

# A* - Priority queue based
open_set = [(f_score, counter, START)]
while open_set:
    f, _, current = heapq.heappop(open_set)  # Lowest f(n)
    for neighbor in CITY_GRAPH[current]:
        f_score = g_score + heuristic
        heapq.heappush(open_set, (f_score, counter, neighbor))
```

### Polish City Network
```
Nodes: 13 cities
Glogow ← START (Blue)
Plock ← GOAL (Red)
Intermediate: Poznań, Wrocław, Zielona Góra, Szczecin, Konin, 
              Łódź, Warsaw, Opole, Kalisz, Radom, Gdańsk

Edges: Weighted with real distances (km)
```

### A* Heuristic
```python
# Straight-line distances to Plock (goal)
HEURISTIC = {
    'Glogow': 380,
    'Poznan': 340,
    'Plock': 0,
    # ...
}

# f(n) = g(n) + h(n)
# g(n) = actual path cost from start
# h(n) = estimated distance to goal
```

### Custom Example
```python
# Run single algorithm
path, explored, steps = depth_first_search()
if path:
    print(f"Found path: {' -> '.join(path)}")
    cost = calculate_path_cost(path)
    print(f"Total distance: {cost} km")
```

### What It Outputs
- Step-by-step algorithm execution
- Open and Closed sets at each step
- Final path (if found)
- Nodes explored count
- Steps to completion
- Comparative analysis of all 3 algorithms

---

## General Guidelines

### Input Validation
- **Weiszfeld:** Non-empty sensor list
- **TSP:** Coordinates in valid range
- **Tile Shatter:** Positive multiplier values
- **Min Centers:** Valid tree structure
- **Energy Grid:** Non-zero demand/capacity
- **Network Sim:** Valid graph with nodes/edges
- **Multithreaded:** Space/comma-separated integers
- **Pathfinding:** Valid city names in graph

### Debugging Tips
1. **Print intermediate values** during execution
2. **Trace algorithm steps** manually for small inputs
3. **Verify test cases** before custom examples
4. **Check complexity** matches problem requirements
5. **Validate output format** matches expected results

---

## Summary Table

| Problem | File | Run | Input | Output |
|---------|------|-----|-------|--------|
| Weiszfeld | question1a.py | `python question1a.py` | Coordinates | Float distance |
| TSP | question1b.py | `python question1b.py` | Num cities | Tour + distance |
| Tile Shatter | question2.py | `python question2.py` | Multipliers | Integer points |
| Min Centers | question3.py | `python question3.py` | Tree list | Integer count |
| Energy Grid | question4.py | `python question4.py` | Demand + sources | Allocation plan |
| Network Sim | question5a.py | `python question5a.py` | GUI buttons | Visualization |
| Multithreaded | question5b.py | `python question5b.py` | Integer array | Sorted array + logs |
| Robot Delivery | question6.py | `python question6.py` | Graph | Path + comparison |

---

**Module:** ST5003CEM Advanced Algorithms  
**Due:** 25 January 2026  
**Format:** Complete Implementation Guide with Examples

