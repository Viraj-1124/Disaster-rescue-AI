"""
Goal Stack Planner for Classical Planning
=========================================

Implements Goal Stack Planning (GSP) for generating action sequences.

AI Concepts:
- Classical Planning
- Goal Stack Planning
- STRIPS representation
- Plan generation
"""

from .state import State
from .actions import Action, create_move_action, create_pick_action, create_drop_action, create_refuel_action, generate_move_actions


class GoalStackPlanner:
    """
    Goal Stack Planning implementation.
    
    Uses a stack to manage goals and subgoals, working backwards from goals
    to find applicable actions.
    """
    
    def __init__(self, city_graph, max_depth=50):
        """
        Initialize the planner.
        
        Args:
            city_graph: City graph for pathfinding
            max_depth: Maximum planning depth to prevent infinite loops
        """
        self.city_graph = city_graph
        self.max_depth = max_depth
    
    def plan(self, initial_state, goal_conditions, available_actions=None):
        """
        Generate a plan using Goal Stack Planning.
        
        Args:
            initial_state: State object representing initial world state
            goal_conditions: Dict of goal conditions
            available_actions: List of possible actions (optional)
        
        Returns:
            List of Action objects representing the plan, or None if no plan found
        """
        if initial_state.is_goal(goal_conditions):
            return []  # Already at goal
        
        # Initialize goal stack with goal conditions
        goal_stack = self._conditions_to_goals(goal_conditions)
        
        # Planning state
        current_state = initial_state.copy()
        plan = []
        depth = 0
        
        while goal_stack and depth < self.max_depth:
            depth += 1
            
            current_goal = goal_stack[-1]  # Top of stack
            
            if self._goal_achieved(current_goal, current_state):
                # Goal achieved, pop it
                goal_stack.pop()
                continue
            
            # Try to find an action that achieves this goal
            action = self._find_action_for_goal(current_goal, current_state, available_actions)
            
            if action:
                # Add action to plan
                plan.append(action)
                
                # Apply action effects to current state
                current_state.apply_action(action)
                
                # Add action preconditions as new subgoals
                for precondition in reversed(action.preconditions):
                    if not self._goal_achieved(precondition, current_state):
                        goal_stack.append(precondition)
            else:
                # No action found - backtrack
                if plan:
                    last_action = plan.pop()
                    # Undo action effects (simplified)
                    current_state = initial_state.copy()
                    # Re-apply all previous actions
                    for a in plan:
                        current_state.apply_action(a)
                else:
                    # No plan possible
                    return None
        
        if goal_stack:
            # Goals not achieved
            return None
        
        return plan
    
    def _conditions_to_goals(self, goal_conditions):
        """Convert goal conditions dict to list of goal predicates."""
        goals = []
        
        if "victim_delivered" in goal_conditions:
            for victim_id in goal_conditions["victim_delivered"]:
                goals.append(("delivered", victim_id))
        
        if "ambulance_at" in goal_conditions:
            for ambulance_id, location in goal_conditions["ambulance_at"].items():
                goals.append(("at", ambulance_id, location))
        
        return goals
    
    def _goal_achieved(self, goal, state):
        """Check if a goal is achieved in the current state."""
        return state.check_precondition(goal)
    
    def _find_action_for_goal(self, goal, state, available_actions):
        """
        Find an action that achieves the given goal.
        
        This is a simplified version - in full GSP, we'd try different actions.
        """
        goal_type, *params = goal
        
        if goal_type == "at":
            # MOVE action
            ambulance_id, target_loc = params
            current_loc = state.ambulance_locations.get(ambulance_id)
            if current_loc and current_loc != target_loc:
                # Find path
                path = self._find_path(current_loc, target_loc)
                if path and len(path) > 1:
                    # Create move action for first step
                    distance = self.city_graph.get_distance(path[0], path[1])
                    if distance is None:
                        distance = 1
                    return create_move_action(ambulance_id, path[0], path[1], distance)
        
        elif goal_type == "picked":
            # PICK action
            victim_id, ambulance_id = params
            victim_loc = self._get_victim_location(victim_id)
            ambulance_loc = state.ambulance_locations.get(ambulance_id)
            if victim_loc and ambulance_loc == victim_loc:
                return create_pick_action(ambulance_id, victim_id, victim_loc)
        
        elif goal_type == "delivered":
            # DROP action
            victim_id = params[0]
            # Find which ambulance has this victim
            for amb_id, vic_id in state.ambulance_victim.items():
                if vic_id == victim_id:
                    hospital = state.hospital
                    ambulance_loc = state.ambulance_locations.get(amb_id)
                    if ambulance_loc == hospital:
                        return create_drop_action(amb_id, victim_id, hospital)
                    break
        
        return None
    
    def _find_path(self, start, goal):
        """Find a path between two locations using A*."""
        from search.astar import astar
        path, _, _ = astar(self.city_graph, start, goal)
        return path
    
    def _get_victim_location(self, victim_id):
        """Get victim's location."""
        return self.victim_locations.get(victim_id, "UNKNOWN")


def generate_rescue_plan(ambulance_id, victim_id, victim_location, initial_state, city_graph):
    """
    Generate a complete rescue plan for an ambulance-victim assignment.
    
    This is a simplified planner that generates actions in sequence:
    1. MOVE to victim location (with refueling if needed)
    2. PICK victim
    3. MOVE to hospital (with refueling if needed)
    4. DROP victim
    
    Args:
        ambulance_id: ID of assigned ambulance
        victim_id: ID of victim to rescue
        victim_location: Location of the victim
        initial_state: Initial State object
        city_graph: City graph
    
    Returns:
        List of Action objects for the complete rescue
    """
    from .actions import generate_move_actions, create_pick_action, create_drop_action
    
    plan = []
    current_ambulance_loc = initial_state.ambulance_locations[ambulance_id]
    current_fuel = initial_state.ambulance_fuel[ambulance_id]
    
    # 1. Generate MOVE actions to victim location (with refueling)
    if current_ambulance_loc != victim_location:
        from search.astar import astar
        path_to_victim, _, _ = astar(city_graph, current_ambulance_loc, victim_location)
        if path_to_victim:
            move_actions = generate_move_actions(ambulance_id, current_ambulance_loc, path_to_victim, 
                                               city_graph, current_fuel, initial_state.fuel_stations)
            plan.extend(move_actions)
            # Update fuel for next segment (simplified)
            current_fuel = 100  # Assume refueled if needed
    
    # 2. PICK action
    pick_action = create_pick_action(ambulance_id, victim_id, victim_location)
    plan.append(pick_action)
    
    # 3. Generate MOVE actions to hospital (with refueling)
    hospital = initial_state.hospital
    if victim_location != hospital:
        from search.astar import astar
        path_to_hospital, _, _ = astar(city_graph, victim_location, hospital)
        if path_to_hospital:
            move_actions = generate_move_actions(ambulance_id, victim_location, path_to_hospital, 
                                               city_graph, current_fuel, initial_state.fuel_stations)
            plan.extend(move_actions)
    
    # 4. DROP action
    drop_action = create_drop_action(ambulance_id, victim_id, hospital)
    plan.append(drop_action)
    
    return plan