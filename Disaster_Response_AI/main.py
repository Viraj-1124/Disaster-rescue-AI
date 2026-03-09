from environment.city_graph import CityGraph
from search.bfs import bfs
from search.dfs import dfs
from search.dfs import dfs
from search.astar import astar
from evaluation.comparison import compare_uninformed
from csp.resource_csp import ResourceCSP
from csp.backtracking import backtracking_search
from visualization.graph_visualizer import visualize_city_graph


city = CityGraph()
# CITY ROAD NETWORK (25 NODES)

# Central Area
city.add_road('A','B',4)
city.add_road('A','C',3)
city.add_road('B','D',5)
city.add_road('C','D',2)

# North Area
city.add_road('B','E',6)
city.add_road('E','F',3)
city.add_road('F','G',4)
city.add_road('G','H',2)

# East Area
city.add_road('D','I',5)
city.add_road('I','J',3)
city.add_road('J','K',4)
city.add_road('K','L',2)

# South Area
city.add_road('C','M',4)
city.add_road('M','N',3)
city.add_road('N','O',5)
city.add_road('O','P',4)

# West Area
city.add_road('A','Q',6)
city.add_road('Q','R',3)
city.add_road('R','S',2)
city.add_road('S','T',4)

# Cross Connections 
city.add_road('F','J',6)
city.add_road('H','L',5)
city.add_road('G','K',3)
city.add_road('N','R',6)
city.add_road('O','S',4)
city.add_road('I','M',7)
city.add_road('D','N',5)
city.add_road('P','T',6)

# Hospital
city.add_road('L','HOSP',3)
city.add_road('T','HOSP',7)
city.add_road('P','HOSP',6)


# CITY COORDINATES
city.set_coordinates('A',0,5)
city.set_coordinates('B',2,7)
city.set_coordinates('C',2,3)
city.set_coordinates('D',5,5)

city.set_coordinates('E',3,9)
city.set_coordinates('F',5,10)
city.set_coordinates('G',7,9)
city.set_coordinates('H',9,9)

city.set_coordinates('I',7,5)
city.set_coordinates('J',9,5)
city.set_coordinates('K',11,5)
city.set_coordinates('L',13,5)

city.set_coordinates('M',5,2)
city.set_coordinates('N',7,1)
city.set_coordinates('O',9,1)
city.set_coordinates('P',11,1)

city.set_coordinates('Q',-2,5)
city.set_coordinates('R',-4,4)
city.set_coordinates('S',-6,3)
city.set_coordinates('T',-8,2)

city.set_coordinates('HOSP',12,3)

#city.block_road('C','E')
city.block_road('F','J')
city.block_road('D','I')
city.block_road('N','O')
print("\nDisaster Update: Road C-E blocked due to debris")

ambulances = [
{"id":"A1","location":"A","fuel":20},
{"id":"A2","location":"M","fuel":15},
{"id":"A3","location":"Q","fuel":18}
]

victims = [
{"id":"V1","location":"G","severity":"critical"},
{"id":"V2","location":"N","severity":"moderate"},
{"id":"V3","location":"S","severity":"critical"},
{"id":"V4","location":"K","severity":"moderate"},
{"id":"V5","location":"O","severity":"critical"}
]

hospital_capacity = 10
visualize_city_graph(city)

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
csp = ResourceCSP(ambulances,victims,hospital_capacity,city)
solution = backtracking_search(csp)

print("\n========== RESCUE ASSIGNMENT ==========")
if not solution:
    print("No victims can be rescued with current constraints.")
else:
    rescued = list(solution.keys())
    all_victims = [v["id"] for v in victims]
    pending = [v for v in all_victims if v not in rescued]
    print("Rescuable victims:", rescued)
    if pending:
        print("Pending victims:", pending)


print("\n========== RESCUE DECISION EXPLANATION ==========")
ambulance_data = {a["id"]:a for a in ambulances}
victim_data = {v["id"]:v for v in victims}

for victim, ambulance in solution.items():
    v = victim_data[victim]
    a = ambulance_data[ambulance]
    path, dist, _ = astar(city,a["location"],v["location"])

    print(f"\nAmbulance {ambulance} assigned to Victim {victim}")
    print(f"Severity: {v['severity']}")
    print(f"Distance to victim: {dist}")
    print(f"Fuel available: {a['fuel']}")
    print(f"Chosen path: {path}")


rescued = set(solution.keys())
all_victims = set(victim_data.keys())
pending = all_victims - rescued

if pending:
    print("\nPending victims due to limited resources:")
    for v in pending:
        victim = victim_data[v]
        print(f"Victim {v}")
        print("Severity:", victim["severity"])
        print("Reason: insufficient ambulances or fuel constraint")