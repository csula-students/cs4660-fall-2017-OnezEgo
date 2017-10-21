"""
utils package is for some quick utility methods

such as parsing
"""

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph

    f = open(file_path, encoding='utf-8')
    lines = f.readlines()
    previous = []
    rows = len(lines)-2
    for x in range(rows):
        line = lines[x+1]
        y = 1
        current_row = []
        while y < len(line)-3:
            z = int((y-1)/2)
            node = Node(Tile(z, x, line[y:y+2]))
            graph.add_node(node)
            y+=2
            
            if node.data.symbol != "##":

                if node.data.x > 0:
                    previous_node = current_row[-1]
                    if previous_node.data.symbol != "##":
                        graph.add_edge(Edge(previous_node, node, 1))
                        graph.add_edge(Edge(node, previous_node, 1))

                if node.data.y > 0:
                    previous_node = previous[z]
                    if previous_node.data.symbol != "##":
                        graph.add_edge(Edge(previous_node, node, 1))
                        graph.add_edge(Edge(node, previous_node, 1))

            current_row.append(node)

        previous = current_row

    f.close()
    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    path = []
    for e in edges:
        if e.to_node.data.x - e.from_node.data.x > 0:
            path.append("E")
        elif e.to_node.data.x - e.from_node.data.x < 0:
            path.append("W")
        elif e.to_node.data.y - e.from_node.data.y < 0:
            path.append("N")
        elif e.to_node.data.y - e.from_node.data.y > 0:
            path.append("S")
    return "".join(path)
