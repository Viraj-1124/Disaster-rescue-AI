"""
Depth First Search (DFS)
------------------------
Uninformed search strategy using LIFO structure.

AI Concepts Covered:
- Uninformed Search
- State Space Search
- Comparison with BFS
"""

def dfs(city_graph, start, goal):
    """
    Perform Depth First Search on the city graph.

    Parameters:
        city_graph : CityGraph object
        start      : Start location
        goal       : Goal location

    Returns:
        path            : List of nodes from start to goal
        path_cost       : Total travel cost
        nodes_expanded  : Number of nodes expanded
    """

    # Stack for DFS (LIFO)
    stack = []
    stack.append(start)

    visited = set()
    parent = {start: None}

    nodes_expanded = 0

    while stack:
        current_node = stack.pop()

        if current_node not in visited:
            visited.add(current_node)
            nodes_expanded += 1

            # Goal Test
            if current_node == goal:
                break

            # Expand neighbors
            # Reverse for consistent traversal order
            neighbors = city_graph.get_neighbors(current_node)
            neighbors.reverse()

            for neighbor, _ in neighbors:
                if neighbor not in visited:
                    parent[neighbor] = current_node
                    stack.append(neighbor)

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