import matplotlib
matplotlib.use("Agg")  

import streamlit as st
import random
import time

from environment.city_graph import CityGraph
from search.astar import astar
from search.bfs import bfs
from search.dfs import dfs
from logic.knowledge_base import KnowledgeBase
from logic.inference_engine import InferenceEngine
from planning.state import State
from planning.planner import generate_rescue_plan
from dynamic.events import add_new_victim, block_road, fuel_drop, unblock_road
from dynamic.monitor import validate_action
from csp.resource_csp import ResourceCSP
from csp.backtracking import backtracking_search
from visualization.graph_visualizer import GraphVisualizer
import config

st.set_page_config(page_title="AI Disaster Rescue", layout="wide")

def initialize_city(num_ambulances=3):
    city = CityGraph()
    kb = KnowledgeBase()
    engine = InferenceEngine()

    
    city.add_road('A','B',4)
    city.add_road('A','C',3)
    city.add_road('B','D',5)
    city.add_road('C','D',2)

    
    city.add_road('B','E',6)
    city.add_road('E','F',3)
    city.add_road('F','G',4)
    city.add_road('G','H',2)

    
    city.add_road('D','I',5)
    city.add_road('I','J',3)
    city.add_road('J','K',4)
    city.add_road('K','L',2)

    
    city.add_road('C','M',4)
    city.add_road('M','N',3)
    city.add_road('N','O',5)
    city.add_road('O','P',4)

    
    city.add_road('A','Q',6)
    city.add_road('Q','R',3)
    city.add_road('R','S',2)
    city.add_road('S','T',4)

    
    city.add_road('F','J',6)
    city.add_road('H','L',5)
    city.add_road('G','K',3)
    city.add_road('N','R',6)
    city.add_road('O','S',4)
    city.add_road('I','M',7)
    city.add_road('D','N',5)
    city.add_road('P','T',6)

    
    city.add_road('L','HOSP',3)
    city.add_road('T','HOSP',7)
    city.add_road('P','HOSP',6)

    
    FUEL_STATIONS = ['FUEL1', 'FUEL2', 'FUEL3']
    city.add_location('FUEL1')
    city.add_location('FUEL2') 
    city.add_location('FUEL3')

    city.add_road('A','FUEL1',2)
    city.add_road('M','FUEL2',3)
    city.add_road('Q','FUEL3',4)
    city.add_road('HOSP','FUEL1',5)

    city.set_coordinates('FUEL1', 0, 4)
    city.set_coordinates('FUEL2', 5, 0) 
    city.set_coordinates('FUEL3', -3, 4)

    
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

    city.block_road('F','J')
    city.block_road('D','I')
    city.block_road('N','O')

    locations = list(city.graph.keys())
    ambulances = []
    for i in range(1, num_ambulances + 1):
        ambulances.append({
            "id": f"A{i}",
            "location": random.choice(locations) if i > 3 else ["A", "M", "Q"][i-1],
            "fuel": random.randint(40, 60) if i > 3 else [50, 45, 40][i-1]
        })

    victims = [
        {"id":"V1","location":"G","severity":"critical"},
        {"id":"V2","location":"N","severity":"moderate"},
        {"id":"V3","location":"S","severity":"critical"},
        {"id":"V4","location":"K","severity":"moderate"},
        {"id":"V5","location":"O","severity":"critical"}
    ]

    kb.add_victims(victims)
    kb.add_ambulances(ambulances)

    return city, kb, engine, FUEL_STATIONS, ambulances, victims

st.title("🚑 AI Disaster Response Simulation")
st.markdown("A dynamic, intelligent rescue agent simulation using A*, Goal Stack Planning, and CSP.")

