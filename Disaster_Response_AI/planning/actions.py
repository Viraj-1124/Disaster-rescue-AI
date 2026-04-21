"""
Action Definitions for Classical Planning
=========================================

Defines STRIPS-style actions for the disaster response system.

AI Concepts:
- STRIPS representation
- Actions with preconditions and effects
- Add and delete lists
"""

import config
from search.astar import astar

class Action:
    """
    Represents a STRIPS action.
    
    Each action has:
    - name: String identifier
    - parameters: List of parameters
    - preconditions: List of conditions that must be true
    - add_effects: List of facts to add to state
    - delete_effects: List of facts to remove from state
    """
    
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


# MOVE Action
def create_move_action(ambulance_id, from_loc, to_loc, distance):
    """
    Create a MOVE action for an ambulance.
    
    Preconditions:
    - Ambulance is at from_loc
    - Road exists between from_loc and to_loc
    - Sufficient fuel for the move
    
    Effects:
    - Ambulance location changes to to_loc
    - Fuel decreases by distance
    """
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


# PICK Action
def create_pick_action(ambulance_id, victim_id, location):
    """
    Create a PICK action for picking up a victim.
    
    Preconditions:
    - Ambulance and victim are at same location
    - Victim is waiting (not already picked)
    
    Effects:
    - Victim status becomes picked
    - Ambulance has the victim
    """
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


# DROP Action
def create_drop_action(ambulance_id, victim_id, hospital):
    """
    Create a DROP action for delivering victim to hospital.
    
    Preconditions:
    - Ambulance is at hospital
    - Ambulance has the victim picked
    
    Effects:
    - Victim status becomes delivered
    - Ambulance no longer has the victim
    """
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


# REFUEL Action
def create_refuel_action(ambulance_id, fuel_station):
    """
    Create a REFUEL action for refueling an ambulance.
    
    Preconditions:
    - Ambulance is at fuel station
    
    Effects:
    - Fuel is restored to maximum
    """
    return Action(
        name="REFUEL",
        parameters=[ambulance_id, fuel_station],
        preconditions=[
            ("at", ambulance_id, fuel_station)
        ],
        add_effects=[
            ("fuel", ambulance_id, config.MAX_FUEL)  # Restore to max fuel
        ],
        delete_effects=[]  # No delete effects for refuel
    )


def generate_move_actions(ambulance_id, current_loc, path, city_graph, current_fuel, fuel_stations):
    """
    Generate a sequence of MOVE actions along a path, inserting REFUEL actions when fuel is low.
    
    Args:
        ambulance_id: ID of the ambulance
        current_loc: Starting location
        path: List of locations in the path
        city_graph: City graph for distance calculation
        current_fuel: Current fuel level of ambulance
        fuel_stations: List of fuel station locations
    
    Returns:
        List of Action objects (MOVE and REFUEL)
    """
    actions = []
    fuel = current_fuel
    
    for i in range(len(path) - 1):
        from_loc = path[i]
        to_loc = path[i + 1]
        
        # Calculate distance
        distance = city_graph.get_distance(from_loc, to_loc)
        if distance is None:
            distance = 1  # Default if no weight
        
        # Check if we have enough fuel for this move
        if fuel < distance:
            # Need to refuel - find nearest fuel station
            nearest_fuel = find_nearest_fuel_station(from_loc, fuel_stations, city_graph)
            if nearest_fuel:
                # Generate moves to fuel station
                fuel_path, _, _ = astar(city_graph, from_loc, nearest_fuel)
                if fuel_path:
                    for j in range(len(fuel_path) - 1):
                        f_from = fuel_path[j]
                        f_to = fuel_path[j + 1]
                        f_dist = city_graph.get_distance(f_from, f_to) or 1
                        actions.append(create_move_action(ambulance_id, f_from, f_to, f_dist))
                    
                    # Add refuel action
                    actions.append(create_refuel_action(ambulance_id, nearest_fuel))
                    fuel = config.MAX_FUEL  # Refueled
        
        # Add the original move
        actions.append(create_move_action(ambulance_id, from_loc, to_loc, distance))
        fuel -= distance
    
    return actions


def find_nearest_fuel_station(current_loc, fuel_stations, city_graph):
    """
    Find the nearest fuel station from current location.
    
    Args:
        current_loc: Current location
        fuel_stations: List of fuel station locations
        city_graph: City graph
    
    Returns:
        Nearest fuel station location or None
    """
    min_distance = float('inf')
    nearest = None
    
    for station in fuel_stations:
        path, distance, _ = astar(city_graph, current_loc, station)
        if path and distance < min_distance:
            min_distance = distance
            nearest = station
    
    return nearest