

class CityGraph:
    def __init__(self):
        
        
        self.graph = {}

        
        self.blocked_roads = set()

        self.coordinates = {}

    
    
    
    def add_location(self, location):

        if location not in self.graph:
            self.graph[location] = {}

    def add_road(self, from_node, to_node, cost):

        self.add_location(from_node)
        self.add_location(to_node)

        self.graph[from_node][to_node] = cost
        self.graph[to_node][from_node] = cost

    def set_coordinates(self, node, x, y):

        self.coordinates[node] = (x, y)

    
    
    
    def block_road(self, from_node, to_node):

        self.blocked_roads.add((from_node, to_node))
        self.blocked_roads.add((to_node, from_node))

    def unblock_road(self, from_node, to_node):

        self.blocked_roads.discard((from_node, to_node))
        self.blocked_roads.discard((to_node, from_node))

    def is_blocked(self, from_node, to_node):

        return (from_node, to_node) in self.blocked_roads

    
    
    
    def get_neighbors(self, node):

        neighbors = []
        if node not in self.graph:
            return neighbors

        for neighbor, cost in self.graph[node].items():
            if not self.is_blocked(node, neighbor):
                neighbors.append((neighbor, cost))

        return neighbors

    def get_distance(self, from_node, to_node):

        if from_node in self.graph and to_node in self.graph[from_node]:
            return self.graph[from_node][to_node]
        return None

    
    
    
    def display(self):

        print("City Graph:")
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")

        if self.blocked_roads:
            print("\nBlocked Roads:")
            for road in self.blocked_roads:
                print(f"{road[0]} <-> {road[1]}")
        else:
            print("\nNo blocked roads.")
