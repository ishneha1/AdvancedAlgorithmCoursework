"""
Robot Delivery Problem - Polish Cities (Procedural Approach)
Implements DFS, BFS, and A* algorithms with detailed step-by-step tracking.
Start: Glogow (Blue) | Goal: Plock (Red)
"""

from collections import deque, defaultdict
import heapq


def build_graph_map():
    """
    Build dictionary-based graph representing Polish city network.
    Returns adjacency list with edge weights.
    """
    graph = {
        'Glogow': {'Poznan': 85, 'Konin': 50},
        'Poznan': {'Glogow': 85, 'Gniezno': 55, 'Leszno': 50},
        'Konin': {'Glogow': 50, 'Kalisz': 60, 'Slupsk': 150},
        'Gniezno': {'Poznan': 55, 'Kalisz': 75, 'Inowroclaw': 70},
        'Kalisz': {'Konin': 60, 'Gniezno': 75, 'Sieradz': 80},
        'Leszno': {'Poznan': 50, 'Lodz': 100, 'Sieradz': 90},
        'Inowroclaw': {'Gniezno': 70, 'Sieradz': 85, 'Wloclawek': 60},
        'Sieradz': {'Kalisz': 80, 'Leszno': 90, 'Inowroclaw': 85, 'Lodz': 45, 'Plock': 120},
        'Wloclawek': {'Inowroclaw': 60, 'Plock': 75},
        'Lodz': {'Leszno': 100, 'Sieradz': 45, 'Radom': 90},
        'Radom': {'Lodz': 90, 'Plock': 85},
        'Plock': {'Sieradz': 120, 'Wloclawek': 75, 'Radom': 85}
    }
    return graph


def build_heuristic_distances():
    """
    Build heuristic values (straight-line distances to goal Plock).
    These are estimates used for A* algorithm.
    """
    heuristic = {
        'Glogow': 280,
        'Poznan': 250,
        'Konin': 240,
        'Gniezno': 200,
        'Kalisz': 190,
        'Leszno': 210,
        'Inowroclaw': 160,
        'Sieradz': 130,
        'Wloclawek': 80,
        'Lodz': 110,
        'Radom': 90,
        'Plock': 0
    }
    return heuristic


def depth_first_search(graph, start, goal):
    """
    Depth-First Search implementation with detailed tracking.
    
    Tracks Open (Frontier) and Closed (Visited) sets at each step.
    Time Complexity: O(V + E) where V = vertices, E = edges
    Space Complexity: O(V) for recursion stack
    
    Returns: path found, steps log, metrics
    """
    steps_log = []
    open_set = [start]
    closed_set = set()
    parent_map = {start: None}
    path_found = None
    
    step_num = 0
    while open_set:
        step_num += 1
        current = open_set.pop()  # DFS: remove from end (LIFO)
        
        # Log current step
        step_info = {
            'step': step_num,
            'current': current,
            'open_before': open_set[:],
            'closed': closed_set.copy()
        }
        
        if current in closed_set:
            continue
        
        closed_set.add(current)
        step_info['open_after'] = open_set[:]
        step_info['closed_after'] = closed_set.copy()
        steps_log.append(step_info)
        
        if current == goal:
            path_found = current
            break
        
        # Explore neighbors
        if current in graph:
            for neighbor in sorted(graph[current].keys()):
                if neighbor not in closed_set and neighbor not in open_set:
                    open_set.append(neighbor)
                    parent_map[neighbor] = current
    
    # Reconstruct path
    path = []
    if path_found:
        node = path_found
        while node:
            path.append(node)
            node = parent_map.get(node)
        path.reverse()
    
    return path, steps_log, len(closed_set)


