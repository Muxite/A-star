# by Muk Chunpongtong, based on tutorial by Sabastian Lague (for C#)
nodes = []  # this is the map. Each node is a class, open and closed hold pointers.
nodes_open = []
nodes_closed = []
start = []  # node to start at
target = []  # node to pathfind towards


# node class stores data
class Node:
    def __init__(self, location, f_cost, state):
        self.location = location
        self.f_cost = f_cost  # distance to target + distance to start
        self.state = state  # 0 base, 1 open, 2 closed


def a_star ():
    global nodes
    global nodes_open
    global nodes_closed
    global start
    global target
    nodes_open.append(start)

    # return the index of the lowest f_min
    def f_min_i(nodes_list):
        lowest = 99999999
        index = -1
        for j in range(len(nodes_list)):
            if nodes_list[j].f_cost < lowest:
                index = j
        return index

    # main loop
    for i in range(0, 10000):
        current = nodes_open[f_min_i(nodes_open)]  # current = lowest f_cost that is open
        nodes_open.remove(current)  # these are just pointers
        nodes_closed.append(current)
        if current.location == target.location:
            print("Pathfinding Finished")
            return
