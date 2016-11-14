# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

import time
import random

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']  # Use these when creating your policy grid.

def print_grid(grid):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    for i in range(grid_rows):
        print grid[i]

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

# ---------------------------------------------
#  General Explanation of how problem was approached and solved:
#  We start by creating a value matrix initialized with everything at collision_cost. We also initialize a matrix
#  Policy where we will store which move generated the least cost value so that we can put the correct arrow at the end.
#  We start by expanding the goal, assigning its 0 value and closing that position so that we won't expand there later.
#  From there we start a loop where each position still in open wil attempt to update its value. When it does so,
#  it also expands to its neighbours, even if they were already visited to make sure they have a chance to update their values as well.
#  When the convergence is achieved at a position, we remove it from the positions considered for update. When all positions converge
#  We leave the loop and update the policy matrix with the appropriate arrows before returning the value and policy matrixes.
# ---------------------------------------------
def stochastic_value(grid, goal, cost_step, collision_cost, success_prob):
    failure_prob = (1.0 - success_prob) / 2.0  # Probability(stepping left) = prob(stepping right) = failure_prob
    grid_rows = len(grid)
    grid_cols = len(grid[0])

    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    value[goal[0]][goal[1]] = 0
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    policy[goal[0]][goal[1]] = '*'
    aux_grid = grid[:]
    aux_grid[goal[0]][goal[1]] = 2  #Prevents from expanding to cells more than once. Also prevents goal from being used mainting its value of 0

    open = [[0, goal[0], goal[1]]]      #Expand goal before loop because goal needs to be deleted from open
    for i in range(len(delta)):
        x3 = open[0][1] + delta[i][0]
        y3 = open[0][2] + delta[i][1]
        g3 = open[0][0] + cost_step

        # check if whether position is possible (not out of bounds or inside obstacles)
        if (min((x3, y3)) >= 0 and x3 < grid_rows and y3 < grid_cols):
            if (aux_grid[x3][y3] == 0):
                # add next_position to the open_position
                aux_grid[x3][y3] = 2
                open.append((g3, x3, y3))
    del open[0]

    #Start Loop that will keep going while values are being changed
    ind = 0
    test = False
    while not len(open) == 0:

        ind = (ind+1)%len(open)             #Iterates cyclically through the various ind currently being considered
        selected = open[ind]
        del open[ind]                   # we can safely delete because everytime a cell is updated it expands to its neighbours
        x2 = selected[1]
        y2 = selected[2]
        g2 = selected[0]
        buff = []
        current_value = value[x2][y2]
        policy_ind = -1
        possible_values = []
        for i in range(len(delta)):
            # Taking advantage of how delta is structured. considering
            # the movement as forward, a left is always delta +1 and
            #  right delta -1
            x3f = x2 + delta[i][0]
            y3f = y2 + delta[i][1]
            x3l = x2 + delta[(i + 1) % 4][0]
            y3l = y2 + delta[(i + 1) % 4][1]
            x3r = x2 + delta[(i - 1) % 4][0]
            y3r = y2 + delta[(i - 1) % 4][1]

            forward_value = 0
            if (min((x3f, y3f)) < 0 or x3f >= grid_rows or y3f >= grid_cols):  #out of bounds
                forward_value = collision_cost
            else:
                if (aux_grid[x3f][y3f] == 1):                                   #Obstacle
                    forward_value = collision_cost
                else:
                    forward_value = value[x3f][y3f]
                    if (aux_grid[x3f][y3f] == 0):                           # If we can, we also expand to this new positiion
                        aux_grid[x3f][y3f] = 2
                        open.append((g2+cost_step, x3f, y3f))
                    elif (aux_grid[x3f][y3f] == 2):
                        buff.append((g2+cost_step, x3f, y3f))
            left_value = 0
            if (min((x3l, y3l)) < 0 or x3l >= grid_rows or y3l >= grid_cols):  #out of bounds
                left_value = collision_cost
            else:
                if (aux_grid[x3l][y3l] == 1):                                  #Obstacle
                    left_value = collision_cost
                else:
                    left_value = value[x3l][y3l]
            right_value = 0
            if (min((x3r, y3r)) < 0 or x3r >= grid_rows or y3r >= grid_cols):  #out of bounds
                right_value = collision_cost
            else:
                if (aux_grid[x3r][y3r] == 1):                                   #Obstacle
                    right_value = collision_cost
                else:
                    right_value = value[x3r][y3r]
            val = cost_step + (success_prob * forward_value) + (failure_prob * left_value) + (failure_prob * right_value)
            possible_values.append(val)
            if(current_value > possible_values[i]):
                current_value = possible_values[i]
                policy_ind = i

        #Update value and policy for this position
        if(abs(current_value - value[x2][y2]) > 0.000001):            #If the change is higher than threshold then we update value
            value[x2][y2] = current_value
            policy[x2][y2] = delta_name[policy_ind]
            for i in range(len(buff)):                                  #If it updates, then we expand again to make sure neighbours account for these changes
                open.append(buff[i])


    print_grid(aux_grid)
    return value, policy


# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0]) - 1]  # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5
# grid = [[0, 0, 0, 1, 0, 0, 0],
#         [0, 1, 0, 0, 0, 1, 0],
#         [0, 1, 1, 0, 1, 1, 0],
#         [0, 1, 1, 1, 1, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0]]
# goal = [0, 6]
# cost_step = 1
# collision_cost = 100
# success_prob = 0.8

value, policy = stochastic_value(grid, goal, cost_step, collision_cost, success_prob)
for row in value:
    print row
for row in policy:
    print row

    # Expected outputs:
    #
    # [57.9029, 40.2784, 26.0665,  0.0000]
    # [47.0547, 36.5722, 29.9937, 27.2698]
    # [53.1715, 42.0228, 37.7755, 45.0916]
    # [77.5858, 100.00, 100.00, 73.5458]
    #
    # ['>', 'v', 'v', '*']
    # ['>', '>', '^', '<']
    # ['>', '^', '^', '<']
    # ['^', ' ', ' ', '^']