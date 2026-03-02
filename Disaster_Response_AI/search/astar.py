"""
A* Search Algorithm
-------------------
Informed search using heuristic guidance.

AI Concepts Covered:
- Informed Search
- Best First Search
- A* Algorithm
- Heuristic Function
"""

import heapq
import math

def heuristic(node, goal, city_graph):
    """
    Euclidean distance heuristic.
    """
    if node not in city_graph.coordinates or goal not in city_graph.coordinates:
        return 0

    x1, y1 = city_graph.coordinates[node]
    x2, y2 = city_graph.coordinates[goal]

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def astar(city_graph, start, goal):
    """
    Perform A* Search on the city graph.

    Returns:
        path
        path_cost
        nodes_expanded
    """

    # Priority Queue (min-heap)
    open_list = []
    heapq.heappush(open_list, (0, start))

    # Cost from start to node
    g_cost = {start: 0}

    # Parent tracking
    parent = {start: None}

    # Visited set
    closed_set = set()

    nodes_expanded = 0

    while open_list:
        current_f, current_node = heapq.heappop(open_list)

        if current_node in closed_set:
            continue

        closed_set.add(current_node)
        nodes_expanded += 1

        # Goal Test
        if current_node == goal:
            break

        for neighbor, cost in city_graph.get_neighbors(current_node):

            tentative_g = g_cost[current_node] + cost

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_cost = tentative_g + heuristic(neighbor, goal, city_graph)

                heapq.heappush(open_list, (f_cost, neighbor))
                parent[neighbor] = current_node

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

    path_cost = g_cost[goal]

    return path, path_cost, nodes_expanded