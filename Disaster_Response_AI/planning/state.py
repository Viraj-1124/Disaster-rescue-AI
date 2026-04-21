"""
State Representation for Classical Planning
===========================================

Represents the world state for the disaster response planning system.

AI Concepts:
- State representation in classical planning
- Initial state and goal state
"""
import config

class State:
    """
    Represents the current state of the disaster response world.
    
    State includes:
    - Ambulance locations and fuel levels
    - Victim statuses (waiting, picked, delivered)
    - Hospital status
    - Fuel stations
    """
    
    def __init__(self, ambulances, victims, hospital="HOSP", fuel_stations=None):
        """
        Initialize state from ambulance and victim data.
        
        Args:
            ambulances: List of ambulance dictionaries
            victims: List of victim dictionaries  
            hospital: Hospital location name
            fuel_stations: List of fuel station location names
        """
        self.ambulance_locations = {a["id"]: a["location"] for a in ambulances}
        self.ambulance_fuel = {a["id"]: a["fuel"] for a in ambulances}
        self.victim_status = {v["id"]: "waiting" for v in victims}
        self.victim_locations = {v["id"]: v["location"] for v in victims}
        self.hospital = hospital
        self.fuel_stations = fuel_stations or []
        
        # Track which ambulance has which victim (for picked status)
        self.ambulance_victim = {a["id"]: None for a in ambulances}
    
    def copy(self):
        """Create a deep copy of the state."""
        import copy
        return copy.deepcopy(self)
    
    def is_goal(self, goal_conditions):
        """
        Check if current state satisfies goal conditions.
        
        Args:
            goal_conditions: Dict of conditions to check
                e.g., {"victim_delivered": ["V1"], "ambulance_at": {"A1": "HOSP"}}
        
        Returns:
            bool: True if all conditions satisfied
        """
        if "victim_delivered" in goal_conditions:
            for victim_id in goal_conditions["victim_delivered"]:
                if self.victim_status.get(victim_id) != "delivered":
                    return False
        
        if "ambulance_at" in goal_conditions:
            for ambulance_id, location in goal_conditions["ambulance_at"].items():
                if self.ambulance_locations.get(ambulance_id) != location:
                    return False
        
        return True
    
    def apply_action(self, action):
        """
        Apply an action's effects to the state.
        
        Args:
            action: Action object with add_effects and delete_effects
        """
        # Apply delete effects first
        for effect in action.delete_effects:
            self._apply_effect(effect, delete=True)
        
        # Apply add effects
        for effect in action.add_effects:
            self._apply_effect(effect, delete=False)
    
    def _apply_effect(self, effect, delete=False):
        """Apply a single effect to the state."""
        effect_type, *params = effect
        
        if effect_type == "at":
            ambulance_id, location = params
            if delete:
                # Remove location (not typical)
                pass
            else:
                self.ambulance_locations[ambulance_id] = location
        
        elif effect_type == "picked":
            victim_id, ambulance_id = params
            if delete:
                self.victim_status[victim_id] = "waiting"
                self.ambulance_victim[ambulance_id] = None
            else:
                self.victim_status[victim_id] = "picked"
                self.ambulance_victim[ambulance_id] = victim_id
        
        elif effect_type == "delivered":
            victim_id = params[0]
            if delete:
                self.victim_status[victim_id] = "picked"
            else:
                self.victim_status[victim_id] = "delivered"
                # Find which ambulance had this victim
                for amb_id, vic_id in self.ambulance_victim.items():
                    if vic_id == victim_id:
                        self.ambulance_victim[amb_id] = None
                        break
        
        elif effect_type == "fuel":
            ambulance_id, fuel_level = params
            if delete:
                pass  # Not typical
            else:
                self.ambulance_fuel[ambulance_id] = min(config.MAX_FUEL, max(0, fuel_level))

        elif effect_type == "fuel_change":
            ambulance_id, fuel_delta = params
            if delete:
                pass  # Not typical
            else:
                self.ambulance_fuel[ambulance_id] = min(config.MAX_FUEL, max(0, self.ambulance_fuel.get(ambulance_id, 0) + fuel_delta))
    
    def check_precondition(self, precondition):
        """Check if a precondition is satisfied in current state."""
        pred_type, *params = precondition
        
        if pred_type == "at":
            ambulance_id, location = params
            return self.ambulance_locations.get(ambulance_id) == location
        
        elif pred_type == "adjacent":
            loc1, loc2 = params
            # This would need city graph - we'll check in action validation
            return True  # Placeholder
        
        elif pred_type == "victim_waiting":
            victim_id = params[0]
            return self.victim_status.get(victim_id) == "waiting"
        
        elif pred_type == "victim_picked":
            victim_id, ambulance_id = params
            return (self.victim_status.get(victim_id) == "picked" and 
                   self.ambulance_victim.get(ambulance_id) == victim_id)
        
        elif pred_type == "at_hospital":
            ambulance_id = params[0]
            return self.ambulance_locations.get(ambulance_id) == self.hospital
        
        elif pred_type == "at_fuel_station":
            ambulance_id = params[0]
            return self.ambulance_locations.get(ambulance_id) in self.fuel_stations
        
        elif pred_type == "fuel_sufficient":
            ambulance_id, required_fuel = params
            return self.ambulance_fuel.get(ambulance_id, 0) >= required_fuel
        
        return False
    
    def __str__(self):
        """String representation for debugging."""
        return f"""State:
Ambulance locations: {self.ambulance_locations}
Ambulance fuel: {self.ambulance_fuel}
Victim status: {self.victim_status}
Ambulance victims: {self.ambulance_victim}"""