st.sidebar.header("Configuration")
config.MAX_ROUNDS = st.sidebar.slider("Max Rounds", 1, 20, 10)
config.MAX_TOTAL_VICTIMS = st.sidebar.slider("Max Victims", 5, 30, 15)
config.ANIMATION_SPEED = st.sidebar.slider("Animation Pause (sec)", 0.0, 2.0, 0.0, step=0.05)
config.SKIP_ANIMATION = st.sidebar.checkbox("Skip Step-by-step Animation (Fast)", False)
num_ambulances = st.sidebar.slider("Number of Ambulances", 1, 10, 3)

col1, col2 = st.columns([1, 1])

if st.button("Start Simulation", type="primary"):
    
    city, kb, engine, FUEL_STATIONS, ambulances, victims = initialize_city(num_ambulances)
    hospital_capacity = 10
    priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
    
    with st.spinner("Evaluating initial victims..."):
        st.subheader("Logical Agent Reasoning")
        reasoning_text = []
        for victim in victims:
            reasoning = engine.evaluate_victim(victim)
            victim.update(reasoning)
            reasoning_text.append(f"Victim {victim['id']} | Severity: {victim['severity']} | Priority: {victim['priority']}")
        victims.sort(key=lambda v: priority_order.get(v.get("priority", "LOW")))
        st.code("\n".join(reasoning_text), language="text")

        
        path_bfs, cost_bfs, exp_bfs = bfs(city, 'A', 'H')
        path_dfs, cost_dfs, exp_dfs = dfs(city, 'A', 'H')
        path_ast, cost_ast, exp_ast = astar(city, 'A', 'H')
        
        
    
    st.subheader("Visual Simulation")
    
    graph_container = st.empty()
    
    
    log_container = st.empty()
    log_text = []

    def log(msg):
        log_text.append(msg)
        
        display_text = "\n".join(log_text[-15:])
        log_container.code(display_text, language="text")

    visualizer = GraphVisualizer(city, "HOSP", pause_time=config.ANIMATION_SPEED, st_container=graph_container)
    visualizer.draw_state(ambulances, victims, title="Initial state")

    remaining_victims = victims.copy()
    round_number = 1
    rescue_summary = []

    log("Starting Disaster Rescue Simulation...")

    while remaining_victims and round_number <= config.MAX_ROUNDS:
        log(f"================ RESCUE ROUND {round_number} ================")
        
        from planning.actions import find_nearest_fuel_station
        active_ambulances = []
        for amb in ambulances:
            nearest = find_nearest_fuel_station(amb["location"], FUEL_STATIONS, city)
            path, dist, _ = astar(city, amb["location"], nearest)
            if path and amb["fuel"] >= dist:
                active_ambulances.append(amb)
            else:
                log(f"[!] Ambulance {amb['id']} is stranded at {amb['location']} with fuel {amb['fuel']} and out of service!")

        csp = ResourceCSP(active_ambulances, remaining_victims, hospital_capacity, city, engine)
        solution = backtracking_search(csp)

        if not solution:
            log("No further rescues possible due to fuel or constraints.")
            break

        rescued = list(solution.keys())
        pending = [v for v in remaining_victims if v["id"] not in rescued]

        log(f"Rescuable victims this round: {rescued}")
        if pending:
            log(f"Pending victims: {[v['id'] for v in pending]}")

        ambulance_data = {a["id"]: a for a in ambulances}
        victim_data = {v["id"]: v for v in remaining_victims}
        initial_state = State(ambulances, remaining_victims, "HOSP", FUEL_STATIONS)
        actually_rescued = []
        all_plans = {}

        for victim, ambulance in solution.items():
            v = victim_data[victim]
            a = ambulance_data[ambulance]
            log(f"--- Planning Rescue: Ambulance {ambulance} >> Victim {victim} ---")
            
            current_state = initial_state.copy()
            result = generate_rescue_plan(ambulance, victim, v["location"], current_state, city)
            if result:
                plan, full_path = result
                all_plans[ambulance] = {
                    "victim": victim,
                    "plan": plan,
                    "full_path": full_path,
                    "current_state": current_state,
                    "start_location": a['location']
                }
            else:
                log(f"[X] No plan could be generated for {ambulance} to rescue {victim}")

        if not all_plans:
            log("[X] No plans could be generated for any rescues")
            remaining_victims = [v for v in remaining_victims if v["id"] not in actually_rescued]
            round_number += 1
            continue

        victim_positions = {v["id"]: v["location"] for v in remaining_victims}
        ambulance_positions = {a["id"]: a["location"] for a in ambulances}
        carried_victims = {}
        delivered_victims = set()

        step_idx = 0
        while True:
            if not all_plans or all(step_idx >= len(data["plan"]) for data in all_plans.values()):
                break
                
            step_action_texts = []
            
            for amb_id, data in list(all_plans.items()):
                plan = data["plan"]
                vic_id = data["victim"]
                amb_state = data["current_state"]
                
                if step_idx < len(plan):
                    action = plan[step_idx]
                    if action is None:
                        continue
                    
                    valid, reason = validate_action(action, amb_state, city)
                    if not valid:
                        log(f"[!] Action failed for {amb_id}: {reason}. Replanning...")
                        result = generate_rescue_plan(amb_id, vic_id, victim_data[vic_id]["location"], amb_state.copy(), city)
                        if result:
                            new_plan, new_path = result
                            log(f"[OK] Replan successful for {amb_id}.")
                            padded_plan = [None] * step_idx + new_plan
                            all_plans[amb_id]["plan"] = padded_plan
                            all_plans[amb_id]["full_path"] = new_path
                            action = padded_plan[step_idx]
                            
                            valid, reason = validate_action(action, amb_state, city)
                            if not valid:
                                log(f"[X] Replanned action failed instantly. Aborting rescue.")
                                del all_plans[amb_id]
                                continue
                        else:
                            log(f"[X] Replanning failed to find valid path. Aborting rescue.")
                            del all_plans[amb_id]
                            continue
                    
                    amb_state.apply_action(action)
                    step_action_texts.append(f"{amb_id}: {action.name}")
                    
                    if action.name == "MOVE":
                        _, _, to_loc = action.parameters
                        ambulance_positions[amb_id] = to_loc
                        ambulance_data[amb_id]["location"] = to_loc
                        ambulance_data[amb_id]["fuel"] = min(config.MAX_FUEL, max(0, amb_state.ambulance_fuel.get(amb_id, 0)))
                        for amb in ambulances:
                            if amb["id"] == amb_id:
                                amb["location"] = to_loc
                                amb["fuel"] = ambulance_data[amb_id]["fuel"]
                                break
                    elif action.name == "PICK":
                        _, p_vic_id = action.parameters
                        carried_victims[p_vic_id] = amb_id
                        log(f"[OK] Ambulance {amb_id} picked up Victim {p_vic_id}")
                    elif action.name == "DROP":
                        _, d_vic_id = action.parameters
                        carried_victims.pop(d_vic_id, None)
                        delivered_victims.add(d_vic_id)
                        actually_rescued.append(d_vic_id)
                        log(f"[OK] Ambulance {amb_id} delivered Victim {d_vic_id} to hospital")
                        rescue_summary.append({
                            "victim": d_vic_id,
                            "ambulance": amb_id,
                            "plan_length": len(plan),
                            "full_path": " >> ".join(data.get("full_path", [])),
                            "fuel_remaining": ambulance_data[amb_id]["fuel"],
                            "refueled": any(act is not None and act.name == "REFUEL" for act in plan)
                        })
                    elif action.name == "REFUEL":
                        _, fuel_station = action.parameters
                        ambulance_positions[amb_id] = fuel_station
                        ambulance_data[amb_id]["fuel"] = config.MAX_FUEL
                        amb_state.ambulance_fuel[amb_id] = config.MAX_FUEL
                        for amb in ambulances:
                            if amb["id"] == amb_id:
                                amb["fuel"] = config.MAX_FUEL
                                break
                        log(f"[FUEL] Ambulance {amb_id} refueled at {fuel_station}")
            
            if step_action_texts:
                if not getattr(config, 'SKIP_ANIMATION', False):
                    visualizer.draw_step(ambulance_positions, victim_positions, carried_victims, delivered_victims, " | ".join(step_action_texts))
            
            
            if random.random() < 0.3:
                block_road(city)
            if random.random() < 0.15:
                unblock_road(city)
            if len(victims) < config.MAX_TOTAL_VICTIMS and random.random() < 0.2:
                new_victim = add_new_victim(remaining_victims, city, [v["id"] for v in victims])
                if new_victim:
                    victims.append(new_victim)
                    log(f"**NEW EVENT**: Victim {new_victim['id']} appeared at {new_victim['location']}!")
            if random.random() < 0.1:
                dropped_ambulance = random.choice(ambulances)
                fuel_drop(dropped_ambulance)
                d_amb_id = dropped_ambulance["id"]
                if d_amb_id in all_plans:
                    all_plans[d_amb_id]["current_state"].ambulance_fuel[d_amb_id] = dropped_ambulance["fuel"]
                ambulance_data[d_amb_id]["fuel"] = dropped_ambulance["fuel"]
                log(f"**NEW EVENT**: Ambulance {d_amb_id} suffered a fuel drop! Now at {dropped_ambulance['fuel']}")
                
            step_idx += 1

        remaining_victims = [v for v in remaining_victims if v["id"] not in actually_rescued]
        visualizer.draw_state(ambulances, remaining_victims, title=f"After round {round_number}")
        round_number += 1

    st.success("Simulation Complete.")
    
    st.subheader("Rescue Summary")
    summary_text = f"Total rescued victims: {len(rescue_summary)} / {len(victims)}\n"
    if rescue_summary:
        for item in rescue_summary:
            summary_text += f"\n  - Victim {item['victim']} rescued by Ambulance {item['ambulance']}\n"
            summary_text += f"      Path: {item['full_path']}\n"
            summary_text += f"      Plan length: {item['plan_length']} actions\n"
            summary_text += f"      Fuel remaining: {item['fuel_remaining']}\n"
            summary_text += f"      Refueled during rescue: {'Yes' if item['refueled'] else 'No'}\n"
    else:
        summary_text += "\nNo victims were rescued in this simulation.\n"

    if remaining_victims:
        summary_text += "\n========== PENDING VICTIMS ANALYSIS ==========\n"
        summary_text += f"Total pending: {len(remaining_victims)}\n"
        
        for v in remaining_victims:
            vic_loc = v['location']
            reachable = False
            closest_amb = None
            min_distance = float('inf')
            
            for amb in ambulances:
                path, distance, _ = astar(city, amb["location"], vic_loc)
                if path:
                    reachable = True
                    if distance < min_distance:
                        min_distance = distance
                        closest_amb = amb["id"]
            
            path_to_hosp, _, _ = astar(city, vic_loc, "HOSP")
            hosp_reachable = path_to_hosp is not None
            
            summary_text += f"\n  Victim {v['id']} (Severity: {v['severity']}, Priority: {v.get('priority', 'LOW')})\n"
            summary_text += f"      Location: {vic_loc}\n"
            
            if not reachable:
                summary_text += f"      Status: UNREACHABLE - No ambulance can reach this location\n"
            elif not hosp_reachable:
                summary_text += f"      Status: UNREACHABLE - Cannot reach hospital from victim location\n"
            elif closest_amb:
                summary_text += f"      Status: FUEL CONSTRAINT - Closest ambulance is {closest_amb} ({min_distance} distance away)\n"
                summary_text += f"                             All ambulances depleted fuel or reassigned to priority victims\n"
            else:
                summary_text += f"      Status: RESOURCE CONSTRAINT - No available ambulances\n"
                
    st.code(summary_text, language="text")
