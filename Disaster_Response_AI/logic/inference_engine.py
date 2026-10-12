

from logic.rules import (
    rule_high_priority,
    rule_medium_priority,
    rule_low_priority,
    rule_need_refuel,
    rule_avoid_low_fuel
)

class InferenceEngine:
    def __init__(self):
        self.rules = [
            rule_high_priority,
            rule_medium_priority,
            rule_low_priority
        ]

    def evaluate_victim(self, victim):
        conclusions = {}

        for rule in self.rules:
            result = rule(victim)
            if result:
                conclusions.update(result)

        return conclusions

    def evaluate_ambulance(self, ambulance, required_fuel):
        
        refuel_decision = rule_need_refuel(ambulance, required_fuel)
        if refuel_decision:
            return refuel_decision
        
        
        
        
        
        
        return None