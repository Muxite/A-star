# by Muk Chunpongtong, algorithm taken from Sebastian Lague pseudocode.
# uses a straight-line heuristic
import math
import random
from PIL import Image
import copy


neigh_dirs = []  # describes the neighbour locations and distance as the last one
adder = []


# produce a 2d node map from an image
def image_to_nodes(walkable_color, unwalkable_color, path):
    image = Image.open(path)
    pixels = image.load()
    width, height = image.size
    bounds = (width, height)
    node_map = []
    closed_nodes = []
    for y in range(height):
        node_map.append([])
        for x in range(width):
            if pixels[x, y] == walkable_color:
                node_map[y].append(Node((x, y), 0, -1, -1))
            elif pixels[x, y] == unwalkable_color:
                node_map[y].append(Node((x, y), -1, -1, -1))  # closed node
                closed_nodes.append(node_map[y][x])
    return node_map, closed_nodes, bounds


# calculate the distance between two points with as many dimensions
def distance(pi, pf):
    dim = len(pi)  # the number of dimensions to use
    combiner = 0
    for i in range(dim):
        combiner += (pi[i] - pf[i]) ** 2
    return round(combiner ** (1 / 2) * 100)


# get neighbours for this number of dimensions
def standard_neighbours(dimensions=2):
    delta = [-1, 0, 1]
    for i in range(len(delta) ** dimensions):
        neigh_dirs.append([])

    # remove [0, 0] or [0, 0, 0]
    center = []
    for i in range(dimensions):
        center.append(0)

    for d in range(dimensions):
        for i in range(len(delta) ** dimensions):
            v = math.floor(i / (len(delta) ** d))
            neigh_dirs[i].append(delta[v % len(delta)])
            # if finishing last dimension
            if d == dimensions - 1:
                neigh_dirs[i].append(distance(center, neigh_dirs[i]))
    center.append(0)  # the distance to center is 0
    neigh_dirs.remove(center)


# return a node using location stored as a list
def get_node(n, s):
    c = n
    # loop apply the axes of s to n in descending order
    for i in range(len(s) - 1, -1, -1):
        c = c[s[i]]
    return c


# add two lists together
def sum_lists(a, b, g):
    # a and b must have equal lengths (IndexError otherwise)
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i] * g)
    return c


# display a 2D node map (for debug)
def display_2d(list_of_lists, name, start, target, bounds):
    im = Image.new('RGB', (bounds[0], bounds[1]), color=(255, 255, 255))
    pix = im.load()
    for i, sublist in enumerate(list_of_lists):
        to_print = []
        for j, node in enumerate(sublist):
            if node.location == target:
                to_print.append("t")
                pix[j, i] = (0, 0, 255)  # blue
            elif node.location == start:
                to_print.append("s")
                pix[j, i] = (0, 255, 0)  # green
            elif node.state == -1:
                to_print.append("#")
                pix[j, i] = (0, 0, 0)  # black
            elif node.state == 1:
                to_print.append("o")
                pix[j, i] = (170, 255, 170)  # light green
            elif node.state == 2:
                to_print.append("c")  # pink
                pix[j, i] = (255, 170, 170)
            elif node.state == 3:
                to_print.append("p")
                pix[j, i] = (255, 0, 255)  # magenta
            else:
                to_print.append(" ")
        # print(to_print)
    im.save(str(name) + ".png")


def release_banner(list_of_lists, start, target, bounds, size):
    im = Image.new('RGB', (bounds[0], bounds[1]), color=(0, 0, 0))
    pix = im.load()
    for i in range(len(list_of_lists)):
        to_print = []
        for j in range(len(list_of_lists[i])):
            if list_of_lists[i][j].location == target:
                to_print.append("t")
                pix[j, i] = (0, 0, 160)  # blue
            elif list_of_lists[i][j].location == start:
                to_print.append("s")
                pix[j, i] = (160, 0, 0)  # red
            elif list_of_lists[i][j].state == -1:
                to_print.append("#")
                pix[j, i] = (160, 160, 160)  # white
            elif list_of_lists[i][j].state == 1:
                to_print.append("o")
                pix[j, i] = (100, 100, 100)
            elif list_of_lists[i][j].state == 2:
                to_print.append("c")  # gray
                pix[j, i] = (40, 40, 40)
            elif list_of_lists[i][j].state == 3:
                to_print.append("p")
                pix[j, i] = (255, 255, 255)  # lightning-esque
            else:
                to_print.append(" ")
        # print(to_print)
    im = im.resize(size)
    return im


# node class stores data
class Node:
    def __init__(self, location, state, g_cost, h_cost):
        self.location = location  # x, y, maybe z. Is a tuple.
        self.g_cost = g_cost  # distance to start
        self.h_cost = h_cost  # distance to target
        self.state = state  # 0 base, 1 open, 2 closed, 3 final path
        self.parent = None  # will set this later


# determine if the location is within the node_map HARDCODED FOR 2D
def check(location, bounds, dimensions=2):
    for i in range(dimensions):
        if 0 > location[i] or location[i] > bounds[i]:
            return False
    return True


