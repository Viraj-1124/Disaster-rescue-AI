import networkx as nx
import matplotlib.pyplot as plt
import time


def visualize_city(city, ambulances, victims, hospital, assignments=None):

    G = nx.Graph()

    for node in city.graph:
        for neighbor, cost in city.graph[node].items():
            G.add_edge(node, neighbor, weight=cost)

    pos = city.coordinates

    victim_nodes = [v["location"] for v in victims]
    ambulance_lookup = {a["id"]: a for a in ambulances}
    victim_lookup = {v["id"]: v for v in victims}

    plt.ion()
    fig, ax = plt.subplots(figsize=(12,8))

    def draw_base(ambulance_positions=None):

        ax.clear()

        # normal edges
        normal_edges = []
        blocked_edges = []

        for u,v in G.edges():
            if city.is_blocked(u,v):
                blocked_edges.append((u,v))
            else:
                normal_edges.append((u,v))

        nx.draw_networkx_edges(G,pos,edgelist=normal_edges,width=2,ax=ax)
        nx.draw_networkx_edges(G,pos,edgelist=blocked_edges,
                               edge_color="red",style="dashed",width=3,ax=ax)

        nx.draw_networkx_nodes(G,pos,node_color="lightblue",node_size=700,ax=ax)

        # hospital
        nx.draw_networkx_nodes(G,pos,nodelist=[hospital],
                               node_color="green",node_size=1200,ax=ax)

        # victims
        nx.draw_networkx_nodes(G,pos,nodelist=victim_nodes,
                               node_color="red",node_size=900,ax=ax)

        # ambulances
        if ambulance_positions:
            nx.draw_networkx_nodes(G,pos,nodelist=ambulance_positions,
                                   node_color="orange",node_size=1000,ax=ax)

        nx.draw_networkx_labels(G,pos,font_size=11,font_weight="bold",ax=ax)

        edge_labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,ax=ax)

        ax.set_title("AI Disaster Rescue Simulation")
        ax.axis("off")

        plt.draw()
        plt.pause(0.5)

    # initial state
    draw_base([a["location"] for a in ambulances])

    if not assignments:
        return

    from search.astar import astar

    for victim_id, ambulance_id in assignments.items():

        ambulance = ambulance_lookup[ambulance_id]
        victim = victim_lookup[victim_id]

        # path ambulance -> victim
        path1, _, _ = astar(city, ambulance["location"], victim["location"])

        # path victim -> hospital
        path2, _, _ = astar(city, victim["location"], hospital)

        full_path = path1 + path2[1:]

        current_pos = ambulance["location"]

        for step in full_path:

            current_pos = step

            draw_base([current_pos])

            time.sleep(0.6)

        ambulance["location"] = hospital

    plt.ioff()
    plt.show()