from environment.city_graph import CityGraph
from search.bfs import bfs
from search.dfs import dfs
from evaluation.comparison import compare_uninformed


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

compare_uninformed(city, 'A', 'H')