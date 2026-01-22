"""
Robot Delivery Path Finding - Procedural Approach
Implements DFS, BFS, and A* search algorithms for Polish city network.
Shows Open/Closed containers at each step for algorithm transparency.
"""

from collections import deque
import heapq


# Graph representation: Polish city network with edge weights (distances in km)
CITY_GRAPH = {
    'Glogow': {'Zielona_Gora': 50, 'Poznan': 85, 'Wroclaw': 120},
    'Zielona_Gora': {'Glogow': 50, 'Poznan': 60, 'Szczecin': 180},
    'Poznan': {'Glogow': 85, 'Zielona_Gora': 60, 'Wroclaw': 90, 'Konin': 70, 'Lodz': 110},
    'Wroclaw': {'Glogow': 120, 'Poznan': 90, 'Opole': 95, 'Kalisz': 130},
    'Szczecin': {'Zielona_Gora': 180, 'Gdansk': 350},
    'Konin': {'Poznan': 70, 'Lodz': 95, 'Warsaw': 180},
    'Lodz': {'Poznan': 110, 'Konin': 95, 'Warsaw': 140, 'Plock': 150},
    'Warsaw': {'Konin': 180, 'Lodz': 140, 'Plock': 120, 'Radom': 100},
    'Plock': {'Lodz': 150, 'Warsaw': 120},
    'Opole': {'Wroclaw': 95, 'Kalisz': 120},
    'Kalisz': {'Wroclaw': 130, 'Opole': 120, 'Lodz': 80},
    'Radom': {'Warsaw': 100},
    'Gdansk': {'Szczecin': 350},
}

# Straight-line distances from each city to Plock (heuristic)
HEURISTIC_DISTANCES = {
    'Glogow': 380,
    'Zielona_Gora': 400,
    'Poznan': 340,
    'Wroclaw': 450,
    'Szczecin': 500,
    'Konin': 280,
    'Lodz': 150,
    'Warsaw': 120,
    'Plock': 0,
    'Opole': 480,
    'Kalisz': 200,
    'Radom': 140,
    'Gdansk': 550,
}

START_CITY = 'Glogow'  # Blue starting point
GOAL_CITY = 'Plock'    # Red goal point


def depth_first_search():
    """
    Depth-First Search (DFS) implementation.
    Uses stack (LIFO) to explore deepest nodes first.
    Shows Open and Closed sets at each step.
    """
    print("\n" + "="*80)
    print("DEPTH-FIRST SEARCH (DFS)")
    print("="*80)
    
    open_set = [START_CITY]  # Stack of unvisited nodes
    closed_set = set()        # Set of visited nodes
    path_tree = {START_CITY: None}  # Track parent nodes
    step = 0
    
    while open_set:
        step += 1
        
        # Pop from end (stack - LIFO)
        current = open_set.pop()
        
        print(f"\nStep {step}:")
        print(f"  Current City: {current}")
        print(f"  Open Set: {open_set}")
        print(f"  Closed Set: {closed_set}")
        
        if current == GOAL_CITY:
            print(f"\n✓ GOAL FOUND: {GOAL_CITY}")
            return reconstruct_path(path_tree, current), len(closed_set), step
        
        closed_set.add(current)
        
        # Add neighbors to open set (right to left for specific order)
        if current in CITY_GRAPH:
            neighbors = list(CITY_GRAPH[current].keys())
            for neighbor in reversed(neighbors):  # Reverse for consistent DFS
                if neighbor not in closed_set and neighbor not in open_set:
                    open_set.append(neighbor)
                    path_tree[neighbor] = current
                    print(f"  Adding to Open: {neighbor} (parent: {current})")
    
    return None, len(closed_set), step


def breadth_first_search():
    """
    Breadth-First Search (BFS) implementation.
    Uses queue (FIFO) to explore nodes level by level.
    Guarantees shortest path in unweighted graphs.
    Shows Open and Closed sets at each step.
    """
    print("\n" + "="*80)
    print("BREADTH-FIRST SEARCH (BFS)")
    print("="*80)
    
    open_set = deque([START_CITY])  # Queue of unvisited nodes
    closed_set = set()               # Set of visited nodes
    path_tree = {START_CITY: None}   # Track parent nodes
    step = 0
    
    while open_set:
        step += 1
        
        # Pop from front (queue - FIFO)
        current = open_set.popleft()
        
        print(f"\nStep {step}:")
        print(f"  Current City: {current}")
        print(f"  Open Set: {list(open_set)}")
        print(f"  Closed Set: {closed_set}")
        
        if current == GOAL_CITY:
            print(f"\n✓ GOAL FOUND: {GOAL_CITY}")
            return reconstruct_path(path_tree, current), len(closed_set), step
        
        closed_set.add(current)
        
        # Add neighbors to queue
        if current in CITY_GRAPH:
            for neighbor in CITY_GRAPH[current].keys():
                if neighbor not in closed_set and neighbor not in open_set:
                    open_set.append(neighbor)
                    path_tree[neighbor] = current
                    print(f"  Adding to Open: {neighbor} (parent: {current})")
    
    return None, len(closed_set), step


