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

    def __init__(self, ambulances, victims, hospital_capacity):

        # Variables = victims
        self.variables = [v["id"] for v in victims]

        # Domains = ambulances that can rescue
        self.domains = {
            v["id"]: [a["id"] for a in ambulances]
            for v in victims
        }

        self.ambulances = ambulances
        self.victims = victims
        self.hospital_capacity = hospital_capacity


    # ------------------------------
    # Constraint Checking
    # ------------------------------

    def is_valid(self, assignment):
        """
        Check if assignment satisfies constraints.

        assignment example:
        {
            V1 : A1,
            V2 : A2
        }
        """

        # Constraint 1:
        # One ambulance cannot rescue multiple victims simultaneously

        used_ambulances = set()

        for victim, ambulance in assignment.items():

            if ambulance in used_ambulances:
                return False

            used_ambulances.add(ambulance)

        # Constraint 2:
        # Hospital capacity

        if len(assignment) > self.hospital_capacity:
            return False

        return True