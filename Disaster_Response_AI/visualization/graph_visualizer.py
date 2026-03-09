import networkx as nx
import matplotlib.pyplot as plt


def visualize_city_graph(city):
    """
    Visualize the city graph using NetworkX.
    """

    G = nx.Graph()

    # Add edges with cost
    for node in city.graph:
        for neighbor, cost in city.graph[node].items():
            G.add_edge(node, neighbor, weight=cost)

    # Use coordinates if available
    pos = city.coordinates if city.coordinates else nx.spring_layout(G)

    # Separate blocked edges
    blocked_edges = list(city.blocked_roads)
    normal_edges = [e for e in G.edges if e not in blocked_edges]

    plt.figure(figsize=(10, 8))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color="skyblue")

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, width=2)

    # Draw blocked edges
    if blocked_edges:
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=blocked_edges,
            edge_color="red",
            style="dashed",
            width=2
        )

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Disaster Response City Graph")
    plt.axis("off")
    plt.show()