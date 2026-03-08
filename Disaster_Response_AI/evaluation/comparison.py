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

    # Run BFS
    bfs_path, bfs_cost, bfs_expanded = bfs(city_graph, start, goal)

    # Run DFS
    dfs_path, dfs_cost, dfs_expanded = dfs(city_graph, start, goal)

    astar_path, astar_cost, astar_expanded = astar(city_graph, start, goal)

    print("\n========== ANALYSIS ==========")
    best_cost = min(bfs_cost, dfs_cost, astar_cost)

    best_algorithms = []
    if bfs_cost == best_cost:
        best_algorithms.append("BFS")
    if dfs_cost == best_cost:
        best_algorithms.append("DFS")
    if astar_cost == best_cost:
        best_algorithms.append("A*")

    print("Best path cost achieved by:", ", ".join(best_algorithms))

    best_nodes = min(bfs_expanded, dfs_expanded, astar_expanded)
    best_expansion = []
    if bfs_expanded == best_nodes:
        best_expansion.append("BFS")
    if dfs_expanded == best_nodes:
        best_expansion.append("DFS")
    if astar_expanded == best_nodes:
        best_expansion.append("A*")

    print("Fewest nodes expanded by:", ", ".join(best_expansion))