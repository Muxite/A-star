# by Muk Chunpongtong, based on tutorial by Sebastian Lague (for C#)
import math

dimensions = 2
nodes = []  # this is the map. Each node is a class, open and closed hold pointers.
nodes_open = []
nodes_closed = []
neighbours = []  # describes the neighbour locations and distance as the last one
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
    def __init__(self, location, state, g_cost, h_cost):
        self.location = location  # x, y, maybe z
        self.g_cost = g_cost  # distance to start
        self.h_cost = h_cost  # distance to target
        self.state = state  # 0 base, 1 open, 2 closed
        self.parent = None  # will set this later


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
            if nodes_list[j].g_cost + nodes_list[j].h_cost < lowest:
                index = j
        return index

    # main loop
    for i in range(0, 10000):
        # except for the first loop
        if i == 0:
            if dimensions == 2:
                current = nodes[start[0]][start[1]]
            elif dimensions == 3:
                current = nodes[start[0]][start[1]][start[2]]
        else:
            current = nodes_open[f_min_i(nodes_open)]  # current = lowest f_cost that is open
        nodes_open.remove(current)  # these are just pointers
        nodes_closed.append(current)

        # stop if at the target
        if current.location == target:
            print("Pathfinding Finished")
            return

        # for neighbours of current
        for j in range(len(neighbours)):
            neighbour = current  # this will change
            try:
                n_location = current.location + neighbours[j]
                if dimensions == 2:
                    neighbour = nodes[n_location[0]][n_location[1]]
                elif dimensions == 3:
                    neighbour = nodes[n_location[0]][n_location[1]][n_location[2]]
            except IndexError:
                j += 1  # skip to next neighbour
            if neighbour is not current:
                # if not closed
                if neighbour.state != 2:
                    # add the previous g_cost with the distance from it to this neighbour cell
                    path_length = current.g_cost + neighbours[i][dimensions]
                    if path_length < neighbour.g_cost or neighbour.state != 1:
                        # update f_cost
                        neighbour.g_cost = path_length
                        neighbour.h_cost = distance(neighbour.location, target)
                        # set the parent to retrace steps later
                        neighbour.parent = current
                        if neighbour not in nodes_open:
                            nodes_open.append(neighbour)
