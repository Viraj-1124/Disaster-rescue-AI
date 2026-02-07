"""
City Graph Representation
-------------------------
This module represents the disaster city as a weighted graph.

Nodes   : Locations in the city
Edges   : Roads with travel cost
Blocked : Roads that are unavailable due to disaster

AI Concepts Covered:
- Knowledge Representation
- State Space Representation
- Route Finding Problem
"""

class CityGraph:
    def __init__(self):
        # Adjacency list representation
        # Example: {'A': {'B': 4, 'C': 2}}
        self.graph = {}

        # Store blocked roads as tuples: ('A', 'B')
        self.blocked_roads = set()

    # -------------------------------
    # Graph Construction
    # -------------------------------
    def add_location(self, location):
        """Add a location (node) to the city graph."""
        if location not in self.graph:
            self.graph[location] = {}

    def add_road(self, from_node, to_node, cost):
        """
        Add a bidirectional road with travel cost.
        """
        self.add_location(from_node)
        self.add_location(to_node)

        self.graph[from_node][to_node] = cost
        self.graph[to_node][from_node] = cost

    # -------------------------------
    # Disaster Handling
    # -------------------------------
    def block_road(self, from_node, to_node):
        """Block a road due to disaster."""
        self.blocked_roads.add((from_node, to_node))
        self.blocked_roads.add((to_node, from_node))

    def unblock_road(self, from_node, to_node):
        """Unblock a previously blocked road."""
        self.blocked_roads.discard((from_node, to_node))
        self.blocked_roads.discard((to_node, from_node))

    def is_blocked(self, from_node, to_node):
        """Check if a road is blocked."""
        return (from_node, to_node) in self.blocked_roads

    # -------------------------------
    # Search Support Functions
    # -------------------------------
    def get_neighbors(self, node):
        """
        Return valid neighboring nodes (excluding blocked roads).
        """
        neighbors = []
        if node not in self.graph:
            return neighbors

        for neighbor, cost in self.graph[node].items():
            if not self.is_blocked(node, neighbor):
                neighbors.append((neighbor, cost))

        return neighbors

    # -------------------------------
    # Utility / Debug
    # -------------------------------
    def display(self):
        """Display the city graph."""
        print("City Graph:")
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")

        if self.blocked_roads:
            print("\nBlocked Roads:")
            for road in self.blocked_roads:
                print(f"{road[0]} <-> {road[1]}")
        else:
            print("\nNo blocked roads.")
