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
class ResourceCSP:

    def __init__(self, ambulances, victims, hospital_capacity, city_graph):

        severity_order = {"critical":0, "moderate":1, "low":2}

        victims = sorted(victims, key=lambda v: severity_order[v["severity"]])

        self.variables = [v["id"] for v in victims]

        self.victims = {v["id"]:v for v in victims}
        self.ambulances = {a["id"]:a for a in ambulances}

        self.domains = {
            v["id"]:list(self.ambulances.keys())
            for v in victims
        }

        self.city_graph = city_graph
        self.hospital_capacity = hospital_capacity

    def is_valid(self, assignment):
        used_ambulances = set()
        for victim_id, ambulance_id in assignment.items():
            # prevent same ambulance rescuing multiple victims simultaneously
            if ambulance_id in used_ambulances:
                return False

            used_ambulances.add(ambulance_id)

            victim = self.victims[victim_id]
            ambulance = self.ambulances[ambulance_id]

            start = ambulance["location"]
            goal = victim["location"]

            path, distance, _ = astar(self.city_graph, start, goal)

            if path is None:
                return False

            # fuel constraint
            if distance > ambulance["fuel"]:
                return False

        # hospital capacity constraint
        if len(assignment) > self.hospital_capacity:
            return False

        return True