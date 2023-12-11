# by Muk Chunpongtong, based on tutorial by Sebastian Lague (for C#)
import math

dimensions = 2
nodes = []  # this is the map. Each node is a class, open and closed hold pointers.
nodes_open = []
nodes_closed = []
neighbours = []  # describes the neighbour locations
start = None  # node to start at
target = None  # node to pathfind towards


# calculate the distance between two points with as many dimensions
def distance(pi, pf):
    dim = len(pi)  # the number of dimensions to use
    adder = 0
    for i in range(len(pi)):
        adder += (pi[i]-pf[i])**2
    return round(adder**(1/2)*100)


def standard_neighbours(dim):
    # get neighbours for this number of dimensions
    delta = [-1, 0, 1]
    for i in range(len(delta) ** dim):
        neighbours.append([])

    # remove [0, 0] or [0, 0, 0]
    center = []
    for i in range(dim):
        center.append(0)

    for d in range(dim):
        for i in range(len(delta) ** dim):
            v = math.floor(i / (len(delta) ** d))
            neighbours[i].append(delta[v % len(delta)])
            # if finishing last dimension
            if d == dim-1:
                neighbours[i].append(distance(center, neighbours[i]))
    center.append(0)  # the distance to center is 0
    neighbours.remove(center)
    print(neighbours)


standard_neighbours(dimensions)


# node class stores data
class Node:
    def __init__(self, location, f_cost, state):
        self.location = location
        self.f_cost = f_cost  # distance to target + distance to start
        self.state = state  # 0 base, 1 open, 2 closed


def a_star():
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

        # stop if at the target
        if current.location == target.location:
            print("Pathfinding Finished")
            return

