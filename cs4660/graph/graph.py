"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter


def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    input_file = open(file_path)

    nodes = int(input_file.readline())
    for i in range(0, nodes):
        graph.add_node(Node(i))

    for line in input_file:
        split_line = line.split(':')
        graph.add_edge(Edge(Node(int(split_line[0])), Node(int(split_line[1])), int(split_line[2])))

    return graph


class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)

    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)


class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == \
                                                                                                 other_node.weight

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        for edge in self.adjacency_list[node_1]:
            if edge.to_node == node_2:
                return True
        return False

    def neighbors(self, node):
        neighbors_list = []
        if node in self.adjacency_list:
            for x in self.adjacency_list[node]:
                neighbors_list.append(x.to_node)
        return neighbors_list

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        else:
            return False

    def remove_node(self, node):
        if node in self.adjacency_list:
            for x in self.adjacency_list.keys():
                key_value = self.adjacency_list[x]
                for y in key_value:
                    if y.to_node == node:
                        self.adjacency_list[x].remove(y)
            self.adjacency_list.pop(node)
            return True
        else:
            return False

    def add_edge(self, edge):
        for x in self.adjacency_list[edge.from_node]:
            if x == edge:
                return False
        if self.adjacency_list[edge.from_node] == {}:
            self.adjacency_list[edge.from_node] = edge
        else:
            self.adjacency_list[edge.from_node].append(edge)
        return True

    def remove_edge(self, edge):
        if edge.from_node in self.adjacency_list:
            if edge in self.adjacency_list[edge.from_node]:
                self.adjacency_list[edge.from_node].remove(edge)
                return True
            else:
                return False


class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if node_1 in self.nodes or node_2 in self.nodes:
            if self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)] != 0:
                return True
        return False

    def neighbors(self, node):
        neighbors_list = []
        if node in self.nodes:
            for x in range(0, len(self.adjacency_matrix[self.__get_node_index(node)])):
                if self.adjacency_matrix[self.__get_node_index(node)][x] > 0:
                    neighbors_list.append(self.nodes[x])
        return neighbors_list

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            self.adjacency_matrix.extend([[0] * len(self.nodes)])
            for eachRow in self.adjacency_matrix:
                eachRow.extend([0])
            return True
        return False

    def remove_node(self, node):
        if node in self.nodes:
            index = self.__get_node_index(node)
            self.nodes.remove(node)
            for x in self.adjacency_matrix:
                del x[index]
            del self.adjacency_matrix[index]
            return True
        return False

    def add_edge(self, edge):
        if self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] == 0:
            self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] = edge.weight
            return True
        return False

    def remove_edge(self, edge):
        if edge.from_node in self.nodes and edge.to_node in self.nodes:
            if self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] > 0:
                self.adjacency_matrix[self.__get_node_index(edge.from_node)][self.__get_node_index(edge.to_node)] = 0
                return True
        return False

    def __get_node_index(self, node):
        return self.nodes.index(node)


class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return True
        return False

    def neighbors(self, node):
        neighbors_list = []
        for x in range(len(self.edges)):
            if self.edges[x].from_node == node:
                neighbors_list.append(self.edges[x].to_node)
        return neighbors_list

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return True
        return False

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            for x in self.edges:
                if x.from_node == node or x.to_node == node:
                    self.remove_edge(x)
            return True
        return False

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)
            return True
        return False

    def remove_edge(self, edge):
        if edge not in self.edges:
            return False
        self.edges.remove(edge)
        return True