def breadth_first_search(graph, start, goal):
    """
    Breadth-First Search implementation with detailed tracking.
    
    Uses queue (FIFO) for level-by-level exploration.
    Guarantees shortest path in unweighted graphs.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Returns: path found, steps log, metrics
    """
    steps_log = []
    open_queue = deque([start])
    closed_set = set()
    parent_map = {start: None}
    path_found = None
    
    step_num = 0
    while open_queue:
        step_num += 1
        current = open_queue.popleft()  # BFS: remove from front (FIFO)
        
        if current in closed_set:
            continue
        
        closed_set.add(current)
        
        # Log step
        step_info = {
            'step': step_num,
            'current': current,
            'open': list(open_queue),
            'closed': closed_set.copy()
        }
        steps_log.append(step_info)
        
        if current == goal:
            path_found = current
            break
        
        # Add neighbors to queue
        if current in graph:
            for neighbor in sorted(graph[current].keys()):
                if neighbor not in closed_set and neighbor not in open_queue:
                    open_queue.append(neighbor)
                    parent_map[neighbor] = current
    
    # Reconstruct path
    path = []
    if path_found:
        node = path_found
        while node:
            path.append(node)
            node = parent_map.get(node)
        path.reverse()
    
    return path, steps_log, len(closed_set)


def astar_search(graph, start, goal, heuristic):
    """
    A* Search implementation with priority queue.
    
    Uses formula: f(n) = g(n) + h(n)
    g(n) = actual cost from start
    h(n) = heuristic estimate to goal
    
    Returns optimal path when heuristic is admissible.
    Time Complexity: O((V + E) log V) with priority queue
    Space Complexity: O(V)
    
    Returns: path found, steps log, metrics
    """
    steps_log = []
    open_set = [(0, start)]  # (f_value, node)
    open_set_nodes = {start}
    closed_set = set()
    g_scores = {start: 0}
    parent_map = {start: None}
    
    step_num = 0
    while open_set:
        step_num += 1
        f_value, current = heapq.heappop(open_set)
        open_set_nodes.discard(current)
        
        if current in closed_set:
            continue
        
        closed_set.add(current)
        
        # Log step
        step_info = {
            'step': step_num,
            'current': current,
            'g_value': g_scores[current],
            'h_value': heuristic.get(current, 0),
            'f_value': f_value,
            'open': list(open_set_nodes),
            'closed': closed_set.copy()
        }
        steps_log.append(step_info)
        
        if current == goal:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node)
                node = parent_map.get(node)
            path.reverse()
            return path, steps_log, len(closed_set)
        
        # Explore neighbors
        if current in graph:
            for neighbor, edge_weight in graph[current].items():
                if neighbor not in closed_set:
                    tentative_g = g_scores[current] + edge_weight
                    
                    if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                        g_scores[neighbor] = tentative_g
                        h_value = heuristic.get(neighbor, 0)
                        f_value = tentative_g + h_value
                        parent_map[neighbor] = current
                        
                        if neighbor not in open_set_nodes:
                            heapq.heappush(open_set, (f_value, neighbor))
                            open_set_nodes.add(neighbor)
    
    return [], steps_log, len(closed_set)


def calculate_path_cost(path, graph):
    """Calculate total cost of a path."""
    if len(path) < 2:
        return 0
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i+1]]
    return cost


def print_algorithm_steps(algorithm_name, steps_log, path, cost):
    """Print detailed algorithm execution steps."""
    print(f"\n{'='*80}")
    print(f"{algorithm_name.upper()} - STEP-BY-STEP EXECUTION")
    print(f"{'='*80}")
    
    for step in steps_log:
        print(f"\nStep {step['step']}:")
        print(f"  Current Node: {step['current']}")
        
        if 'g_value' in step:  # A* specific
            print(f"  g(n) [cost from start]: {step['g_value']}")
            print(f"  h(n) [heuristic to goal]: {step['h_value']}")
            print(f"  f(n) [g(n) + h(n)]: {step['f_value']}")
        
        print(f"  Open (Frontier): {step.get('open_before', step.get('open', []))}")
        print(f"  Closed (Visited): {sorted(step.get('closed', []))}")
    
    print(f"\n{'-'*80}")
    print(f"Final Path: {' -> '.join(path) if path else 'No path found'}")
    print(f"Path Cost: {cost}")
    print(f"Nodes Explored: {len(steps_log)}")