def a_star_search():
    """
    A* Search implementation.
    Uses priority queue based on f(n) = g(n) + h(n).
    g(n) = actual path cost from start
    h(n) = heuristic estimate to goal (straight-line distance)
    """
    print("\n" + "="*80)
    print("A* SEARCH")
    print("="*80)
    
    # Priority queue: (f_score, counter, city)
    counter = 0
    open_set = [(HEURISTIC_DISTANCES[START_CITY], counter, START_CITY)]
    counter += 1
    
    closed_set = set()
    g_scores = {START_CITY: 0}  # Actual cost from start
    path_tree = {START_CITY: None}
    step = 0
    
    while open_set:
        step += 1
        
        # Get city with lowest f(n)
        f_score, _, current = heapq.heappop(open_set)
        
        if current in closed_set:
            continue
        
        open_cities = [city for _, _, city in open_set]
        
        print(f"\nStep {step}:")
        print(f"  Current City: {current}")
        print(f"  f(n) = g(n) + h(n) = {g_scores[current]} + {HEURISTIC_DISTANCES[current]} = {f_score}")
        print(f"  Open Set: {open_cities}")
        print(f"  Closed Set: {closed_set}")
        
        if current == GOAL_CITY:
            print(f"\n✓ GOAL FOUND: {GOAL_CITY}")
            return reconstruct_path(path_tree, current), len(closed_set), step
        
        closed_set.add(current)
        
        # Explore neighbors
        if current in CITY_GRAPH:
            for neighbor, edge_weight in CITY_GRAPH[current].items():
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g(n)
                tentative_g = g_scores[current] + edge_weight
                
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    # Update best path to neighbor
                    g_scores[neighbor] = tentative_g
                    f_n = tentative_g + HEURISTIC_DISTANCES[neighbor]
                    path_tree[neighbor] = current
                    
                    heapq.heappush(open_set, (f_n, counter, neighbor))
                    counter += 1
                    
                    print(f"  Adding/Updating {neighbor}: g={tentative_g}, h={HEURISTIC_DISTANCES[neighbor]}, f={f_n}")
    
    return None, len(closed_set), step


def reconstruct_path(path_tree, goal):
    """Reconstruct path from start to goal using parent pointers."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = path_tree[current]
    return list(reversed(path))


def calculate_path_cost(path):
    """Calculate total distance for a path."""
    cost = 0
    for i in range(len(path) - 1):
        if path[i] in CITY_GRAPH and path[i+1] in CITY_GRAPH[path[i]]:
            cost += CITY_GRAPH[path[i]][path[i+1]]
    return cost


def generate_comparative_report(dfs_result, bfs_result, astar_result):
    """Generate comparative analysis of all three algorithms."""
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS REPORT")
    print("="*80)
    
    dfs_path, dfs_explored, dfs_steps = dfs_result
    bfs_path, bfs_explored, bfs_steps = bfs_result
    astar_path, astar_explored, astar_steps = astar_result
    
    print("\n1. PATH COMPARISON:")
    print(f"   DFS Path:  {' -> '.join(dfs_path) if dfs_path else 'No path found'}")
    if dfs_path:
        print(f"   DFS Cost:  {calculate_path_cost(dfs_path)} km, Length: {len(dfs_path)-1} edges")
    
    print(f"\n   BFS Path:  {' -> '.join(bfs_path) if bfs_path else 'No path found'}")
    if bfs_path:
        print(f"   BFS Cost:  {calculate_path_cost(bfs_path)} km, Length: {len(bfs_path)-1} edges")
    
    print(f"\n   A* Path:   {' -> '.join(astar_path) if astar_path else 'No path found'}")
    if astar_path:
        print(f"   A* Cost:   {calculate_path_cost(astar_path)} km, Length: {len(astar_path)-1} edges")
    
    print("\n2. EFFICIENCY COMPARISON:")
    print(f"   DFS - Steps: {dfs_steps}, Nodes Explored: {dfs_explored}")
    print(f"   BFS - Steps: {bfs_steps}, Nodes Explored: {bfs_explored}")
    print(f"   A*  - Steps: {astar_steps}, Nodes Explored: {astar_explored}")
    
    print("\n3. PATH OPTIMALITY:")
    if astar_path and bfs_path:
        astar_cost = calculate_path_cost(astar_path)
        bfs_cost = calculate_path_cost(bfs_path)
        print(f"   A* finds optimal path: {'✓ Yes' if astar_cost <= bfs_cost else '✗ No'}")
    
    print("\n4. TIME & SPACE COMPLEXITY ANALYSIS:")
    print("   DFS: O(b^d) time, O(d) space (best case with good ordering)")
    print("   BFS: O(b^d) time, O(b^d) space (explores all nodes at depth d)")
    print("   A*:  O(b^d) time, O(b^d) space (typically best with good heuristic)")
    
    print("\n5. ALGORITHM CHARACTERISTICS:")
    print("   DFS  - Non-optimal, memory efficient, can get stuck in cycles")
    print("   BFS  - Optimal (unweighted), explores breadth-wise, memory intensive")
    print("   A*   - Optimal (with admissible heuristic), guided by heuristic, best for this task")
    
    print("\n6. RECOMMENDATION FOR ROBOT DELIVERY:")
    print("   Use A* Search because:")
    print("   - Guarantees optimal path with proper heuristic")
    print("   - Explores fewer nodes than BFS by using heuristic guidance")
    print("   - More efficient for weighted graphs like real road networks")
    print("   - Straight-line distances provide good admissible heuristic")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ROBOT DELIVERY PATHFINDING - POLISH CITY NETWORK")
    print(f"Start (Blue): {START_CITY} → Goal (Red): {GOAL_CITY}")
    print("="*80)
    
    # Run all algorithms
    dfs_result = depth_first_search()
    bfs_result = breadth_first_search()
    astar_result = a_star_search()
    
    # Generate comparison
    generate_comparative_report(dfs_result, bfs_result, astar_result)
