# ----------
# User Instructions:
#
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's
# optimal path to the position specified in goal;
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a
# right turn.

import time

forward = [[-1, 0],  # go up
           [0, -1],  # go left
           [1, 0],  # go down
           [0, 1]]  # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0]  # given in the form [row,col,direction]
# direction = 0: up
#             1: left
#             2: down
#             3: right

goal = [2, 0]  # given in the form [row,col]

cost = [2, 1, 20]  # cost has 3 values, corresponding to making


# a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def print_grid(grid):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    for i in range(grid_rows):
        print grid[i]

def path_grid(path_map, initial_position, final_position, grid):

    path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    path[final_position[1]][final_position[2]] = '*'
    current_x = final_position[1]
    current_y = final_position[2]
    current_teta = final_position[3]
    current_g = final_position[0]

    initial_x = initial_position[0]
    initial_y = initial_position[1]
    initial_teta = initial_position[2]

    print initial_position
    while current_x != initial_x or current_y != initial_y:

        (previous_g, previous_x, previous_y, previous_teta) = path_map[(current_g, current_x, current_y, current_teta)]

        ind = []
        for i in range(len(action)):
            if(((previous_teta + action[i]) % len(forward)) == current_teta):
                ind = i
                break

        path[previous_x][previous_y] = action_name[ind]

        current_x = previous_x
        current_y = previous_y
        current_teta = previous_teta
        current_g = previous_g

    # print_grid(path)

    return path

def optimum_policy2D(grid, init, goal, cost):
    grid_rows = len(grid)
    grid_cols = len(grid[0])

    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]

    aux_grid = [[-1*grid[col][row] for row in range(len(grid[0]))] for col in range(len(grid))]  # auxiliary Grid that will have 2 on positions already visited
    resign = False
    found = False
    count = 0

    open = [[0, init[0], init[1], init[2]]]        # [cost, x, y, teta]
    path_map = {}
    policy = []
    while not found and not resign:
        # selected_position position with lowest cost
        min_value = float("inf")
        selected = []               # position selected for expansion

        for i in range(len(open)):
            x = open[i][1]
            y = open[i][2]
            g = open[i][0]
            teta = open[i][3]
            if (min_value > g):
                min_value = g
                ind = i
                selected = open[i]

        del open[ind]
        x2 = selected[1]
        y2 = selected[2]
        g2 = selected[0]
        teta2 = selected[3]
        expand[x2][y2] = count
        count += 1

        # expand this postion
        for i in range(len(action)):
            teta3 = (teta2 + action[i]) % len(forward)
            delta = forward[teta3]
            x3 = x2 + delta[0]
            y3 = y2 + delta[1]
            g3 = g2 + cost[i]

            #check if whether position is possible (not out of bounds or inside obstacles)
            if(min((x3,y3)) >= 0 and x3 < grid_rows and y3 < grid_cols):
                if(aux_grid[x3][y3] >= 0):

                    #check whether it is at goal
                    if([x3, y3] == goal):
                        print 'Reached Goal!'
                        path = (g3, x3, y3, teta3)
                        expand[x3][y3] = count
                        found = True
                        path_map[(g3, x3, y3,teta3)] = (g2, x2, y2,teta2)
                        # policy = path_grid(path_map, init, path, aux_grid)
                    else:
                        #add next_position to the open_position
                        aux_grid[x3][y3] = g3
                        open.append((g3, x3, y3, teta3))
                        path_map[(g3, x3, y3, teta3)] = (g2, x2, y2, teta2)

        if(len(open) == 0 and not found):     # no more possible moves and not at goal
            path = 'fail'
            resign = True

    if(path != 'fail'):
        policy = path_grid(path_map, init, path, aux_grid)
    else:
        policy = 'fail'
    return policy

optimum_policy2D(grid, init, goal, cost)