def generate_comparison_report(dfs_data, bfs_data, astar_data):
    """Generate comparative analysis of all three algorithms."""
    print(f"\n{'='*80}")
    print("COMPARATIVE ANALYSIS: DFS vs BFS vs A*")
    print(f"{'='*80}")
    
    print("\nAlgorithm Performance:")
    print(f"{'Algorithm':<12} {'Path Found':<15} {'Path Cost':<15} {'Nodes Explored':<15}")
    print("-" * 60)
    
    dfs_path, dfs_steps, dfs_nodes = dfs_data
    bfs_path, bfs_steps, bfs_nodes = bfs_data
    astar_path, astar_steps, astar_nodes = astar_data
    
    graph = build_graph_map()
    
    dfs_cost = calculate_path_cost(dfs_path, graph)
    bfs_cost = calculate_path_cost(bfs_path, graph)
    astar_cost = calculate_path_cost(astar_path, graph)
    
    print(f"{'DFS':<12} {'Yes' if dfs_path else 'No':<15} {dfs_cost:<15} {dfs_nodes:<15}")
    print(f"{'BFS':<12} {'Yes' if bfs_path else 'No':<15} {bfs_cost:<15} {bfs_nodes:<15}")
    print(f"{'A*':<12} {'Yes' if astar_path else 'No':<15} {astar_cost:<15} {astar_nodes:<15}")
    
    print("\nKey Observations:")
    print("- DFS: Uses stack (LIFO), explores deeply. May not find optimal path.")
    print("- BFS: Uses queue (FIFO), explores level-by-level. Finds shortest path in unweighted graphs.")
    print("- A*: Uses heuristic (f=g+h), guided search. Finds optimal path with fewer explorations.")
    
    print(f"\nOptimality Analysis:")
    print(f"- A* path cost ({astar_cost}) vs BFS path cost ({bfs_cost}): ", end="")
    if astar_cost <= bfs_cost:
        print("✓ A* finds optimal/better solution")
    else:
        print("BFS competitive on this weighted graph")
    
    print(f"\nEfficiency Analysis:")
    print(f"- A* explored {astar_nodes} nodes (heuristic guidance)")
    print(f"- BFS explored {bfs_nodes} nodes (blind search)")
    print(f"- DFS explored {dfs_nodes} nodes (depth-first)")
    print(f"- Reduction: {((bfs_nodes - astar_nodes) / bfs_nodes * 100):.1f}% fewer nodes explored by A*")


if __name__ == "__main__":
    print("ROBOT DELIVERY SYSTEM - POLISH CITIES ROUTING")
    print("Start: Glogow (Blue) | Goal: Plock (Red)")
    
    graph = build_graph_map()
    heuristic = build_heuristic_distances()
    start_city = 'Glogow'
    goal_city = 'Plock'
    
    # Run all algorithms
    dfs_path, dfs_steps, dfs_nodes = depth_first_search(graph, start_city, goal_city)
    bfs_path, bfs_steps, bfs_nodes = breadth_first_search(graph, start_city, goal_city)
    astar_path, astar_steps, astar_nodes = astar_search(graph, start_city, goal_city, heuristic)
    
    # Print results
    print_algorithm_steps("DFS", dfs_steps, dfs_path, calculate_path_cost(dfs_path, graph))
    print_algorithm_steps("BFS", bfs_steps, bfs_path, calculate_path_cost(bfs_path, graph))
    print_algorithm_steps("A*", astar_steps, astar_path, calculate_path_cost(astar_path, graph))
    
    # Generate comparison
    generate_comparison_report(
        (dfs_path, dfs_steps, dfs_nodes),
        (bfs_path, bfs_steps, bfs_nodes),
        (astar_path, astar_steps, astar_nodes)
    )
