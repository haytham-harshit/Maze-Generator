###################################
# Python maze generator and solver program
# using PyGame for animation
# Harshit Rajput
# Jangid Abhishek Vijay
# Python 3.9
# 20.11.2021
###################################
import copy

import pygame
import time
import random

# set up pygame window
WIDTH = 440
HEIGHT = 440
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (37, 117, 82,)
BLUE = (26, 215, 222)
YELLOW = (249, 249, 30)

# initialise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator & Solver")
clock = pygame.time.Clock()

# setup maze variables
x = 0  # x axis
y = 0  # y axis
w = 20  # width of cell

row_col_size = 20
size = row_col_size * row_col_size
adjacencey_mat = [[0 for i in range(size)] for j in range(size)]

grid = []
visited = []
stack = []
solution = {}


# build the grid -------------------------------------------------------------------------------------------------------
def build_grid(x, y, w):
    for i in range(1, 21):
        x = 20                                                              # set x coordinate to start position
        y = y + 20                                                          # start a new row
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])             # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])     # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])     # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])             # left of cell
            grid.append((x, y))                                             # add cell to grid list
            x = x + 20                                                      # move cell to new position


# -------------------------------------------------------------------------------------------------------------

def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)       # draw a rectangle twice the width of the cell
    pygame.display.update()                                             # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


# -------------------------------------------------------------------------------------------------------------

def single_cell(x, y):
    pygame.draw.rect(screen, YELLOW, (x + 1, y + 1, 18, 18), 0)         # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 18, 18), 0)           # used to re-colour the path after single_cell
    pygame.display.update()                                             # has visited cell


def solution_cell(x, y):
    pygame.draw.rect(screen, YELLOW, (x + 8, y + 8, 5, 5), 0)           # used to show the solution
    pygame.display.update()                                             # has visited cell


def solution_cell_2(x, y):
    pygame.draw.rect(screen, GREEN, (x + 8, y + 8, 5, 5), 0)            # used to show the solution
    pygame.display.update()                                             # has visited cell


def pixel_to_vertex(x, y):
    row = (y / 20) - 1
    column = (x / 20) - 1
    vertex = row * row_col_size + column
    vertex = int(vertex)
    return vertex


def vertex_to_pixel(x):
    row = x / row_col_size
    row = int(row)
    column = x % row_col_size
    a = column * row_col_size + 20
    b = row * row_col_size + 20
    a = int(a)
    b = int(b)
    return a, b


# -------------------------------------------------------------------------------------------------------------

def carve_out_maze(x, y):
    single_cell(x, y)                                                   # starting positing of maze
    stack.append((x, y))                                                # place starting cell into stack
    visited.append((x, y))                                              # add starting cell to visited list

    while len(stack) > 0:                                               # loop until stack is empty
        time.sleep(.03)                                                 # slow program now a bit
        cell = []                                                       # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:            # right cell available?
            cell.append("right")                                        # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:            # left cell available?
            cell.append("left")

        if (x, y + w) not in visited and (x, y + w) in grid:            # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x, y - w) in grid:            # up cell available?
            cell.append("up")

        if len(cell) > 0:                                               # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                         # select one of the cell randomly

            p = pixel_to_vertex(x, y)
            q = pixel_to_vertex(x + w, y)
            r = pixel_to_vertex(x - w, y)
            s = pixel_to_vertex(x, y + w)
            t = pixel_to_vertex(x, y - w)

            if cell_chosen == "right":                                  # if this cell has been chosen
                adjacencey_mat[p][q] = 1
                adjacencey_mat[q][p] = 1

                push_right(x, y)                                        # call push_right function
                solution[(x + w, y)] = x, y                             # solution = dictionary key = new cell, other = current cell
                x = x + w                                               # make this cell the current cell
                visited.append((x, y))                                  # add to visited list
                stack.append((x, y))                                    # place current cell on to stack

            elif cell_chosen == "left":
                adjacencey_mat[p][r] = 1
                adjacencey_mat[r][p] = 1

                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                adjacencey_mat[p][s] = 1
                adjacencey_mat[s][p] = 1

                push_down(x, y)
                solution[(x, y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                adjacencey_mat[p][t] = 1
                adjacencey_mat[t][p] = 1

                push_up(x, y)
                solution[(x, y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                      # if no cells are available pop one from the stack
            single_cell(x, y)                                       # use single_cell function to show backtracking image
            time.sleep(.03)                                         # slow program down a bit
            backtracking_cell(x, y)                                 # change colour to green to identify backtracking path


# ----------------------------------------------------------------------------------------------------------------------

def dijkstra(src, dest):
    def min_distance(dist, sp_set):                     # choose b/n a vertex from set of vertices connected to parent
        min = 10 ** 10
        global min_index
        for v in range(400):                            # minimum distant adjacent vertex is chosen
            if sp_set[v] == False and dist[v] <= min:
                min = dist[v]
                min_index = v
        return min_index

    graph = copy.deepcopy(adjacencey_mat)
    parent = [-2 for i in range(400)]                   # every vertex keep track of its parent vertex

    dist = [10 ** 10 for i in range(size)]              # stores the dist w.r.t to src
    sp_set = [False for i in range(size)]               # tells whether already selected or covered along path
    dist[src] = 0
    parent[src] = -1

    for i in range(size - 1):
        u = min_distance(dist, sp_set)                  # returns the minimum distant adjacent vertex
        sp_set[u] = True
        # find all the vertices connected to the selected vertex u
        for v in range(size):
            if sp_set[v] is False and graph[u][v] != 0 and dist[u] != 10 ** 10 and dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u

    def ancestor(des):
        list1 = []
        stop = des
        while parent[stop] != -1:                       # process of finding ancestory of destination vertex
            list1.append(parent[stop])
            stop = parent[stop]

        return list1

    destination_parent = ancestor(dest)
    print(destination_parent)

    for index in range(len(destination_parent)):
        e, f = vertex_to_pixel(dest)
        solution_cell_2(e, f)
        s = destination_parent[index]
        m, n = vertex_to_pixel(s)
        solution_cell_2(m, n)
        time.sleep(.03)


# ----------------------------------------------------------------------------------------------------------------------

def plot_route_back(x, y):
    solution_cell(x, y)                         # solution list contains all the coordinates to route back to start
    while (x, y) != (20, 20):                   # loop until cell position == start position
        x, y = solution[x, y]                   # "key value" now becomes the new key
        solution_cell(x, y)                     # animate route back
        time.sleep(.03)


# main function call ---------------------------------------------------------------------------------------------------
x, y = 20, 20               # starting position of grid
build_grid(40, 0, 20)       # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
carve_out_maze(x, y)        # call build the maze  function
plot_route_back(400, 400)   # call the plot solution function
dijkstra(19, 159)

# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
