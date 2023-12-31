# by Muk Chunpongtong, based on tutorial by Sebastian Lague (for C#)
# uses a straight-line heuristic
import math
from PIL import Image

image_path = 'D:\Github\A-star\TestMap.png'
dimensions = 2
nodes = []  # this is the map. Each node is a class, open and closed hold pointers.
nodes_open = []
nodes_closed = []
neighbours = []  # describes the neighbour locations and distance as the last one
start = [0, 0]  # node to start at (positions are lists for now)
target = [7, 7]  # node to pathfind towards


# produce a 2d node map from an image
def image_to_nodes(path, walkable_color, unwalkable_color):
    image = Image.open(path)
    pixels = image.load()
    width, height = image.size
    node_map = []
    closed_nodes = []
    for y in range(height):
        node_map.append([])
        for x in range(width):
            if pixels[x, y] == walkable_color:
                node_map[y].append(Node([x, y], 0, -1, -1))
            elif pixels[x, y] == unwalkable_color:
                node_map[y].append(Node([x, y], 2, -1, -1))  # closed node
                closed_nodes.append(node_map[y][x])
    return node_map, closed_nodes


# calculate the distance between two points with as many dimensions
def distance(pi, pf):
    dim = len(pi)  # the number of dimensions to use
    adder = 0
    for i in range(dim):
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


standard_neighbours(dimensions)


def get_current_node(n, s):
    c = nodes
    for i in s:
        c = c[i]
    return c


def sum_lists(a, b, g):
    # a and b must have equal lengths (IndexError otherwise)
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i]*g)
    return c


def ascii_display_2d(list_of_lists):
    for i in range(len(list_of_lists)):
        to_print = []
        for j in range(len(list_of_lists[i])):
            if list_of_lists[i][j].location == target:
                to_print.append("X")
            elif list_of_lists[i][j].location == start:
                to_print.append("O")
            elif list_of_lists[i][j].state == 1:
                to_print.append("@")
            elif list_of_lists[i][j].state == 2:
                to_print.append("#")
            else:
                to_print.append("/")
        print(to_print)


# node class stores data
class Node:
    def __init__(self, location, state, g_cost, h_cost):
        self.location = location  # x, y, maybe z. This is currently a list.
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
            current = get_current_node(nodes, start)
        else:
            current = nodes_open[f_min_i(nodes_open)]  # current = lowest f_cost that is open
        nodes_open.remove(current)  # these are just pointers
        nodes_closed.append(current)
        current.state = 2  # change state to closed

        # stop if at the target
        if current.location == target:
            print("Pathfinding Finished")
            return

        # for neighbours of current
        for j in range(len(neighbours)):
            neighbour = current  # this will change
            try:
                n_location = sum_lists(current.location, neighbours[j], 1)
                neighbour = current = get_current_node(nodes, n_location)
            except IndexError:
                j += 1  # skip to next neighbour

            # if no IndexError
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


nodes, nodes_closed = image_to_nodes(image_path, (255, 255, 255), (0, 0, 0))
ascii_display_2d(nodes)
