"""
Comparison Module
-----------------
Compares BFS and DFS performance.

AI Concepts Covered:
- Comparison of Uninformed Search Strategies
- Performance Metrics
"""

from search.bfs import bfs
from search.dfs import dfs
from search.astar import astar


def compare_uninformed(city_graph, start, goal):
    """
    Compare BFS and DFS on:
    - Path found
    - Path cost
    - Nodes expanded
    """

    print("\n========== UNINFORMED SEARCH COMPARISON ==========")

    # Run BFS
    bfs_path, bfs_cost, bfs_expanded = bfs(city_graph, start, goal)

    # Run DFS
    dfs_path, dfs_cost, dfs_expanded = dfs(city_graph, start, goal)

    astar_path, astar_cost, astar_expanded = astar(city_graph, start, goal)

    # Print Results
    print("\n--- BFS Result ---")
    print("Path:", bfs_path)
    print("Path Cost:", bfs_cost)
    print("Nodes Expanded:", bfs_expanded)

    print("\n--- DFS Result ---")
    print("Path:", dfs_path)
    print("Path Cost:", dfs_cost)
    print("Nodes Expanded:", dfs_expanded)

    print("\n--- A* Result ---")
    print("Path:", astar_path)
    print("Path Cost:", astar_cost)
    print("Nodes Expanded:", astar_expanded)

    print("\n========== ANALYSIS ==========")

    if bfs_cost < dfs_cost:
        print("BFS found a cheaper path.")
    elif dfs_cost < bfs_cost:
        print("DFS found a cheaper path.")
    else:
        print("Both found equal cost paths.")

    if bfs_expanded < dfs_expanded:
        print("BFS expanded fewer nodes.")
    elif dfs_expanded < bfs_expanded:
        print("DFS expanded fewer nodes.")
    else:
        print("Both expanded equal number of nodes.")

    print("==================================================\n")