

from .state import State
from .actions import Action, create_move_action, create_pick_action, create_drop_action, create_refuel_action, generate_move_actions
import config

def generate_rescue_plan(ambulance_id, victim_id, victim_location, initial_state, city_graph):

    from .actions import generate_move_actions, create_pick_action, create_drop_action
    from search.astar import astar
    
    plan = []
    full_path = []  
    current_ambulance_loc = initial_state.ambulance_locations[ambulance_id]
    current_fuel = initial_state.ambulance_fuel[ambulance_id]
    refuel_count = 0
    
    
    path_to_victim = None
    already_picked = (initial_state.ambulance_victim.get(ambulance_id) == victim_id)
    
    if already_picked:
        full_path.append(current_ambulance_loc)
        victim_location = current_ambulance_loc 
    elif current_ambulance_loc != victim_location:
        path_to_victim, path_cost, _ = astar(city_graph, current_ambulance_loc, victim_location)
        if path_to_victim:
            full_path.extend(path_to_victim)  
            move_actions = generate_move_actions(ambulance_id, current_ambulance_loc, path_to_victim, 
                                               city_graph, current_fuel, initial_state.fuel_stations)
            plan.extend(move_actions)
            
            
            refuel_count += sum(1 for a in move_actions if a.name == "REFUEL")
            
            
            if refuel_count > 0:
                current_fuel = config.MAX_FUEL
            else:
                current_fuel = max(0, min(config.MAX_FUEL, current_fuel - path_cost))
    else:
        full_path.append(current_ambulance_loc)
    
    
    if not already_picked:
        pick_action = create_pick_action(ambulance_id, victim_id, victim_location)
        plan.append(pick_action)
    
    
    hospital = initial_state.hospital
    if victim_location != hospital:
        path_to_hospital, path_cost, _ = astar(city_graph, victim_location, hospital)
        if path_to_hospital:
            
            if len(path_to_hospital) > 1:
                full_path.extend(path_to_hospital[1:])
            
            move_actions = generate_move_actions(ambulance_id, victim_location, path_to_hospital, 
                                               city_graph, current_fuel, initial_state.fuel_stations)
            plan.extend(move_actions)
            
            
            refuel_count += sum(1 for a in move_actions if a.name == "REFUEL")
            
            
            if refuel_count > 0:
                current_fuel = config.MAX_FUEL
            else:
                current_fuel = max(0, min(config.MAX_FUEL, current_fuel - path_cost))
    else:
        if not full_path or full_path[-1] != hospital:
            full_path.append(hospital)
    
    
    drop_action = create_drop_action(ambulance_id, victim_id, hospital)
    plan.append(drop_action)
    
    return plan, full_path