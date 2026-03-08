from environment.city_graph import CityGraph
from search.bfs import bfs
from search.dfs import dfs
from search.dfs import dfs
from search.astar import astar
from evaluation.comparison import compare_uninformed
from csp.resource_csp import ResourceCSP
from csp.backtracking import backtracking_search


city = CityGraph()

city.add_road('A','B',4)
city.add_road('A','C',2)
city.add_road('B','D',3)
city.add_road('C','D',8)
city.add_road('C','E',2)
city.add_road('E','F',2)
city.add_road('F','H',2)
city.add_road('D','H',10)

city.set_coordinates('A',0,0)
city.set_coordinates('B',2,4)
city.set_coordinates('C',3,1)
city.set_coordinates('D',6,3)
city.set_coordinates('E',5,0)
city.set_coordinates('F',7,-1)
city.set_coordinates('H',9,0)

#city.block_road('C','E')
print("\nDisaster Update: Road C-E blocked due to debris")

ambulances = [
{"id":"A1","location":"A","fuel":10},
{"id":"A2","location":"C","fuel":8}
]

victims = [
    {"id": "V1", "location": "B", "severity": "critical"},
    {"id": "V2", "location": "D", "severity": "critical"},
    {"id": "V3", "location": "C", "severity": "moderate"}
]

hospital_capacity = 3

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