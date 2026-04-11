from environment.city_graph import CityGraph
from search.bfs import bfs
from search.dfs import dfs
from search.astar import astar
from evaluation.comparison import compare_uninformed
from csp.resource_csp import ResourceCSP
from csp.backtracking import backtracking_search
from visualization.graph_visualizer import GraphVisualizer
from logic.knowledge_base import KnowledgeBase
from logic.inference_engine import InferenceEngine
from planning.state import State
from planning.planner import GoalStackPlanner, generate_rescue_plan


city = CityGraph()
# CITY ROAD NETWORK (25 NODES)
kb = KnowledgeBase()

engine = InferenceEngine()

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

# FUEL STATIONS - Add fuel stations at strategic locations
FUEL_STATIONS = ['FUEL1', 'FUEL2', 'FUEL3']
city.add_location('FUEL1')
city.add_location('FUEL2') 
city.add_location('FUEL3')

# Connect fuel stations to city
city.add_road('A','FUEL1',2)      # Central fuel station
city.add_road('M','FUEL2',3)      # South fuel station  
city.add_road('Q','FUEL3',4)      # West fuel station
city.add_road('HOSP','FUEL1',5)   # Hospital connected to central fuel

# Set coordinates for fuel stations
city.set_coordinates('FUEL1', 0, 4)
city.set_coordinates('FUEL2', 5, 0) 
city.set_coordinates('FUEL3', -3, 4)


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

ambulances = [
{"id":"A1","location":"A","fuel":120},  # Low but sufficient for some paths
{"id":"A2","location":"M","fuel":100},  # Low fuel
{"id":"A3","location":"Q","fuel":800}    # Very low fuel
]

victims = [
{"id":"V1","location":"G","severity":"critical"},
{"id":"V2","location":"N","severity":"moderate"},
{"id":"V3","location":"S","severity":"critical"},
{"id":"V4","location":"K","severity":"moderate"},
{"id":"V5","location":"O","severity":"critical"}
]

hospital_capacity = 10
kb.add_victims(victims)
kb.add_ambulances(ambulances)
# ================= LOGICAL AGENT EXECUTION =================

print("\n========== LOGICAL AGENT REASONING ==========")

priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}

for victim in victims:
    reasoning = engine.evaluate_victim(victim)
    victim.update(reasoning)

    print(f"Victim {victim['id']} → Severity: {victim['severity']} → Priority: {victim['priority']}")

# Sort victims based on priority BEFORE CSP
victims.sort(key=lambda v: priority_order.get(v.get("priority", "LOW")))

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
csp = ResourceCSP(ambulances, victims, hospital_capacity, city, engine)
remaining_victims = victims.copy()
round_number = 1
rescue_summary = []

