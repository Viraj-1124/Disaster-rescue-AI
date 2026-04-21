"""Execution monitoring helpers for dynamic disaster response."""


def is_move_valid(action, city_graph):
    if action.name != "MOVE":
        return True

    _, from_loc, to_loc = action.parameters
    distance = city_graph.get_distance(from_loc, to_loc)
    if distance is None:
        return False

    return not city_graph.is_blocked(from_loc, to_loc)


def is_fuel_sufficient(ambulance, required_distance):
    return ambulance.get("fuel", 0) >= required_distance


def validate_action(action, state, city_graph):
    if action.name == "MOVE":
        ambulance_id, from_loc, to_loc = action.parameters

        if state.ambulance_locations.get(ambulance_id) != from_loc:
            return False, f"Ambulance {ambulance_id} is not at {from_loc}."

        if not is_move_valid(action, city_graph):
            return False, f"Road from {from_loc} to {to_loc} is blocked or unavailable."

        required_distance = city_graph.get_distance(from_loc, to_loc) or 1
        current_fuel = state.ambulance_fuel.get(ambulance_id, 0)
        if not is_fuel_sufficient({"fuel": current_fuel}, required_distance):
            return False, f"Ambulance {ambulance_id} does not have enough fuel for move ({current_fuel} < {required_distance})."

        return True, "MOVE valid"

    if action.name == "PICK":
        ambulance_id, victim_id = action.parameters
        victim_location = state.victim_locations.get(victim_id)
        ambulance_location = state.ambulance_locations.get(ambulance_id)

        if victim_location is None:
            return False, f"Victim {victim_id} location unknown."
        if ambulance_location != victim_location:
            return False, f"Ambulance {ambulance_id} is not at victim {victim_id} location."
        if not state.check_precondition(("victim_waiting", victim_id)):
            return False, f"Victim {victim_id} is not waiting."

        return True, "PICK valid"

    if action.name == "DROP":
        ambulance_id, victim_id = action.parameters
        if not state.check_precondition(("at_hospital", ambulance_id)):
            return False, f"Ambulance {ambulance_id} is not at the hospital."
        if not state.check_precondition(("victim_picked", victim_id, ambulance_id)):
            return False, f"Victim {victim_id} is not picked by ambulance {ambulance_id}."

        return True, "DROP valid"

    if action.name == "REFUEL":
        ambulance_id, fuel_station = action.parameters
        if state.ambulance_locations.get(ambulance_id) != fuel_station:
            return False, f"Ambulance {ambulance_id} is not at {fuel_station}."
        if fuel_station not in state.fuel_stations:
            return False, f"{fuel_station} is not a recognized fuel station."

        return True, "REFUEL valid"

    return False, f"Unknown action {action.name}."
