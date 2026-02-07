from environment.city_graph import CityGraph
from search.bfs import bfs

city = CityGraph()

city.add_road('A', 'B', 4)
city.add_road('A', 'C', 2)
city.add_road('B', 'D', 5)
city.add_road('C', 'D', 8)
city.add_road('D', 'H', 3)

path, cost, expanded = bfs(city, 'A', 'H')

print("BFS Path:", path)
print("Path Cost:", cost)
print("Nodes Expanded:", expanded)
