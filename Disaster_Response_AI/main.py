from environment.city_graph import CityGraph
from search.bfs import bfs
from search.dfs import dfs
from search.dfs import dfs
from search.astar import astar
from evaluation.comparison import compare_uninformed
from csp.resource_csp import ResourceCSP
from csp.backtracking import backtracking_search


city = CityGraph()

city.add_road('A', 'B', 4)
city.add_road('A', 'C', 2)
city.add_road('B', 'D', 5)
city.add_road('C', 'D', 8)
city.add_road('D', 'H', 3)

city.set_coordinates('A', 0, 0)
city.set_coordinates('B', 2, 4)
city.set_coordinates('C', 3, 1)
city.set_coordinates('D', 6, 3)
city.set_coordinates('H', 8, 2)

ambulances = [
    {"id": "A1", "location": "A"},
    {"id": "A2", "location": "C"}
]

victims = [
    {"id": "V1", "location": "B", "severity": "critical"},
    {"id": "V2", "location": "D", "severity": "moderate"},
    {"id": "V3", "location": "C", "severity": "critical"},
]

hospital_capacity = 2

print("\n--- BFS Result ---")
path, cost, expanded = bfs(city, 'A', 'H')
print("BFS Path:", path)
print("Path Cost:", cost)
print("Nodes Expanded:", expanded)

print("\n--- DFS Result ---")
path, cost, expanded = dfs(city, 'A', 'H')
print("DFS Path:", path)
print("Path Cost:", cost)
print("Nodes Expanded:", expanded)

print("\n--- A* Result ---")
path, cost, expanded = astar(city, 'A', 'H')
print("A* Path:", path)
print("Path Cost:", cost)
print("Nodes Expanded:", expanded)

compare_uninformed(city, 'A', 'H')
csp = ResourceCSP(ambulances, victims, hospital_capacity)

solution = backtracking_search(csp)

print("\n========== CSP RESOURCE ALLOCATION ==========")
print("Assignment:", solution)