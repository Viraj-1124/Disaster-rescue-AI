import networkx as nx
import matplotlib.pyplot as plt
import config


class GraphVisualizer:
    """Persistent graph visualizer for rescue planning animation."""

    def __init__(self, city, hospital, pause_time=None, fuel_stations=None):
        self.city = city
        self.hospital = hospital
        self.fuel_stations = fuel_stations if fuel_stations is not None else [node for node in city.graph if str(node).upper().startswith("FUEL")]
        self.pause_time = pause_time if pause_time is not None else config.ANIMATION_SPEED
        self.pos = city.coordinates
        self.G = nx.Graph()
        self._build_graph()
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.ion()

    def _build_graph(self):
        self.G.clear()
        for node in self.city.graph:
            for neighbor, cost in self.city.graph[node].items():
                self.G.add_edge(node, neighbor, weight=cost)

    def draw_state(self, ambulances, victims, title="Current state"):
        self.ax.clear()

        normal_edges = []
        blocked_edges = []
        for u, v in self.G.edges():
            if self.city.is_blocked(u, v):
                blocked_edges.append((u, v))
            else:
                normal_edges.append((u, v))

        nx.draw_networkx_edges(self.G, self.pos, edgelist=normal_edges, width=2, ax=self.ax)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=blocked_edges,
                               edge_color="red", style="dashed", width=3, ax=self.ax)

        nx.draw_networkx_nodes(self.G, self.pos, node_color="lightblue", node_size=700, ax=self.ax)
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[self.hospital],
                               node_color="green", node_size=1200, ax=self.ax)

        if self.fuel_stations:
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.fuel_stations,
                                   node_color="blue", node_size=800, alpha=0.7, ax=self.ax)

        victim_locations = [v["location"] for v in victims]
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=victim_locations,
                               node_color="red", node_size=900, ax=self.ax)

        ambulance_positions = [a["location"] for a in ambulances]
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=ambulance_positions,
                               node_color="orange", node_size=1000, ax=self.ax)

        nx.draw_networkx_labels(self.G, self.pos, font_size=11, font_weight="bold", ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        self.ax.set_title(f"AI Disaster Rescue Simulation | {title}")
        self.ax.axis("off")

        self.fig.canvas.draw()
        plt.pause(self.pause_time)

    def animate_plan(self, ambulances, victims, plan, title="Plan animation"):
        victim_positions = {v["id"]: v["location"] for v in victims}
        ambulance_positions = {a["id"]: a["location"] for a in ambulances}
        carried_victims = {}
        delivered_victims = set()

        self.draw_state(ambulances, victims, title=f"{title} (start)")

        for action in plan:
            action_text = str(action)
            if action.name == "MOVE":
                amb_id, _, to_loc = action.parameters
                ambulance_positions[amb_id] = to_loc
            elif action.name == "PICK":
                _, vict_id = action.parameters
                carried_victims[vict_id] = action.parameters[0]
            elif action.name == "DROP":
                _, vict_id = action.parameters
                carried_victims.pop(vict_id, None)
                delivered_victims.add(vict_id)
            elif action.name == "REFUEL":
                amb_id, fuel_station = action.parameters
                ambulance_positions[amb_id] = fuel_station

            self.draw_step(ambulance_positions, victim_positions, carried_victims,
                            delivered_victims, action_text)

        self.draw_step(ambulance_positions, victim_positions, carried_victims,
                        delivered_victims, "Plan complete")

    def draw_step(self, ambulance_positions, victim_positions, carried_victims, delivered_victims, action_text):
        self.ax.clear()

        normal_edges = []
        blocked_edges = []
        for u, v in self.G.edges():
            if self.city.is_blocked(u, v):
                blocked_edges.append((u, v))
            else:
                normal_edges.append((u, v))

        nx.draw_networkx_edges(self.G, self.pos, edgelist=normal_edges, width=2, ax=self.ax)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=blocked_edges,
                               edge_color="red", style="dashed", width=3, ax=self.ax)

        nx.draw_networkx_nodes(self.G, self.pos, node_color="lightblue", node_size=700, ax=self.ax)
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[self.hospital],
                               node_color="green", node_size=1200, ax=self.ax)

        if self.fuel_stations:
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.fuel_stations,
                                   node_color="blue", node_size=800, alpha=0.7, ax=self.ax)

        waiting_victims = [loc for vid, loc in victim_positions.items()
                           if vid not in carried_victims and vid not in delivered_victims]
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=waiting_victims,
                               node_color="red", node_size=900, ax=self.ax)

        carried_positions = [ambulance_positions[amb_id] for amb_id in set(carried_victims.values())]
        if carried_positions:
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=carried_positions,
                                   node_color="yellow", node_size=900, ax=self.ax)

        ambulance_positions_list = list(ambulance_positions.values())
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=ambulance_positions_list,
                               node_color="orange", node_size=1000, ax=self.ax)

        nx.draw_networkx_labels(self.G, self.pos, font_size=11, font_weight="bold", ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        self.ax.set_title(f"AI Disaster Rescue Simulation | {action_text}")
        self.ax.axis("off")

        self.fig.canvas.draw()
        plt.pause(self.pause_time)

    def show(self):
        plt.ioff()
        plt.show(block=True)


def visualize_city(*args, **kwargs):
    visualizer = GraphVisualizer(args[0], args[3], pause_time=kwargs.get('pause_time', config.ANIMATION_SPEED))
    if kwargs.get('plan'):
        visualizer.animate_plan(args[1], args[2], kwargs.get('plan'))
    else:
        visualizer.draw_state(args[1], args[2])
    if kwargs.get('block', True):
        visualizer.show()
    return visualizer
