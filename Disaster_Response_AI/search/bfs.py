

from collections import deque

def bfs(city_graph, start, goal):

    
    queue = deque()
    queue.append(start)

    
    visited = set()
    visited.add(start)

    
    parent = {start: None}

    
    nodes_expanded = 0

    
    
    
    while queue:
        current_node = queue.popleft()
        nodes_expanded += 1

        
        if current_node == goal:
            break

        
        for neighbor, _ in city_graph.get_neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)

    
    
    
    path = []
    path_cost = 0

    if goal not in parent:
        return None, float('inf'), nodes_expanded

    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    path.reverse()

    
    for i in range(len(path) - 1):
        path_cost += city_graph.graph[path[i]][path[i + 1]]

    return path, path_cost, nodes_expanded
