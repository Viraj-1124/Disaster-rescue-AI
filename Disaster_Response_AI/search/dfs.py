

def dfs(city_graph, start, goal):

    
    stack = []
    stack.append(start)

    visited = set()
    parent = {start: None}

    nodes_expanded = 0

    while stack:
        current_node = stack.pop()

        if current_node not in visited:
            visited.add(current_node)
            nodes_expanded += 1

            
            if current_node == goal:
                break

            
            
            neighbors = city_graph.get_neighbors(current_node)
            neighbors.reverse()

            for neighbor, _ in neighbors:
                if neighbor not in visited:
                    parent[neighbor] = current_node
                    stack.append(neighbor)

    
    
    
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