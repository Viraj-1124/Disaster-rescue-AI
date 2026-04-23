import random


def block_road(city_graph):
    """Block a random active road in the city graph."""
    active_edges = []
    for node, neighbors in city_graph.graph.items():
        for neighbor in neighbors:
            if node < neighbor and not city_graph.is_blocked(node, neighbor):
                active_edges.append((node, neighbor))

    if not active_edges:
        print("[EVENT] No active road available to block.")
        return None

    road = random.choice(active_edges)
    city_graph.block_road(*road)
    print(f"[EVENT] Road blocked between {road[0]} and {road[1]} due to disaster.")
    return road


def unblock_road(city_graph):
    """Unblock a random blocked road in the city graph."""
    blocked_edges = []
    for u, v in city_graph.blocked_roads:
        if u < v:
            blocked_edges.append((u, v))

    if not blocked_edges:
        print("[EVENT] No blocked road available to restore.")
        return None

    road = random.choice(blocked_edges)
    city_graph.unblock_road(*road)
    print(f"[EVENT] Road restored between {road[0]} and {road[1]}.")
    return road


def add_new_victim(victims, city_graph, existing_victim_ids=None):
    """Add a new victim dynamically to the simulation."""
    if existing_victim_ids is None:
        existing_victim_ids = [victim["id"] for victim in victims]
    existing_ids = set(existing_victim_ids)

    new_id = 1
    while f"V{new_id}" in existing_ids:
        new_id += 1

    locations = [node for node in city_graph.graph if node != "HOSP" and not str(node).startswith("FUEL")]
    if not locations:
        print("[EVENT] No valid location available for a new victim.")
        return None

    location = random.choice(locations)
    severity = random.choices(["critical", "moderate", "low"], weights=[3, 2, 1], k=1)[0]
    new_victim = {"id": f"V{new_id}", "location": location, "severity": severity}
    victims.append(new_victim)

    print(f"[EVENT] New victim {new_victim['id']} appeared at {location} (severity={severity}).")
    return new_victim


def fuel_drop(ambulance):
    """Simulate sudden fuel loss for an ambulance."""
    current_fuel = ambulance.get("fuel", 0)
    if current_fuel <= 0:
        print(f"[EVENT] Ambulance {ambulance['id']} already has no fuel.")
        return 0

    loss = random.randint(2, 5)
    ambulance["fuel"] = max(0, current_fuel - loss)
    print(f"[EVENT] Ambulance {ambulance['id']} lost {loss} fuel due to an emergency event. Remaining fuel: {ambulance['fuel']}.")
    return ambulance["fuel"]
