

import config
from search.astar import astar

class Action:

    
    def __init__(self, name, parameters, preconditions, add_effects, delete_effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.delete_effects = delete_effects
    
    def __str__(self):
        return f"{self.name}({', '.join(self.parameters)})"
    
    def __repr__(self):
        return self.__str__()

def create_move_action(ambulance_id, from_loc, to_loc, distance):

    return Action(
        name="MOVE",
        parameters=[ambulance_id, from_loc, to_loc],
        preconditions=[
            ("at", ambulance_id, from_loc),
            ("adjacent", from_loc, to_loc),
            ("fuel_sufficient", ambulance_id, distance)
        ],
        add_effects=[
            ("at", ambulance_id, to_loc),
            ("fuel_change", ambulance_id, -distance)
        ],
        delete_effects=[
            ("at", ambulance_id, from_loc)
        ]
    )

def create_pick_action(ambulance_id, victim_id, location):

    return Action(
        name="PICK",
        parameters=[ambulance_id, victim_id],
        preconditions=[
            ("at", ambulance_id, location),
            ("victim_waiting", victim_id)
        ],
        add_effects=[
            ("picked", victim_id, ambulance_id)
        ],
        delete_effects=[
            ("victim_waiting", victim_id)
        ]
    )

def create_drop_action(ambulance_id, victim_id, hospital):

    return Action(
        name="DROP",
        parameters=[ambulance_id, victim_id],
        preconditions=[
            ("at", ambulance_id, hospital),
            ("victim_picked", victim_id, ambulance_id)
        ],
        add_effects=[
            ("delivered", victim_id)
        ],
        delete_effects=[
            ("picked", victim_id, ambulance_id)
        ]
    )

def create_refuel_action(ambulance_id, fuel_station):

    return Action(
        name="REFUEL",
        parameters=[ambulance_id, fuel_station],
        preconditions=[
            ("at", ambulance_id, fuel_station)
        ],
        add_effects=[
            ("fuel", ambulance_id, config.MAX_FUEL)  
        ],
        delete_effects=[]  
    )

def generate_move_actions(ambulance_id, current_loc, path, city_graph, current_fuel, fuel_stations):

    actions = []
    fuel = current_fuel
    def path_length(p):
        from search.astar import astar
        return sum((city_graph.get_distance(p[k], p[k+1]) or 1) for k in range(len(p)-1)) if p else 0

    current_path = path.copy()
    
    while len(current_path) > 1:
        from_loc = current_path[0]
        to_loc = current_path[1]
        
        distance = city_graph.get_distance(from_loc, to_loc) or 1
        
        
        
        
        if fuel < path_length(current_path) + 15:
            
            nearest_fuel = find_nearest_fuel_station(from_loc, fuel_stations, city_graph)
            if nearest_fuel and nearest_fuel != from_loc:
                fuel_path, f_cost, _ = astar(city_graph, from_loc, nearest_fuel)
                if fuel_path and fuel >= f_cost:
                    
                    for j in range(len(fuel_path) - 1):
                        f_from = fuel_path[j]
                        f_to = fuel_path[j + 1]
                        f_dist = city_graph.get_distance(f_from, f_to) or 1
                        actions.append(create_move_action(ambulance_id, f_from, f_to, f_dist))
                        fuel -= f_dist
                    
                    
                    actions.append(create_refuel_action(ambulance_id, nearest_fuel))
                    fuel = config.MAX_FUEL  
                    
                    
                    final_dest = current_path[-1]
                    new_path, _, _ = astar(city_graph, nearest_fuel, final_dest)
                    if new_path:
                        current_path = new_path
                        continue
        
        
        actions.append(create_move_action(ambulance_id, from_loc, to_loc, distance))
        fuel -= distance
        current_path.pop(0)
    
    return actions

def find_nearest_fuel_station(current_loc, fuel_stations, city_graph):

    min_distance = float('inf')
    nearest = None
    
    for station in fuel_stations:
        path, distance, _ = astar(city_graph, current_loc, station)
        if path and distance < min_distance:
            min_distance = distance
            nearest = station
    
    return nearest