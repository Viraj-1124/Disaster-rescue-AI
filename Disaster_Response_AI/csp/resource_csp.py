from search.astar import astar
import config
"""
Resource Allocation CSP
-----------------------

Assign ambulances to victims under constraints.

AI Concepts Covered:
- Constraint Satisfaction Problem
- Variables
- Domains
- Constraints
"""
PRIORITY_WEIGHTS = {
    "HIGH": 100,
    "MEDIUM": 50,
    "LOW": 10
}

class ResourceCSP:

    def __init__(self, ambulances, victims, hospital_capacity, city_graph, engine=None):

        severity_order = {"critical":0, "moderate":1, "low":2}

        victims = sorted(victims, key=lambda v: severity_order[v["severity"]])

        self.variables = [v["id"] for v in victims]

        self.victims = {v["id"]:v for v in victims}
        self.ambulances = {a["id"]:a for a in ambulances}
        self.engine = engine

        self.domains = {
            v["id"]:list(self.ambulances.keys())
            for v in victims
        }

        self.city_graph = city_graph
        self.hospital_capacity = hospital_capacity

    def is_valid(self, assignment):

        used_ambulances = set()

        for victim_id, ambulance_id in assignment.items():

            if ambulance_id in used_ambulances:
                if config.DEBUG: print(f"DEBUG: Ambulance {ambulance_id} already used")  # Debug
                return False

            used_ambulances.add(ambulance_id)

            victim = self.victims[victim_id]
            ambulance = self.ambulances[ambulance_id]

            start = ambulance["location"]
            goal = victim["location"]

            path, dist1, _ = astar(self.city_graph, start, goal)
            path2, dist2, _ = astar(self.city_graph, goal, "HOSP")

            if path is None or path2 is None:
                if config.DEBUG: print(f"DEBUG: No path found: {start} -> {goal} or {goal} -> HOSP")  # Debug
                return False

            total_distance = dist1 + dist2

            # ================== AGENT LOGIC ==================
            if self.engine:
                decision = self.engine.evaluate_ambulance(ambulance, total_distance)

                if decision:
                    if decision.get("decision") == "REJECT_ASSIGNMENT":
                        if config.DEBUG: print(f"DEBUG: Agent rejected assignment: {decision}")  # Debug
                        return False
                    elif decision.get("action") == "REFUEL":
                        if config.DEBUG: print(f"DEBUG: Agent suggests refuel: {decision}")  # Debug
                        return False  # agent rejects this assignment
            # =================================================

            # fuel constraint (relaxed for planning - planning module handles refueling)
            # if not self.engine and total_distance > ambulance["fuel"]:
            #     return False

        if len(assignment) > self.hospital_capacity:
            if config.DEBUG: print(f"DEBUG: Exceeded hospital capacity: {len(assignment)} > {self.hospital_capacity}")  # Debug
            return False

        if config.DEBUG: print(f"DEBUG: Assignment is valid: {assignment}")  # Debug
        return True
    
    def calculate_score(self, assignment):

        total_score = 0

        for victim_id, ambulance_id in assignment.items():

            victim = self.victims[victim_id]
            ambulance = self.ambulances[ambulance_id]

            priority = victim.get("priority", "LOW")
            score = PRIORITY_WEIGHTS[priority]

            path1, dist1, _ = astar(self.city_graph, ambulance["location"], victim["location"])
            path2, dist2, _ = astar(self.city_graph, victim["location"], "HOSP")

            if path1 is None or path2 is None:
                total_distance = float('inf')
                score -= 10000  # heavy penalty
            else:
                total_distance = dist1 + dist2

            # reward closer rescues
            score -= total_distance

            total_score += score

        return total_score