# the main function that modifies nodes, nodes_open, and nodes_closed into the solution
def a_star(nodes, nodes_open, nodes_closed, start, target, bounds,
           banner=False, add=None, dimensions=2, size=(240, 240)):
    if add is None:
        add = adder
    nodes_open.append(get_node(nodes, start))
    current = None
    # return the index of the lowest f_min

    def f_min_i(nodes_list):
        lowest = 99999999
        index = -1
        for k, node in enumerate(nodes_list):
            if node.g_cost + node.h_cost < lowest:
                lowest = node.g_cost + node.h_cost
                index = k
        return index

    # main loop
    for i in range(10000):
        # except for the first loop
        if i < 1:
            current = get_node(nodes, start)

        else:
            current = nodes_open[f_min_i(nodes_open)]  # current = lowest f_cost that is open
            nodes_open.remove(current)  # these are just pointers
        nodes_closed.append(current)
        current.state = 2  # change state to closed

        # stop if at the target
        if current.location == target:
            print("Pathfinding Finished")
            break

        # for neighbours of current
        for j, neigh_dir in enumerate(neigh_dirs):
            neighbour = current  # this will change
            try:
                n_location = sum_lists(current.location, neigh_dir[0:dimensions], 1)
                if check(n_location, bounds):
                    neighbour = get_node(nodes, n_location)
            except IndexError:
                pass

            # if no IndexError
            if neighbour is not current:
                # if not closed
                if neighbour.state != 2 and neighbour.state != -1:
                    # add the previous g_cost with the distance from it to this neighbour cell
                    path_length = current.g_cost + neigh_dir[dimensions]
                    if path_length < neighbour.g_cost or neighbour.state != 1:

                        # update f_cost
                        neighbour.g_cost = path_length
                        neighbour.h_cost = distance(neighbour.location, target)

                        # set the parent to retrace steps later
                        neighbour.parent = current
                        if neighbour.state != 1:
                            nodes_open.append(neighbour)
                            neighbour.state = 1
        # end if no open nodes remain, without this there will be an error + wasted processing
        if len(nodes_open) == 0:
            print('failed')
            break

        # give a snapshot of the algorithm each loop
        if banner:
            add.append(release_banner(nodes, start, target, bounds, size))

        else:
            display_2d(nodes, i, start, target, bounds)

    # trace the path
    parent_child_node = current  # get the last one
    start_node = get_node(nodes, start)
    path = []  # path as a list of nodes, use path[i].location for location data
    for i in range(1000):
        path.append(parent_child_node)
        parent_child_node.state = 3  # set to path
        if parent_child_node is not start_node:
            parent_child_node = parent_child_node.parent
        else:
            break

    print("Path Traced")
    if banner:
        # many of the traced frame
        for i in range(50):
            add.append(release_banner(nodes, start, target, bounds, size))

    else:
        display_2d(nodes, "end", start, target, bounds)


def banners_generate(nodes,  nodes_open, nodes_closed, bounds, title, n_travels, duration, size):
    node_save = copy.deepcopy(nodes)
    nodes_open_save = copy.deepcopy(nodes_open)
    nodes_closed_save = copy.deepcopy(nodes_closed)
    # it will pathfind from point a to b, b to c, c to d, and so on, then back to a
    initial_start = None
    start = (0, 0)  # default
    end = (2, 1)  # for debug purposes
    for i in range(n_travels):
        nodes = node_save
        nodes_open = nodes_open_save
        nodes_closed = nodes_closed_save
        # get a start position if its the first time, otherwise, end becomes new start
        if i == 0:
            while True:
                test = (random.randint(0, bounds[0]-1), random.randint(0, bounds[1]-1))
                if nodes[test[1]][test[0]].state == 0:
                    start = test
                    initial_start = test
                    break
        elif i == n_travels-1:
            end = initial_start  # go to the start for the last one (HARD CODED)
        else:
            start = end  # previous end, which is viable because it was checked last round
        if i != n_travels-1:
            while True:
                test = (random.randint(0, bounds[0] - 1), random.randint(0, bounds[1] - 1))
                if nodes[test[1]][test[0]].state == 0:
                    end = test
                    break

        a_star(nodes, nodes_open, nodes_closed, start, end, bounds, banner=True, size=size)  # fills add
    print("SAVING...")
    adder[0].save(title, save_all=True, append_images=adder[1:], optimize=True, duration=duration,
                  loop=0)


def main():
    standard_neighbours()
    nodes_open = []
    original = str(input("Location of original image: "))
    nodes, nodes_closed, bounds = image_to_nodes((0, 0, 0), (160, 160, 160), original)
    if str(input("Make banner? (y/n): ") == 'y'):
        title = str(input("Title of new banner: "))
        n_travels = int(input("Number of travel sections:"))
        duration = int(input("ms per frame: "))
        size = int(input("X of size: ")), int(input("Y of size: "))
        banners_generate(nodes, nodes_open, nodes_closed, bounds, title, n_travels, duration, size)
    else:
        start = int(input("X of start: ")), int(input("Y of start: "))
        target = int(input("X of target: ")), int(input("Y of target: "))
        a_star(nodes, nodes_open, nodes_closed, start, target, bounds)


def test_system():
    standard_neighbours()
    nodes_open = []
    original = r"D:\GitHub\A-star\Banner1.png"
    nodes, nodes_closed, bounds = image_to_nodes((0, 0, 0), (160, 160, 160), original)
    title = "TESTTEST.gif"
    n_travels = 4
    duration = 20
    size = (960, 240)
    banners_generate(nodes, nodes_open, nodes_closed, bounds, title, n_travels, duration, size)


#  main()
test_system()
