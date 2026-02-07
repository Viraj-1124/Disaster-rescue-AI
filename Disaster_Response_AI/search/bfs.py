"""
Breadth First Search (BFS)
-------------------------
Uninformed search strategy used for route finding.

AI Concepts Covered:
- Uninformed Search
- State Space Search
- Completeness and Optimality (unweighted)
"""

from collections import deque


def bfs(city_graph, start, goal):
    """
    Perform Breadth First Search on the city graph.

    Parameters:
        city_graph : CityGraph object
        start      : Start location
        goal       : Goal location (e.g., hospital)

    Returns:
        path            : List of nodes from start to goal
        path_cost       : Total travel cost
        nodes_expanded  : Number of nodes expanded
    """

    # Queue for BFS (FIFO)
    queue = deque()
    queue.append(start)

    # Track visited nodes
    visited = set()
    visited.add(start)

    # Parent dictionary for path reconstruction
    parent = {start: None}

    # Track number of expanded nodes
    nodes_expanded = 0

    # -----------------------
    # BFS Loop
    # -----------------------
    while queue:
        current_node = queue.popleft()
        nodes_expanded += 1

        # Goal Test
        if current_node == goal:
            break

        # Expand neighbors
        for neighbor, _ in city_graph.get_neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)

    # -----------------------
    # Path Reconstruction
    # -----------------------
    path = []
    path_cost = 0

    if goal not in parent:
        return None, float('inf'), nodes_expanded

    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    path.reverse()

    # Compute path cost
    for i in range(len(path) - 1):
        path_cost += city_graph.graph[path[i]][path[i + 1]]

    return path, path_cost, nodes_expanded
