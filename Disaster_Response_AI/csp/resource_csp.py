from search.astar import astar
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
                return False

            used_ambulances.add(ambulance_id)

            victim = self.victims[victim_id]
            ambulance = self.ambulances[ambulance_id]

            start = ambulance["location"]
            goal = victim["location"]

            path, dist1, _ = astar(self.city_graph, start, goal)
            path2, dist2, _ = astar(self.city_graph, goal, "HOSP")

            if path is None or path2 is None:
                return False

            total_distance = dist1 + dist2

            # ================== AGENT LOGIC ==================
            if self.engine:
                decision = self.engine.evaluate_ambulance(ambulance, total_distance)

                if decision and decision.get("action") == "REFUEL":
                    return False  # agent rejects this assignment
            # =================================================

            # fuel constraint (fallback if no agent logic)
            if not self.engine and total_distance > ambulance["fuel"]:
                return False

        if len(assignment) > self.hospital_capacity:
            return False

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

            total_distance = dist1 + dist2

            # reward closer rescues
            score -= total_distance

            total_score += score

        return total_score