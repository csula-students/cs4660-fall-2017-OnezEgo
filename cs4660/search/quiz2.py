"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

def bfs(start, end):
    queue = []
    queue.append((0, start));
    e = {}
    d = {}
    d[start] = 0
    p = {}

    while len(queue) > 0:
        pop = get_state(queue.pop()[1])
        neighbors = pop['neighbors']
        for x in range(len(neighbors)):
            next_n = neighbors[x]
            if next_n['id'] not in d:
                edge = transition_state(pop['id'], next_n['id'])
                e[next_n['id']] = edge
                d[next_n['id']] = d[pop['id']] + 1
                p[next_n['id']] = pop['id']
                if next_n['id'] != end:
                    queue.append((d[next_n['id']], next_n['id']))
        queue = sorted(queue, key=lambda x: x[0])
        queue.reverse()
    path = []
    node = end
    while node in p:
        path.append(e[node])
        node = p[node]
    path.reverse()
    print("\nBFS:")
    last, hp_tot = start, 0
    for x in range(len(path)):
        node, get_id = get_state(last), path[x]['id']
        hp_tot += path[x]['event']['effect']
        print("%s(%s):%s(%s):%i" % (node['location']['name'], last, path[x]['action'], path[x]['id'], path[x]['event']['effect']))
        last = get_id
    print("Total HP: %i" % hp_tot)

def dijkstra(start, end):
    queue = []
    visited = []
    queue.append((0, start))
    d = {}
    d[start] = 0
    p = {}
    e = {}

    while len(queue) > 0:
        pop = get_state(queue.pop()[1])
        visited.append(pop['id'])
        neighbors = pop['neighbors']

        for x in range(len(neighbors)):
            next_n = neighbors[x]
            edge = transition_state(pop['id'], next_n['id'])
            v = d[pop['id']] + edge['event']['effect']
            if next_n['id'] not in visited and (next_n['id'] not in d or v > d[next_n['id']]):
                if next_n['id'] in d:
                    queue.remove((d[next_n['id']], next_n['id']))
                queue.append((v, next_n['id']))
                d[next_n['id']] = v
                p[next_n['id']] = pop['id']
                e[next_n['id']] = edge
        queue = sorted(queue, key=lambda x: x[0])
    path = []
    node = end
    while node in p:
        path.append(e[node])
        node = p[node]
    path.reverse()
    print("\nDijkstra:")
    last, hp_tot = start, 0
    for x in range(len(path)):
        node, get_id = get_state(last), path[x]['id']
        hp_tot += path[x]['event']['effect']
        print("%s(%s):%s(%s):%i" % (node['location']['name'], last, path[x]['action'], path[x]['id'], path[x]['event']['effect']))
        last = get_id
    print("Total HP: %i" % hp_tot)

if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')
    print("May take a second to print results")
    bfs(empty_room['id'], dark_room['id'])
    dijkstra(empty_room['id'], dark_room['id'])