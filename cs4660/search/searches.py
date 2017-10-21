"""
Searches module defines all different search algorithms
"""
import math

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    queue.append((0, initial_node));
    d = {}
    d[initial_node] = 0
    p = {}
    e = {}

    while len(queue) > 0:
        pop = queue.pop()[1]

        for node in graph.neighbors(pop):
            if node not in d:
                e[node] = graph.distance(pop, node)
                d[node] = d[pop] + e[node].weight
                p[node] = pop

                if node != dest_node:
                    queue.append((d[node], node))

        queue = sorted(queue, key=lambda x:x[0])
        queue.reverse()

    path = []
    node = dest_node

    while node in p:
        path.append(e[node])
        node = p[node]

    path.reverse()

    return path

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    for node in graph.neighbors(initial_node):
        if node == dest_node:
            return [graph.distance(initial_node, dest_node)]
        else:
            path = dfs(graph, node, dest_node)
            if path != []:
                trans = [graph.distance(initial_node, node)]
                trans.extend(path)
                return trans
    return []

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    queue.append((0, initial_node))
    d = {}
    d[initial_node] = 0
    e = {}
    p = {}
    
    while len(queue) > 0:
        pop = queue.pop()[1]

        for neighbor in graph.neighbors(pop):
            edge = graph.distance(pop, neighbor)
            u = d[pop] + edge.weight

            if neighbor not in d or u < d[neighbor]:
              
                if neighbor in d:
                    queue.remove((d[neighbor], neighbor))
                
                queue.append((u, neighbor))

                d[neighbor] = u
                p[neighbor] = pop
                e[neighbor] = edge

       
        queue = sorted(queue, key=lambda x:x[0])
        queue.reverse()
    
    path = []
    node = dest_node

    while node in p:
        path.append(e[node])
        node = p[node]

    path.reverse()

    return path


def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    explored = []
    not_explored = [(0, initial_node)]
    p = {}
    e = {}

    g = {}
    g[initial_node] = 0

    f = {}
    f[initial_node] = heuristic(initial_node, dest_node)

    while len(not_explored) > 0:
        u = not_explored.pop()[1]
       
        if u == dest_node:
            
            current_node = u
            actions = []
            while current_node in p:
                actions.append(e[current_node])
                current_node = p[current_node]
            actions.reverse()
            return actions

      
    return []

def heuristic(initial_node, dest_node):
    dx = initial_node.data.x - dest_node.data.x
    dy = initial_node.data.y - dest_node.data.y
    return 2*math.sqrt(dx * dx + dy * dy)
