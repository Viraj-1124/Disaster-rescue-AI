# logic/rules.py

def rule_high_priority(victim):
    if victim["severity"] == "critical":
        return {"priority": "HIGH"}
    return None


def rule_medium_priority(victim):
    if victim["severity"] == "moderate":
        return {"priority": "MEDIUM"}
    return None


def rule_low_priority(victim):
    if victim["severity"] == "low":
        return {"priority": "LOW"}
    return None


def rule_need_refuel(ambulance, required_fuel):
    if ambulance["fuel"] < required_fuel:
        return {"action": "REFUEL"}
    return None


def rule_avoid_low_fuel(ambulance, required_distance):
    if ambulance["fuel"] < required_distance:
        return {"decision": "REJECT_ASSIGNMENT"}
    return None


def rule_refuel_needed(ambulance):
    if ambulance["fuel"] < 20:
        return {"action": "REFUEL"}
    return None