print("\nStarting Disaster Rescue Simulation...")
visualizer = GraphVisualizer(city, "HOSP", pause_time=0.6)
visualizer.draw_state(ambulances, victims, title="Initial state")
while remaining_victims:

    print(f"\n================ RESCUE ROUND {round_number} ================")

    csp = ResourceCSP(ambulances, remaining_victims, hospital_capacity, city, engine)
    solution = backtracking_search(csp)
    
    print(f"DEBUG: CSP found solution: {solution}")  # Debug output

    if not solution:
        print("No further rescues possible due to fuel or constraints.")
        break

    rescued = list(solution.keys())
    pending = [v for v in remaining_victims if v["id"] not in rescued]

    print("\n========== RESCUE ASSIGNMENT ==========")
    print("Rescuable victims:", rescued)

    if pending:
        print("Pending victims:", [v["id"] for v in pending])

    print("\n========== RESCUE DECISION EXPLANATION ==========")

    ambulance_data = {a["id"]: a for a in ambulances}
    victim_data = {v["id"]: v for v in remaining_victims}

    # Create initial state for planning
    initial_state = State(ambulances, remaining_victims, "HOSP", FUEL_STATIONS)

    # Track actually rescued victims
    actually_rescued = []

    for victim, ambulance in solution.items():

        v = victim_data[victim]
        a = ambulance_data[ambulance]

        print(f"\n--- Planning Rescue for Ambulance {ambulance} → Victim {victim} ---")
        print(f"Severity: {v['severity']}, Location: {v['location']}")
        print(f"Ambulance Location: {a['location']}, Fuel: {a['fuel']}")

        start_location = a['location']

        # Generate rescue plan using Goal Stack Planning
        plan = generate_rescue_plan(ambulance, victim, v["location"], initial_state, city)

        if plan:
            print(f"Generated Plan ({len(plan)} actions):")
            for i, action in enumerate(plan, 1):
                print(f"  {i}. {action}")

            print("\nAnimating Plan on map...")
            visualizer.animate_plan(ambulances, remaining_victims, plan, title=f"Rescue plan for {victim} by {ambulance}")
            
            # Execute the plan step by step
            print("\nExecuting Plan:")
            current_state = initial_state.copy()
            plan_successful = True
            
            for action in plan:
                print(f"  Executing: {action}")
                
                # Check if action is valid in current state
                preconditions_met = all(current_state.check_precondition(precond) 
                                      for precond in action.preconditions)
                
                if not preconditions_met:
                    print(f"    ❌ Precondition failed for {action}")
                    plan_successful = False
                    break
                
                # Apply action effects
                current_state.apply_action(action)
                
                # Update actual ambulance data
                if action.name == "MOVE":
                    amb_id, _, to_loc = action.parameters
                    ambulance_data[amb_id]["location"] = to_loc
                    # Fuel consumption
                    distance = city.get_distance(action.parameters[1], to_loc) or 1
                    ambulance_data[amb_id]["fuel"] = max(0, ambulance_data[amb_id]["fuel"] - distance)
                
                elif action.name == "PICK":
                    amb_id, vic_id = action.parameters
                    print(f"    ✅ Ambulance {amb_id} picked up Victim {vic_id}")
                
                elif action.name == "DROP":
                    amb_id, vic_id = action.parameters
                    print(f"    ✅ Ambulance {amb_id} delivered Victim {vic_id} to hospital")
                    actually_rescued.append(vic_id)
                    rescue_summary.append({
                        "victim": vic_id,
                        "ambulance": amb_id,
                        "plan_length": len(plan),
                        "final_location": ambulance_data[amb_id]["location"],
                        "start_location": start_location,
                        "fuel_remaining": ambulance_data[amb_id]["fuel"],
                        "refueled": any(act.name == "REFUEL" for act in plan)
                    })
                
                elif action.name == "REFUEL":
                    amb_id, fuel_station = action.parameters
                    ambulance_data[amb_id]["fuel"] = 100  # Max fuel
                    print(f"    ⛽ Ambulance {amb_id} refueled at {fuel_station}")
            
            if plan_successful:
                # Update initial state for next planning
                initial_state = current_state
            else:
                print("    ❌ Plan execution failed")
        
        else:
            print("❌ No plan could be generated for this rescue")
    
    # Update remaining victims - only remove actually rescued ones
    remaining_victims = [v for v in remaining_victims if v["id"] not in actually_rescued]
    visualizer.draw_state(ambulances, remaining_victims, title=f"After round {round_number}")

    # remove rescued victims
    remaining_victims = pending

    round_number += 1

print("\n========== FINAL VERDICT ==========")
if rescue_summary:
    print(f"Total rescued victims: {len(rescue_summary)} / {len(victims)}")
    for item in rescue_summary:
        print(f"  - Victim {item['victim']} rescued by Ambulance {item['ambulance']}")
        print(f"      Plan length: {item['plan_length']} actions")
        print(f"      Start: {item['start_location']} → End: {item['final_location']}")
        print(f"      Fuel remaining: {item['fuel_remaining']}")
        print(f"      Refueled during rescue: {'Yes' if item['refueled'] else 'No'}")
else:
    print("No victims were rescued in this simulation.")

print("\nOverall strategy:")
print("  - Logical Agent: priority-based victim scoring")
print("  - CSP Assignment: ambulance-to-victim matching")
print("  - Planning: stepwise MOVE, PICK, DROP actions")
print("  - Path search: A* for MOVE action routing")
print("  - Fuel management: refueling planned when needed")

if remaining_victims:
    print("\nPending victims due to limited resources:")
    for victim in remaining_victims:
        reasoning = engine.evaluate_victim(victim)
        victim.update(reasoning)

    remaining_victims.sort(key=lambda v: priority_order.get(v.get("priority", "LOW")))

    for v in remaining_victims:
        print(f"\nVictim {v['id']}")
        print("Severity:", v["severity"])
        print("Reason: insufficient fuel or unreachable location")